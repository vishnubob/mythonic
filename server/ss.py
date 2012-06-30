#!/usr/bin/env python

import math
import random
import serial
import signal
import sys
import time

import yaml

import midi.sequencer
import midi

from mythonic.manager import Coordinator
from mythonic.manager import EffectsManager
from mythonic.pictureframe import PictureFrame
from mythonic.music import make_looper
from biscuit import HardwareChain

import pprint
pp = pprint.PrettyPrinter(indent=4, depth=5)

PRINT_STATUS = False

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

    manager.run()

def make_music_box(client, port, path):
    pattern = midi.read_midifile(path)
    seq = midi.sequencer.SequencerWrite(sequencer_resolution=pattern.resolution)
    seq.subscribe_port(client, port)
    seq.start_sequencer()
    return MusicBox(pattern, seq)

def load_manager(tty_dev, config, midi_client, midi_port):
    tty = serial.Serial(tty_dev, baudrate=1000000, parity=serial.PARITY_EVEN)
    music_box = make_music_box(midi_client, midi_port, config["midi"]["path"])

    picture_frames = []
    addresses = []
    for pf_config in config["frames"]:
        main_tracks = []
        if "main_tracks" in  pf_config:
            main_tracks = [music_box.tracks[i] for i in pf_config["main_tracks"]]
        bonus_tracks = []
        if "bonus_tracks" in  pf_config:
            bonus_tracks = [music_box.tracks[i] for i in pf_config["bonus_tracks"]]
        picture_frames.append(SSPictureFrame(main_tracks, bonus_tracks))
        addresses.append(int(pf_config["address"]))

    hc = HardwareChain(tty, len(addresses), .001, addresses)
    # Patterns of picture frames.
    patterns = [[picture_frames[i] for i in p] for p in config["patterns"]]

    return Coordinator(hc, SSManager(picture_frames, patterns, music_box))

class SSPictureFrame(PictureFrame):

    # TODO: Move all Track handling to SSManager

    def __init__(self, main_tracks=[], bonus_tracks=[]):
        self.main_tracks = main_tracks
        self.bonus_tracks = bonus_tracks
        super(self.__class__, self).__init__()

    def mute(self):
        self.mute_main()
        self.mute_bonus()

    def mute_main(self):
        for track in self.main_tracks:
            track.mute()

    def unmute_main(self):
        for track in self.main_tracks:
           track.unmute()

    def mute_bonus(self):
        for track in self.bonus_tracks:
            track.mute()

    def unmute_bonus(self):
        for track in self.bonus_tracks:
            track.unmute()

    def step_screensaver(self, offset):
        """
        Called when screen saver is active
        """
        if PRINT_STATUS: print "screenserver: ", offset
        t = time.time() + offset
        self.blackout()
        self.uv = int(abs((math.sin(t) * self.MAX_UV) / 10))

    def step_inactive(self, offset):
        """
        Effects for when this frame is not active and not screensavering

        Shine only white light at 1/3rd intensity.
        """
        if PRINT_STATUS: print "inactive: ", offset
        self.mute()
        self.blackout()
        self.white = self.MAX_WHITE / 3

    def step_active(self, offset):
        """
        Effects for after a picture frame has been activated.

        Minimize white and do a steady overlaping fade of RGB and UV.
        """
        if PRINT_STATUS: print "active: ", offset
        t = time.time() + offset
        self.unmute_main()
        self.white = self.MIN_WHITE
        self.hsv = (abs(math.sin(t * 0.5)), 1, 0.5)
        self.uv = int(abs(math.sin(t * 0.25) * self.MAX_UV))

    def step_active_hint(self, offset):
        """
        Hint that this selectd picture frame is part of a pattern.

        Slowly flash UV.
        """
        if PRINT_STATUS: print "active_hint: ", offset
        t = time.time() + offset
        self.uv = self.MAX_UV if math.sin(t * 2) >= 0 else self.MIN_UV

    def step_bonus(self, offset):
        """
        Effects for when this frame is part of a completed pattern

        Play bonus tracks and shine red and only red
        """
        if PRINT_STATUS: print "bonus: ", offset
        t = time.time() + offset
        self.unmute_bonus()
        self.hsv = (random.random(), random.random(), random.random())
        self.uv = abs(int(random.random() * self.MAX_UV))
        self.white = abs(int(math.sin(t) * self.MAX_WHITE / 10))

class SSManager(EffectsManager):
    """
    Runner for Sonic Storyboard.
    """

    def __init__(self, picture_frames, patterns, music_box=None):
        self.music_box = music_box
        # TODO: Get rid of this screensaver crap and implement it properly
        self.screensaver = Screensaver(picture_frames, patterns)
        #self.screensaver_timeout = 60 * 3
        self.screensaver_timeout = 60 * 3
        super(self.__class__, self).__init__(picture_frames, patterns)

    def update(self):
        """
        Manage effects
        """
        if self.untouched_for >= self.screensaver_timeout:
            if not self.screensaver.active:
                self.screensaver.activate()
                for pf in self.active_frames:
                    pf.deactivate()
                    pf.blackout()
                    pf.mute()
            self.screensaver.step()
        else:
            self.screensaver.deactivate()
            for idx, pf in enumerate(self.picture_frames):
                if pf.active:
                    pf.step_active(idx)
                    if self.in_target_pattern(pf):
                        if self.pattern_complete:
                            pf.step_bonus(idx)
                        else:
                            pf.step_active_hint(idx)
                else:
                    pf.step_inactive(idx)
        if self.music_box is not None:
            self.music_box.step()

# XXX: This is an abomination. Kill on sight. Meld into SSManager
class Screensaver(object):

    def __init__(self, picture_frames, patterns):
        self.picture_frames = picture_frames
        self.patterns = list(patterns)
        self._active = False
        self.period_length = 5

    @property
    def current_pattern(self):
        if len(self.patterns) <= 0:
            return None

        idx = int(math.fmod((time.time() / self.period_length), len(self.patterns)))
        return self.patterns[idx]

    def activate(self):
        self._active = True

    def deactivate(self):
        self._active = False

    active = property(lambda self: self._active)

    def step(self):
        if not self.active or self.current_pattern is None:
            return
        for idx, pf in enumerate(self.current_pattern):
            pf.step_screensaver(idx)

if __name__ == '__main__':
    main()
