from player import *
import sys
import time
###############################################################################
#String Frequencies
###############################################################################
High_E_freq = 220 * 2 ** (19 / 12)
B_freq = 220 * 2 ** (14 / 12)
G_freq = 220 * 2 ** (10 / 12)
D_freq = 220 * 2 ** (5 / 12)
A_freq = 220 * 2
Low_E_freq = 220 * 2 ** (-5 / 12)
###############################################################################
#Create GUITAR
###############################################################################
high_e_string = guitar_string(High_E_freq)
b_string = guitar_string(B_freq)
g_string = guitar_string(G_freq)
d_string = guitar_string(D_freq)
a_string = guitar_string(A_freq)
low_e_string = guitar_string(Low_E_freq)

GUITAR = [high_e_string,b_string,g_string, d_string, a_string, low_e_string]
###############################################################################

tab = process_text(filter_text(input4))

n = min(list(map(len,tab)))
offset = np.array([0,0,0,0,0,0])
for i in range(n):
    index = offset+i
    notes=list(map(lambda x,y: x[int(y)], tab, index))
    print(notes)
    note_lengths = np.array(list(map(len, notes)))
    offset += (max(note_lengths) - note_lengths)
    play_obj = list(map(lambda x,y: x.generate_note(y), GUITAR, notes))
    if notes != ['-','-','-','-','-','-']:
            time.sleep(.1)
