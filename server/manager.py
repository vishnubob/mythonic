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

    def __init__(self, hc, storyboard, looper=None):
        self.hc = hc
        self.storyboard = storyboard
        self.looper = looper
        self.current_story = None

    def select_story(self):
        """
        The story to delegate to
        """

    def pf_to_addr(self, pf):
        idx = self.storyboard.index(pf)
        return self.hc.addresses[idx]

    def think(self):
        # Handle touch
        for addr, directions in enumerate(self.hc.get_touch_triggers()):
            if reduce(lambda a, b: a or b, directions):
                position = self.hc.addresses.index(addr)
                self.storyboard[position].touch()
        # Handle story selection/deselection
        next_story = self.select_story()
        if next_story != self.current_story:
            if self.current_story is not None:
                self.current_story.deactivate()
            next_story.activate()
            self.current_story = next_story
            print "Story changed to", str(next_story.__class__)
        # Advance the story
        self.current_story.think()
        # Advance the looper
        if self.looper is not None:
            self.looper.think()
        # Push changes and reset touch
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
        self.transition_started_at = None
        self.plot_started_at = None

    def think(self):
        """
        Manage effects
        """
        if not self.transitioned:
            if self.transition_started_at is None:
                self.transition_started_at = time.time()
            t = time.time() - self.transition_started_at
            self.transitioned = not self.transition(t)
        else:
            if self.plot_started_at is None:
                self.plot_started_at = time.time()
            t = time.time() - self.plot_started_at
            if self.plot(t):
                self.finished = False
            else:
                self.finished = True
                self.transitioned = False
                self.transition_started_at = None

    def transition(self, t):
        """
        Transition into this story

        Return True if the transition is still in progress.

        Default is to fade out by an increment of 1 each call
        """
        work_left = [pf.fadeout() for pf in self.storyboard]
        return reduce(lambda a, b: a or b, work_left)

    def plot(self, t):
        """
        Modify storyboard

        Return True if plot is ongoing
        """
        return False

    def deactivate(self):
        self._active = False
        self.finished = False
        self.transitioned = False
        self.transition_started_at = None
        self.plot_started_at = None

    def activate(self):
        self._active = True

    active = property(lambda self: self._active)

class MusicalStory(Story):

    def __init__(self, storyboard, looper=None):
        self.looper = looper
        super(MusicalStory, self).__init__(storyboard)

    def play(self, track_idx):
        if self.looper is not None:
            self.looper.ensure_playing(track_idx)

    def stop(self, track_idx):
        if self.looper is not None:
            self.looper.ensure_stopped(track_idx)
