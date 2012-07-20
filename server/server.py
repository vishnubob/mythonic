#!/usr/bin/env python

import math
import random
import serial

import midi.sequencer
import midi

import biscuit
from music import make_looper
import pictureframe

from ss.pictureframes import *

MIDI_CLIENT = 128
MIDI_PORT = 0

MIDI_TRACKS = [
    "../music_raw/drum_36.mid",
    "../music_raw/drum_37.mid",
    "../music_raw/drum_39.mid",
    "../music_raw/drum_42.mid",
    "../music_raw/drum_49.mid",
    "../music_raw/drum_51.mid",
    "../music_raw/drum_77.mid"
]

ROUTING = {
    "/dev/ttyUSB0": [0, 1, 2],
    "/dev/ttyUSB1": []
}

PICTURE_FRAMES = [
    RedSitsAlone(),
    RedSewsBat(),
    RedFinishesBat(),
    RedHugsBat(),
    RedPlaysWithBat(),
    RedHangsBat(),
    BatFliesAway(),
    BatTakesOff(),
    BatEatsStars(),
    BatTripsBalls(),
    RedIsSad(),
    PlanetTapsShoulder(),
    PlanetHangout()
]

def main():
    looper = make_looper(MIDI_TRACKS, MIDI_CLIENT, MIDI_PORT)
    addresses = []
    serial_ports = []
    picture_frames = []
    for tty_dev in ROUTING:
        tty = serial.Serial(tty_dev, baudrate=1000000)
        for address in ROUTING[tty_dev]:
            addresses.append(address)
            serial_ports.append(tty)
        picture_frame = [pf for pf in PICTURE_FRAMES if pf.address == address][0]
        picture_frames.append(picture_frame)
    hc = HardwareChain(serial_ports, addresses)
    manager = SSManager(hc, pictureframe.Storyboard(picture_frames), looper)
    manager.run()

if __name__ == '__main__':
    main()
