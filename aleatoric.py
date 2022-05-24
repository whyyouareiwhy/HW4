import numpy as np
import simpleaudio as sa
import scipy.io.wavfile as wav
import time
import sys
import getopt
import argparse


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
    # clipped_audio = np.clip(audio, -8192, 8192)

    # write to wav file (can remove later!!!)
    # wav.write('clipped.wav', sample_rate, clipped_audio)

    return audio


def play_measure(octave_notes):
    for note in major_scale_notes:
        pitch = octave_notes[note]
        audio_sample = sin_wave(pitch)
        # Play using audio buffer
        wave_obj = sa.WaveObject(audio_sample, 1, 2, 48000)
        play_obj = wave_obj.play()
        play_obj.wait_done()


# generate music in C[root] measure, root = 2-7
def random_music(root):
    print("To Do")


octave = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
major_scale = [0, 2, 4, 5, 7, 9, 11]
notes = [octave[i] for i in major_scale]
major_scale_notes = [octave[0], octave[2], octave[4], octave[5], octave[7], octave[9], octave[11]]

'''Create notes for octave 2-8 which will be sampled for the measure to generate random keys
using a C note as the base frequency.'''
octave_2_notes = {octave[i]: 65.41 * pow(2, (i/12)) for i in range(len(octave))}  # C2 root (key 36)
octave_3_notes = {octave[i]: 130.81 * pow(2, (i/12)) for i in range(len(octave))}  # C3 root (key 48)
octave_4_notes = {octave[i]: 261.63 * pow(2, (i/12)) for i in range(len(octave))}  # C4 root (key 60)
octave_5_notes = {octave[i]: 523.25 * pow(2, (i/12)) for i in range(len(octave))}  # C5 root (key 72)
octave_6_notes = {octave[i]: 1046.5 * pow(2, (i/12)) for i in range(len(octave))}  # C6 root (key 84)
octave_7_notes = {octave[i]: 2093.0 * pow(2, (i/12)) for i in range(len(octave))}  # C7 root (key 96)

'''Default values are set for all possible arguments, but can be modified by user.'''
parser = argparse.ArgumentParser(description='Random music generator.')
parser.add_argument('--root', dest='root', type=int, default=48)  # root note key (C2 = 48)
parser.add_argument('--beats', dest='beats', type=int, default=8)  # beats per measure
parser.add_argument('--bpm', dest='bpm', type=float, default=90.0)  # beats per minute
parser.add_argument('--ramp', dest='ramp', type=float, default=0.50)  # attack and release time
parser.add_argument('--accent', dest='accent', type=float, default=5.0)  # volume for accented 1st beat
parser.add_argument('--volume', dest='volume', type=float, default=5.0)  # volume for unaccented beats
args = parser.parse_args()

# wave_obj = sa.WaveObject.from_wave_file('clipped.wav')
# play_obj = wave_obj.play()
# play_obj.wait_done()
