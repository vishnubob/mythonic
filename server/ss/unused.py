import manager
import mmath
import random
import time

from ss.pictureframes import *

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

class Chaos(manager.Story):
    def plot(self, t):
        for pf in self.storyboard:
            pf.hsv = tuple(random.random() for i in range(3))
            pf.rgb = tuple(random.random() * 255 for i in range(3))
            pf.white = random.random() * pf.MAX_WHITE
            pf.uv = random.random() * pf.MAX_UV
        return True

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

class MuffinTest(manager.Story):

    def plot(self, t):
        color = int(mmath.travel(t, 20, 0, 5))
        for pf in self.storyboard:
            if pf.touched:
                print "[TOUCH] Human address %d" % (pf.human_address)
            pf.blackout()
            if color == 0:
               pf.red = pf.MAX_RED
            elif color == 1:
               pf.green = pf.MAX_GREEN
            elif color == 2:
               pf.blue= pf.MAX_BLUE
            elif color == 3:
               pf.white = pf.MAX_WHITE
            elif color >= 4:
               pf.uv = pf.MAX_UV
        return color < 5

class StartupTest(manager.Story):

    def plot(self, t):
        for idx, pf in enumerate(self.storyboard):
            pf.blackout()
            if pf.real_address < t:
                pf.blue = pf.MAX_BLUE
            else:
                pf.red = pf.MAX_RED
        return t < max(pf.real_address for pf in self.storyboard) + 1
