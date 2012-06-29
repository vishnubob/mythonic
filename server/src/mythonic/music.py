import midi

class Track(object):
    _now_playing = False 
    current_measure = 0

    def __init__(self, mf, beats_per_measure=4):
        # Merge events from all tracks in the midi file
        mf.make_ticks_abs()
        self.events = []
        for track in mf:
            self.events += track
        self.events.sort()
        # Go go gadget maths
        self.resolution = mf.resolution
        self.ticks_per_measure = self.resolution * beats_per_measure
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

    def __init__(self, midi_writer, tracks, beats_per_measure=4):
        self.tracks = tracks
        self.midi_writer = midi_writer
        self.tick_offsets = {}
        for track in self.tracks:
            self.tick_offsets.append(0)
        self.resolution = tracks[0].resolution
        self.tps =  bpm * self.resolution / 60.0
        self.window_s = (measure_ticks/2.0) * self.tps
        self.last_write = None

    def write_event(self, event):
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
                next
            tick_offset = self.tick_offsets[idx]
            for event in track.events:
                event = eval(repr(event))
                event.tick = event.tick + tick_offset
                events.append(event)
            self.tick_offsets[idx] += track.ticks_per_measure + 1
        return events

    @property
    def push_pending(self):
        now = time.time()
        return self.last_write is None or now - self.last_write >= self.window_s

    def step(self):
        if not push_pending():
            return
        for event in self.next_measure():
            self.write_event(event)
