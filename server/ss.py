#!/usr/bin/env python

import math
import random
import serial
import sys

import yaml

import midi.sequencer
import midi

import biscuit
from music import make_looper
import manager
import mmath
import pictureframe

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

    midi_paths = config["midi"]["tracks"]
    looper = None
    if midi_paths is not None and len(midi_paths) > 0:
        looper = make_looper(midi_paths, midi_client, midi_port)

    picture_frames = []
    addresses = []
    for pf_config in config["frames"]:
        picture_frames.append(SSPictureFrame())
        addresses.append(int(pf_config["address"]) - 1)

    hc = HardwareChain(tty, len(addresses), .001, addresses)

    # Patterns of picture frames.
    if "patterns" not in config or config["patterns"] is None:
        patterns = []
    else:
        patterns = [[picture_frames[i] for i in p] for p in config["patterns"]]

    return SSManager(hc, Storyboard(picture_frames, patterns), looper)

class SSPictureFrame(pictureframe.PictureFrame):

    def pattern_hint(self, t):
        """
        Hint that this selectd picture frame is part of a pattern.
        """
        if int(t % 2) == 1:
            self.uv = self.MAX_UV
        else:
            self.uv = self.MIN_UV

    def step_bonus(self, offset):
        """
        Effects for when this frame is part of a completed pattern
        """
        if PRINT_STATUS: print "bonus: ", offset
        self.step_chaos()
        sys.exit()

    def step_chaos(self):
        self.hsv = (random.random(), random.random(), random.random())
        self.uv = abs(int(random.random() * self.MAX_UV))
        #self.white = abs(int(math.sin(t) * self.MAX_WHITE / 10))

class SSManager(manager.StoryManager):
    """
    Manages which stories get activated next
    """
    SCREENSAVER_TIMEOUT = 60 * 3
    #SCREENSAVER_TIMEOUT = 5#0 * 3

    def __init__(self, hc, storyboard, looper=None):
        self.screensaver = Screensaver(storyboard, 5)
        self.instrument = Instrument(storyboard, looper)
        super(SSManager, self).__init__(hc, storyboard, looper)

    def select_story(self):
        # Start off with instrument mode
        if self.current_story is None:
            return self.instrument
        #if self.storyboard.pattern_complete:
        if self.storyboard.untouched_for >= self.SCREENSAVER_TIMEOUT:
            return self.screensaver
        # Come out of screensaver mode into instrument mode
        elif isinstance(self.current_story, Screensaver):
            return self.instrument
        if not self.current_story.finished:
            return self.current_story

class Bonus(manager.Story):

    def transition(self, t):
        for pf in self.storyboard:
            pf.blackout()

class Instrument(manager.Story):

    def __init__(self, storyboard, looper):
        self.looper = looper
        super(Instrument, self).__init__(storyboard)

    def transition(self, t):
        for pf in self.storyboard:
            pf.deactivate()

    def plot(self, since_start):
        """
        Manage effects
        """
        for idx, pf in enumerate(self.storyboard):
            t = since_start + idx
            if pf.active:
                self.looper.ensure_playing(idx)
                pf.white = pf.MIN_WHITE
                pf.cycle_hue(t, 20, 1, 0.5)
                pf.uv = int(mmath.sin_abs(t / 3, True) * pf.MAX_UV)
                if self.storyboard.in_target_pattern(pf):
                    pf.pattern_hint(t)
            else:
                self.looper.ensure_stopped(idx)
                pf.blackout()
                pf.white = pf.MAX_WHITE / 3
        return True

class Screensaver(manager.Story):

    def __init__(self, storyboard, period_length):
        self.period_length = 6
        self.pattern_idx = 0
        super(Screensaver, self).__init__(storyboard)

    def hinted_pattern(self, t):
        patterns = self.storyboard.patterns
        if len(patterns) <= 0:
            return None
        idx = int(t / self.period_length) % len(patterns)
        if self.pattern_idx != idx:
            for pf in patterns[self.pattern_idx]:
                pf.blackout()
            self.pattern_idx = idx
        return patterns[self.pattern_idx]

    def transition(self, t):
        work_left = [pf.fadeout() for pf in self.storyboard]
        return reduce(lambda a, b: a or b, work_left)

    def plot(self, t):
        pattern = self.hinted_pattern(t)
        if pattern is None:
            pattern = []
        for offset, pf in enumerate(pattern):
            pf.pattern_hint(t + offset)
        return True

if __name__ == '__main__':
    main()
