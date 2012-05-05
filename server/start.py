#!/usr/bin/env python

import sys
import serial
from mythonic import *
from wired import *

def main():
    if len(sys.argv) != 2:
        script_name = sys.argv[0]
        print "Usage:   {0} <tty>".format(sys.argv[0])
        print "Example: {0} /dev/ttyUSB0".format(sys.argv[0])
        exit(2)

    tty = sys.argv[1]
    bus = serial.Serial(tty, 250000)

    picture_frames = [WiredPictureFrame(i) for i in range(7)]
    mediator = MythonicMediator(picture_frames, bus)

    while True:
        time.sleep(0.1)
        mediator.think()

if __name__ == "__main__":
    main()
