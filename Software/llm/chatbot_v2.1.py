
# Description ： ChatBot_v2.0 + WebUI + MQTT.

import sys

from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.agents import Tool, initialize_agent, AgentType
import time

import riva.client
import riva.client.audio_io

from asr import ASR
from tts import TTS
from local_llm import CustomLLM
from ha import HomeAssistant
from mqtt import MQTT


class SeeeBot:
    def __init__(self, openai_api=None, text_inference_server='http://192.168.49.103:8899/generate', riva_server=None,
                 asr_input_device_id=16, asr_sample_rate_hz=48000, tts_output_device_id=16, tts_sample_rate_hz=48000,
                 mqtt_broker="192.168.49.104"):

        tools = [
            Tool(
                name='turn_off_light_of_living_room',
                func=self.turn_off_light_of_living_room,
                description=f"""When you need to turn off the light of living room, please execute this tool."""
            ),
            Tool(
                name='turn_on_light_of_living_room',
                func=self.turn_on_light_of_living_room,
                description=f"""When you need to turn on the light of living room, please execute this tool."""
            ),
        ]
        self.memory = ConversationBufferMemory(memory_key='chat_history')

        if openai_api is not None:
            llm = OpenAI(openai_api_key=openai_api, temperature=0.5)
            self.agent = initialize_agent(
                tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=self.memory,
                handle_parsing_errors=True, agent_kwargs={"prefix": "Assume you are a smart chatbot named Seeebot."}
            )
            # print(f"Built-in prompt template：\n >>> \n {self.agent.agent.llm_chain.prompt.template} \n <<<")
        elif text_inference_server is not None:
            # llm = CustomLLM(url=text_inference_server, temperature=0.1, max_new_tokens=1023)
            llm = CustomLLM()

            def _handle_error(error) -> str:
                return f"AI : {error}"

            self.agent = initialize_agent(
                tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=self.memory,
                handle_parsing_errors=_handle_error, agent_kwargs={"prefix": "Assume you are a smart chatbot named Seeebot."}
            )
            print(f"Built-in prompt template：\n >>> \n {self.agent.agent.llm_chain.prompt.template} \n <<<")
        else:
            print('No model to load!')
            sys.exit(0)

        self.auth = None
        self.chat_history = []
        if riva_server is not None:
            self.auth = riva.client.Auth(uri=riva_server)
            self.asr = ASR(self.auth, input_device=asr_input_device_id, sample_rate_hz=asr_sample_rate_hz,
                           callback=self.on_asr_transcript)
            self.asr_interrupt_flag = None
            self.tts = TTS(self.auth, output_device=tts_output_device_id, sample_rate_hz=tts_sample_rate_hz)

            self.asr_mute = False

            self.wakeup = False
            self.wakeup_world = ['Mira', 'Miro', 'mirror', 'Mirror']
            self.sleep_world = ['goodbye', 'Goodbye', 'good bye']
        else:
            self.auth = None

        self.ha = HomeAssistant()
        self.mqtt_client = MQTT(mqtt_broker=mqtt_broker, mqtt_port=1883)

    def run(self):
        if self.auth is not None:
            self.run_riva()
        else:
            self.run_webui()

    def run_riva(self):
        self.asr.start()
        time.sleep(0.5)
        while True:
            if self.asr_interrupt_flag is not None:
                self.asr_mute = True
                if self.wakeup:
                    for world in self.sleep_world:
                        if world in self.asr_interrupt_flag[0]:
                            self.wakeup = False
                            self.mqtt_client.send_msg("/seeebot", 'Good bye, have a good day.')
                            self.tts.output_audio('Have a nice day.')
                            break
                else:
                    for world in self.wakeup_world:
                        if world in self.asr_interrupt_flag[0]:
                            self.wakeup = True
                            self.mqtt_client.send_msg("/wakeup", 'wakeup')
                            self.mqtt_client.send_msg("/seeebot", 'How can I help you?')
                            self.tts.output_audio('How can I help you? ')
                            break
                    # time.sleep(2)

                if self.wakeup and self.asr_interrupt_flag[1] > 0.2:
                    self.mqtt_client.send_msg("/human", self.asr_interrupt_flag[0])
                    output = self.agent.run(input=self.asr_interrupt_flag[0])
                    self.mqtt_client.send_msg("/seeebot", output)
                    print(output)
                    self.tts.output_audio(output)
                time.sleep(2)
                self.asr_interrupt_flag = None
                self.asr_mute = False
            else:
                time.sleep(0.1)

    def run_webui(self):
        import gradio as gr

        def respond(message):
            self.mqtt_client.send_msg("/human", message)
            bot_message = self.agent.run(input=message)
            self.mqtt_client.send_msg("/seeebot", bot_message)
            self.chat_history.append((message, bot_message))
            return "", self.chat_history

        with gr.Blocks() as demo:
            gr.Markdown("# This is a simple webUI for reMirror")
            chat_msg = gr.Chatbot(height=500)
            msg = gr.Textbox(label="Prompt")
            btn = gr.Button("Submit")
            clear = gr.ClearButton(components=[msg, chat_msg], value="Clear console")
            btn.click(respond, inputs=[msg], outputs=[msg, chat_msg])
            msg.submit(respond, inputs=[msg], outputs=[msg, chat_msg])
        gr.close_all()
        demo.launch()

    def on_asr_transcript(self, response):
        try:
            if self.asr_mute:
                # print('waiting tts...')
                return 'waiting...'
            for result in response.results:
                if self.asr_mute:
                    return 'waiting...'
                if not result.alternatives:
                    continue
                transcript = result.alternatives[0].transcript
                if result.is_final:
                    self.asr_interrupt_flag = (transcript, result.alternatives[0].confidence)
                    print("## " + transcript + f"Confidence:{result.alternatives[0].confidence:9.4f}")
                else:
                    # print('>> ' + transcript)
                    pass
        finally:
            pass

    def turn_off_light_of_living_room(self, args):
        self.ha.setup_switch('off', self.ha.entity_ids['light'])
        return 'I have turned off the light of living room for you'

    def turn_on_light_of_living_room(self, args):
        self.ha.setup_switch('on', self.ha.entity_ids['light'])
        return 'I have turned on the light of living room for you'

    def respond(self, args):
        bot_message = self.agent.run(input=args)
        return bot_message


if __name__ == '__main__':

    chatbot = SeeeBot(
        openai_api='',
        # text_inference_server='http://192.168.49.104:8899/generate',
        riva_server="192.168.49.104:50051",
    )
    chatbot.run()



