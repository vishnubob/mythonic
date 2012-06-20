#!/usr/bin/env python

import serial
import signal
import sys
import time

import midi.sequencer
import midi

from mythonic import MythonicManager
from mythonic import MythonicPictureFrame
from mythonic import MusicBox
from biscuit import HardwareChain

PFRAME_COUNT = 3

def make_music_box(client, port, path):
    pattern = midi.read_midifile(path)
    seq = midi.sequencer.SequencerWrite(sequencer_resolution=pattern.resolution)
    seq.subscribe_port(client, port)
    seq.start_sequencer()
    return MusicBox(pattern, seq)

def main():
    if len(sys.argv) != 4:
        script_name = sys.argv[0]
        print "Usage:   {0} <midi client> <midi port> <tty>".format(sys.argv[0])
        print "Example: {0} 128 0 /dev/ttyUSB0".format(sys.argv[0])
        exit(2)

    client = sys.argv[1]
    port = sys.argv[2]
    tty = sys.argv[3]

    tty = serial.Serial(tty, baudrate=1000000, parity=serial.PARITY_EVEN)
    hc = HardwareChain(tty, PFRAME_COUNT, .001)
    music_box = make_music_box(client, port, "/home/chao/projects/python-midi/sample.mid")

    manager = SSManager(hc, music_box)

    def signal_handler(signal, frame):
        manager.blackout()
        for i in range(PFRAME_COUNT * 2):
            man.cycle()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    manager.run()

class SSPictureFrame(MythonicPictureFrame):

    def step_inactive(self):
        """
        Effects for when this frame has either not been activated yet
        or has been deactivated.

        Shine only white light at 1/3rd intensity.
        """
        self.mute()
        self.blackout()
        self.white = self.MAX_WHITE / 3

    def step_active(self):
        """
        Effects for after a picture frame has been activated.

        Minimize white and do a steady overlaping fade of RGB and UV.
        """
        self.unmute_main()
        offset = self.address * 10
        self.white = self.MIN_WHITE
        self.red = self.calc_sin(self.MAX_RED,  0 + offset)
        self.green = self.calc_sin(self.MAX_GREEN, 85 + offset)
        self.blue = self.calc_sin(self.MAX_BLUE, 170 + offset)
        self.uv = self.calc_sin(self.MAX_UV, 0 + offset, 0.5)

    def step_active_hint(self):
        """
        Hint that this selectd picture frame is part of a pattern.

        Slowly flash UV.
        """
        self.uv = self.calc_square(self.MIN_UV, self.MAX_UV)

    def step_bonus(self):
        """
        Effects for when this frame is part of a completed pattern

        Play bonus tracks and shine red and only red
        """
        self.unmute_bonus()
        self.blackout()
        self.red = self.MAX_RED

class SSManager(MythonicManager):
    """
    Runner for Sonic Storyboard.
    """

    def __init__(self, hc, music_box):
        picture_frames = []
        for idx in range(hc.length):
            print "MAKING!"
            pf = SSPictureFrame(idx, hc, [music_box.tracks[idx + 1]])
            picture_frames.append(pf)
        patterns = [[picture_frames[i] for i in [0, 1]]]
        super(SSManager, self).__init__(hc, picture_frames, patterns, music_box)

if __name__ == '__main__':
    main()
