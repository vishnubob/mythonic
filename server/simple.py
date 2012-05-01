#!/usr/bin/env python

import sys
import time
import serial

def main():

    if len(sys.argv) != 2:
        script_name = sys.argv[0]
        print "Usage:   {0} <tty>".format(sys.argv[0])
        print "Example: {0} /dev/ttyUSB0".format(sys.argv[0])
        exit(2)

    tty = sys.argv[1]

    bus = serial.Serial(tty)
    storyboard = WiredStoryboard(bus, [WiredPictureFrame(i) for i in range(7)])

    metranome = Metranome(60)
    schedular = EffectScheduler(metranome.time)

    frame = storyboard[0]
    for t in range(1, 9, 3):
        schedular.fade(frame.increase_blue, 3, 2, t)
        schedular.fade(frame.decrease_blue, 2, 1, t + 2)

    beat = None
    while beat < 10:
        total_run = schedular.run_due(1)
        if total_run > 0: print frame.blue
        beat = metranome.next_beat()
        if beat is not None:
            print "==== " + str(beat) + " ====="
           
class Scheduler(object):
    def __init__(self, time_f):
        self._now   = time_f
        self._sched = {}

    def schedule(self, f, time):
        sched = self._sched
        if time not in sched:
            sched[time] = []
        sched[time].append(f)

    def run_due(self, n):
        now   = self._now()
        sched = self._sched

        total_run = 0

        if len(sched.keys()) == 0:
            return total_run

        for i in range(n):
            soonest = min(sched.keys())

            if soonest <= now:
                f = sched[soonest].pop()
                f()
                total_run = total_run + 1
                if len(sched[soonest]) == 0:
                    del sched[soonest]

        return total_run

class EffectScheduler(Scheduler):
    def fade(self, f, amount, duration, start):
        print "fade(f, {0}, {1}, {2}):".format(amount, duration, start)
        t = start
        for i in range(amount):
           self.schedule(f, t)
           t = t + duration/float(amount)

class Metranome(object):

    def __init__(self, bpm):
        self.bpm = bpm
        self.last_beat_at = None
        self.current_beat = None
        self.start_time   = time.time()

    def get_seconds_per_beat(self):
        return self.bpm / 60.0

    seconds_per_beat = property(get_seconds_per_beat)

    def _increment_beat(self):
        now = time.time()
        
        if self.current_beat is None:
            self.current_beat = 1
        else:
            self.current_beat = self.current_beat + 1

        self.last_beat_at = now
 
        return self.current_beat

    def start(self):
        self.next_beat()
    
    # Time in beats, but not greater than current beat. No more than 5 decimal place precision
    def time(self):
        if self.current_beat is None:
            return None

        ungated_time = (((time.time() - self.last_beat_at) * 60) / float(self.bpm)) + self.current_beat

        # XXX: don't exceed counted beats
        return min(ungated_time, self.current_beat + 0.99999)

    def can_increment(self):
        return self.last_beat_at is None or time.time() - self.last_beat_at >= self.seconds_per_beat

    def next_beat(self):
        if self.can_increment():
            return self._increment_beat()

        return None

class PictureFrame(object):
    "A picture frame with lighting"

    __slots__ = ["red", "green", "blue", "uv", "white"]

    MAX_INTENSITY = 255
    MIN_INTENSITY = 0

    def __init__(self):
        self.red   = 0
        self.green = 0
        self.blue  = 0
        self.uv    = 0
        self.white = 0

    def increase_blue(self, intensity=1, ceiling=MAX_INTENSITY):
        "Increase the intensity of blue by the given intensity"
        result = self.blue + intensity
        if result > ceiling:
            self.blue = ceiling
            return False
        self.blue = result
        return True

    def decrease_blue(self, intensity=1, floor=MIN_INTENSITY):
        "Decrease the intensity of blue by the given intensity"
        result = self.blue - intensity
        if result < floor:
            self.blue = floor
            return False
        self.blue = result
        return True

class WiredPictureFrame(PictureFrame):
    "A picture frame with support for our protocol"

    __slots__ = ["address"]

    def __init__(self, address):
        self.address = address
        super(WiredPictureFrame, self).__init__()
    
    def lights_by_channel(self):
        "light intensities ordered by their corresponding channels on board"
        [self.red, self.green, self.blue, self.uv, self.white]

    def packet(self):
        return 'W' + str.join('', map(chr, [self.address] + self.lights_by_channel()))

class Storyboard(list):
    "A series of picture frames"

class WiredStoryboard(Storyboard):
    "A series of MAGICAL picture frames"

    def __init__(self, bus, frames):
        self.bus = bus
        super(WiredStoryboard, self).__init__(frames)

    def refresh_lighting(self):
        "Look at the lighting values of each picture_frame and send update accordingly"
        packets = [frame.packet() for frame in self.picture_frames]
        for ch in str.join('', packets):
            self.bus.write(ch)

    def receive_feedback(self, time_code):
        ""
        if self.bus.inWaiting() < 6:
            return None

        packet  = self.bus.read(6)
        command = packet[0]
        picture_frame = self.picture_frames[int(packet[1])]
        v1, v2, v3, v4 = map(int, packet[2:5])

        if command == "T":
            return Touch(picture_frame, v1, v2, v3, v4)

        return None

class Feedback(object):
    "Feedback from our audiance"

class Touch(Feedback):
    "Represents one of our picture_frames being touched"

    __slots__ = ["picture_frame", "up", "down", "left", "right"]

    def __init__(self, picture_frame, up, down, left, right):
        self.picture_frame = picture_frame
        self.up    = up
        self.down  = down
        self.left  = left
        self.right = right


if __name__ == "__main__":
    main()
