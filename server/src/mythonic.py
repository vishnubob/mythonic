"""
Mythonic core creative classes
"""

import colorsys
import math
import time

import midi

import biscuit

class PictureFrame(object):
    MAX_RED = 0xff
    MIN_RED = 0x0

    MAX_GREEN = 0xff
    MIN_GREEN = 0x0

    MAX_BLUE = 0xff
    MIN_BLUE = 0x0

    MAX_WHITE = 0xff
    MIN_WHITE = 0x0

    MAX_UV = 0xff
    MIN_UV = 0x0

    def __init__(self):
        self.red = self.MIN_RED
        self.green = self.MIN_GREEN
        self.blue = self.MIN_BLUE
        self.white = self.MIN_WHITE
        self.uv = self.MIN_UV
        self._touched = False
        self._active = False
        self.touch_history = []

    def color_property(color, minimum, maximum):
        """
        Creates a property instance for the given color
        with bounds checking on assignment.
        """
        attr = "_" + color
        def getcolor(self):
            return self.__dict__[attr]
        def setcolor(self, intensity):
            if intensity > maximum or intensity < minimum:
                raise ValueError(color + " intensity of " + str(intensity) + " is out of bounds.")
            self.__dict__[attr] = intensity
        return property(getcolor, setcolor)

    red = color_property("red", MIN_RED, MAX_RED)
    green = color_property("green", MIN_GREEN, MAX_GREEN)
    blue = color_property("blue", MIN_BLUE, MAX_BLUE)
    white = color_property("white", MIN_WHITE, MAX_WHITE)
    uv = color_property("uv", MIN_UV, MAX_UV)

    def touch(self):
        self.touch_history.append(time.time())
        if self.active:
            self.deactivate()
        else:
            self.activate()
        self._touched = True
    touched = property(lambda self: self._touched)

    def activate(self):
        self._active = True
    def deactivate(self):
        self._active = False
    active = property(lambda self: self._active)

    @property
    def hsv(self):
        red = max(self.MIN_RED, self.red / float(self.MAX_RED))
        green = max(self.MIN_GREEN, self.green / float(self.MAX_GREEN))
        blue = max(self.MIN_BLUE, self.blue / float(self.MAX_BLUE))
        return colorsys.rgb_to_hsv(red, green, blue)
    @hsv.setter
    def hsv(self, hsv):
        rgb = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])
        self.red = int(rgb[0] * self.MAX_RED)
        self.green = int(rgb[1] * self.MAX_GREEN)
        self.blue = int(rgb[2] * self.MAX_BLUE)

    def blackout(self):
        self.red = self.MIN_RED
        self.green = self.MIN_GREEN
        self.blue = self.MIN_BLUE
        self.uv = self.MIN_UV
        self.white = self.MIN_WHITE

class DelegationManager(biscuit.Manager):
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

class MythonicTrack(midi.Track):
    """
    A list of midi events representing a musical track.

    Extends functionality of midi.Track by adding mute/unmute and friends
    """

    _muted = False
    _velocities = {}

    def __init__(self, events):
        super(MythonicTrack, self).__init__(events)
        for event in self.note_on_events:
            self._velocities[id(event)] = event.velocity

    def increase_ticks(self, increase):
        for event in self:
            event.tick = event.tick + increase

    def mute(self):
        if not self._muted:
            for event in self.note_on_events:
                # Record last unmuted value in case there were changes to it
                self._velocities[id(event)] = event.velocity
                event.velocity = 0
        self._muted = True

    def unmute(self):
        if self._muted:
            for event in self.note_on_events:
                event.velocity = self._velocities[id(event)]
        self._muted = False

    @property
    def note_on_events(self):
        return filter(lambda e: isinstance(e, midi.NoteOnEvent), self)

#class MusicBox(midi.Pattern):
class MusicBox(object):
    """
    Loop and manage midi tracks
    """

    def __init__(self, pattern, midi_seq):
        self.midi_seq = midi_seq
        pattern.make_ticks_abs()
        self.pattern = pattern
        self.tick_cursor = 0
        self.last_cursor_update = None
        self.tracks = map(MythonicTrack, pattern)
        self.original_max_cursor = self.max_cursor

    @property
    def ticks_per_s(self):
        return self.tempo / float(self.resolution)

    @property
    def resolution(self):
        return self.pattern.resolution

    @property
    def tempo(self):
        return 60 * 1000000 / self.midi_seq.sequencer_tempo

    @property
    def max_cursor(self):
        return max(event.tick for track in self.tracks for event in track)

    def increment_tick_cursor(self):
        if self.tick_cursor >= self.max_cursor:
            for track in self.tracks:
                track.increase_ticks(self.original_max_cursor + 1)
        self.tick_cursor += 1
        self.last_cursor_update = time.time()

    @property
    def ticks_transpired(self):
        if self.last_cursor_update is not None:
            start = self.last_cursor_update
            end = time.time()
            return int((end - start) * self.ticks_per_s)
        else:
           return 1

    @property
    def events_by_tick(self):
        events_by_tick = {}
        for track in self.tracks:
            for event in track:
                if event.tick not in events_by_tick:
                    events_by_tick[event.tick] = []
                events_by_tick[event.tick] += [event]
        return events_by_tick

    def step(self):
        """
        Handles any event sending that might need to happen.
        """
        ticks_transpired = self.ticks_transpired
        if ticks_transpired <= 0:
            return
        events_by_tick = self.events_by_tick
        events = []
        for i in range(ticks_transpired):
            if self.tick_cursor in events_by_tick:
                events += events_by_tick[self.tick_cursor]
            self.increment_tick_cursor()
        events.sort()
        for event in events:
            self.write_event(event)

    def write_event(self, event):
        buf = self.midi_seq.event_write(event, False, False, True)
        if buf is not None and buf < 1000:
            # TODO: Do something smarter than sleep
            print "WARNING! event_write buf < 1000"
            time.sleep(.5)
        return buf
