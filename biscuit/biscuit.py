#!/usr/bin/env python

import sys
import serial
import time

port = serial.Serial(sys.argv[1], 250000)

def send(data):
    for ch in data:
        port.write(ch)
        port.flush()

def recv():
    if not port.inWaiting():
        return
    ch = port.read(1)
    if ch == 'T':
        val = port.read(1)
        print "GOT T", ord(val)
    else:
        print "unk", ch, ord(ch)

def pulse():
    for ch in range(6):
        if ch == 1:
            continue
        for x in range(0xff):
            data = [0, 0, 0, 0, 0, 0]
            data[ch] = x
            final = []
            for box in range(7):
                final.extend(data) 
            cmd = 'L' + str.join('', map(chr, final))
            print x, len(cmd)
            port.write(cmd)
            port.flush()
            time.sleep(.01)
        for x in range(0xff, 0, -1):
            data = [0, 0, 0, 0, 0, 0]
            data[ch] = x
            final = []
            for box in range(7):
                final.extend(data) 
            cmd = 'L' + str.join('', map(chr, final))
            print x, len(cmd)
            port.write(cmd)
            port.flush()
            time.sleep(.01)

def ping():
    for x in range(7):
        raw_input("next %s>" % (x + 1))
        cmd = 'R' + chr(x)
        port.write(cmd)

while 1:
    pulse()
#ping()

