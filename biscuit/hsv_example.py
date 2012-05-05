#!/usr/bin/env python

from colorsys import *
import serial
import sys, serial, time

port = "/dev/ttyUSB0"
if len(sys.argv) > 1:
    port = sys.argv[1]
biscuit = serial.Serial(port, 57600)
print "sync'n"
while 1:
    biscuit.write('&')
    if biscuit.inWaiting():
        ch = biscuit.read(1)
        if ch == '!':
            biscuit.flushInput()
            break

while 1:
    for step in range(1000):
        hue = step / 1000.0
        print hue
        rgb = [int(val * 0xFF) for val in hsv_to_rgb(hue, 1.0, 1.0)]
        packet = 'W' + str.join('', map(chr, rgb + [0, 0, 0]))
        print map(ord, packet)
        for ch in packet:
            biscuit.write(ch)
        time.sleep(.1)

arduino.close()



