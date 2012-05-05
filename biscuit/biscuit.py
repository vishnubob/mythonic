#!/usr/bin/env python

import serial
import time

port = serial.Serial('/dev/tty.usbserial-A100JOEV', 250000)

def send(data):
    for ch in data:
        port.write(ch)
        recv()

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
    while 1:
        for x in range(0xff):
            print x
            cmd = 'L' + (chr(0) * 2) + chr(x) + (chr(0) * 137)
            send(cmd)
            port.flush()
            time.sleep(.05)
        for x in range(0xff, 0, -1):
            print x
            cmd = 'L' + (chr(0) * 2) + chr(x) + (chr(0) * 137)
            send(cmd)
            time.sleep(.05)

pulse()
