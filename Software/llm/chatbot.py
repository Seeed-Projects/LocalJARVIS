# Description ： LangChain + OpenAI API / Text-Inference-Generation + Riva / WebUI + MQTT.

import sys
import pyaudio
import argparse

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


def parse_args():
    parser = argparse.ArgumentParser(description="Control smart furniture by LLM")
    parser.add_argument(
        "--openai_api", type=str, help="Get API Key from: https://openai.com/blog/openai-api",
    )
    parser.add_argument(
        "--text_inference_server", type=str, default='http://192.168.88.104:8899/generate',
        help="URL to the local large model inference service",
    )
    parser.add_argument(
        "--riva_server", type=str, help="URL of the Riva server, For example: '192.168.49.104:50051'.",
    )

    parser.add_argument("--ha_access_token", type=str, help="Access token of HomeAssistant.")
    parser.add_argument("--ha_base_url", type=str, default='http://aeassistant.lan:8123/', help="URL of the HomeAssistant")

    parser.add_argument("--mqtt_broker_ip", type=str, default='192.168.88.104', help="IP of mqtt broker")
    parser.add_argument("--mqtt_broker_port", type=str, default='1883', help="Port of mqtt broker")

    args = parser.parse_args()
    return args


class SeeeBot:
    def __init__(
            self, openai_api=None,
            text_inference_server='http://192.168.88.104:8899/generate',
            riva_server=None,
            asr_input_device_id=None,
            asr_sample_rate_hz=None,
            tts_output_device_id=None,
            tts_sample_rate_hz=None,
            mqtt_broker_ip="192.168.88.104",
            mqtt_broker_port="1883",
            ha_access_token='',
            ha_base_url='http://aeassistant.lan:8123/'
    ):
        # whether to activate MQTT.
        if mqtt_broker_ip is not None:
            self.mqtt_client = MQTT(mqtt_broker=mqtt_broker_ip, mqtt_port=mqtt_broker_port)

        # Create tools for the large langchain agent.
        # Please refer to the example below, add the tool in HomeAssistant, and declare it in the Tools section below.
        self.ha = HomeAssistant(ha_access_token, ha_base_url)
        tools = [
            Tool(
                name='turn_on_air_conditioner',
                func=self.ha.turn_on_air_conditioner,
                description=f"""When you need to turn on the air conditioner, please execute this tool."""
            ),
            Tool(
                name='turn_off_air_conditioner',
                func=self.ha.turn_off_air_conditioner,
                description=f"""When you need to turn off the air conditioner, please execute this tool."""
            )
        ]

        # Instantiate the large language model agent by langchain.
        self.memory = ConversationBufferMemory(memory_key='chat_history')
        if openai_api is not None:
            llm = OpenAI(openai_api_key=openai_api, temperature=0.7)
            self.agent = initialize_agent(
                tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=self.memory,
                handle_parsing_errors=True, max_iterations=3,
                agent_kwargs={
                    "prefix": "Assume you are a smart chatbot named Frank. You can adjust the status of smart home devices based on human input."}
            )
        elif text_inference_server is not None:
            llm = CustomLLM(url=text_inference_server, temperature=0.1, max_new_tokens=128)

            def _handle_error(error) -> str:
                return f"AI : {error}"

            self.agent = initialize_agent(
                tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=self.memory,
                max_iterations=3, handle_parsing_errors=_handle_error,
                agent_kwargs={
                    "prefix": "Assume you are a smart chatbot named Frank. You can adjust the status of smart home devices based on human input."}
            )
        else:
            print('No model to load!')
            sys.exit(0)
        print(f"Built-in prompt template：\n >>> \n {self.agent.agent.llm_chain.prompt.template} \n <<<")

        # Human-computer interaction tool
        self.auth = None
        self.chat_history = []
        if riva_server is not None:
            self.auth = riva.client.Auth(uri=riva_server)

            if asr_input_device_id is None:
                input_device, output_device = self.get_riva_devices_list()
                asr_input_device_id = input_device['index']
                asr_sample_rate_hz = int(input_device['defaultSampleRate'])
                tts_output_device_id = output_device['index']
                tts_sample_rate_hz = int(output_device['defaultSampleRate'])
                print(f"Default ASR Device: {asr_input_device_id}, {asr_sample_rate_hz}")
                print(f"Default TTS Device: {tts_output_device_id}, {tts_sample_rate_hz}")

            self.asr = ASR(
                self.auth, input_device=asr_input_device_id, sample_rate_hz=asr_sample_rate_hz,
                callback=self.on_asr_transcript
            )
            self.tts = TTS(self.auth, output_device=tts_output_device_id, sample_rate_hz=tts_sample_rate_hz)
            self.asr_interrupt_flag = None
            self.asr_mute = False

            self.wakeup = False
            self.wakeup_world = ['Frank', 'frank']
            self.sleep_world = ['goodbye', 'Goodbye', 'good bye', 'Good bye', 'Good Bye']

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
                            self.send_mqtt_message("/seeebot", 'Good bye, have a good day.')
                            self.tts.output_audio('Goodbye, Have a nice day.')
                            self.send_mqtt_message("/bye", 'bye')
                            break
                    break
                else:
                    for world in self.wakeup_world:
                        if world in self.asr_interrupt_flag[0]:
                            self.wakeup = True
                            self.send_mqtt_message("/wakeup", 'wakeup')
                            self.send_mqtt_message("/seeebot", 'How can I help you?')
                            self.tts.output_audio('How can I help you? ')
                            break
                    break

                if self.wakeup and self.asr_interrupt_flag[1] > 0.1:
                    self.send_mqtt_message.send_msg("/human", self.asr_interrupt_flag[0])
                    output = self.agent.run(input=self.asr_interrupt_flag[0])
                    self.send_mqtt_message.send_msg("/seeebot", output)
                    print(output)
                    self.tts.output_audio(output)
                time.sleep(1)
                self.asr_interrupt_flag = None
                self.asr_mute = False
            else:
                time.sleep(0.1)

    def run_webui(self):
        import gradio as gr

        def respond(message):
            self.send_mqtt_message("/human", message)
            bot_message = self.agent.run(input=message)
            self.send_mqtt_message("/seeebot", bot_message)
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
                    if 'How can' in transcript or 'how can' in transcript:
                        return 'wakeup...'
                    self.asr_interrupt_flag = (transcript, result.alternatives[0].confidence)
                    print("## " + transcript + f"Confidence:{result.alternatives[0].confidence:9.4f}")
                else:
                    # print('>> ' + transcript)
                    pass
        finally:
            pass

    def send_mqtt_message(self, topic, message):
        if self.mqtt_client is not None:
            self.mqtt_client.send_msg(topic, message)
        else:
            return 0

    @staticmethod
    def get_riva_devices_list():
        input_device, output_device = None, None
        p = pyaudio.PyAudio()

        print("Input audio devices:")
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info['maxInputChannels'] < 1:
                continue
            if 'USB' in info["name"]:
                input_device = info
            print(f"{info['index']}: {info['name']}")

        print("Output audio devices:")
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info['maxOutputChannels'] < 1:
                continue
            if 'USB' in info["name"]:
                output_device = info
            print(f"{info['index']}: {info['name']}")

        p.terminate()
        if input_device is None or output_device is None:
            print('No available riva device found, please manually config an device.')
            sys.exit(0)
        else:
            return input_device, output_device


if __name__ == '__main__':
    args = parse_args()
    chatbot = SeeeBot(
        openai_api=args.openai_api,
        text_inference_server=args.text_inference_server,
        riva_server=args.riva_server,
        ha_access_token=args.ha_access_token
    )
    chatbot.run()

