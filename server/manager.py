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

    def think(self):
        # Handle touch
        for position, touched in enumerate(self.hc.get_touch_triggers()):
            if touched:
                self.storyboard[position].touch()
        # Handle story selection/deselection
        next_story = self.select_story()
        if next_story != self.current_story:
            next_story.reset()
            self.current_story = next_story
            print "Story changed to", str(next_story.__class__.__name__)
        # Advance the story
        self.current_story.think()
        # Advance the looper
        if self.looper is not None:
            self.looper.think()
        # Push changes and reset touch
        for pf in self.current_story.storyboard:
            pf.untouch()
            idx = self.hc.addresses.index(pf.real_address)
            self.hc.set_light(idx, self.RED_IDX, pf.red)
            self.hc.set_light(idx, self.GREEN_IDX, pf.green)
            self.hc.set_light(idx, self.BLUE_IDX, pf.blue)
            self.hc.set_light(idx, self.WHITE_IDX, pf.white)
            self.hc.set_light(idx, self.UV_IDX, pf.uv)

class Story(object):
    """
    Manages effects by modifying PictureFrame instances.
    """

    def __init__(self, storyboard):
        self.storyboard = storyboard
        self.stages = [self.setup, self.plot, self.teardown]
        self.reset()

    def reset(self):
        self.stage_idx = 0
        self.stage_started_at = None
        self.looped_count = 0

    def think(self):
        """
        Manage effects/stage
        """
        self.finished = False
        stage = self.stages[self.stage_idx]
        if self.stage_started_at is None:
            self.stage_started_at = time.time()
        t = time.time() - self.stage_started_at
        if not stage(t):
            old_idx = self.stage_idx
            self.stage_idx = (self.stage_idx + 1) % len(self.stages)
            if old_idx > self.stage_idx:
                self.looped_count += 1
                self.finished = True
            self.stage_started_at = None

    def setup(self, t):
        """
        Transition into this story

        Return True if the transition is still in progress.

        Blackout all boxes
        """
        for pf in self.storyboard:
            pf.blackout()

    def plot(self, t):
        """
        Modify storyboard

        Return True if plot is ongoing
        """

    def teardown(self, t):
        """
        Just like setup and plot, but happens after
        """

class MusicalStory(Story):

    def __init__(self, storyboard, looper=None):
        self.looper = looper
        super(MusicalStory, self).__init__(storyboard)

    def play(self, track_idx):
        self.looper.ensure_playing(track_idx)

    def stop(self, track_idx):
        self.looper.ensure_stopped(track_idx)
