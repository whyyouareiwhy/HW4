import numpy as np
import simpleaudio as sa
import scipy.io.wavfile as wav
import time


def sin_wave(freq):
    frequency = freq         # Hz (cycles/second)
    sample_rate = 48000     # samples/second
    duration = 0.5            # seconds

    t = np.linspace(0, duration, int(duration * sample_rate), False)
    sine_note = np.sin(frequency * t * (2 * np.pi))
    audio = sine_note * (2 ** 15 - 1) / np.max(np.abs(sine_note))

    # scale audio to 1/2 amplitude
    amplitude = 10 ** (-6 / 20)
    audio *= amplitude
    audio = audio.astype(np.int16)

    # clip amplitude over/under 1/4
    clipped_audio = np.clip(audio, -8192, 8192)
    # write to wav file (can remove later!!!)
    wav.write('clipped.wav', sample_rate, clipped_audio)

    return clipped_audio


octave = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
# base_freq = 261.63  # C4 note
major_scale = [0, 2, 4, 5, 7, 9, 11]
notes = [octave[i] for i in major_scale]
major_scale_notes = [octave[0], octave[2], octave[4], octave[5], octave[7], octave[9], octave[11]]
# freq_range = {octave[i]: base_freq * pow(2, (i/12)) for i in range(len(octave))}

# Create notes for octave 2 - 8 which will be sampled for the random music generator
octave_2_notes = {octave[i]: 65.41 * pow(2, (i/12)) for i in range(len(octave))}
octave_3_notes = {octave[i]: 130.81 * pow(2, (i/12)) for i in range(len(octave))}
octave_4_notes = {octave[i]: 261.63 * pow(2, (i/12)) for i in range(len(octave))}
octave_5_notes = {octave[i]: 523.25 * pow(2, (i/12)) for i in range(len(octave))}
octave_6_notes = {octave[i]: 1046.5 * pow(2, (i/12)) for i in range(len(octave))}
octave_7_notes = {octave[i]: 2093.0 * pow(2, (i/12)) for i in range(len(octave))}
octave_8_notes = {octave[i]: 4186.01 * pow(2, (i/12)) for i in range(len(octave))}

print(major_scale_notes)
print(octave_6_notes)
for note in major_scale_notes:
    test = octave_6_notes[note]
    audio_sample = sin_wave(test)
    ''' Play sample audio in buffer for testing purposes'''
    wave_obj = sa.WaveObject(audio_sample, 1, 2, 48000)
    play_obj = wave_obj.play()
    play_obj.wait_done()

#
# time.sleep(1)

''' Part (3) Play the clipped audio wav file '''
# wave_obj = sa.WaveObject.from_wave_file('clipped.wav')
# play_obj = wave_obj.play()
# play_obj.wait_done()
