import pprint
import select
import sys
import time

import midi
import midi.sequencer

BEATS_PER_MEASURE = 4
TEMPO = 120

def make_looper(midi_files, client, port, beats=BEATS_PER_MEASURE, tempo=TEMPO):
    patterns = [midi.read_midifile(path) for path in midi_files]

    res = patterns[0].resolution

    seq = midi.sequencer.SequencerWrite(sequencer_resolution=res)
    seq.subscribe_port(client, port)

    tracks = []
    for pattern in patterns:
        assert(pattern.resolution == res)
        tracks.append(LoopedTrack(pattern))

    return Looper(tracks, seq, beats, res, tempo)

class LoopedTrack(object):
    def __init__(self, mf):
        # Merge events from all tracks in the midi file
        mf.make_ticks_abs()
        self.events = []
        for track in mf:
            self.events += track
        self.events.sort()
        self.max_tick = max([event.tick for event in self.events])

class Looper(object):
    now_playing = set()
    last_write = None

    def __init__(self, tracks, midi_writer, beats_per_measure, resolution, tempo):
        self.midi_writer = midi_writer
        self.tracks = tracks
        self.beats_per_measure = beats_per_measure
        self.resolution = resolution
        self.tempo = tempo

        self.ticks_per_measure = self.beats_per_measure * self.resolution
        self.measure_s = self.beats_per_measure/(self.tempo/60.0)

        self.offsets = [0 for track in tracks]
        self.tick_cursors = [0 for track in tracks]

        # Validate that ticks are absolute
        for track in tracks:
            last_tick = 0
            for event in track.events:
                assert(event.tick >= last_tick)
                last_tick = event.tick

    def play(self, idx):
        track = self.tracks[idx]
        self.offsets[idx] += self.tick_cursors[idx]
        self.tick_cursors[idx] = 0
        self.now_playing.add(track)

    def stop(self, idx):
        track = self.tracks[idx]
        self.now_playing.remove(track)

    @property
    def need_push(self):
        now = time.time()
        return self.last_write is None or now - self.last_write >= self.measure_s

    def think(self):
        if not self.need_push:
            return
        now = time.time()
        if self.last_write is None:
            # Reset sequencer to reset tick count
            self.midi_writer.stop_sequencer()
        for event in self.next_measure():
            self.write_event(event)
        if self.last_write is None:
            self.midi_writer.start_sequencer()
        self.last_write = time.time()

    def write_event(self, event):
        #print "write_event(", event, ")"
        buf = self.midi_writer.event_write(event, False, False, True)
        if buf is not None and buf < 1000:
            # TODO: Do something smart
            print "WARNING! event_write buf < 1000"

    def next_measure(self):
        """
        Retrieve the next measure worth of events.
        Only events part of "now_playing" tracks are included.
        """
        upcoming_events = []
        #TODO ticks_transpired = self.ticks_transpired
        ticks_transpired = self.ticks_per_measure
        for idx, track in enumerate(self.tracks):
            if track not in self.now_playing:
                self.offsets[idx] += ticks_transpired
                continue
            lower = self.tick_cursors[idx]
            upper = min(track.max_tick, lower + self.ticks_per_measure - 1)
            # TODO min(track.max_tick, ticks_transpired - 1) 
            qualifies = lambda e: e.tick >= lower and e.tick <= upper
            offset_events = []
            for event in filter(qualifies, track.events):
                # Clone the event and increment its ticks
                event = eval(repr(event))
                event.tick = event.tick + self.offsets[idx]
                offset_events.append(event)
            upcoming_events += offset_events
            self._advance_cursor(idx, ticks_transpired)
        return upcoming_events

    @property
    def ticks_transpired(self):
        return int((time.time() - self.last_write) * self.ticks_per_s)

    def _advance_cursor(self, idx, amount):
        track = self.tracks[idx]
        self.tick_cursors[idx] += amount
        if self.tick_cursors[idx] >= track.max_tick:
            self.tick_cursors[idx] = 0
            self.offsets[idx] += track.max_tick + 1
