import manager

from ss.stories import *

class SSManager(manager.StoryManager):
    """
    Manages which stories get activated next
    """
    SCREENSAVER_TIMEOUT = 0#60 * 3

    def __init__(self, hc, storyboard, looper=None):
        self.screensaver = Screensaver(storyboard, span=10)
        self.instrument = Instrument(storyboard, looper)
        self.startup_test = StartupTest(storyboard)
        time_per_frame = 1
        self.naratives = [
            BatAdventure(storyboard, looper, time_per_frame),
            TreeArt(storyboard, looper, time_per_frame),
            FriendshipPlanet(storyboard, looper, time_per_frame)
        ]
        for narative in self.naratives:
            activators = [pf for idx, pf in enumerate(narative.foci) if idx % 2 != 0]
            storyboard.patterns.append(pictureframe.Pattern(activators, narative))
        super(SSManager, self).__init__(hc, storyboard, looper)

    def select_story(self):
        current = self.current_story
        if current is None:
            #return self.startup_test
            return self.instrument
        if isinstance(current, Instrument):
             if self.storyboard.untouched_for >= self.SCREENSAVER_TIMEOUT:
                return self.screensaver
             if self.storyboard.pattern_complete:
                return self.storyboard.target_pattern.triggered_story
        if isinstance(current, Screensaver):
            if self.storyboard.touched:
                return self.instrument
            if current.finished and current.looped_count >= 2:
                return self.naratives[int(random.random() * len(self.naratives))]
            return self.screensaver
        if not current.finished:
            return current
        # Default to Instrument
        return self.instrument

