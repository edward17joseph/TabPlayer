'''Player.py controls logic and playback of guitar strings, creating and
manipulating sin waves used by simpleaudio library for production of sound.'''

import simpleaudio as sa
import numpy as np
from tab_parser import *


samples = 10
##############################################################################
# get timesteps for each sample, T is note duration in seconds
##############################################################################
sample_rate = 44100
T=1
t = np.linspace(0, T, int(T * sample_rate), False)
##############################################################################
#Sound Wave Globals
#Wave Model: http://large.stanford.edu/courses/2007/ph210/pelc2/
##############################################################################
n = np.arange(1,samples+1)
A = A_n(.3,samples)
e = np.e ** (-1 * n * 2)
y= A * np.array(list(map(lambda i:e ** i, t)))


def f_n(freq, n):
    b = .03
    if n ==1:
        return np.array([freq])
    else:
        return np.concatenate((f_n(freq, n - 1),
            [n * freq * (1 + (b * n) ** (2)) ** (1/2)]))

def A_n(L_d, n):
    h = 1
    A = 2 * h * (L_d * (1 - L_d ** - 1) ** -1) / (
        (np.pi * n) ** 2) * np.sin(n * np.pi * L_d ** (-1))
    if n == 1:
        return np.array([A])
    else:
        return np.concatenate((A_n(L_d, n-1), [A]))
##############################################################################
#GUITAR STRING OBJECTS
##############################################################################
class guitar_string:
    def __init__(self, freq):
        self.freq = freq
    def generate_note(self, seq):
        arr = list(filter(None, re.split('(\d+)',seq)))
        #b denotes bend in string
        if 'b' in arr:
            freq = bend(self.freq, arr)
        #\ denotes slide
        elif '\\' in arr:
            freq = slide(self.freq, arr)
        #- denotes no note
        elif '-' in arr:
            return 0
        #p, h, or numerical denotes normal note.
        else:
            freq = hammer_pick(self.freq, arr)
        #normalize sound wave and convert to 16-bit arr
        freq = normalize(freq)
        play_obj = sa.play_buffer(freq.astype(np.int16), 1, 2, sample_rate)

##############################################################################
#TYPES OF STRING HITS
##############################################################################
'''String Bends, denoted with two or less numerical values, start at initial
note and continuously rise to second pitch until followed by continuous
decrease to base pitch.'''
def bend(start_freq, seq):
    start = int(seq[0])
    if len(seq) == 2:
        end = start + 2
    else:
        end = int(seq[2])
    height = np.linspace(start_freq * 2 ** (start/12),
        start_freq * 2 ** (end/12), int(T * sample_rate), False)
    #create sine wave
    freq = np.sin(height * t * 2 * np.pi)
    freq = np.concatenate((freq[:-1],freq[::-1]))
    return freq

'''String Slides start at initial frequency and discretely increase in pitch
until end pitch is reached.'''
def slide(start_freq, seq):
    if len(seq) == 2:
        end = int(seq[1])
        start = end - 2
    else:
        start = int(seq[0])
        end = int(seq[2])
    height = start_freq * 2 ** (np.arange(start, end + 1) / 12)
    height = np.repeat(height, int(T * sample_rate//(end - start +1)))
    #create sine wave
    freq = np.sin(height * t * 2 * np.pi)
    return freq

'''Hammer-Pick begins at begins at initial frequency and switches to following
pitch if present.'''
def hammer_pick(start_freq, seq):
    #create sine wave
    freq = f_n(start_freq * 2 ** (int(seq[0])/ 12), samples) * 2 * np.pi
    freq = np.array(list(map(lambda i,j:sum(np.sin(freq * i)* j), t, y)))
    freq = fade(freq)
    if len(seq)!=1:
        freq = np.append(freq, hammer_pick(start_freq,seq[2:]))
    return freq


##############################################################################
#Miscellaneous
##############################################################################
'''Fades volume of wave in and out to reduce rough transition between waves'''
def fade(freqs):
    t = np.linspace(0, 1, len(freqs), False)
    taper = np.sin(t * np.pi + np.sin(t * np.pi)/4)
    return freqs*taper

'''Normalizes frequencies to 16 bit value'''
def normalize(x):
    if np.max(x) == 0:
        return np.zeros(1)
    else:
        return x*32767 / np.max(np.abs(x))
