
# Description ： Chatbot_v1.0 + HomeAssistant.

import sys

from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain_core.prompts.prompt import PromptTemplate
import time

import riva.client
import riva.client.audio_io

from asr import ASR
from tts import TTS
from local_llm import CustomLLM
from ha import HomeAssistant


class SeeeBot:
    def __init__(self, openai_api=None, text_inference_server='http://192.168.49.103:8899/generate', riva_server=None,
                 asr_input_device_id=7, asr_sample_rate_hz=48000, tts_output_device_id=7, tts_sample_rate_hz=48000):

        if openai_api is not None:
            self.llm = OpenAI(openai_api_key=openai_api, temperature=0)
            self.memory = ConversationBufferWindowMemory(k=5)
            self.conversation = ConversationChain(llm=self.llm, verbose=True, memory=self.memory)
        elif text_inference_server is not None:
            llm = CustomLLM(url=text_inference_server, temperature=0.5, max_new_tokens=100)
            template = """ Please answer the human question in short sentences. 
            Just answer the questions and don't generate too much content.
            Current conversation:
            {history}
            Human: {input}
            AI:
            """
            memory = ConversationBufferWindowMemory(k=5)
            prompt = PromptTemplate(input_variables=["history", "input"], template=template)
            self.conversation = ConversationChain(llm=llm, verbose=True, prompt=prompt, memory=memory)
        else:
            print('No model to load!')
            sys.exit(0)

        self.auth = None
        self.chat_history = []
        if riva_server is not None:
            self.auth = riva.client.Auth(uri=riva_server)
            self.asr = ASR(self.auth, input_device=asr_input_device_id, sample_rate_hz=asr_sample_rate_hz, callback=self.on_asr_transcript)
            self.asr_interrupt_flag = None
            self.tts = TTS(self.auth, output_device=tts_output_device_id, sample_rate_hz=tts_sample_rate_hz)

            self.asr_mute = False
            self.wakeup = False
            self.wakeup_world = ['Mira', 'Miro', 'mirror', 'Mirror']
            self.sleep_world = ['goodbye', 'Goodbye']

        self.ha = HomeAssistant()

    def run(self):
        if self.auth is not None:
            self.asr.start()
            time.sleep(0.5)
            while True:
                if self.asr_interrupt_flag is not None:
                    self.asr_mute = True
                    if self.wakeup:
                        for world in self.sleep_world:
                            if world in self.asr_interrupt_flag[0]:
                                self.wakeup = False
                                self.tts.output_audio('Have a nice day.')
                                break
                    else:
                        for world in self.wakeup_world:
                            if world in self.asr_interrupt_flag[0]:
                                self.wakeup = True
                                self.tts.output_audio('How can I help you?')
                                break

                    if self.wakeup and self.asr_interrupt_flag[1] > 0.2:
                        output = self.conversation.predict(input=self.asr_interrupt_flag[0])
                        print(output)
                        self.tts.output_audio(output)
                    time.sleep(1.5)
                    self.asr_interrupt_flag = None
                    self.asr_mute = False
                else:
                    time.sleep(0.1)

    def on_asr_transcript(self, response):
        try:
            if self.asr_mute:
                # print('waiting tts...')
                return 'waiting...'
            for result in response.results:
                if not result.alternatives:
                    continue
                transcript = result.alternatives[0].transcript
                if result.is_final:
                    self.asr_interrupt_flag = (transcript, result.alternatives[0].confidence)
                    print("## " + transcript + f"Confidence:{result.alternatives[0].confidence:9.4f}")
                else:
                    print('>> ' + transcript)
        finally:
            pass

    def turn_off_light_of_living_room(self, args):
        self.ha.setup_switch('off', self.ha.entity_ids['light'])

    def turn_on_light_of_living_room(self, args):
        self.ha.setup_switch('on', self.ha.entity_ids['light'])


if __name__ == '__main__':
    chatbot = SeeeBot(
        openai_api='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',
        # riva_server="192.168.49.103:50051",
    )

    chatbot.run()
