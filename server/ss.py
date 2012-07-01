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

from manager import Coordinator
from manager import EffectsManager
from pictureframe import MusicalPictureFrame
from music import make_looper
import mmath
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

def load_manager(tty_dev, config, midi_client, midi_port):
    tty = serial.Serial(tty_dev, baudrate=1000000, parity=serial.PARITY_EVEN)

    looper = make_looper(config["midi"]["tracks"], midi_client, midi_port) 

    picture_frames = []
    addresses = []
    for pf_config in config["frames"]:
        main_tracks = []
        if "main_tracks" in  pf_config:
            main_tracks = map(int, pf_config["main_tracks"])

        bonus_tracks = []
        if "bonus_tracks" in  pf_config:
            bonus_tracks = map(int, pf_config["bonus_tracks"])

        picture_frames.append(SSPictureFrame(looper, main_tracks, bonus_tracks))
        addresses.append(int(pf_config["address"]) - 1)

    hc = HardwareChain(tty, len(addresses), .001, addresses)

    # Patterns of picture frames.
    if "patterns" not in config or config["patterns"] is None:
        patterns = []
    else:
        patterns = [[picture_frames[i] for i in p] for p in config["patterns"]]


    return Coordinator(hc, SSManager(picture_frames, patterns, looper))

class SSPictureFrame(MusicalPictureFrame):

    def __init__(self, looper, main_tracks=[], bonus_tracks=[]):
        self.looper = looper
        self.main_tracks = main_tracks
        self.bonus_tracks = bonus_tracks
        super(SSPictureFrame, self).__init__(looper, main_tracks + bonus_tracks)

    def stop_main_tracks(self):
        self.stop_tracks(self.main_tracks)

    def play_main_tracks(self):
        self.play_tracks(self.main_tracks)

    def stop_bonus_tracks(self):
        self.stop_tracks(self.bonus_tracks)

    def play_bonus_tracks(self):
        self.play_tracks(self.bonus_tracks)

    def step_inactive(self, offset):
        """
        Effects for when this frame is not active and not screensavering
        """
        if PRINT_STATUS: print "inactive: ", offset
        self.white = self.MAX_WHITE / 3

    def step_active(self, offset):
        """
        Effects for after a picture frame has been activated.
        """
        if PRINT_STATUS: print "active: ", offset
        t = time.time() + offset
        self.play_main_tracks()
        self.white = self.MIN_WHITE
        # Slowly cycle through hue
        hue = mmath.sawtooth(t / 10.0, 1)
        self.hsv = (hue, 1, 0.5)
        self.uv = int(abs((math.sin(t) * self.MAX_UV) / 10))

    def step_pattern_hint(self, offset):
        """
        Hint that this selectd picture frame is part of a pattern.
        """
        if PRINT_STATUS: print "active_hint: ", offset
        t = time.time() + offset
        if int(t % 3) == 2:
            print "UV ON!"
            self.uv = self.MAX_UV
        elif int(t % 3) == 0:
            print "UV OFF!"
            self.uv = self.MIN_UV


    def step_bonus(self, offset):
        """
        Effects for when this frame is part of a completed pattern
        """
        if PRINT_STATUS: print "bonus: ", offset
        self.step_chaos(offset)

    def step_chaos(self):
        self.play_tracks()
        self.hsv = (random.random(), random.random(), random.random())
        self.uv = abs(int(random.random() * self.MAX_UV))
        self.white = abs(int(math.sin(t) * self.MAX_WHITE / 10))

class SSManager(EffectsManager):
    """
    Runner for Sonic Storyboard.
    """

    def __init__(self, picture_frames, patterns, looper=None):
        self.looper = looper
        # TODO: Get rid of this screensaver crap and implement it properly
        self.screensaver = Screensaver(picture_frames, patterns, 5)
        #self.screensaver_timeout = 60 * 3
        self.screensaver_timeout = 10
        super(self.__class__, self).__init__(picture_frames, patterns)

    def update(self):
        """
        Manage effects
        """
        if self.untouched_for >= self.screensaver_timeout:
            if not self.screensaver.active:
                self.screensaver.activate()
        else:
            #print self.screensaver_timeout - self.untouched_for
            if self.screensaver.active:
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
        if self.looper is not None:
            self.looper.think()

# XXX: This is an abomination. Kill on sight. Meld into SSManager
class Screensaver(EffectsManager):

    def __init__(self, picture_frames, patterns, period_length):
        self._active = False
        self.period_length = 5
        super(Screensaver, self).__init__(picture_frames[:], patterns[:])

    def activate(self):
        if self._active:
            raise "Screensaver is already activate"
        self._active = True
        for pf in self.active_frames:
            pf.deactivate()

    def deactivate(self):
        if not self._active:
            raise "Screensaver was already deactivated"
        self._active = False
        for pf in self.active_frames:
            pf.deactivate()

    @property
    def current_pattern(self):
        if len(self.patterns) <= 0:
            return None
        idx = int(math.fmod((time.time() / self.period_length), len(self.patterns)))
        return self.patterns[idx]

    active = property(lambda self: self._active)

    def think(self):
        if not self.active or self.current_pattern is None:
            return
        print "SCREENSAVER!"
        pattern = self.current_pattern
        if pattern is None:
            pattern = []
        for idx, pf in enumerate(self.current_pattern):
            pf.step_pattern_hint(idx)

if __name__ == '__main__':
    main()
