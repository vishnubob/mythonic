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
        touch_triggers = self.hc.get_touch_triggers()
        for pf in self.storyboard:
            idx = self.hc.addresses.index(pf.real_address)
            if touch_triggers[idx]:
                pf.touch()
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
        for pf in self.storyboard:
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
        self.new_stage = True

    def think(self):
        """
        Manage effects/stage
        """
        self.finished = False
        stage = self.stages[self.stage_idx]
        if self.new_stage:
            self.stage_started_at = time.time()
            self.new_stage = False
        if not stage(time.time() - self.stage_started_at):
            print "stage change"
            old_idx = self.stage_idx
            self.stage_idx = (self.stage_idx + 1) % len(self.stages)
            if old_idx > self.stage_idx:
                self.looped_count += 1
                self.finished = True
            self.new_stage = True

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

    def teardown(self, t):
        for idx, track in enumerate(self.looper.tracks):
            self.looper.ensure_stopped(idx)

    def play(self, track_name):
        """
        Ensure the track corresponding to the given track name
        (as according to self.storyboard.track_listing) is playing
        """
        self.looper.ensure_playing(self.storyboard.track_listing[track_name])

    def stop(self, track_name):
        """
        Ensure the track corresponding to the given track name
        (as according to self.storyboard.track_listing) is stopped
        """
        self.looper.ensure_stopped(self.storyboard.track_listing[track_name])
