import colorsys
import time

class PictureFrame(object):
    MAX_RED = 0xff
    MIN_RED = 0x0

    MAX_GREEN = 0xff
    MIN_GREEN = 0x0

    MAX_BLUE = 0xff
    MIN_BLUE = 0x0

    MAX_WHITE = 0xff
    MIN_WHITE = 0x0

    MAX_UV = 0xff
    MIN_UV = 0x0

    def __init__(self):
        self.red = self.MIN_RED
        self.green = self.MIN_GREEN
        self.blue = self.MIN_BLUE
        self.white = self.MIN_WHITE
        self.uv = self.MIN_UV
        self._touched = False
        self._active = False
        self.touch_history = []

    def color_property(color, minimum, maximum):
        """
        Creates a property instance for the given color
        with bounds checking on assignment.
        """
        attr = "_" + color
        def getcolor(self):
            return self.__dict__[attr]
        def setcolor(self, intensity):
            if intensity > maximum or intensity < minimum:
                raise ValueError(color + " intensity of " + str(intensity) + " is out of bounds.")
            self.__dict__[attr] = intensity
        return property(getcolor, setcolor)

    red = color_property("red", MIN_RED, MAX_RED)
    green = color_property("green", MIN_GREEN, MAX_GREEN)
    blue = color_property("blue", MIN_BLUE, MAX_BLUE)
    white = color_property("white", MIN_WHITE, MAX_WHITE)
    uv = color_property("uv", MIN_UV, MAX_UV)

    def touch(self):
        self.touch_history.append(time.time())
        if self.active:
            self.deactivate()
        else:
            self.activate()
        self._touched = True
    touched = property(lambda self: self._touched)

    def activate(self):
        self._active = True
    def deactivate(self):
        self._active = False
    active = property(lambda self: self._active)

    @property
    def hsv(self):
        red = max(self.MIN_RED, self.red / float(self.MAX_RED))
        green = max(self.MIN_GREEN, self.green / float(self.MAX_GREEN))
        blue = max(self.MIN_BLUE, self.blue / float(self.MAX_BLUE))
        return colorsys.rgb_to_hsv(red, green, blue)
    @hsv.setter
    def hsv(self, hsv):
        rgb = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])
        self.red = int(rgb[0] * self.MAX_RED)
        self.green = int(rgb[1] * self.MAX_GREEN)
        self.blue = int(rgb[2] * self.MAX_BLUE)

    def blackout(self):
        self.red = self.MIN_RED
        self.green = self.MIN_GREEN
        self.blue = self.MIN_BLUE
        self.uv = self.MIN_UV
        self.white = self.MIN_WHITE

class MusicalPictureFrame(PictureFrame):
    def __init__(self, looper, tracks):
        self.tracks = tracks 
        super(MusicalPictureFrame, self).__init__()

    def stop_tracks(self, only_these=None):
        if only_these is None:
            only_these = self.tracks
        for track in only_these:
            if self.looper.tracks[track] in self.looper.now_playing:
                self.looper.stop(track)

    def play_tracks(self, only_these=None):
        if only_these is None:
            only_these = self.tracks
        for track in only_these:
            if self.looper.tracks[track] in self.looper.now_playing:
                continue
            self.looper.play(track)

