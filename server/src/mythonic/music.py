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
        self.open_events = {}

    def start(self, start_measure):
        self.start_offset_in_ticks = (self.resolution * self.beats_per_measure) * start_measure
        self.loop_count = 0
        self.enabled = True

    def stop(self, sequencer):
        self.enabled = False
        for pitch in self.open_events:
            new_event = self.open_events[pitch].copy()
            new_event.velocity = 0
            new_event.tick = 0
            sequencer.event_write(new_event, direct=True)

    def inc_current_measure(self):
        self.current_measure = (self.current_measure + 1) % self.max_measure
        if self.current_measure == 0:
            self.loop_count += 1

    def next_measure(self):
        start_tick = self.current_measure_in_ticks
        end_tick = self.next_measure_in_ticks
        qualifies = lambda e: isinstance(e, midi.NoteEvent) and e.tick >= start_tick and e.tick <= end_tick
        ret = []
        for event in filter(qualifies, self):
            if isinstance(event, midi.NoteOnEvent):
                if event.pitch not in self.open_events:
                    self.open_events[event.pitch] = event
            if isinstance(event, midi.NoteOffEvent):
                if event.pitch in self.open_events:
                    del self.open_events[event.pitch]
            new_tick = event.tick + self.get_tick_offset()
            new_event = event.copy(tick=new_tick)
            ret.append(new_event)
        print ret
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
        self.start_sequencer()

    def start_sequencer(self):
        self.sequencer.start_sequencer()
        self.sequencer_playing = True

    def stop_sequencer(self):
        self.sequencer.stop_sequencer()
        self.sequencer_playing = False

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

    @property
    def need_push(self):
        """
        True once halfway through the first measure.
        Every measure length after that point.
        """
        if not self.playing:
            if self.sequencer_playing:
                #self.stop_sequencer()
                self.last_push = None
            return
        if self.last_push is None:
            ret = True
        else:
            now = self.sequencer.queue_get_tick_time()
            ret = (now - self.last_push) >= self.ticks_per_measure
        if ret:
            self.last_push = self.sequencer.queue_get_tick_time()
        return ret

    def think(self):
        if not self.need_push:
            return
        print "Push tick-time!", self.sequencer.queue_get_tick_time()
        if not self.sequencer_playing:
            self.start_sequencer()
        for track in self.tracks:
            if not track.playing:
                continue
            for event in track.next_measure():
                self.write_event(event)

    def write_event(self, event):
        if not isinstance(event, midi.NoteEvent):
            return
        print "write_event(", event, ")"
        buf = self.sequencer.event_write(event, tick=True)
        #buf = self.sequencer.event_write(event, False, False, True)
        if buf is not None and buf < 1000:
            # TODO: Do something smart
            print "WARNING! event_write buf < 1000"

    @property
    def next_logical_measure(self):
        return math.ceil(self.sequencer.queue_get_tick_time() / float(self.ticks_per_measure))
