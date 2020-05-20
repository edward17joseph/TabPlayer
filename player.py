import simpleaudio as sa
import numpy as np

# get timesteps for each sample, T is note duration in seconds
sample_rate = 44100
T = .25
t = np.linspace(0, T, int(T * sample_rate), False)

# calculate string frequencies
High_E_freq = 220 * 2 ** (19 / 12)
B_freq = 220 * 2 ** (14 / 12)
G_freq = 220 * 2 ** (10 / 12)
D_freq = 220 * 2 ** (5 / 12)
A_freq = 220 * 2
Low_E_freq = 220 * 2 ** (-5 / 12)

#[HIGHE, B, G, D, A, LOWE]
frequencies = [Low_E_freq * 2 ** (24 / 12), Low_E_freq * 2 ** (19 / 12),
    Low_E_freq * 2 ** (15 / 12), Low_E_freq * 2 ** (10 / 12),
    Low_E_freq * 2 ** (5 / 12), Low_E_freq]

# generate sine wave notes where nsteps is str containing the number of half
# steps higher than base frequency for each guitar string
def generate_note(nsteps):
    # calculate note frequencies
    freqs = note_freq(nsteps)
    #create sine wave
    freqs = list(map(lambda x: np.sin(x * t * 2 * np.pi), freqs))
    # normalize to 16-bit range
    freqs = list(map(normalize, freqs))
    # convert to 16-bit data
    list(map(lambda x: sa.play_buffer(x.astype(np.int16), 1, 2, sample_rate),
    freqs))

def note_freq(nsteps):
    freq=[]
    for step in range(6):
        if nsteps[step] == "-":
            freq += [0]
        else:
            freq += [frequencies[step] * 2 ** (int(nsteps[step]) / 12)]
    return freq

def normalize(x):
    if np.max(np.abs(x)) == 0:
        return np.zeros(int(44100*T))
    else:
        return x*32767 / np.max(np.abs(x))
