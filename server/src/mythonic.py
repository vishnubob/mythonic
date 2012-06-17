"""
The business logic for Sonic Storyboard
"""

import math
import time

import midi

from biscuit import Manager
from pictureframe import PictureFrame

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
        self.orginal_max_cursor = self.max_cursor

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
        return max(event.tick for track in self.pattern for event in track)
    max_cursor = property(get_max_cursor)

    def increment_cursor(self):
        old_cursor = self.tick_cursor
        self.tick_cursor += 1
        if self.tick_cursor > self.max_cursor:
            # Increment the ticks of all the events
            # Otherwise looping around replays everything
            for track in self.pattern:
                for event in track:
                    if event.tick != old_cursor:
                        event.tick += self.orginal_max_cursor
        self.last_cursor_update = time.time()
        return old_cursor

    def step(self):
        """
        Handles any event sending that might need to happen.
        """
        if self.last_cursor_update is not None:
            start = self.last_cursor_update
            end = time.time()
            ticks_transpired = int((end - start) * self.ticks_per_s)
        else:
           ticks_transpired = 1
        if ticks_transpired <= 0:
            return
        time.sleep(0.001)

        events_by_tick = {}
        for track in self.pattern:
            for event in track:
                if event.tick not in events_by_tick:
                    events_by_tick[event.tick] = []
                events_by_tick[event.tick] += [event]

        events = []
        for i in range(ticks_transpired):
            cursor = self.increment_cursor()
            if cursor in events_by_tick:
                events += events_by_tick[cursor]

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

class SSManager(Manager):
    """
    Runner for Sonic Storyboard.
    """

    def __init__(self, midi_seq, hc, number_of_boxes):
        super(SSManager, self).__init__(hc)
        self.picture_frames = []
        for idx in range(number_of_boxes):
            self.picture_frames.append(PictureFrame(idx, hc))
        self.active_frames = []
        self.patterns = [[self.picture_frames[i] for i in [0, 1]]]
        self.midi_seq = midi_seq

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

    # In order to select a pattern, pf has to be the start of a new pattern or within the old
    def next_target_pattern(self, pf):
        return self.get_target_pattern([pf])

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
        next_target_pattern = self.next_target_pattern(activated_pf)
#
#        # Old pattern canceled
#        if self.target_pattern is not None and next_target_pattern is None:
#            print "Out of bounds of the old pattern"
#            for pf in self.active_frames:
#                if pf in self.target_pattern:
#                    self.deactivate(pf)
#        # New pattern selected
#        elif self.target_pattern is None and next_target_pattern is not None:
#            print "New pattern selected"
#            for pf in self.active_frames:
#                if pf not in next_target_pattern:
#                    self.deactivate(pf)
#        elif self.target_pattern != next_target_pattern:
#            print "Pattern changed"
#
#        if next_target_pattern is None:
#            print "Free mode"
#
        self.active_frames.append(activated_pf)

    def play_music(self):
        self.midi_seq.event_write(midi.NoteOnEvent(tick=0, channel=1, data=[int(abs(math.sin(time.time() * 10) * 127)), 50]), False, False, True)

    def think(self):
        """
        Entertain the burners and burn-heads
        """
        touched = []
        triggers = self.hc.get_touch_triggers()
        for idx, directions in enumerate(triggers):
            if reduce(lambda a, b: a or b, directions):
                touched.append(self.picture_frames[idx])
        for pf in self.picture_frames:
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
                        self.play_music()
                        pf.blackout()
                        pf.red = pf.MAX_RED
                    else:
                        # Flashing UV when in pattern
                        pf.uv = self.calc_flashing(pf.MIN_UV, pf.MAX_UV, 0, 10)
            else:
                # Deactivated frames look borring
                pf.blackout()
                pf.white = pf.MAX_WHITE / 3
