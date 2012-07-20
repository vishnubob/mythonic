import manager
import mmath

from ss.pictureframes import *

class StartupTest(manager.Story):
    def plot(self, t):
        for idx, pf in enumerate(self.storyboard):
            pf.blackout()
            if pf.address < t:
                pf.blue = pf.MAX_BLUE
            else:
                pf.red = pf.MAX_RED
        return t < max([pf.address * 2 for pf in self.storyboard])

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
                if idx < len(self.looper.tracks):
                    self.play(idx)
                pf.cycle_hue(t, 20, 1, 0.5)
                pf.uv = int(mmath.sin_abs(t / 3, True) * pf.MAX_UV)
                if self.storyboard.in_target_pattern(pf):
                    pf.pattern_hint(t)
            else:
                if idx < len(self.looper.tracks):
                    self.stop(idx)
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
        super(TreeArt, self).__init__(storyboard, looper, foci, time_per_frame)

class FriendshipPlanet(Narative):

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
        super(FriendshipPlanet, self).__init__(storyboard, looper, foci, time_per_frame)

class BatAdventure(Narative):

    def __init__(self, storyboard, looper, time_per_frame=10):
        foci_classes = [
            RedSitsAlone,
            RedSewsBat,
            RedFinishesBat,
            BatFliesAway,
            BatTakesOff,
            BatEatsStars,
            BatTripsBalls
        ]
        foci = [pf for pf in storyboard if pf.__class__ in foci_classes]
        super(BatAdventure, self).__init__(storyboard, looper, foci, time_per_frame)


class Screensaver(manager.Story):

    def __init__(self, storyboard, span):
        self.span = span
        self.pattern_idx = 0
        super(Screensaver, self).__init__(storyboard)

    @property
    def pattern_span(self):
        return float(self.span) / len(self.storyboard.patterns)

    def hinted_pattern(self, t):
        """
        Returns the next pattern to hint at.
        When finished, returns None
        """
        patterns = self.storyboard.patterns
        if len(patterns) == 0:
            return None
        idx = int(t / self.pattern_span)
        if idx >= len(patterns):
            return None
        if self.pattern_idx != idx:
            for pf in patterns[self.pattern_idx]:
                pf.blackout()
            self.pattern_idx = idx
        return patterns[self.pattern_idx]

    def plot(self, t):
        pattern = self.hinted_pattern(t)
        if pattern is None:
            return False
        for pf in self.storyboard:
            pf.blackout()
        hinted_frame_idx = int(t/(self.pattern_span/float(len(pattern))))
        if hinted_frame_idx < len(pattern):
            hinted_frame = pattern[hinted_frame_idx]
            hinted_frame.uv = hinted_frame.MAX_UV
        return True
