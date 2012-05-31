#!/usr/bin/env python

import sys
import serial
import time
import colorsys

port = serial.Serial(sys.argv[1], baudrate=57600)

def touched():
    data = 'T'
    port.write(data)
    vals = port.read(4)
    for val in vals:
        if ord(val) > 50:
            return True
    return False

val = 0

while 1:
    if touched():
        val = min(255, val + 1)
    else:
        val = max(0, val - 1)
    vals = [val] + ([0] * 5)
    vals = [chr(x) for x in vals]
    data = 'L' + str.join('', vals)
    port.write(data)
