"""
The business logic for Sonic Storyboard
"""

import copy
import math
import time

import midi

from biscuit import Manager
from pictureframe import PictureFrame

class MythonicPictureFrame(PictureFrame):

    def __init__(self, main_tracks=[], bonus_tracks=[]):
        self.main_tracks = main_tracks
        self.bonus_tracks = bonus_tracks

    def mute(self):
        self.mute_bonus()
        self.mute_main()

    def mute_main(self):
        for track in self.main_tracks:
            track.mute()

    def unmute_main(self):
        for track in self.main_tracks:
            track.unmute()

    def mute_bonus(self):
        for track in self.bonus_tracks:
            track.mute()

    def unmute_bonus(self):
        for track in self.bonus_tracks:
            track.unmute()

    def calc_sin(self, ceiling, offset=0, rate=1):
        """
        Return an intensity staggered by "offset", changing at "rate"
        """
        seed = time.time() * rate + offset
        intensity = int(math.sin(seed) * ceiling)
        return max(intensity, 0)

    def calc_square(self, low, high, offset=0, rate=10):
        seed = time.time() * rate + offset
        return low if math.sin(seed) <= 0 else high

    def step_inactive(self):
        """
        A picture frame at rest. Only white light at 1/3rd intensity
        """
        self.mute()
        self.blackout()
        # TODO: Flicker instead?
        self.white = pf.MAX_WHITE / 3

    def step_active(self):
        offset = self.address * 10
        self.white = pf.MIN_WHITE
        self.red = self.calc_sin(pf.MAX_RED,  0 + offset)
        self.green = self.calc_sin(pf.MAX_GREEN, 85 + offset)
        self.blue = self.calc_sin(pf.MAX_BLUE, 170 + offset)
        self.uv = self.calc_sin(pf.MAX_UV, 0 + offset, 0.5)

    def step_active_hint(self):
        """
        Hint that this selectd picture frame is part of a pattern
        """
        pf.uv = self.calc_square(pf.MIN_UV, pf.MAX_UV)

    def step_inactive_hint(self):
        """
        Hints that this inactive picture frame is part of a pattern
        """
        pass

    def step_bonus(self):
        """
        Spectacle for a special occasion, like being part of a completed
        pattern
        """
        pf.unmute_bonus()
        pf.blackout()
        pf.red = pf.MAX_RED

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
        if self.muted:
            return
        for event in self.note_on_events:
            # Record last unmuted value in case there were changes to it
            self._velocities[id(event)] = event.velocity
            event.velocity = 0
        self._muted = True

    def unmute(self):
        if not self.muted:
            return
        for event in self.note_on_events:
            event.velocity = self._velocities[id(event)]
        self._muted = False

    def get_note_on_events(self):
        return filter(lambda e: isinstance(e, midi.NoteOnEvent), self)
    note_on_events = property(get_note_on_events)

    def get_muted(self):
        return self._muted
    muted = property(get_muted)


#class MusicBox(midi.Pattern):
class MusicBox(object):
    """
    Loop and manage midi tracks
    """

    def __init__(self, midi_seq, pattern):
        self.midi_seq = midi_seq
        pattern.make_ticks_abs()
        self.pattern = pattern
        self.tick_cursor = 0
        self.last_cursor_update = None
        self.tracks = map(MythonicTrack, pattern)
        self.original_max_cursor = self.max_cursor

    def get_ticks_per_s(self):
        return self.tempo / float(self.resolution)
    ticks_per_s = property(get_ticks_per_s)

    def get_resolution(self):
        return self.pattern.resolution
    resolution = property(get_resolution)

    def get_tempo(self):
        return 60 * 1000000 / self.midi_seq.sequencer_tempo
    tempo = property(get_tempo)

    def get_max_cursor(self):
        return max(event.tick for track in self.tracks for event in track)
    max_cursor = property(get_max_cursor)

    def increment_cursor(self):
        old_cursor = self.tick_cursor
        if old_cursor > self.max_cursor:
            for track in self.tracks:
                track.increase_ticks(self.original_max_cursor)
        self.tick_cursor += 1
        self.last_cursor_update = time.time()
        return old_cursor

    def get_ticks_transpired(self):
        if self.last_cursor_update is not None:
            start = self.last_cursor_update
            end = time.time()
            return int((end - start) * self.ticks_per_s)
        else:
           return 1
    ticks_transpired = property(get_ticks_transpired)

    def get_events_by_tick(self):
        events_by_tick = {}
        for track in self.tracks:
            for event in track:
                if event.tick not in events_by_tick:
                    events_by_tick[event.tick] = []
                events_by_tick[event.tick] += [event]
        return events_by_tick
    events_by_tick = property(get_events_by_tick)

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
            cursor = self.increment_cursor()
            if cursor in events_by_tick:
                events += events_by_tick[cursor]
        events.sort()
        for event in events:
            self.write_event(event)
            print event

    def write_event(self, event):
        buf = self.midi_seq.event_write(event, False, False, True)
        if buf is not None and buf < 1000: 
            # TODO: Do something smarter than sleep
            print "WARNING! event_write buf < 1000"
            time.sleep(.5) 
        return buf

class SSManager(Manager):
    """
    Runner for Sonic Storyboard.
    """

    def __init__(self, music_box, hc, number_of_boxes):
        super(SSManager, self).__init__(hc)
        self.music_box = music_box
        self.picture_frames = []
        for idx in range(number_of_boxes):
            pf = PictureFrame(idx, hc, self.music_box.tracks[idx + 1])
            self.picture_frames.append(pf)
        self.active_frames = []
        self.patterns = [[self.picture_frames[i] for i in [0, 1]]]

    def blackout(self):
        for pf in self.picture_frames:
            pf.blackout()

    def get_target_pattern(self, additional=[]):
        considered = additional + self.active_frames
        for pattern in self.patterns:
            # All active frames must be within a pattern
            # and start of pattern must be an active frame
            if considered <= pattern and pattern[0] <= considered:
                return pattern
        return None
    target_pattern = property(get_target_pattern)

    def activate(self, pf):
        self.active_frames.append(pf)

    def deactivate(self, pf):
        self.active_frames.remove(pf)

    def is_active(self, pf):
        return pf in self.active_frames

    def in_target_pattern(self, pf):
        return self.target_pattern is not None and pf in self.target_pattern

    def is_pattern_complete(self):
        return self.active_frames == self.target_pattern
    pattern_complete = property(is_pattern_complete)

    def think(self):
        """
        Entertain the burners and burn-heads
        """
        # Collect touch data
        touched = []
        triggers = self.hc.get_touch_triggers()
        for idx, directions in enumerate(triggers):
            if reduce(lambda a, b: a or b, directions):
                touched.append(self.picture_frames[idx])
        # Update picture frames
        for pf in self.picture_frames:
            if pf in touched:
                # Handle (de)activation by touch
                if self.is_active(pf):
                    self.deactivate(pf)
                else:
                    self.activate(pf)
            if self.is_active(pf):
                pf.step_active()
                if self.in_target_pattern(pf):
                    if self.pattern_complete:
                        # Frame is part of exclusive and complete pattern
                        pf.step_special()
                    else:
                        # Frame is in pattern, but pattern is incomplete
                        pf.step_active_hint()
            else:
                # Frame is inactive
                pf.step_inactive()
        self.music_box.step()
