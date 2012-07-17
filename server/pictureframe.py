import colorsys
import time

import mmath

class Storyboard(list):
    """
    A container for picture frames and patterns with convenience
    methods for inspecting both.
    """
    def __init__(self, picture_frames, patterns):
        for pattern in patterns:
            for idx, pf_or_idx in enumerate(pattern):
                if not isinstance(pf_or_idx, PictureFrame):
                    pattern[idx] = picture_frames[pf_or_idx]
        self.patterns = patterns
        self.initialized_at = time.time()
        super(Storyboard, self).__init__(picture_frames)

    @property
    def touched_frames(self):
        return filter(lambda pf: pf.touched, self)

    @property
    def active_frames(self):
        return filter(lambda pf: pf.active, self)

    @property
    def untouched_for(self):
        """
        Number of seconds since creation we have gone without a touch
        """
        most_recent = self.initialized_at
        for history in [pf.touch_history for pf in self]:
            most_recent = max(history + [most_recent])
        return time.time() - most_recent

    @property
    def pattern_complete(self):
        return self.active_frames == self.target_pattern

    @property
    def target_pattern(self):
        """
        To be the "target pattern"
          1. all active frames must be within the pattern
          2. the  start of pattern must be an active frame
        """
        for pattern in self.patterns:
            if set(self.active_frames).issubset(set(pattern)):
                return pattern
        return None

    def in_target_pattern(self, pf):
        return self.target_pattern is not None and pf in self.target_pattern

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
        providing bound checking and history recording.
        """
        color_attr = "_" + color
        def set_color(self, intensity):
            if intensity > maximum or intensity < minimum:
                raise ValueError(color + " intensity of " + str(intensity) + " is out of bounds.")
            setattr(self, color_attr, intensity)
        return property(lambda self: getattr(self, color_attr), set_color)

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

    def untouch(self):
        self._touched = False

    touched = property(lambda self: self._touched)

    def activate(self):
        self._active = True

    def deactivate(self):
        self._active = False
        self.blackout()

    active = property(lambda self: self._active)

    def cycle_hue(self, t, rate, saturation, value):
        """
        Rotate hue while maintaining saturation and value.

        rate is revolutions a second
        """
        hue = mmath.segment(t, rate, 0, 1)
        self.hsv = (hue, saturation, value)

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

    def fadeout(self):
        self.red = max(self.red - 1, self.MIN_RED)
        self.green = max(self.green - 1, self.MIN_GREEN)
        self.blue = max(self.blue - 1, self.MIN_BLUE)
        self.uv = max(self.uv - 1, self.MIN_UV)
        self.white = max(self.white - 1, self.MIN_WHITE)
        work_left = [
            self.red > self.MIN_RED,
            self.green > self.MIN_GREEN,
            self.blue > self.MIN_BLUE,
            self.uv > self.MIN_UV,
            self.white > self.MIN_WHITE,
        ]
        return reduce(lambda a, b: a or b, work_left)

class MusicalPictureFrame(PictureFrame):
    def __init__(self, looper, tracks):
        self.tracks = tracks
        super(MusicalPictureFrame, self).__init__()

    def deactivate(self):
        self.stop_tracks()
        super(MusicalPictureFrame, self).deactivate()

    def stop_tracks(self, only_these=None):
        if only_these is None:
            only_these = self.tracks
        for track in only_these:
            if self.looper.tracks[track].playing:
                self.looper.stop(track)

    def play_tracks(self, only_these=None):
        if only_these is None:
            only_these = self.tracks
        for track in only_these:
            if self.looper.tracks[track].playing:
                continue
            self.looper.play(track)
