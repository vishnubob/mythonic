import manager
import mmath
import random
import time

from ss.pictureframes import *

SCREENSAVER_TIMEOUT = 60 * 3
SCREENSAVER_SPAN = 5
SCREENSAVER_LOOPS = 2
NARATIVE_SPAN = 10

class SSManager(manager.StoryManager):
    """
    Manages which stories get activated next
    """

    def __init__(self, hc, storyboard, looper=None):
        self.screensaver = Screensaver(storyboard, span=SCREENSAVER_SPAN)
        self.instrument = Instrument(storyboard, looper)
        self.naratives = [
            BatAdventure(storyboard, looper, NARATIVE_SPAN),
            TreeArt(storyboard, looper, NARATIVE_SPAN),
            FriendshipPlanet(storyboard, looper, NARATIVE_SPAN)
        ]
        for narative in self.naratives:
            activators = [pf for idx, pf in enumerate(narative.foci) if idx % 2 != 0]
            storyboard.patterns.append(pictureframe.Pattern(activators, narative))
        super(SSManager, self).__init__(hc, storyboard, looper)

    def select_story(self):
        current = self.current_story
        if current is None:
            return self.instrument
        if isinstance(current, Instrument):
            untouched_since = max(current.stage_started_at, self.storyboard.untouched_since)
            if time.time() - untouched_since >= SCREENSAVER_TIMEOUT:
               return self.screensaver
            if self.storyboard.pattern_complete:
               return self.storyboard.target_pattern.triggered_story
            return self.instrument
        if isinstance(current, Screensaver):
            if self.storyboard.touched:
                return self.instrument
            if current.finished and current.looped_count >= SCREENSAVER_LOOPS:
                return self.naratives[int(random.random() * len(self.naratives))]
            return self.screensaver
        if not current.finished:
            return current
        # Default to Instrument
        return self.instrument

class Instrument(manager.MusicalStory):

    def setup(self, t):
        # list of track names, duplicates
        self.now_playing = []
        for pf in self.storyboard:
            pf.blackout()
            pf.deactivate()

    def plot(self, since_start):
        """
        Manage effects
        """
        for idx, pf in enumerate(self.storyboard):
            t = since_start + idx * 1.3
            pf.blackout()
            if pf.touched:
                self.handle_touch(pf)
            if pf.active:
                pf.cycle_hue(t, 20, 1, 0.5)
                pf.uv = int(mmath.sin_abs(t / 3, True) * pf.MAX_UV)
                if self.storyboard.in_target_pattern(pf):
                    pf.pattern_hint(t)
            elif not self.storyboard.active_frames:
                pf.white = pf.MAX_WHITE / 3
        return True

    def handle_touch(self, pf):
        if pf.active:
            self.now_playing += pf.tracks
            for track in pf.tracks:
                self.play(track)
            print "Now playing:", self.now_playing
        else:
            for track in pf.tracks:
                self.now_playing.remove(track)
                if track not in self.now_playing:
                    self.stop(track)
            print "Now playing:", self.now_playing

    def teardown(self):
        for idx, track in enumerate(self.looper.tracks):
            self.stop(idx)
        return super(Instrument, self).teardown()

class Narative(manager.MusicalStory):

    def __init__(self, storyboard, looper, foci, span):
        self.foci = foci
        self.span = span
        self.last_focus = None
        super(Narative, self).__init__(storyboard, looper)

    @property
    def time_per_frame(self):
        return int(self.span/float(len(self.foci)))

    def plot(self, t):
        if len(self.foci) == 0:
            return False
        focus_idx = int(mmath.travel(t, self.span, 0, len(self.foci)))
        if focus_idx >= len(self.foci):
            return False
        focus = self.foci[focus_idx]
        if self.last_focus != focus:
            self.last_focus = focus
        for pf in self.storyboard:
            if pf == focus:
                continue
            pf.blackout()
            focus.mood(pf, t, self.time_per_frame)
        focus.blackout()
        focus.white = focus.MAX_WHITE / 3
        return True

class TreeArt(Narative):

    def __init__(self, storyboard, looper, span):
        foci_classes = [
            RedSitsAlone,
            RedSewsBat,
            RedFinishesBat,
            RedHugsBat,
            RedPlaysWithBat,
            RedHangsBat
        ]
        foci = []
        for fc in foci_classes:
            foci += [pf for pf in storyboard if isinstance(pf, fc)]
        super(TreeArt, self).__init__(storyboard, looper, foci, span)

class FriendshipPlanet(Narative):

    def __init__(self, storyboard, looper, span):
        foci_classes = [
            RedSitsAlone,
            RedSewsBat,
            RedFinishesBat,
            BatFliesAway,
            RedIsSad,
            PlanetTapsShoulder,
            PlanetHangout
        ]
        foci = []
        for fc in foci_classes:
            foci += [pf for pf in storyboard if isinstance(pf, fc)]
        super(FriendshipPlanet, self).__init__(storyboard, looper, foci, span)

    def setup(self, t):
        drums = ["drums_1_37", "drums_1_38", "drums_1_41", "drums_1_42", "drums_1_43"]
        lead = ["lead_1"]
        for track in drums + lead:
            self.play(track)

class BatAdventure(Narative):

    def __init__(self, storyboard, looper, span=10):
        foci_classes = [
            RedSitsAlone,
            RedSewsBat,
            RedFinishesBat,
            BatFliesAway,
            BatTakesOff,
            BatEatsStars,
            BatTripsBalls
        ]
        foci = []
        for fc in foci_classes:
            foci += [pf for pf in storyboard if isinstance(pf, fc)]
        super(BatAdventure, self).__init__(storyboard, looper, foci, span)


class Screensaver(manager.Story):

    def __init__(self, storyboard, span):
        self.span = span
        super(Screensaver, self).__init__(storyboard)

    def setup(self, t):
        self.pattern_idx = 0
        self.foci = list(self.storyboard)
        random.shuffle(self.foci)

    @property
    def pattern_span(self):
        return float(self.span) / len(self.storyboard.patterns)

    @property
    def focus_span(self):
        return self.pattern_span

    def current_focus(self, t):
        return self.foci[int(t/self.focus_span)]

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
        focus = self.current_focus(t)
        for pf in self.storyboard:
            if pf is focus:
                focus.blackout()
                focus.white = focus.MAX_WHITE / 3
            else:
                pf.uv = pf.MIN_UV
                pf.white = pf.MIN_WHITE
                focus.mood(pf, t, self.focus_span)
        hinted_frame_idx = int(t/(self.pattern_span/float(len(pattern)))) % len(pattern)
        if hinted_frame_idx < len(pattern):
            hinted_frame = pattern[hinted_frame_idx]
            hinted_frame.uv = hinted_frame.MAX_UV
        return True
