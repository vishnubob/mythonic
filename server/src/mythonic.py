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
            self.picture_frames.append(PictureFrame(idx, hc.light_frames[idx]))

    def calc_intensity(self, ceiling, offset=0, rate=1):
        """
        Return an intensity staggered by "offset", changing at "rate"
        """
        seed = time.time() * rate + offset
        unbound = int(math.sin(seed) * ceiling)
        if unbound < 0:
            return 0

        return unbound % ceiling

    def blackout(self):
        for pf in self.picture_frames:
            pf.blackout()

    def think(self):
        """
        Cycle through various combinations of colors
        """

        for idx, pf in enumerate(self.picture_frames):
            offset = idx * 10
            pf.set_red(self.calc_intensity(pf.MAX_RED,  0 + offset))
            pf.set_green(self.calc_intensity(pf.MAX_GREEN, 85 + offset))
            pf.set_blue(self.calc_intensity(pf.MAX_BLUE, 170 + offset))
            pf.set_uv(self.calc_intensity(pf.MAX_UV, 0 + offset, 0.5))
            print pf
        
