import time

import biscuit

class Coordinator(biscuit.Manager):
    """
    Reads state of hardware, updates storyboard, and
    then delegates to an effects manager.

    After delegation to said effects manager, reads state of
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
        self.last_effects_manager = None

    def select_effects_manager(self):
        """
        The effects manager to delegate to
        """

    def think(self):
        effects_manager = self.select_effects_manager()
        if effects_manager != self.last_effects_manager:
            if self.last_effects_manager is not None:
                self.last_effects_manager.deactivate()
            self.last_effects_manager = effects_manager
            effects_manager.activate()
        for addr, directions in enumerate(self.hc.get_touch_triggers()):
            if reduce(lambda a, b: a or b, directions):
                position = self.hc.addresses.index(addr)
                self.storyboard[position].touch()
        effects_manager.think()
        for addr, pf in enumerate(self.storyboard):
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

    def __init__(self, storyboard):
        self.storyboard = storyboard
        self.activated_at = None
        self.deactivated_at = None

    def think(self):
        """
        Manage effects
        """

    def activate(self):
        """
        """
        self.activated_at = time.time()

    def deactivate(self):
        """
        """
        for pf in self.storyboard:
            pf.blackout()
        self.deactivated_at = time.time()

    @property
    def run_time(self):
        if self.activated_at is None:
            return None
        else:
            return time.time() - self.activated_at
