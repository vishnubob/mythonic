"""Mythonic/installation-specific implementations of abstractions"""

from wired import WiredMediator
from mode import Mode
from event import *

class MythonicMediator(WiredMediator):

    def __init__(self, picture_frames, bus):
        super(MythonicMediator, self).__init__(picture_frames, bus)

        self.idle_mode = IdleMode(picture_frames, self)
        self.screensaver_mode = ScreenSaverMode(picture_frames, self)
        self.instrument_mode = InstrumentMode(picture_frames, self)

        self.activate_mode(self.idle_mode)

    def handle_event(self, event):
        if isinstance(event, ModeEnd):
            mode = event.mode
            if mode is self.idle_mode or mode is self.screensaver_mode:
                self.activate_mode(self.screensaver_mode)
            else:
                self.activate_mode(self.idle_mode)
            return True
        if isinstance(event, Touch):
            # Put into instrument mode if not already
            if self.active_mode is not self.instrument_mode:
                self.activate_mode(self.instrument_mode)

        return super(MythonicMediator, self).handle_event(event)

class InstrumentMode(Mode):

    def handle_event(self, event):
        if not isinstance(event, Touch):
            return False

        touch = event
        frame = event.picture_frame

        frame.set_blue(touch.up)
        frame.set_green(touch.left)
        frame.set_red(touch.down)
        frame.set_uv(touch.right)

        self.send_mediator(LightChange(self))

class ScreenSaverMode(Mode):

    def think(self):
        "Awesome effects"
        self.send_mediator(ModeEnd(self))

class IdleMode(Mode):

    def think(self):
        if self.time_passed >= 5:
            self.send_mediator(ModeEnd(self))
