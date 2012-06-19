"""
The business logic for Sonic Storyboard
"""

import copy
import math
import time

import midi

from biscuit import Manager
from pictureframe import PictureFrame

class MythonicTrack(midi.Track):
    """
    A list of midi events representing a musical track.

    Extends functionality of midi.Track by adding mute/unmute
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

    def calc_flashing(self, mini, maxi, offset=0, rate=1):
        seed = time.time() * rate + offset
        return mini if math.sin(seed) <= 0 else maxi

    def calc_intensity(self, ceiling, offset=0, rate=1):
        """
        Return an intensity staggered by "offset", changing at "rate"
        """
        seed = time.time() * rate + offset
        intensity = int(math.sin(seed) * ceiling)
        return max(intensity, 0)

    def blackout(self):
        for pf in self.picture_frames:
            pf.blackout()

    def deactivate(self, pf):
        self.active_frames.remove(pf)

    def get_target_pattern(self, additional=[]):
        considered = additional + self.active_frames
        for pattern in self.patterns:
            # All active frames must be within a pattern
            # and start of pattern must be an active frame
            if considered <= pattern and pattern[0] <= considered:
                return pattern
        return None
    target_pattern = property(get_target_pattern)

    def activate(self, activated_pf):
        self.active_frames.append(activated_pf)

    def think(self):
        """
        Entertain the burners and burn-heads
        """
        touched = []
        triggers = self.hc.get_touch_triggers()
        for idx, directions in enumerate(triggers):
            if reduce(lambda a, b: a or b, directions):
                touched.append(self.picture_frames[idx])
        for pf_idx, pf in enumerate(self.picture_frames):
            if pf in touched:
                # Handle (de)activation by touch
                if pf in self.active_frames:
                    self.deactivate(pf)
                else:
                    self.activate(pf)
            if pf in self.active_frames:
                # Activated frames look cool
                offset = pf.address * 10
                pf.white = pf.MIN_WHITE
                pf.red = self.calc_intensity(pf.MAX_RED,  0 + offset)
                pf.green = self.calc_intensity(pf.MAX_GREEN, 85 + offset)
                pf.blue = self.calc_intensity(pf.MAX_BLUE, 170 + offset)
                pf.uv = self.calc_intensity(pf.MAX_UV, 0 + offset, 0.5)
                if self.target_pattern is not None and pf in self.target_pattern:
                    if self.active_frames == self.target_pattern:
                        pf.blackout()
                        pf.red = pf.MAX_RED
                    else:
                        # Flashing UV when in pattern
                        pf.uv = self.calc_flashing(pf.MIN_UV, pf.MAX_UV, 0, 10)
                pf.track.unmute()
            else:
                # Deactivated frame...
                pf.track.mute()
                pf.blackout()
                pf.white = pf.MAX_WHITE / 3
        self.music_box.step()
