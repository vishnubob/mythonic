""" The mythonic-tech abstractions """

from pictureframe import PictureFrame
from storyboard   import Storyboard

class WiredStoryboard(Storyboard):
    "A storyboard with the electronic interface we designed"

    def __init__(self, bus, frames):
        self.bus = bus
        super(WiredStoryboard, self).__init__(frames)

    def refresh(self):
        self.refresh_lighting()

    def refresh_lighting(self):
        "Update lighting based on state of picture frames"
        picture_frames = sorted(self.picture_frames)
        packets = [frame.packet() for frame in self.picture_frames]
        # 'L' plus 140 byte string representing each level
        update = "L" + sr.join('', packets).ljust(140, chr(0))
        for ch in update
            self.bus.write(ch)

    def read_interaction(self, timestamp):
        "Returns an Interaction"
        if self.bus.inWaiting() < 6:
            return None

        packet  = self.bus.read(6)
        command = packet[0]
        if command not in ["T"]:
            print "WARNING! Received crap command: " + str(packet)
            return None
        picture_frame = self.picture_frames[int(packet[1])]
        v1, v2, v3, v4 = map(int, packet[2:5])

        if command == "T":
            return Touch(picture_frame, timestamp, v1, v2, v3, v4)

        return None

class WiredPictureFrame(PictureFrame):
    "A picture frame with support for our protocol"

    __slots__ = ["ordinal"]

    def __lt__(self, other):
        return self.ordinal < other.ordinal

    def __init__(self, ordinal):
        super(WiredPictureFrame, self).__init__()

        self.ordinal = ordinal 

    def light_update_packet(self):
        lights = [self.red, 0, self.green, self.blue, self.white, self.uv]
        return str.join('', map(chr, lights))
