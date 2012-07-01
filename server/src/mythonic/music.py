import math
import pprint
import select
import sys

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
        tracks.append(LoopedTrack(pattern, BEATS_PER_MEASURE))

    return Looper(tracks, seq, beats, res, tempo)

class LoopedTrack(midi.Track):
    def __init__(self, mf, beats_per_measure):
        self.beats_per_measure = beats_per_measure
        self.mf = mf
        self.loop_count = 0
        self.start_offset = 0
        self.current_measure = 0
        self.enabled = False
        # load the track
        self.resolution = mf.resolution
        # XXX: track is assumed to be the first!
        super(LoopedTrack, self).__init__(mf[0])
        self.make_ticks_abs()
        self.max_tick = max([event.tick for event in self])
        self.max_measure = math.ceil(self.max_tick / (self.resolution * self.beats_per_measure))

    def start(self, start_measure):
        self.start_offset_in_ticks = (self.resolution * self.beats_per_measure) * start_measure
        self.loop_count = 0
        self.enabled = True

    def stop(self):
        self.enabled = False

    def inc_current_measure(self):
        self.current_measure = (self.current_measure + 1) % self.max_measure
        if self.current_measure == 0:
            self.loop_count += 1

    def next_measure(self):
        start_tick = self.current_measure_in_ticks
        end_tick = self.next_measure_in_ticks
        self.inc_current_measure()
        qualifies = lambda e: e.tick >= start_tick and e.tick < end_tick
        events = filter(qualifies, self)
        for event in events:
            event.tick += self.get_tick_offset()
        return events

    def get_tick_offset(self):
        return self.start_offset_in_ticks + (self.loop_count * (self.max_measure * self.resolution * self.beats_per_measure))

    @property
    def next_measure_in_ticks(self):
        return ((self.current_measure + 1) * self.resolution * self.beats_per_measure)

    @property
    def current_measure_in_ticks(self):
        return (self.current_measure * self.resolution * self.beats_per_measure)
        
    @property
    def playing(self):
        return self.enabled

class Looper(object):
    def __init__(self, tracks, sequencer, beats_per_measure, resolution, tempo):
        self.sequencer = sequencer
        self.tracks = tracks
        self.beats_per_measure = beats_per_measure
        self.resolution = resolution
        self.tempo = tempo

        self.ticks_per_measure = self.beats_per_measure * self.resolution

        self.last_push = None
        self.sequencer_restarted = False
        # XXX: stop / start sequencer as needed
        self.restart_sequencer()

    def restart_sequencer(self):
        self.sequencer.stop_sequencer()
        self.sequencer.start_sequencer()
        self.sequencer_restarted = True

    def play(self, idx):
        print "PLAY!", idx
        track = self.tracks[idx]
        track.start(self.next_logical_measure)

    def stop(self, idx):
        print "STOP!", idx
        track = self.tracks[idx]
        track.stop()

    @property
    def need_push(self):
        """
        True once halfway through the first measure.
        Every measure length after that point.
        """
        now = self.sequencer.queue_get_tick_time()
        if self.last_push is None:
            return now >= self.ticks_per_measure / 2.0
        return now - self.last_push >= self.ticks_per_measure

    def think(self):
        if not self.need_push:
            return
        print "Push tick-time!", self.sequencer.queue_get_tick_time()
        for track in self.tracks:
            if not track.playing:
                continue
            for event in track.next_measure():
                self.write_event(event)
        self.last_push = self.sequencer.queue_get_tick_time()

    def write_event(self, event):
        if not isinstance(event, midi.NoteEvent):
            return
        print "write_event(", event, ")"
        buf = self.sequencer.event_write(event, tick=True)
        if buf is not None and buf < 1000:
            # TODO: Do something smart
            print "WARNING! event_write buf < 1000"

    @property
    def next_logical_measure(self):
        return (self.sequencer.queue_get_tick_time() / self.ticks_per_measure) + 1
