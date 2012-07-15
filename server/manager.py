import time

import biscuit

class StoryManager(biscuit.Manager):
    """
    Reads state of hardware, updates storyboard, and
    then delegates to a story.

    After delegation to said story, reads state of
    storyboard and sends the appropriate updates to the hardware.
    """

    RED_IDX = 0
    GREEN_IDX = 2
    BLUE_IDX = 3
    WHITE_IDX = 4
    UV_IDX = 5

    def __init__(self, hc, storyboard):
        self.hc = hc
        self.storyboard = storyboard
        self.current_story = None

    def select_story(self):
        """
        The story to delegate to
        """

    def pf_to_addr(self, pf):
        idx = self.storyboard.index(pf)
        return self.hc.addresses[idx]

    def think(self):
        next_story = self.select_story()
        if next_story != self.current_story:
            if self.current_story is not None:
                self.current_story.deactivate()
            next_story.activate()
            self.current_story = next_story
            print "Story changed to", str(next_story.__class__)
        for addr, directions in enumerate(self.hc.get_touch_triggers()):
            if reduce(lambda a, b: a or b, directions):
                position = self.hc.addresses.index(addr)
                self.storyboard[position].touch()
        self.current_story.think()
        for pf in self.current_story.storyboard:
            pf.untouch()
            addr = self.pf_to_addr(pf)
            self.hc.set_light(addr, self.RED_IDX, pf.red)
            self.hc.set_light(addr, self.GREEN_IDX, pf.green)
            self.hc.set_light(addr, self.BLUE_IDX, pf.blue)
            self.hc.set_light(addr, self.WHITE_IDX, pf.white)
            self.hc.set_light(addr, self.UV_IDX, pf.uv)

class Story(object):
    """
    Manages effects by modifying PictureFrame instances.
    """

    def __init__(self, storyboard):
        self.storyboard = storyboard
        self.transitioned = False
        self.finished = False

    def think(self):
        """
        Manage effects
        """
        if not self.transitioned:
            self.transitioned = not self.transition()
        else:
            if self.plot():
                self.finished = False
            else:
                self.finished = True
                self.transitioned = True

    def transition(self):
        """
        Transition into this story

        Return True if the transition is still in progress
        """
        return False

    def plot(self):
        """
        Modify storyboard

        Return True if plot is ongoing
        """
        return False

    def deactivate(self):
        self._active = False
        self.finished = False
        self.transitioned = False

    def activate(self):
        self._active = True

    active = property(lambda self: self._active)
