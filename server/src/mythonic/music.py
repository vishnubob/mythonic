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
    def __init__(self, tracks, midi_writer, beats_per_measure, resolution, tempo):
        self.midi_writer = midi_writer
        self.tracks = tracks
        self.beats_per_measure = beats_per_measure
        self.resolution = resolution
        self.tempo = tempo

        self.ticks_per_measure = self.beats_per_measure * self.resolution
        self.measure_s = self.beats_per_measure/(self.tempo/60.0)

        # We hang back a measure
        self.offsets = [self.ticks_per_measure for track in tracks]
        self.tick_cursors = [0 for track in tracks]

        self.now_playing = set()
        self.last_push = None
        self.sequencer_started_at = None

    def restart_sequencer(self):
        self.midi_writer.stop_sequencer()
        self.midi_writer.start_sequencer()
        self.sequencer_started_at = time.time()

    def play(self, idx):
        print "PLAY!"
        track = self.tracks[idx]
        self.offsets[idx] += self.tick_cursors[idx]
        self.tick_cursors[idx] = 0
        self.now_playing.add(track)

    def stop(self, idx):
        print "STOP!"
        track = self.tracks[idx]
        self.now_playing.remove(track)

    @property
    def need_push(self):
        """
        True once halfway through the first measure.
        Every measure length after that point.
        """
        now = time.time()
        if self.last_push is None:
            return now - self.sequencer_started_at >= self.measure_s/2.0
        return self.last_push is None or now - self.last_push >= self.measure_s

    def think(self):
        if self.sequencer_started_at is None:
            self.restart_sequencer()
            print self.sequencer_started_at
        if not self.need_push:
            return
        print "Push time!", self.midi_writer.queue_get_tick_time()
        for event in self.next_measure():
            self.write_event(event)
        self.last_push = time.time()

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
        for idx, track in enumerate(self.tracks):
            if track not in self.now_playing:
                self.offsets[idx] += self.ticks_per_measure
                continue
            lower = self.tick_cursors[idx]
            upper = min(track.max_tick, lower + self.ticks_per_measure - 1)
            qualifies = lambda e: e.tick >= lower and e.tick <= upper
            offset_events = []
            for event in filter(qualifies, track.events):
                # Clone the event and increment its ticks
                event = eval(repr(event))
                event.tick = event.tick + self.offsets[idx]
                offset_events.append(event)
            upcoming_events += offset_events
            self._advance_cursor(idx, self.ticks_per_measure)
        return upcoming_events

    def _advance_cursor(self, idx, amount):
        track = self.tracks[idx]
        self.tick_cursors[idx] += amount
        if self.tick_cursors[idx] >= track.max_tick:
            self.tick_cursors[idx] = 0
            self.offsets[idx] += track.max_tick + 1
