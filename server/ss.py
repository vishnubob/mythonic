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

    return SSManager(hc, SonicStoryboard(picture_frames, patterns), looper)

class SSManager(manager.StoryManager):
    """
    Manages which stories get activated next
    """
    #SCREENSAVER_TIMEOUT = 60 * 3
    SCREENSAVER_TIMEOUT = 5#0 * 3

    def __init__(self, hc, storyboard, looper=None):
        self.screensaver = Screensaver(storyboard, period_length=5)
        self.instrument = Instrument(storyboard, looper)
        self.bonus = PoC(storyboard, looper)
        super(SSManager, self).__init__(hc, storyboard, looper)

    def select_story(self):
        if self.current_story is None:
            return self.instrument
        if isinstance(self.current_story, Instrument):
             if self.storyboard.untouched_for >= self.SCREENSAVER_TIMEOUT:
                return self.screensaver
             elif self.storyboard.pattern_complete:
                return self.bonus
        # Come out of screensaver mode into instrument mode if touched
        if isinstance(self.current_story, Screensaver) and self.storyboard.touched:
            return self.instrument
        # Patiently wait for whatever is running to finish
        if not self.current_story.finished:
            return self.current_story
        # Default to Instrument
        return self.instrument

class Instrument(manager.MusicalStory):

    def transition(self, t):
        for pf in self.storyboard:
            pf.blackout()
            pf.deactivate()

    def plot(self, since_start):
        """
        Manage effects
        """
        for idx, pf in enumerate(self.storyboard):
            t = since_start + idx
            pf.blackout()
            if pf.active:
                self.play(idx)
                pf.cycle_hue(t, 20, 1, 0.5)
                pf.uv = int(mmath.sin_abs(t / 3, True) * pf.MAX_UV)
                if self.storyboard.in_target_pattern(pf):
                    pf.pattern_hint(t)
            else:
                self.play(idx)
                pf.white = pf.MAX_WHITE / 3
        return True

class PoC(manager.MusicalStory):
    STORY_LENGTH = 10

    def plot(self, t):
        focus_idx = int(mmath.segment(t, self.STORY_LENGTH, 0, len(self.storyboard)))
        focus = self.storyboard[focus_idx]
        for pf in self.storyboard:
            if pf == focus:
                continue
            pf.blackout()
            focus.mood(pf, t)
        focus.blackout()
        focus.white = focus.MAX_WHITE
        return t < self.STORY_LENGTH

class SonicStoryboard(pictureframe.Storyboard):
    pass
    # Turn this into a field of
#    moods = [
#        lambda pf, t: pf.boredom(t),
#        lambda pf, t: pf.craftsmanship(t),
#        lambda pf, t: pf.accomplishment(t),
#        lambda pf, t: pf.love(t),
#        lambda pf, t: pf.fun(t),
#        lambda pf, t: pf.contentment(t),
#    ]

class Screensaver(manager.Story):

    def __init__(self, storyboard, period_length):
        self.period_length = period_length
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

    def plot(self, t):
        pattern = self.hinted_pattern(t)
        if pattern is None:
            pattern = []
        for offset, pf in enumerate(pattern):
            pf.pattern_hint(t + offset)
        return True

class SSPictureFrame(pictureframe.PictureFrame):

    def pattern_hint(self, t):
        """
        Hint that this selectd picture frame is part of a pattern.
        """
        if int(t % 2) == 1:
            self.uv = self.MAX_UV
        else:
            self.uv = self.MIN_UV

class RedSitsAlone(SSPictureFrame):
    """
    Red sitting alone bored
    """
    @staticmethod
    def mood(pf, t):
        pf.blue = pf.MAX_BLUE

class RedSewsBat(SSPictureFrame):
    """
    Red sewing, making the bat
    """
    @staticmethod
    def mood(pf, t):
        pf.red = 255
        pf.green = 255
        pf.blue = 0

class RedFinishesBat(SSPictureFrame):
    """
    Red finishes creation, sense of accomplishment
    """
    @staticmethod
    def mood(pf, t):
        pf.green = pf.MAX_GREEN

class RedHugsBat(SSPictureFrame):
    """
    Love, hugging creation
    """
    @staticmethod
    def mood(pf, t):
        pf.red = pf.MAX_RED
 
class RedPlaysWithBat(SSPictureFrame):
    pass

class RedHangsBat(SSPictureFrame):
    pass

class BatFliesAway(SSPictureFrame):
    pass

class BatTakesOff(SSPictureFrame):
    pass

class BatEatsStars(SSPictureFrame):
    pass

class BatTripsBalls(SSPictureFrame):
    pass

class RedSittingAlone(SSPictureFrame):
    pass

class RedIsSad(SSPictureFrame):
    pass

class PlanetTapsShoulder(SSPictureFrame):
    pass

class PlanetFriendship(SSPictureFrame):
    pass

if __name__ == '__main__':
    main()
