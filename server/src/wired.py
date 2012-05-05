""" The mythonic-tech abstractions """

from pictureframe import PictureFrame
from mediator     import Mediator
from event        import Touch, LightChange

class WiredMediator(Mediator):
    "Mediator supporting interaction with serial picture frame protocol"

    def __init__(self, picture_frames, bus):
        self.bus = bus
        super(WiredMediator, self).__init__(picture_frames)

    def refresh_lighting(self):
        "Update lighting based on state of picture frames"
        picture_frames = sorted(self.picture_frames)
        packets = [frame.light_update_packet() for frame in self.picture_frames]
        # 'L' plus 140 byte string representing each level
        update = "L" + str.join('', packets).ljust(43, chr(0))
        for ch in update:
            self.bus.write(ch)

        print repr(update)

    def handle_event(self, event):
        "Handle LightChange events or pass through"
        if isinstance(event, LightChange):
            self.refresh_lighting()
            return True

        return super(WiredMediator, self).handle_event(event)

    def think(self):
        "Automatically read new events and delegate to handle_event"
        super(WiredMediator, self).think()

        event = self.read_event()
        if event is not None:
            self.handle_event(event)

    def read_event(self):
        "Returns an Event"
        if self.bus.inWaiting() < 6:
            return None

        packet  = self.bus.read(6)
        command = packet[0]
        if command not in ["T"]:
            print "WARNING! Received crap command: " + str(packet)
            return None
        picture_frame = self.picture_frames[int(packet[1])]
        v1, v2, v3, v4 = map(ord, packet[2:6])

        if command == "T":
            return Touch(picture_frame, v1, v2, v3, v4)

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
