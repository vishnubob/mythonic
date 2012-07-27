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

MIDI_CLIENT = 24
MIDI_PORT = 0

MIDI_TRACKS = glob.glob(os.path.join("..", "music_raw", "ssb", "*.mid"))

ROUTING = {
    "/dev/ttyUSB0": range(1, 6),
    "/dev/ttyUSB1": range(7, 14)
}

PICTURE_FRAMES = [
    RedSitsAlone(1),
    RedSewsBat(2),
    RedFinishesBat(3),
    RedHugsBat(4),
    RedPlaysWithBat(5),
    RedHangsBat(6),
    BatFliesAway(10),
    BatTakesOff(9),
    BatEatsStars(8),
    BatTripsBalls(7),
    RedIsSad(11),
    PlanetTapsShoulder(12),
    PlanetHangout(13)
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
