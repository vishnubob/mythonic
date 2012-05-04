from schedule import Schedule
import itertools

class Story(object):
    "An experience we want to communicate to participants through picture frames and sound"

    def __init__(self, picture_frames):
        self.picture_frames = picture_frames
        self.last_started = None
        self.is_running = False

    def start(self, time_code):
        self.reset()
        self.is_running = True
        self.last_started = time_code
        self.restart_schedule()

    def stop(self, time_code):
        self.reset()
        self.running = False

    def restart_schedule(self, time_offset=0):
        self._schedule = self._make_schedule(time_offset)

    def reset(self):
        "Reset state"

    def advance_plot(self, time_code):
        "Advance this story if needed. Time code can (and sometimes should) be fractional"
        if not self.is_running:
            if self._should_start(time_code):
                self.start(time_code)
            else:
                return False

        if self._should_stop(time_code):
            return self.stop(time_code)

        offset = time_code - self.last_started
        for f in self._schedule.pop_due(1, offset):
            f()

    def _make_schedule(self, time_offset):
        "create a schedule based off of offset"
        return Schedule(time_offset)

    def _should_start(self, time_code):
        "Returns whether interaction should lead to start"
        return False

    def _should_stop(self, time_code):
        "Returns whether interaction should terminate and reset"
        return False

class InteractiveStory(Story):
    "A story the audiance can interact with"

    def __init__(self, picture_frames):
        super(InteractiveStory, self).__init__(picture_frames)

        self.interactions = []

    def reset(self):
        self.interactions = []

    def interact(self, interaction):
        "Receive the participant's interaction. Return list of Spectacle"
        self.interactions.append(interaction)
        self._handle_interaction(interaction)

    def _handle_interaction(self, interaction):
        "Respond to interaction"

class TriggeredStory(InteractiveStory):
    "A story tarts once it has been triggered by certain interaction"

class Storyboard(list):
    "A series of stories told through picture frames, sound, and emergent spectacle"

    def __init__(self, stories):
        super(Storyboard, self).__init__(stories)

    def get_picture_frames(self):
        lists_of_frames = [s.picture_frames for s in self]
        return set(itertools.chain.from_iterable(lists_of_frames))
    picture_frames = property(get_picture_frames)
