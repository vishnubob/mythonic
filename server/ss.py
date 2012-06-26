#!/usr/bin/env python

import colorsys
import math
import random
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
        pf = SSPictureFrame(address, hc, tracks)
        picture_frames.append(pf)

    # Patterns of picture frames.
    patterns = [[picture_frames[i] for i in p] for p in config["patterns"]]

    # Hardware/file components
    return SSManager(hc, picture_frames, patterns, music_box)

class SSPictureFrame(MythonicPictureFrame):

    def __init__(self, address, hc, main_tracks=[], bonus_tracks=[]):
        self.main_tracks = main_tracks
        self.bonus_tracks = bonus_tracks
        super(MythonicPictureFrame, self).__init__(address, hc)

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

    def step_screensaver(self):
        """
        Called when screen saver is active
        """
        print "screenserver: ", self.address
        t = time.time() + self.address
        self.mute()
        self.blackout()
        self.uv = int(abs((math.sin(t) * self.MAX_UV) / 10))

    def step_inactive(self):
        """
        Effects for when this frame is not active and not screensavering

        Shine only white light at 1/3rd intensity.
        """
        print "inactive: ", self.address
        self.mute()
        self.blackout()
        self.white = self.MAX_WHITE / 3

    def step_active(self):
        """
        Effects for after a picture frame has been activated.

        Minimize white and do a steady overlaping fade of RGB and UV.
        """
        print "active: ", self.address
        t = time.time() + self.address
        self.unmute_main()
        self.white = self.MIN_WHITE
        self.hsv = (abs(math.sin(t * 0.5)), 1, 0.5)
        self.uv = int(abs(math.sin(t * 0.25) * self.MAX_UV))

    def step_active_hint(self):
        """
        Hint that this selectd picture frame is part of a pattern.

        Slowly flash UV.
        """
        print "active_hint: ", self.address
        t = time.time() + self.address
        self.uv = self.MAX_UV if math.sin(t * 2) >= 0 else self.MIN_UV

    def step_bonus(self):
        """
        Effects for when this frame is part of a completed pattern

        Play bonus tracks and shine red and only red
        """
        print "bonus: ", self.address
        t = time.time() + self.address
        self.unmute_bonus()
        self.hsv = (random.random(), random.random(), random.random())
        self.uv = abs(int(random.random() * self.MAX_UV))
        self.white = abs(int(math.sin(t) * self.MAX_WHITE / 10))

class SSManager(MythonicManager):
    """
    Runner for Sonic Storyboard.
    """

    def __init__(self, hc, picture_frames, patterns, music_box):
        self.music_box = music_box
        self.screensaver = Screensaver(patterns)
        self.screensaver_timeout = 60 * 3
        super(SSManager, self).__init__(hc, picture_frames, patterns)

    def think(self):
        """
        Entertain the burners and burn-heads
        """
        now = time.time()
        # Collect touch data
        touched = self.clear_touched() # Update picture frames for pf in self.picture_frames:

        # Touch activates or deactivates frames
        for pf in touched:
            if self.is_active(pf):
                self.deactivate(pf)
            else:
                self.activate(pf)
        # Either we handle the screen saver or handle our lovely frames
        if len(touched) <= 0 and self.untouched_for >= self.screensaver_timeout:
            if not self.screensaver.active:
                self.screensaver.activate()
                for pf in self.active_frames:
                    self.deactivate(pf)
            self.screensaver.step()
        else:
            self.screensaver.deactivate()
            # Handle effects for active frames
            for pf in self.active_frames:
                pf.step_active()
                if self.in_target_pattern(pf):
                    if self.pattern_complete:
                        # Frame is part of exclusive and complete pattern
                        pf.step_bonus()
                    else:
                        # Frame is in pattern, but pattern is incomplete
                        pf.step_active_hint()
            # Handle effects for innactive frames
            for pf in set(self.picture_frames) - set(self.active_frames):
                pf.step_inactive()

        if self.music_box is not None:
            self.music_box.step()

class Screensaver(object):

    def __init__(self, patterns):
        self.patterns = list(patterns)
        self._active = False
        self.last_change = None
        self.period_length = 5
        self.possition = 0

    @property
    def current_pattern(self):
        if self.last_change is None:
            self.last_change = time.time()
        elif (time.time() - self.last_change) >= self.period_length:
            for pf in self.patterns[self.possition]:
                pf.blackout()
            self.possition += 1
            if self.possition >= len(self.patterns):
                random.shuffle(self.patterns)
                self.possition = 0
            self.last_change = time.time()
        return self.patterns[self.possition]

    def activate(self):
        if not self._active:
            # TODO: BUG SHOULD BLACKOUT ALL NOT JUST CURRENT
            for pf in self.current_pattern:
                pf.blackout()
        self._active = True

    def deactivate(self):
        self._active = False

    active = property(lambda self: self._active)

    def step(self):
        if not self.active:
            return
        for pf in self.current_pattern:
            pf.step_screensaver()

if __name__ == '__main__':
    main()
