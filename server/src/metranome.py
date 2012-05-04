import time

class Metranome(object):
    "Keeps track of time in beats"

    def __init__(self, bpm):
        self.bpm = bpm
        self.last_update = None
        self.current_beat = None
        self.start_time   = time.time()

    def get_seconds_per_beat(self):
        return self.bpm / 60.0
    seconds_per_beat = property(get_seconds_per_beat)

    def _set_beat(self, beat):
        now = time.time()

        self.current_beat = beat
        self.last_update  = now

    def _increment_beat(self):
        if self.current_beat is None:
            self.start()
        else:
            self._set_beat(self.current_beat + 1)

        return self.current_beat

    def start(self):
        self._set_beat(1)
        return self.current_beat

    def time(self):
        "Time in beats, but no greater than current beat"
        if self.current_beat is None:
            return None

        ungated_offset = (((time.time() - self.last_update) * 60) / float(self.bpm))

        # Don't exceed counted beats
        return self.current_beat + min(ungated_offset, 0.99999)

    def can_increment(self):
        now = time.time()
        last_update = self.last_update
        return last_update is None or now - last_update >= self.seconds_per_beat
    can_increment = property(can_increment)

    def next_beat(self):
        if self.can_increment:
            return self._increment_beat()

        return None


