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

class Pattern(list):

    def __init__(self, picture_frames, triggered_story):
        self.triggered_story = triggered_story
        super(Pattern, self).__init__(picture_frames)
        
class SSManager(manager.StoryManager):
    """
    Manages which stories get activated next
    """
    #SCREENSAVER_TIMEOUT = 60 * 3
    SCREENSAVER_TIMEOUT = 5#0 * 3

    # TODO storyboard -> picture_frames
    def __init__(self, hc, storyboard, looper=None):
        self.screensaver = Screensaver(storyboard, period_length=5)
        self.instrument = Instrument(storyboard, looper)
        self.bat_adventure = BatAdventure(storyboard, looper, 1)
        patterns = []
        for narative in [self.bat_adventure]:
            activators = [pf for idx, pf in enumerate(narative.foci) if idx % 2 != 0]
            patterns.append(Pattern(activators, narative))
            print activators
        # TODO: create a new storyboard instead
        storyboard.patterns = patterns

        super(SSManager, self).__init__(hc, storyboard, looper)

    def select_story(self):
        if self.current_story is None:
            return self.instrument
        if isinstance(self.current_story, Instrument):
             if self.storyboard.untouched_for >= self.SCREENSAVER_TIMEOUT:
                return self.screensaver
             elif self.storyboard.pattern_complete:
                return self.storyboard.target_pattern.triggered_story
        # Come out of screensaver mode into instrument mode if touched
        if isinstance(self.current_story, Screensaver) and self.storyboard.touched:
            return self.instrument
        # XXX: TODO: Make screensaver "finish", keep track of loops here
        #            And after so many, restart
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

class Narative(manager.MusicalStory):

    def __init__(self, storyboard, looper, foci, time_per_frame=10):
        self.foci = foci
        self.time_per_frame = time_per_frame
        super(Narative, self).__init__(storyboard, looper)

    def plot(self, t):
        story_length = len(self.foci) * self.time_per_frame
        focus_idx = int(mmath.segment(t, story_length, 0, len(self.foci)))
        focus = self.storyboard[focus_idx]
        for pf in self.storyboard:
            if pf == focus:
                continue
            pf.blackout()
            focus.mood(pf, t, self.time_per_frame)
        focus.blackout()
        focus.white = focus.MAX_WHITE
        return t < story_length

class TreeArt(Narative):

    def __init__(self, storyboard, looper, time_per_frame=10):
        foci_classes = [
            RedSitsAlone,
            RedSewsBat,
            RedFinishesBat,
            RedHugsBat,
            RedPlaysWithBat,
            RedHangsBat
        ]
        foci = [pf for pf in storyboard if pf.__class__ in foci_classes]
        super(BatAdventure, self).__init__(storyboard, looper, foci, time_per_frame)

class BatAdventure(Narative):

    def __init__(self, storyboard, looper, time_per_frame=10):
        foci_classes = [
            RedSitsAlone,
            RedSewsBat,
            RedFinishesBat,
            BatFliesAway,
            BatIsSad,
            PlanetTapsShoulder,
            PlanetHangout
        ]
        foci = [pf for pf in storyboard if pf.__class__ in foci_classes]
        super(BatAdventure, self).__init__(storyboard, looper, foci, time_per_frame)

class BatAdventure(Narative):

    def __init__(self, storyboard, looper, time_per_frame=10):
        foci_classes = [
            RedSitsAlone,
            RedSewsBat,
            RedFinishesBat,
            BatFliesAway,
            RedIsSad,
            PlanetTapsShoulder,
            PlanetHangout
        ]
        foci = [pf for pf in storyboard if pf.__class__ in foci_classes]
        super(BatAdventure, self).__init__(storyboard, looper, foci, time_per_frame)

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
    def mood(pf, t, span):
        pf.blue = pf.MAX_BLUE #mmath.triangle(t, span, pf.MIN_BLUE, pf.MAX_BLUE)

class RedSewsBat(SSPictureFrame):
    """
    Red sewing, making the bat
    """
    @staticmethod
    def mood(pf, t, span):
        # yellow
        pf.hsv = (1, 1, 0)

class RedFinishesBat(SSPictureFrame):
    """
    Red finishes creation, sense of accomplishment
    """
    @staticmethod
    def mood(pf, t, span):
        pf.green = pf.MAX_GREEN

class RedHugsBat(SSPictureFrame):
    """
    Love, hugging creation
    """
    @staticmethod
    def mood(pf, t, span):
        pf.red = pf.MAX_RED

class RedPlaysWithBat(SSPictureFrame):
    """
    Playing with bat toy, having fun
    """
    @staticmethod
    def mood(pf, t, span):
        # magenta
        pf.red = 255
        pf.green = 0
        pf.blue = 255

class RedHangsBat(SSPictureFrame):
    """
    Hangs bat in the tree
    """
    @staticmethod
    def mood(pf, t, span):
        pf.red = 160
        pf.green = 32
        pf.blue = 240

class BatFliesAway(SSPictureFrame):
    """
    Bat flies away
    """
    @staticmethod
    def mood(pf, t, span):
        pf.blue = pf.MAX_BLUE

class BatTakesOff(SSPictureFrame):
    """
    Bat takes off, sense of adventure
    """
    @staticmethod
    def mood(pf, t, span):
        pf.red = 255
        pf.green = 165
        pf.blue = 0

class BatEatsStars(SSPictureFrame):
    """
    Bat eating stars adventure
    """
    @staticmethod
    def mood(pf, t, span):
        """
        Yellow to purple
        """
        #TODO
        pass
        

class BatTripsBalls(SSPictureFrame):
    """
    Bat glowing sparkly showoff
    """
    @staticmethod
    def mood(pf, t, span):
        """
        Really fucking trippy
        """
        pass

class RedIsSad(SSPictureFrame):
    """
    Red is sad
    """
    @staticmethod
    def mood(pf, t, span):
        pf.blue = pf.MAX_BLUE / 2.0

class PlanetTapsShoulder(SSPictureFrame):
    """
    Planet taps on shoulder to console
    """
    @staticmethod
    def mood(pf, t, span):
        """
        TODO: teal
        """
        pf.red = 0
        pf.green = 193
        pf.blue = 255

class PlanetHangout(SSPictureFrame):
    """
    Red and Planet friendship, hanging out
    """
    @staticmethod
    def mood(pf, t, span):
        """
        TODO: fuschia
        """
        pf.red = 255
        pf.green = 192
        pf.blue = 203

if __name__ == '__main__':
    main()
