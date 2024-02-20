#!/usr/bin/env python3
import time
import riva.client
import riva.client.audio_io


class TTS:
    def __init__(self, auth, output_device=None, sample_rate_hz=16000, language_code='en-US', voice='English-US.Female-1'):
        self.tts_service = riva.client.SpeechSynthesisService(auth)
        self.output_device = output_device
        self.sample_rate_hz = sample_rate_hz
        self.language_code = language_code
        self.voice = voice

    def output_audio(self, text):
        sound_stream = None
        try:
            sound_stream = riva.client.audio_io.SoundCallBack(
                self.output_device, nchannels=1, sampwidth=2, framerate=self.sample_rate_hz
            )

            responses = self.tts_service.synthesize_online(
                text, self.voice, self.language_code, sample_rate_hz=self.sample_rate_hz
            )

            for resp in responses:
                if sound_stream is not None:
                    sound_stream(resp.audio)
        finally:
            if sound_stream is not None:
                sound_stream.close()

    @staticmethod
    def list_devices():
        riva.client.audio_io.list_output_devices()


if __name__ == '__main__':
    TTS.list_devices()

    # riva_server = "192.168.49.103:50051"
    # output_device = 7
    # sample_rate_hz = 48000
    # auth = riva.client.Auth(uri=riva_server)
    # tts = TTS(auth, output_device, sample_rate_hz)
    # tts.output_audio(
    #     "According to the test standards you provided, under the premise that the resource utilization rate "
    #     "should not exceed 70%, the reComputer can support up to 8 cameras."
    # )
    # print('Done')
    # time.sleep(2)
