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
        self.active_frames = set()

    def calc_intensity(self, ceiling, offset=0, rate=1):
        """
        Return an intensity staggered by "offset", changing at "rate"
        """
        seed = time.time() * rate + offset
        unbound = int(math.sin(seed) * ceiling)
        if unbound < 0:
            return 0

        return unbound

    def blackout(self):
        for pf in self.picture_frames:
            pf.blackout()

    def think(self):
        """
        Entertain the burners and burn-heads
        """
        touched = set()
        triggers = self.hc.get_touch_triggers()
        for idx, directions in enumerate(triggers):
            if reduce(lambda a, b: a or b, directions):
                touched.add(self.picture_frames[idx])
        for pf in self.picture_frames:
            if pf in touched:
                if pf in self.active_frames:
                    self.active_frames.remove(pf)
                    pf.set_white(pf.MIN_WHITE)
                else:
                    self.active_frames.add(pf)
                    pf.set_white(pf.MAX_WHITE / 2)
            offset = pf.address * 10
            pf.set_red(self.calc_intensity(pf.MAX_RED,  0 + offset))
            pf.set_green(self.calc_intensity(pf.MAX_GREEN, 85 + offset))
            pf.set_blue(self.calc_intensity(pf.MAX_BLUE, 170 + offset))
            pf.set_uv(self.calc_intensity(pf.MAX_UV, 0 + offset, 0.5))
