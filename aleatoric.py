import numpy as np
import scipy.fft
import scipy.signal as sps
import simpleaudio as sa
import scipy.io.wavfile as wav
import argparse
import random

SAMPLERATE = 48000

# TO-DO
# ramp envelope


def music_note(freq, amp, clip):
    duration = 60.0 / options.bpm
    t = np.linspace(0, duration, int(duration * SAMPLERATE), False)
    sine_note = np.sin(freq * t * (2 * np.pi))
    audio = sine_note * (2 ** 15 - 1) / np.max(np.abs(sine_note))

    # root note amplitude => [--accent] and non-root note => [--volume]
    audio *= (amp/10)

    # Square the note if clip arg is True (for root note of each measure)
    if clip:
        audio = np.clip(audio, a_min=-8192, a_max=8192)
        wav.write('clipped.wav', SAMPLERATE, audio)  # for testing in Audacity

    audio = audio.astype(np.int16)
    return audio


# Play a given measure in order from C base note to next octave's C
def play_measure(octave_notes):
    for note in major_scale_notes:
        pitch = octave_notes[note]
        audio_sample = music_note(pitch, options.accent)
        wave_obj = sa.WaveObject(audio_sample, 1, 2, SAMPLERATE)
        play_obj = wave_obj.play()
        play_obj.wait_done()


# generate music in C[root] measure, root = C2-C7
def random_music(measure):
    beat = 1
    # play root note with [--accent] volume settings
    root = major_notes[0]
    print(f"Note -> {root}  |  Frequency -> {format(measure[root], '.2f')} Hz  |  Beat -> {beat}")
    beat += 1
    root_note = music_note(measure[root], options.accent, True)
    wave_obj = sa.WaveObject(root_note, 1, 2, SAMPLERATE)
    play_obj = wave_obj.play()
    play_obj.wait_done()

    # play non-root notes in the rest of the measure
    for i in range(1, options.beats):
        rand_note = random.choice(major_notes)
        print(f"Note -> {rand_note}  |  Frequency -> {format(measure[rand_note], '.2f')} Hz  |  Beat -> {beat}")
        beat += 1
        non_root_note = music_note(measure[rand_note], options.volume, False)
        wave_obj = sa.WaveObject(non_root_note, 1, 2, SAMPLERATE)
        play_obj = wave_obj.play()
        play_obj.wait_done()
    print("---------------------------------------------------")


octave = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C+']  # C+ is next octave's C root note
major_scale = [0, 2, 4, 5, 7, 9, 11, 12]  # major scale that ends on root C note of next octave
major_notes = [octave[i] for i in major_scale]
major_scale_notes = [octave[0], octave[2], octave[4], octave[5], octave[7], octave[9], octave[11], octave[12]]

# create notes for octave 2-8 which will be sampled for the measure to generate random keys
# using a C note as the base frequency
octave_2_notes = {octave[i]: 65.41 * pow(2, (i/12)) for i in range(len(octave))}  # C2 root (key 36)
octave_3_notes = {octave[i]: 130.81 * pow(2, (i/12)) for i in range(len(octave))}  # C3 root (key 48)
octave_4_notes = {octave[i]: 261.63 * pow(2, (i/12)) for i in range(len(octave))}  # C4 root (key 60)
octave_5_notes = {octave[i]: 523.25 * pow(2, (i/12)) for i in range(len(octave))}  # C5 root (key 72)
octave_6_notes = {octave[i]: 1046.5 * pow(2, (i/12)) for i in range(len(octave))}  # C6 root (key 84)
octave_7_notes = {octave[i]: 2093.0 * pow(2, (i/12)) for i in range(len(octave))}  # C7 root (key 96)

# default values are set for all possible arguments, but can be modified by user
parser = argparse.ArgumentParser(description='Random music generator.')
parser.add_argument('--root', dest='root', type=int, default=48)  # root note key (C2 = 48)
parser.add_argument('--beats', dest='beats', type=int, default=8)  # beats per measure
parser.add_argument('--bpm', dest='bpm', type=float, default=90.0)  # beats per minute
parser.add_argument('--ramp', dest='ramp', type=float, default=0.50)  # attack and release time
parser.add_argument('--accent', dest='accent', type=float, default=5.0)  # volume for accented 1st beat
parser.add_argument('--volume', dest='volume', type=float, default=5.0)  # volume for unaccented beats
options = parser.parse_args()

print(f"--root {options.root} --beats {options.beats} --bpm {options.bpm} --ramp {options.ramp} --accent {options.accent}"
      f"--volume {options.volume}")
while True:
    if options.root == 36:
        random_music(octave_2_notes)
    elif options.root == 48:
        random_music(octave_3_notes)
    elif options.root == 60:
        random_music(octave_4_notes)
    elif options.root == 72:
        random_music(octave_5_notes)
    elif options.root == 84:
        random_music(octave_6_notes)
    elif options.root == 96:
        random_music(octave_7_notes)
