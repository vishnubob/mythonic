"""
The business logic for Sonic Storyboard
"""

import math
import time

from biscuit import Manager
from pictureframe import PictureFrame

class SSManager(Manager):
    """
    Runner for Sonic Storyboard.
    """

    def __init__(self, hc, number_of_boxes):
        super(SSManager, self).__init__(hc)
        self.picture_frames = []
        for idx in range(number_of_boxes):
            self.picture_frames.append(PictureFrame(idx, hc))
        self.active_frames = []
        self.patterns = [[self.picture_frames[i] for i in [0]]]
        self.target_pattern = None

    def calc_flashing(self, mini, maxi, offset=0, rate=1):
        seed = time.time() * rate + offset
        return mini if math.sin(seed) <= 0 else maxi

    def calc_intensity(self, ceiling, offset=0, rate=1):
        """
        Return an intensity staggered by "offset", changing at "rate"
        """
        seed = time.time() * rate + offset
        intensity = int(math.sin(seed) * ceiling)
        return max(intensity, 0)

    def blackout(self):
        for pf in self.picture_frames:
            pf.blackout()

    def deactivate(self, pf):
        self.active_frames.remove(pf)

    # In order to select a pattern, pf has to be the start of a new pattern or within the old
    def next_target_pattern(self, pf):
        # Is new frame consistent with old pattern?
        if pf <= self.target_pattern:
            return self.target_pattern
        # Is there a pattern that starts with our frame?
        for pattern in self.patterns:
            if pf == pattern[0]:
                return pattern
        return None

    def get_target_pattern(self):
        for pattern in self.patterns:
            # All active frames must be within a pattern
            # and start of pattern must be an active frame
            if self.active_frames <= pattern and pattern[0] <= self.active_frames:
                return pattern
        return None
    target_pattern = property(get_target_pattern)

    def activate(self, activated_pf):
        next_target_pattern = self.next_target_pattern(activated_pf)
        # Old pattern canceled
        if self.target_pattern is not None and next_target_pattern is None:
            print "Canceled old pattern"
            pass
        # New pattern selected
        elif self.target_pattern is None and next_target_pattern is not None:
            print "New pattern"
            for pf in active_frames:
                if pf not in next_target_pattern:
                    self.deactivate(pf)
        elif self.target_pattern != next_target_pattern:
            print "Pattern changed"

        self.active_frames.append(activated_pf)
        assert(self.target_pattern == next_target_pattern)

    def think(self):
        """
        Entertain the burners and burn-heads
        """
        touched = []
        triggers = self.hc.get_touch_triggers()
        for idx, directions in enumerate(triggers):
            if reduce(lambda a, b: a or b, directions):
                touched.append(self.picture_frames[idx])
        for pf in self.picture_frames:
            if pf in touched:
                # Handle (de)activation by touch
                if pf in self.active_frames:
                    self.deactivate(pf)
                else:
                    self.activate(pf)
            if pf in self.active_frames:
                # Activated frames look cool
                offset = pf.address * 10
                pf.white = pf.MIN_WHITE
                pf.red = self.calc_intensity(pf.MAX_RED,  0 + offset)
                pf.green = self.calc_intensity(pf.MAX_GREEN, 85 + offset)
                pf.blue = self.calc_intensity(pf.MAX_BLUE, 170 + offset)
                pf.uv = self.calc_intensity(pf.MAX_UV, 0 + offset, 0.5)
                if self.target_pattern is not None and pf in self.target_pattern:
                    # Flashing UV when in pattern
                    pf.uv = self.calc_flashing(pf.MIN_UV, pf.MAX_UV, 0, 10)
            else:
                # Deactivated frames look borring
                pf.blackout()
                pf.white = pf.MAX_WHITE/3
