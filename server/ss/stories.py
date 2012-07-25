import manager
import mmath
import random
import time

from ss.pictureframes import *

class SSManager(manager.StoryManager):
    """
    Manages which stories get activated next
    """
    SCREENSAVER_TIMEOUT = 60 * 3

    def __init__(self, hc, storyboard, looper=None):
        self.screensaver = Screensaver(storyboard, span=10)
        self.instrument = Instrument(storyboard, looper)
        self.startup_test = StartupTest(storyboard)
        self.dice = Dice(storyboard)
        self.blackout_game = BlackoutGame(storyboard)
        time_per_frame = 5
        self.naratives = [
            BatAdventure(storyboard, looper, time_per_frame),
            TreeArt(storyboard, looper, time_per_frame),
            FriendshipPlanet(storyboard, looper, time_per_frame)
        ]
        for narative in self.naratives:
            activators = [pf for idx, pf in enumerate(narative.foci) if idx % 2 != 0]
            storyboard.patterns.append(pictureframe.Pattern(activators, narative))
        super(SSManager, self).__init__(hc, storyboard, looper)

    def select_story(self):
        current = self.current_story
        if current is None:
            return self.startup_test
            #return self.instrument
        if isinstance(current, Instrument):
            untouched_since = max(current.stage_started_at, self.storyboard.untouched_since)
            if time.time() - untouched_since >= self.SCREENSAVER_TIMEOUT:
               return self.screensaver
            if self.storyboard.pattern_complete:
               return self.storyboard.target_pattern.triggered_story
        if isinstance(current, Screensaver):
            if self.storyboard.touched:
                return self.instrument
            if current.finished and current.looped_count >= 2:
                return self.naratives[int(random.random() * len(self.naratives))]
            return self.screensaver
        if not current.finished:
            return current
        # Default to Instrument
        return self.instrument

class BlackoutGame(manager.Story):

    def __init__(self, storyboard):
        super(BlackoutGame, self).__init__(storyboard)
        self.blacked_out = [random.choice(self.storyboard)]

    @property
    def lighted(self):
        return [pf for pf in self.storyboard if pf not in self.blacked_out]

    def plot(self, t):
        for pf in self.storyboard:
            if pf.touched:
                if pf in self.blacked_out:
                    self.blacked_out.remove(pf)
                    if len(self.lighted) > 0:
                        candidates = self.lighted
                        candidates.remove(pf)
                    if len(self.lighted) > 0:
                        self.blacked_out.append(random.choice(candidates))
                else:
                    self.blacked_out.append(pf)
            if pf in self.blacked_out:
                pf.blackout()
            else:
                pf.white = pf.MAX_WHITE
        return len(self.lighted) > 0

class Dice(manager.Story):

    def randomize(self, pf, saturation=1):
        pf.hsv = (random.random(), saturation, 1)
        pf.uv = pf.MAX_UV if random.random() >= 0.5 else pf.MIN_UV

    def setup(self, t):
        for pf in self.storyboard:
            self.randomize(pf)

    def plot(self, t):
        for idx, pf in enumerate(self.storyboard):
            if idx > t:
                self.randomize(pf)
        return t < len(self.storyboard) + 10

class StartupTest(manager.Story):

    def plot(self, t):
        for idx, pf in enumerate(self.storyboard):
            pf.blackout()
            if pf.real_address < t:
                pf.blue = pf.MAX_BLUE
            else:
                pf.red = pf.MAX_RED
        return not self.storyboard.touched

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
                pf.cycle_hue(t, 5, 1, 0.5)
                pf.uv = int(mmath.sin_abs(t / 3, True) * pf.MAX_UV)
                if self.storyboard.in_target_pattern(pf):
                    pf.pattern_hint(t)
            else:
                pf.white = pf.MAX_WHITE / 3
        return True

    def handle_touch(self, pf):
        if pf.active:
            self.now_playing += pf.tracks
            for track in pf.tracks:
                self.play(track)
            print self.now_playing
        else:
            for track in pf.tracks:
                self.now_playing.remove(track)
                if track not in self.now_playing:
                    self.stop(track)
            print self.now_playing

    def teardown(self):
        for idx, track in enumerate(self.looper.tracks):
            self.stop(idx)
        return super(Instrument, self).teardown()

class Narative(manager.MusicalStory):

    def __init__(self, storyboard, looper, foci, time_per_frame=10):
        self.foci = foci
        self.time_per_frame = time_per_frame
        super(Narative, self).__init__(storyboard, looper)

    def plot(self, t):
        if len(self.foci) == 0:
            return False
        story_length = len(self.foci) * self.time_per_frame
        focus_idx = int(mmath.travel(t, story_length, 0, len(self.foci)))
        if focus_idx >= len(self.foci):
            return False
        focus = self.foci[focus_idx]
        for pf in self.storyboard:
            if pf == focus:
                continue
            pf.blackout()
            focus.mood(pf, t, self.time_per_frame)
        focus.blackout()
        focus.white = focus.MAX_WHITE
        return True

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
        hinted_frame_idx = int(t/(self.pattern_span/float(len(pattern)))) % len(pattern)
        if hinted_frame_idx < len(pattern):
            hinted_frame = pattern[hinted_frame_idx]
            hinted_frame.uv = hinted_frame.MAX_UV
        return True
