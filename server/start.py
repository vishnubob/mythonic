#!/usr/bin/env python

import sys
import serial
from metranome import Metranome
from mythonic import *

def main():
    if len(sys.argv) != 2:
        script_name = sys.argv[0]
        print "Usage:   {0} <tty>".format(sys.argv[0])
        print "Example: {0} /dev/ttyUSB0".format(sys.argv[0])
        exit(2)

    tty = sys.argv[1]
    bus = serial.Serial(tty)

    picture_frames = [MythonicPictureFrame(i) for i in range(7)]
    storyboard = MythonicStoryboard(bus, picture_frames)

    metranome = Metranome(60)
    beat = metranome.start()
    while beat is None or beat < 10:
        if beat is not None:
            print "==== " + str(beat) + " ====="

        storyboard.update(metranome.time())

        # "None" if a beat passes, a whole beat number otherwise
        beat = metranome.next_beat()

if __name__ == "__main__":
    main()
