import math
import pprint
import select
import sys

import midi
import midi.sequencer

BEATS_PER_MEASURE = 4
TEMPO = 105

def make_looper(midi_files, client, port, beats=BEATS_PER_MEASURE, tempo=TEMPO):
    patterns = [midi.read_midifile(path) for path in midi_files]

    res = patterns[0].resolution

    seq = midi.sequencer.SequencerWrite(sequencer_resolution=res, sequencer_tempo=TEMPO)
    seq.subscribe_port(client, port)

    tracks = []
    for pattern in patterns:
        assert(pattern.resolution == res)
        tracks.append(LoopedTrack(pattern, beats))

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
        self.open_events = {}

    def start(self, start_measure):
        self.start_offset_in_ticks = (self.resolution * self.beats_per_measure) * start_measure
        self.loop_count = 0
        self.current_measure = 0
        self.enabled = True

    def stop(self, sequencer):
        self.enabled = False
        for pitch in self.open_events:
            new_event = self.open_events[pitch].copy()
            new_event.velocity = 0
            # XXX: quantized on the beat
            new_event.tick += self.resolution
            sequencer.event_write(new_event, tick=True)

    def inc_current_measure(self):
        self.current_measure = (self.current_measure + 1) % self.max_measure
        if self.current_measure == 0:
            self.loop_count += 1

    def next_measure(self):
        start_tick = self.current_measure_in_ticks
        end_tick = self.next_measure_in_ticks
        if (self.current_measure + 1) == self.max_measure:
            qualifies = lambda e: isinstance(e, midi.NoteEvent) and e.tick >= start_tick and e.tick <= end_tick
        else:
            qualifies = lambda e: isinstance(e, midi.NoteEvent) and e.tick >= start_tick and e.tick < end_tick
        ret = []
        for event in filter(qualifies, self):
            new_tick = event.tick + self.get_tick_offset()
            new_event = event.copy(tick=new_tick)
            if isinstance(new_event, midi.NoteOnEvent):
                self.open_events[event.pitch] = new_event
            if isinstance(new_event, midi.NoteOffEvent):
                if new_event.pitch in self.open_events:
                    del self.open_events[new_event.pitch]
            ret.append(new_event)
        self.inc_current_measure()
        return ret

    def get_tick_offset(self):
        return int(self.start_offset_in_ticks + (self.loop_count * (self.max_measure * self.resolution * self.beats_per_measure)))

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
        self.last_push = None
        self.ticks_per_measure = self.beats_per_measure * self.resolution
        self.sequencer_playing = False
        # XXX: teehee
        self.next_push = -(self.beats_per_measure / 2.0)
        self.sequencer.start_sequencer()

    def play(self, idx):
        print "PLAY!", idx
        track = self.tracks[idx]
        track.start(self.next_logical_measure)

    def stop(self, idx):
        print "STOP!", idx
        track = self.tracks[idx]
        track.stop(self.sequencer)

    @property
    def playing(self):
        for track in self.tracks:
            if track.playing:
                return True
        return False

    def push_needed(self):
        now = self.sequencer.queue_get_tick_time()
        if now > self.next_push:
            self.next_push += (self.beats_per_measure * self.resolution)
            return True
        return False

    def think(self):
        if not self.push_needed():
            return
        print "Push tick-time!", self.sequencer.queue_get_tick_time()
        for track in self.tracks:
            if not track.playing:
                continue
            for event in track.next_measure():
                self.write_event(event)
        #self.sequencer.drain()

    def write_event(self, event):
        if not isinstance(event, midi.NoteEvent):
            return
        #print "write_event(", event, ")"
        buf = self.sequencer.event_write(event, tick=True)
        #buf = self.sequencer.event_write(event, False, False, True)
        if buf is not None and buf < 1000:
            # TODO: Do something smart
            print "WARNING! event_write buf < 1000"

    @property
    def next_logical_measure(self):
        print "NL", math.ceil((self.sequencer.queue_get_tick_time() + self.resolution) / float(self.ticks_per_measure))
        return math.ceil(self.sequencer.queue_get_tick_time() / float(self.ticks_per_measure))
