#!/usr/bin/env python

import serial
import signal
import sys
import time

import yaml

import midi.sequencer
import midi

from mythonic import MythonicManager
from mythonic import MythonicPictureFrame
from mythonic import MusicBox
from biscuit import HardwareChain

def make_music_box(client, port, path):
    pattern = midi.read_midifile(path)
    seq = midi.sequencer.SequencerWrite(sequencer_resolution=pattern.resolution)
    seq.subscribe_port(client, port)
    seq.start_sequencer()
    return MusicBox(pattern, seq)

def load_manager(tty_dev, config, midi_client, midi_port):
    tty = serial.Serial(tty_dev, baudrate=1000000, parity=serial.PARITY_EVEN)
    hc = HardwareChain(tty, len(config["frames"]), .001)
    music_box = make_music_box(midi_client, midi_port, config["midi"]["path"])

    picture_frames = []
    for pf_config in config["frames"]:
        tracks = [music_box.tracks[i] for i in pf_config["main_tracks"]]
        address = int(pf_config["address"])
        picture_frames.append(SSPictureFrame(address, hc, tracks))

    # Patterns of picture frames.
    patterns = [[picture_frames[i] for i in p] for p in config["patterns"]]

    # Hardware/file components
    return SSManager(hc, picture_frames, patterns, music_box)

def main():
    if len(sys.argv) not in [3, 5]:
        script_name = sys.argv[0]
        print "Usage:   {0} <config> <tty> [<midi client> <midi port>]".format(sys.argv[0])
        print "Example: {0} ss.yaml /dev/ttyUSB0 128 0".format(sys.argv[0])
        exit(2)

    config_file = sys.argv[1]
    tty_dev = sys.argv[2]
    client = 128 if len(sys.argv) < 4 else int(sys.argv[3])
    port = 0 if len(sys.argv) < 5 else int(sys.argv[4])

    config_stream = open(config_file)
    manager = load_manager(tty_dev, yaml.load(config_stream), client, port)
    config_stream.close()

    def signal_handler(signal, frame):
        manager.blackout()
        for i in range(len(manager.picture_frames) * 2):
            manager.cycle()
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

    def __init__(self, hc, picture_frames, patterns, music_box):
        super(SSManager, self).__init__(hc, picture_frames, patterns, music_box)

if __name__ == '__main__':
    main()
