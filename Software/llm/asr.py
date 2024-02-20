#!/usr/bin/env python3
import time
import threading
import riva.client
import riva.client.audio_io


class ASR(threading.Thread):

    def __init__(self, auth=None, input_device=None, sample_rate_hz=16000, audio_chunk=1600, audio_channels=1,
                 automatic_punctuation=True, verbatim_transcripts=True, profanity_filter=False,
                 language_code='en-US', boosted_lm_words=None, boosted_lm_score=4.0, callback=None):
        super(ASR, self).__init__()

        assert auth is not None, f"Invalid parameter： {auth}"
        self.asr_service = riva.client.ASRService(auth)

        self.input_device = input_device
        self.sample_rate_hz = sample_rate_hz
        self.audio_chunk = audio_chunk
        self.callback = callback
        if self.callback is None:
            self.callback = self.callback_example

        self.asr_config = riva.client.StreamingRecognitionConfig(
            config=riva.client.RecognitionConfig(
                encoding=riva.client.AudioEncoding.LINEAR_PCM,
                language_code=language_code,
                max_alternatives=1,
                profanity_filter=profanity_filter,
                enable_automatic_punctuation=automatic_punctuation,
                verbatim_transcripts=verbatim_transcripts,
                sample_rate_hertz=sample_rate_hz,
                audio_channel_count=audio_channels,
            ),
            interim_results=True,
        )

        riva.client.add_word_boosting_to_config(self.asr_config, boosted_lm_words, boosted_lm_score)
        self.mute_flag = False
        self.stop_flag = False

    def run(self):
        with riva.client.audio_io.MicrophoneStream(
                self.sample_rate_hz,
                self.audio_chunk,
                device=self.input_device,
        ) as audio_chunk_iterator:
            responses = self.asr_service.streaming_response_generator(
                audio_chunks=audio_chunk_iterator, streaming_config=self.asr_config
            )
            for response in responses:
                if self.stop_flag:
                    audio_chunk_iterator.close()
                    print("ASR Server Shutdown!")
                if self.get_mute_state():
                    continue
                else:
                    if not response.results:
                        continue
                    self.callback(response)

    @staticmethod
    def callback_example(response):
        try:
            for result in response.results:
                if not result.alternatives:
                    continue
                transcript = result.alternatives[0].transcript
                if result.is_final:
                    print("## " + transcript)
                    print(f"Confidence:{result.alternatives[0].confidence:9.4f}" + "\n")
                    return True
                else:
                    print(">> " + transcript)
                    print(f"Stability：{result.stability:9.4f}" + "\n")
        finally:
            pass

    def get_mute_state(self):
        return self.mute_flag

    @staticmethod
    def list_devices():
        riva.client.audio_io.list_input_devices()


if __name__ == '__main__':

    ASR.list_devices()

    # _riva_server = "192.168.49.74:50051"
    # _input_device = 16
    # _sample_rate_hz = 16000
    # _auth = riva.client.Auth(uri=_riva_server)
    # asr = ASR(_auth, input_device=_input_device, sample_rate_hz=_sample_rate_hz)
    # asr.start()
    #
    # while True:
    #     print(">>>> The main line into the ongoing. <<<<")
    #     time.sleep(5)
    #     break
    #
    # asr.stop_flag = True
    # print(">>>> waiting... <<<<")
    # time.sleep(5)
