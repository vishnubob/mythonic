#!/usr/bin/env python

import glob
import math
import os.path
import random
import serial

import midi.sequencer
import midi

import biscuit
from music import make_looper
import pictureframe

import ss
from ss.pictureframes import *

MIDI_CLIENT = 20
MIDI_PORT = 0

MIDI_TRACKS = glob.glob(os.path.join("..", "music_raw", "ssb", "*.mid"))

ROUTING = {
    "/dev/ttyUSB0": range(1, 7),
    "/dev/ttyUSB1": range(7, 14)
}

PICTURE_FRAMES = [
    RedSitsAlone(1, tracks=["drums_3_36"]),
    RedSewsBat(2, tracks=["lead_1"]),
    RedFinishesBat(3, tracks=["drums_3_37"]),
    RedHugsBat(4, tracks=["drums_3_38"]),
    RedPlaysWithBat(5, tracks=["pad"]),
    RedHangsBat(6, tracks=["drums_3_39"]),
    BatFliesAway(10, tracks=["bass"]),
    BatTakesOff(9, tracks=["lead_2"]),
    BatEatsStars(8, tracks=["drums_3_40"]),
    BatTripsBalls(7, tracks=["drums_3_41"]),
    RedIsSad(11, tracks=["lead_3"]),
    PlanetTapsShoulder(12, tracks=["drums_3_46"]),
    PlanetHangout(13, tracks=["drums_3_49"])
]

def main():
    looper = make_looper(MIDI_TRACKS, MIDI_CLIENT, MIDI_PORT)
    addresses = []
    serial_ports = []
    picture_frames = []
    for tty_dev in ROUTING:
        tty = serial.Serial(tty_dev, baudrate=1000000)
        for human_address in ROUTING[tty_dev]:
            real_address = human_address - 1
            addresses.append(real_address)
            serial_ports.append(tty)
            picture_frame = [pf for pf in PICTURE_FRAMES if pf.real_address == real_address][0]
            picture_frames.append(picture_frame)
    hc = biscuit.HardwareChain(serial_ports, addresses)
    manager = ss.SSManager(hc, pictureframe.Storyboard(picture_frames, track_listing(MIDI_TRACKS)), looper)
    manager.run()

def track_listing(tracks):
    return dict((os.path.splitext(os.path.basename(path))[0], idx) for idx, path in enumerate(tracks))

if __name__ == '__main__':
    main()
