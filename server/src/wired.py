""" The mythonic-tech abstractions """

from pictureframe import PictureFrame
from storyboard   import Storyboard

class WiredStoryboard(Storyboard):
    "A series of MAGICAL picture frames"

    def __init__(self, bus, frames):
        self.bus = bus
        super(WiredStoryboard, self).__init__(frames)

    def refresh_lighting(self):
        "Update lighting based on state of picture frames"
        packets = [frame.packet() for frame in self.picture_frames]
        for ch in str.join('', packets):
            self.bus.write(ch)

    def read_event(self, time_code):
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
            return Touch(picture_frame, time_code, v1, v2, v3, v4)

        return None

class WiredPictureFrame(PictureFrame):
    "A picture frame with support for our protocol"

    __slots__ = ["address"]

    def __init__(self, address):
        super(WiredPictureFrame, self).__init__()
        self.address = address

    def lights_by_channel(self):
        "light intensities ordered by their corresponding channels on board"
        return [self.red, self.green, self.blue, self.uv, self.white]

    def packet(self):
        return 'W' + str.join('', map(chr, [self.address] + self.lights_by_channel()))

