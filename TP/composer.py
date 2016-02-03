#code from 15110 sound lab
import wave
from math import *
from array import array
from struct import pack, unpack_from

def applyImageFilter(image):
    pixels=image.loads()

ARATE = 96000
MAX_AMP = 0x7FFF

def sine_tone(freq, dur, amp):
    sine = [0.0] * int(dur/1000.0 * ARATE)
    for i in range(len(sine)):
        sine[i] = amp * sin(i * 2 * pi * freq / ARATE)
    return envelope(sine, 0.1, 0.2)

def samples_to_shorts(sound):
    data = bytearray()
    for s in sound:
        if abs(s) > 1:
            s = s / abs(s)
        data += pack('h', int(MAX_AMP * s))
    return data

def write_wave(sound,name):
    wf = wave.open(name, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(ARATE)
    wf.writeframes(samples_to_shorts(sound))
    #wf.writeframes(samples_to_shorts(sound))
    wf.close()

def envelope(sound, attack, decay):
    # attack is the duration of the onset
    # decay is the duration of the ending
    attack = int(attack * 44100) # convert to samples
    decay = int(decay * 44100)
    if attack + decay > len(sound):
        attack = len(sound) // 2
        decay = attack
    for i in range(attack):
        sound[i] = sound[i] * i / attack
    last = len(sound) - 1
    for i in range(decay):
        sound[last - i] = sound[last - i] * i / decay
    return sound


def read_wave(name):
    wf = wave.open(name, 'rb')
    size = wf.getnframes()
    chans = wf.getnchannels()
    data = wf.readframes(size)
    samples = []
    skip = 2 * chans # the frame size
    for i in range(size): # read first sample of each frame
        samples.append(
            unpack_from('h', data, offset = i * skip)[0] / MAX_AMP)
    return samples


#time in milliseconds of each note length

s = 150 #sixteenth
e = 2*s #eighth
de = 3*s #dotted eighth
q = 2*e #quarter
dq = 3*e #dotted_quarter
h = 2*q #half
dh = 3*q #dotted_half
w = 4*q #whole

rhythms=[s,e,de,q,dq,h,dh,w]

#note Frequency Definitions
C3 = 142
Csh3 = 151
D3 = 160
Dsh3 = 169
E3 = 180
F3 = 190
Fsh3 = 202
G3 = 213
Gsh3 = 227
A3 = 240
Ash3 = 255
B3 = 269
C4 = 285   # middle C
Csh4 = 303 # C#/Db
D4 = 319   # D
Dsh4 = 338 # D#/Eb
E4 = 358
F4 = 381
Fsh4 = 402
G4 = 426
Gsh4 = 453
A4 = 480
Ash4 = 507
B4 = 537
C5 = 570
Csh5 =604
D5 = 640
Dsh5 = 678
E5 = 716
F5 = 760
Fsh5 = 805
G5 = 855
Gsh5 = 904
A5 = 958
Ash5 = 1014
B5 = 1074
C6 = 1140
Csh6 = 1210
D6 = 1280
Dsh6 = 1355
E6 = 1436
F6 = 1520
Fsh6 = 1613
G6 = 1710


notes=[C3,Csh3,D3,Dsh3,E3,F3,Fsh3,G3,Gsh3,A3,Ash3,B3,C4,Csh4,
D4,Dsh4,E4,F4,Fsh4,G4,Gsh4,A4,Ash4,B4,C5,Csh5,D5,Dsh5,E5,F5,
Fsh5,G5,Gsh5,A5,Ash5,B5,C6,Csh6,D6,Dsh6,E6,F6,Fsh6,G6]

#A melody is composed of a note
# (frequency) and the length
# that a note is played.
lullaby = [ [B4, h], [D5, q], [A4, h], [G4, e],
            [A4, e],[B4, h],  [D5, q],[A4, dh],
            [B4, h], [D5, q], [A5, h], [G5, q],
            [D5, h], [C5, e], [B4, e], [A4, dh],
            [B4, h], [D5, q], [A4, h], [G4, e],
            [A4, e], [B4, h], [D5, q],[A4, dh],
            [B4, h], [D5, q], [A5, h], [G5, q],
            [D6, 7*q],[D6, h],[C6, e],[B5, e],
            [C6, e], [B5, e], [G5, h], [C6, h],
            [B5, e], [A5, e], [B5, e],[A5, e],
            [E5, h], [D6, h], [C6, e], [B5, e],
            [C6, e], [B5, e], [G5, q], [C6, q],
            [G6, 3*h], [0, 2*h] ]

def write_tune(tune, filename):
    tune_list = []
    for note in tune:
        tune_list += sine_tone(note[0], note[1], 190.0/note[0])
    write_wave(tune_list, filename)

def speed(sound, factor):
    result = []
    loc = 0
    while(loc < len(sound)):
        result.append(sound[int(loc)])
        loc = loc + factor
    return result