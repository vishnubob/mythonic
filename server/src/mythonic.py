"""Mythonic/installation-specific implementations of abstractions"""

import random
from storyboard   import InteractiveStory
from spectacle    import SpectacleSchedule
from pictureframe import FadeBlack, Touch
from wired        import WiredStoryboard, WiredPictureFrame

class MythonicStoryboard(WiredStoryboard):
    "Yay storyboard full of our mythonic stories!"

    def __init__(self, bus, picture_frames):
        super(MythonicStoryboard, self).__init__(bus, [])

        # Kick in screen saver after 3 time codes of silence
        self.screensaver    = Screensaver(picture_frames, 3)
        # Kick in tilt based on rolling average of 10 interactions
#        self.tilt_mode      = Tilt(picture_frames, 10, 10)
#        # Yay!
#        self.pictured_story = OctopusAndBuilder(picture_frames)
        # Instrument mode
        self.instrument     = Instrument(picture_frames)
#
        self.append(self.screensaver)
#        self.append(self.tilt_mode)
#        self.append(self.pictured_story)
        self.append(self.instrument)
#
    def update(self, time_code):
        "Update stories and board based on given time_code"
        interaction = self.read_interaction(time_code)

        stories_to_update = []
        # If either of these are active, we want only them to run
#        if self.tilt_mode.is_running or self.screensaver.is_running:
#           stories_to_update = [self.tilt_mode, self.screensaver]
        if self.screensaver.is_running:
            stories_to_update = [self.screensaver]
        else:
            stories_to_update = list(self)

        something_ran = False
        for story in stories_to_update:
            if interaction is not None:
                story.interact(interaction, time_code)
            something_ran = story.advance_plot(time_code) or something_ran

        # shitty way of deciding this
        if something_ran: 
            self.refresh()

class MythonicPictureFrame(WiredPictureFrame):
    "Mythonic picture frame"

class MythonicStory(InteractiveStory):
    "An exciting story from the good folks at Mythonic UnLtd."

#class OctopusAndBuilder(MythonicStory):
#    "Interactive story on our pictures"

class Instrument(MythonicStory):
    "Allows the user to define the stories themself"

    def _should_start(self, time_code):
        return len(self.interactions) > 0

    def _handle_interaction(self, interaction):
        "Adjusts lights based on Touch inputs"
        sched = self._schedule

        if not isinstance(interaction, Touch):
            return
        touch = interaction
        frame = touch.picture_frame
        
        # Schedule changes to happen immediately
        sched.schedule(lambda : frame.set_blue(touch.up), 0)
        sched.schedule(lambda : frame.set_green(touch.left), 0)
        sched.schedule(lambda : frame.set_red(touch.down), 0)
        sched.schedule(lambda : frame.set_uv(touch.right), 0)

#class Tilt(MythonicStory):
#    "Tilt mode. When input rate spikes, freak out and go silent."
#
#    def __init__(self, picture_frames, threshold, sample_size, timeout):
#        "Threshold is in interactions per whole time code."
#        super(Tilt, self).__init__(picture_frames)
#        self.threshold = threshold
#        self.sample_size = sample_size
#        self.timeout = timeout
#

class Screensaver(MythonicStory):
    "Free running animation to attract people. Interaction stops."

    def __init__(self, picture_frames, timeout):
        super(Screensaver, self).__init__(picture_frames)

        self.timeout = timeout

    def _should_start(self, time_code):
        if len(self.interactions) <= 0:
            return True

        return time_code - self.interactions[-1].time_code >= self.timeout

    def _should_stop(self, time_code):
        return len(self.interactions) > 0

    def _make_schedule(self, time_offset=0):
        "Screen saver schedule from offset. Restarts at end."
        sched = SpectacleSchedule(time_offset)
        frames = self.picture_frames

        # Black out the lights
        for p in frames:
            sched.append_spectacle(FadeBlack(p, 1))

        first_frame = frames[0]
        # Make the frame shine blue
        sched.append(lambda : first_frame.set_blue(p.MAX_BLUE))
        # Blackout first frame after 2 whole time codes 
        sched.append(first_frame.blackout, 2)

        # Random white flashes
        rand_frames = list(frames[1:])
        random.shuffle(rand_frames)
        for p in rand_frames:
            sched.append(lambda p=p: p.set_white(p.MAX_WHITE))
            # After one time code, black out
            sched.append(p.blackout, 1)

        # Restart the schedule
        sched.append(lambda : self.restart_schedule(sched.insertion_point))

        return sched

