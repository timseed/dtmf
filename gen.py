#!/usr/bin/env python3

import pyaudio
import array
import math
from time import sleep
import wave

user_freq = [697.0, 770.0, 852.0, 941.0,
             1209.0, 1336.0, 1477.0, 1633.0]
user_tones = {
    '1': (user_freq[0], user_freq[4]),
    '2': (user_freq[0], user_freq[5]),
    '3': (user_freq[0], user_freq[6]),
    'A': (user_freq[0], user_freq[7]),
    '4': (user_freq[1], user_freq[4]),
    '5': (user_freq[1], user_freq[5]),
    '6': (user_freq[1], user_freq[6]),
    'B': (user_freq[1], user_freq[7]),
    '7': (user_freq[2], user_freq[4]),
    '8': (user_freq[2], user_freq[5]),
    '9': (user_freq[2], user_freq[6]),
    'C': (user_freq[2], user_freq[7]),
    '*': (user_freq[3], user_freq[4]),
    '0': (user_freq[3], user_freq[5]),
    '#': (user_freq[3], user_freq[6]),
    'D': (user_freq[3], user_freq[7]),
}
op_freq = [700.0, 900.0, 1100.0, 1300.0, 1300.0, 1500.0, 1700.0]

op_tones = {
    '1': (op_freq[0], op_freq[1]),
    '2': (op_freq[0], op_freq[2]),
    '3': (op_freq[1], op_freq[2]),
    '4': (op_freq[0], op_freq[3]),
    '5': (op_freq[1], op_freq[3]),
    '6': (op_freq[2], op_freq[3]),
    '7': (op_freq[0], op_freq[4]),
    '8': (op_freq[1], op_freq[4]),
    '9': (op_freq[2], op_freq[4]),
    '0': (op_freq[3], op_freq[4]),  # 0 or "10"
    'A': (op_freq[3], op_freq[4]),  # 0 or "10"
    'B': (op_freq[0], op_freq[5]),  # 11 or ST3
    'C': (op_freq[1], op_freq[5]),  # 12 or ST2
    'D': (op_freq[2], op_freq[5]),  # KP
    'E': (op_freq[3], op_freq[5]),  # KP2
    'F': (op_freq[4], op_freq[5]),  # ST
}



length = 0.25
volume = .65
frames=[]

p = pyaudio.PyAudio()

CHUNK = 10240
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
WAVE_OUTPUT_FILENAME = "t.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                frames_per_buffer=CHUNK,
                output=True)

tone_set = user_tones
beeps = input('>>>')
for command in beeps:
        if command is 'U':
            tone_set = user_tones
            continue
        elif command is 'O':
            tone_set = op_tones
            continue
        try:
            tone = tone_set[command]
            data=array.array('f',
                                             ((volume * math.sin(i / (tone[0] / 100.)) + volume * math.sin(i / (tone[1] / 100.)))
                                              for i in range(int(RATE*length)))).tostring()
        except KeyError:
            if command.upper() is 'Q':
                 break
            if command is  ' ':
                #Create an Empty Buffer
                data=array.array('f',   ((0)
                                  for i in range(int(RATE*length)))).tostring()
        print("Length of Data is ",len(data))
        stream.write(data)
        frames.append(data)
sleep(2)
print("Replay")

for f in frames:
    stream.write(f)
print("Replay Over")

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

stream.close()
p.terminate()
