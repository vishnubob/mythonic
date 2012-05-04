#!/usr/bin/env python

import sys
import time
import serial
import midi
import midi.sequencer

def main():

    if len(sys.argv) != 2:
        script_name = sys.argv[0]
        print "Usage:   {0} <tty>".format(sys.argv[0])
        print "Example: {0} /dev/ttyUSB0".format(sys.argv[0])
        exit(2)

    tty = sys.argv[1]

    bus = serial.Serial(tty)
    storyboard = WiredStoryboard(bus, [WiredPictureFrame(i) for i in range(7)])

    metranome = Metranome(120)

    while True:
        beat = metranome.next_beat()
        if beat is not None:
            print beat


class Metranome(object):

    def __init__(self, bpm):
        self.bpm = bpm
        self.last_beat_at = None
        self.current_beat = None

    def get_seconds_per_beat(self):
        return self.bpm / 60.0

    seconds_per_beat = property(get_seconds_per_beat)

    def _increment_beat(self, now):
        if self.current_beat is None:
            self.current_beat = 1
        else:
            self.current_beat = self.current_beat + 1

        self.last_beat_at = now

        return self.current_beat

    def next_beat(self):
        now = time.time()

        if self.last_beat_at is None:
            return self._increment_beat(now)

        if now - self.last_beat_at >= self.seconds_per_beat:
            return self._increment_beat(now)
            
        return None

class PictureFrame(object):
    "A picture frame with lighting"

    __slots__ = ["red", "green", "blue", "uv", "white"]

    def __init__(self, address):
        self.address = address
        self.last_touched = None

class WiredPictureFrame(PictureFrame):
    "A picture frame with support for our protocol"

    def __init__(self, address):
        self.address = address
    
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
            picture_frame.last_touched = time_code
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
