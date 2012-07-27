import manager
import mmath
import random
import time
import ss
from ss.pictureframes import *

SCREENSAVER_TIMEOUT = 1 * 60
SCREENSAVER_SPAN = 30
SCREENSAVER_LOOPS = int((1 * 60) / SCREENSAVER_SPAN)
NARATIVE_SPAN = 60

class SSManager(manager.StoryManager):
    """
    Manages which stories get activated next
    """

    def __init__(self, hc, storyboard, looper=None):
        self.screensaver = Screensaver(storyboard, span=SCREENSAVER_SPAN)
        self.instrument = Instrument(storyboard, looper)
        self.startup_test = ss.unused.MuffinTest(storyboard)
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
        #return self.startup_test
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
        self.trippy = False
        self.friendly = False
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
                pf.uv = int(mmath.sin_abs(t / 2, True) * pf.MAX_UV)
                if self.storyboard.in_target_pattern(pf):
                    pf.pattern_hint(t)
            elif not self.storyboard.active_frames:
                pf.white = pf.MAX_WHITE / 3
            else:
                if self.trippy:
                    pf.uv = pf.MAX_UV
                if self.friendly:
                    pf.red = int(mmath.sin_abs(t / 2, True) * pf.MAX_RED/2.0)
        return True

    def lookup_tracks(self, pf):
        tracks_per_class = {
            RedSitsAlone: [["drums_3_36"]],
            RedSewsBat: [["lead_1"]],
            RedFinishesBat: [["drums_3_37"]],
            RedHugsBat: [["drums_3_38"]],
            RedPlaysWithBat: [["pad"]],
            RedHangsBat: [["drums_3_39"]],
            BatFliesAway: [["bass"]],
            BatTakesOff: [["lead_2"]],
            BatEatsStars: [["drums_3_40"]],
            BatTripsBalls: [[]],
            RedIsSad: [["lead_3"]],
            PlanetTapsShoulder: [["drums_3_41"]],
            PlanetHangout: [[]]
        }
        song_idx = 0
        tracks = []
        for c in tracks_per_class:
            if isinstance(pf, c):
                tracks += tracks_per_class[c][song_idx]
        return tracks

    def handle_touch(self, pf):
        if pf.active:
            tracks = self.lookup_tracks(pf)
            self.now_playing += tracks
            for track in tracks:
                self.play(track)
            if isinstance(pf, BatTripsBalls):
                self.trippy = True
            if isinstance(pf, PlanetHangout):
                self.friendly = True
        else:
            for track in self.lookup_tracks(pf):
                if track in self.now_playing:
                    self.now_playing.remove(track)
                if track not in self.now_playing:
                    self.stop(track)
            if isinstance(pf, BatTripsBalls):
                self.trippy = False
            if isinstance(pf, PlanetHangout):
                self.friendly = False 

class Narative(manager.MusicalStory):

    def __init__(self, storyboard, looper, foci, span):
        self.foci = foci
        self.span = span
        super(Narative, self).__init__(storyboard, looper)

    def setup(self, t):
        self.last_focus = None
        self.last_change = None
        for pf in self.storyboard:
            pf.uv = pf.MIN_UV
        for track in self.soundtrack:
            self.play(track)

    @property
    def soundtrack(self):
        """
        The names of the tracks to play during the narative
        """

    @property
    def time_per_frame(self):
        return int(self.span/float(len(self.foci)))

    def plot(self, t):
        if self.last_change is None:
            self.last_change = t
        if len(self.foci) == 0:
            return False
        focus_idx = int(mmath.travel(t, self.span, 0, len(self.foci)))
        if focus_idx >= len(self.foci):
            return False
        focus = self.foci[focus_idx]
        if self.last_focus is not focus and self.last_focus is not None:
            # Change last focuses RGB so it transitions in unform with others
            for pf in self.storyboard:
                if pf is not self.last_focus:
                    self.last_focus.rgb = pf.rgb
            self.last_change = t
        self.last_focus = focus
        focus.blackout()
        focus.white = focus.MAX_WHITE / 3
        for pf in self.storyboard:
            if pf is focus:
                continue
            pf.white = pf.MIN_WHITE
            focus.mood(pf, t - self.last_change, self.time_per_frame)
        return not self.storyboard.touched

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

    @property
    def soundtrack(self):
       drums = ["drums_3_36", "drums_3_37", "drums_3_38", "drums_3_39", "drums_3_40", "drums_3_41", "drums_3_42", "drums_3_46", "drums_3_49"]
       lead = ["lead_3"]
       return drums + lead

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

    @property
    def soundtrack(self):
       drums = ["drums_1_37", "drums_1_38", "drums_1_41", "drums_1_42", "drums_1_43"]
       lead = ["lead_1"]
       return drums + lead

class BatAdventure(Narative):

    def __init__(self, storyboard, looper, span):
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

    @property
    def soundtrack(self):
       drums = ["drums_2_36", "drums_2_38", "drums_2_40", "drums_2_41", "drums_2_42", "drums_2_46", "drums_2_48"]
       lead = ["lead_2"]
       return drums + lead

class Screensaver(manager.Story):

    def __init__(self, storyboard, span):
        self.span = span
        super(Screensaver, self).__init__(storyboard)

    def setup(self, t):
        self.hinted_pattern = random.choice(self.storyboard.patterns)
        self.focus = random.choice(self.storyboard)

    def plot(self, t):
        self.focus.blackout()
        self.focus.white = self.focus.MAX_WHITE / 3
        for pf in self.storyboard:
            if pf is self.focus:
                continue
            pf.uv = pf.MIN_UV
            pf.white = pf.MIN_WHITE
            self.focus.mood(pf, t, self.span)
        pattern = self.hinted_pattern
        hinted_frame_idx = int(t/(self.span/float(len(pattern)))) % len(pattern)
        if hinted_frame_idx < len(pattern):
            hinted_frame = pattern[hinted_frame_idx]
            hinted_frame.uv = hinted_frame.MAX_UV
        return t <= self.span
