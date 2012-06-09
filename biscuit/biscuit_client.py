#!/usr/bin/env python

import sys
import serial
import time
import colorsys

port = serial.Serial(sys.argv[1], baudrate=57600)

def touched():
    data = 'T'
    port.write(data)
    vals = map(ord, port.read(8))
    res = []
    for frame in range(2):
        touched = False
        for side in range(4):
            idx = frame * 4 + side
            if vals[idx] > 100:
                touched = True
                break
        res.append(touched)
    return res

frames = [0, 0]

while 1:
    for (frame_idx, tflag) in enumerate(touched()):
        val = frames[frame_idx]
        if tflag:
            val = min(255, val + 1)
        else:
            val = max(0, val - 1)
        frames[frame_idx] = val
    data = []
    for val in frames:
        data.append(val)
        data.extend([0] * 5)
    data = [chr(x) for x in data]
    data = 'L' + str.join('', data)
    port.write(data)
