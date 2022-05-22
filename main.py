import numpy as np
import simpleaudio as sa
import scipy.io.wavfile as wav
import time

frequency = 440         # Hz (cycles/second)
sample_rate = 48000     # samples/second
duration = 1            # seconds

t = np.linspace(0, duration, duration * sample_rate, False)
sine_note = np.sin(frequency * t * (2 * np.pi))
audio = sine_note * (2 ** 15 - 1) / np.max(np.abs(sine_note))

# scale audio to 1/2 amplitude
amplitude = 10 ** (-6 / 20)
audio *= amplitude
audio = audio.astype(np.int16)

# clip amplitude over/under 1/4
clipped_audio = np.clip(audio, -8192, 8192)

wav.write('clipped.wav', sample_rate, clipped_audio)

''' Play sample audio in buffer for testing purposes'''
# wave_obj = sa.WaveObject(audio, 1, 2, sample_rate)
# play_obj = wave_obj.play()
# play_obj.wait_done()
#
# time.sleep(1)

''' Part (3) Play the clipped audio wav file '''
wave_obj = sa.WaveObject.from_wave_file('clipped.wav')
play_obj = wave_obj.play()
play_obj.wait_done()
