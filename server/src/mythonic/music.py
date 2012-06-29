import sys
import time

import midi
import midi.sequencer

BEATS_PER_MEASURE = 4
TEMPO = 120

def main():
    if len(sys.argv) < 4:
        script_name = sys.argv[0]
        print "Usage: %s <midi client> <midi port> <file1, ...>" % script_name
        exit(2)

    client = int(sys.argv[1])
    port = int(sys.argv[2])
    file_paths = sys.argv[3:]

    if len(file_paths) <= 0:
        print "No MIDI files specified"
        return

    patterns = [midi.read_midifile(path) for path in file_paths]
    beats = BEATS_PER_MEASURE
    tempo = TEMPO
    res = patterns[0].resolution
    tracks = []
    for pattern in patterns:
        assert(pattern.resolution == res)
        track = Track(pattern, beats, res)
        tracks.append(track)
    midi_writer = make_midi_writer(client, port, res)
    sequencer = Sequencer(tracks, midi_writer, beats, res, tempo)
    for track in tracks:
        track.play()
    while True:
        sequencer.think()

def make_midi_writer(client, port, res):
    seq = midi.sequencer.SequencerWrite(sequencer_resolution=res)
    seq.subscribe_port(client, port)
    seq.start_sequencer()
    return seq

class Track(object):
    _now_playing = False
    current_measure = 0

    def __init__(self, mf, beats_per_measure, resolution):
        # Merge events from all tracks in the midi file
        mf.make_ticks_abs()
        self.events = []
        for track in mf:
            self.events += track
        self.events.sort()
        self.beats_per_measure = beats_per_measure
        self.resolution = resolution
        self.ticks_per_measure = self.resolution * self.beats_per_measure
        self.last_measure = self.measure_of(max([event.tick for event in self.events]))

    def play(self):
        self._now_playing = True
        self.current_measure = 0

    def stop(self):
        self._now_playing = False

    now_playing = property(lambda s: s._now_playing)

    def measure_of(self, tick):
        return tick / self.ticks_per_measure

    def next_measure(self):
        events = []
        for event in self.events:
            if self.measure_of(e.tick) == self.current_measure:
                events.append(event)
        self.current_measure = (self.current_measure + 1) % self.current_measure
        return events

class Sequencer(object):

    def __init__(self, tracks, midi_writer, beats_per_measure, resolution, tempo):
        self.midi_writer = midi_writer
        self.tracks = tracks
        self.beats_per_measure = beats_per_measure
        self.resolution = resolution
        self.tempo = tempo

        self.measure_s = self.beats_per_measure/(self.tempo/60.0)

        self.last_write = None

        self.tick_offsets = []
        for track in self.tracks:
            self.tick_offsets.append(0)

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
        events = []
        for idx, track in enumerate(self.tracks):
            if not track.now_playing:
               continue 
            tick_offset = self.tick_offsets[idx]
            for event in track.events:
                event = eval(repr(event))
                event.tick = event.tick + tick_offset
                events.append(event)
            self.tick_offsets[idx] += track.ticks_per_measure + 1
        return events

    @property
    def need_push(self):
        now = time.time()
        return self.last_write is None or now - self.last_write >= self.measure_s

    def think(self):
        if not self.need_push:
            return
        for event in self.next_measure():
            self.write_event(event)
        self.last_write = time.time()

if __name__ == "__main__":
    main()
