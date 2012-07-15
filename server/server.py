#!/usr/bin/env python

import math
import random
import serial

import midi.sequencer
import midi

import biscuit
from music import make_looper
import pictureframe

import ss
from ss.pictureframes import *

MIDI_CLIENT = 128
MIDI_PORT = 0

MIDI_TRACKS = [
    "../music_raw/ssb/drum_37.mid",
    "../music_raw/ssb/drum_38.mid",
    "../music_raw/ssb/drum_41.mid",
    "../music_raw/ssb/drum_42.mid",
    "../music_raw/ssb/drum_43.mid",
    # range(5,)
    "../music_raw/ssb/lead_66.mid",
    "../music_raw/ssb/lead_68.mid",
    "../music_raw/ssb/lead_71.mid",
    "../music_raw/ssb/lead_73.mid",
    "../music_raw/ssb/lead_76.mid",
    "../music_raw/ssb/lead_77.mid",
    "../music_raw/ssb/lead_78.mid",
    "../music_raw/ssb/lead_80.mid",
    "../music_raw/ssb/lead_81.mid",
    "../music_raw/ssb/lead_83.mid",
    "../music_raw/ssb/lead_84.mid",
    "../music_raw/ssb/lead_85.mid",
    "../music_raw/ssb/lead_88.mid",
    "../music_raw/ssb/lead_89.mid",
    "../music_raw/ssb/lead_90.mid",
    "../music_raw/ssb/lead_92.mid",
    "../music_raw/ssb/lead_93.mid",
    "../music_raw/ssb/lead_95.mid",
]

ROUTING = {
    "/dev/ttyUSB0": [1, 2, 3, 4, 5, 6],
    "/dev/ttyUSB0": [1, 2],
#    "/dev/ttyUSB1": []
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
    load_tracks(picture_frames)
    hc = biscuit.HardwareChain(serial_ports, addresses)
    manager = ss.SSManager(hc, pictureframe.Storyboard(picture_frames), looper)
    manager.run()

# XXX: has hard-coded knowlege of MIDI_TRACKS (i.e. lead vs drum indexes)
def load_tracks(picture_frames):
    for idx, pf in enumerate(picture_frames):
        # XXX: HACK ATTACK! Shouldn't be hard coded
        pf.lead_tracks.append(idx % (len(MIDI_TRACKS) - 5) + 5)
        pf.drum_tracks.append(idx % 5)

if __name__ == '__main__':
    main()
