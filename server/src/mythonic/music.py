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
        tracks.append(LoopedTrack(pattern))

    return Looper(tracks, seq, beats, res, tempo)

class LoopedTrack(object):
    def __init__(self, mf):
        self.resolution = mf.resolution
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

        self.current_measure = [0 for track in tracks]
        self.tick_cursors = [0 for track in tracks]
        # We hang back a measure
        self.global_measure = 1

        self.now_playing = set()
        self.last_push = None
        self.sequencer_restarted = False

    def restart_sequencer(self):
        self.midi_writer.stop_sequencer()
        self.midi_writer.start_sequencer()
        self.sequencer_restarted = True

    def play(self, idx):
        print "PLAY!"
        track = self.tracks[idx]
        self.current_measure[idx] = 0
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
        now = self.midi_writer.queue_get_tick_time()
        if self.last_push is None:
            return now >= self.ticks_per_measure / 2.0
        return now - self.last_push >= self.ticks_per_measure

    def think(self):
        if not self.sequencer_restarted:
            self.restart_sequencer()
        if not self.need_push:
            return
        print "Push tick-time!", self.midi_writer.queue_get_tick_time()
        for event in self.next_measure():
            self.write_event(event)
        self.last_push = self.midi_writer.queue_get_tick_time()

    def write_event(self, event):
        print "write_event(", event, ")"
        buf = self.midi_writer.event_write(event, False, False, True)
        if buf is not None and buf < 1000:
            # TODO: Do something smart
            print "WARNING! event_write buf < 1000"

    @property
    def global_offset(self):
        return self.global_measure * self.beats_per_measure * self.resolution

    def next_measure(self):
        """
        Retrieve the next measure worth of events.
        Only events part of "now_playing" tracks are included.
        """
        print "Global measure", self.global_measure
        upcoming_events = []
        for idx, track in enumerate(self.tracks):
            if track not in self.now_playing:
                continue
            print "Local measure", self.current_measure[idx]
            lower = self.current_measure[idx] * self.beats_per_measure * self.resolution
            upper = (self.current_measure[idx] + 1) * self.beats_per_measure * self.resolution
            print "Events withs ticks [%d, %d)" % (lower, upper)
            qualifies = lambda e: e.tick >= lower and e.tick < upper
            for event in filter(qualifies, track.events):
                # Clone the event and increment its ticks
                event = eval(repr(event))
                event.tick = event.tick + self.global_offset
                upcoming_events.append(event)
            self.current_measure[idx] = self.current_measure[idx] + 1 % self.max_measure(idx)
        self.global_measure += 1
        return upcoming_events

    def max_measure(self, idx):
        return math.ceil(self.tracks[idx].max_tick/(self.resolution * self.beats_per_measure))
