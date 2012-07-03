import time

import biscuit

class Coordinator(biscuit.Manager):
    """
    Reads state of hardware, updates picture frames, and
    then delegates to the effects manager.

    After delegation to the effects manager, reads state of
    picture frames and sends the appropriate updates to the hardware.
    """

    RED_IDX = 0
    GREEN_IDX = 2
    BLUE_IDX = 3
    WHITE_IDX = 4
    UV_IDX = 5

    def __init__(self, hc, effects_manager):
        self.hc = hc
        self.effects_manager = effects_manager

    def think(self):
        picture_frames = self.effects_manager.picture_frames
        for addr, directions in enumerate(self.hc.get_touch_triggers()):
            if reduce(lambda a, b: a or b, directions):
                picture_frames[addr].touch()
        self.effects_manager.update()
        for addr, pf in enumerate(picture_frames):
            pf.untouch()
            self.hc.set_light(addr, self.RED_IDX, pf.red)
            self.hc.set_light(addr, self.GREEN_IDX, pf.green)
            self.hc.set_light(addr, self.BLUE_IDX, pf.blue)
            self.hc.set_light(addr, self.WHITE_IDX, pf.white)
            self.hc.set_light(addr, self.UV_IDX, pf.uv)

class EffectsManager(object):
    """
    Manages effects by modifying PictureFrame instances.
    """

    def __init__(self, picture_frames, patterns=[]):
        self.picture_frames = picture_frames
        self.patterns = patterns
        self.initialized_at = time.time()

    def update(self):
        """
        Manage effects
        """

    @property
    def run_time(self):
        return time.time() - self.initialized_at

    @property
    def touched_frames(self):
        return filter(lambda pf: pf.touched, self.picture_frames)

    @property
    def active_frames(self):
        return filter(lambda pf: pf.active, self.picture_frames)

    @property
    def untouched_for(self):
        """
        Number of seconds since creation we have gone without a touch
        """
        most_recent = self.initialized_at
        for history in [pf.touch_history for pf in self.picture_frames]:
            most_recent = max(history + [most_recent])
        return time.time() - most_recent

    @property
    def pattern_complete(self):
        return self.active_frames == self.target_pattern

    @property
    def target_pattern(self):
        """
        To be the "target pattern"
          1. all active frames must be within the pattern
          2. the  start of pattern must be an active frame
        """
        considered = self.active_frames
        for pattern in self.patterns:
            if considered <= pattern and pattern[0] <= considered:
                return pattern
        return None

    def in_target_pattern(self, pf):
        return self.target_pattern is not None and pf in self.target_pattern
