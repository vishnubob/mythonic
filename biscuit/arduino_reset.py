#!/usr/bin/env python
import sys, serial, time

port = "/dev/ttyUSB0"
if len(sys.argv) > 1:
    port = sys.argv[1]
arduino = serial.Serial(port, 115200)
arduino.setRTS(0)
arduino.setDTR(0)
time.sleep(.3)
arduino.setRTS(1)
arduino.setDTR(1)
arduino.close()
time.sleep(.3)
