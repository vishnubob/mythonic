import colorsys
import random
import time

import mmath

class Pattern(list):
    def __init__(self, picture_frames, triggered_story):
        self.triggered_story = triggered_story
        super(Pattern, self).__init__(picture_frames)

class Storyboard(list):
    """
    A container for picture frames and patterns with convenience
    methods for inspecting both.
    """
    def __init__(self, picture_frames, patterns=[]):
        for pattern in patterns:
            for pf in pattern:
                if pf not in picture_frames:
                    raise ValueError("Picture frames in arg 'patterns' must exist in arg 'picture_frames'")
        self.patterns = patterns
        self.initialized_at = time.time()
        super(Storyboard, self).__init__(picture_frames)

    @property
    def touched_frames(self):
        return [pf for pf in self if pf.touched]

    @property
    def touched(self):
        return len(self.touched_frames) > 0

    @property
    def active_frames(self):
        return [pf for pf in self if pf.active]

    @property
    def untouched_for(self):
        """
        Number of seconds since creation we have gone without a touch
        """
        return time.time() - self.untouched_since

    @property
    def untouched_since(self):
        most_recent = self.initialized_at
        for history in [pf.touch_history for pf in self]:
            most_recent = max(history + [most_recent])
        return most_recent

    @property
    def pattern_complete(self):
        if self.target_pattern is None:
            return False
        return set(self.active_frames) == set(self.target_pattern)

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

    def __init__(self, human_address):
        self.human_address = human_address
        self.red = self.MIN_RED
        self.green = self.MIN_GREEN
        self.blue = self.MIN_BLUE
        self.white = self.MIN_WHITE
        self.uv = self.MIN_UV
        self._touched = False
        self._active = False
        self.touch_history = []
        self.fades = {}

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

    @property
    def real_address(self):
        return self.human_address - 1

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

    active = property(lambda self: self._active)

    @property
    def rgb(self):
        return (self.red, self.green, self.blue)

    @rgb.setter
    def rgb(self, rgb):
        self.red = rgb[0]
        self.green = rgb[1]
        self.blue = rgb[2]

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

    @property
    def brightness(self):
        return self.hsv[2]

    @brightness.setter
    def brightness(self, brightness):
        self.hsv = (self.hsv[0], self.hsv[1], brightness)

    def blackout(self):
        self.brightness = 0
        self.uv = 0
        self.white = self.MIN_WHITE

    def randomize_hsv(self, hue=None, saturation=None, brightness=None):
        attribs = [hue, saturation, brightness]
        hsv = [random.random() if x is None else x for x in attribs]
        self.hsv = tuple(hsv)

    def fade_color(self, t, span, color, target):
        fade = Fade(span, getattr(self, color), target)
        if color not in self.fades or fade != self.fades[color]:
            self.fades[color] = fade
        else:
            fade = self.fades[color]
        setattr(self, color, fade.calc(t))
        return getattr(self, color) != target

    def fade_red(self, t, span, target):
        return self.fade_color(t, span, "red", target)

    def fade_green(self, t, span, target):
        return self.fade_color(t, span, "green", target)

    def fade_blue(self, t, span, target):
        return self.fade_color(t, span, "blue", target)

    def fade_rgb(self, t, span, red, green, blue):
        work_left = False
        work_left |= self.fade_red(t, span, red)
        work_left |= self.fade_green(t, span, green)
        work_left |= self.fade_blue(t, span, blue)
        return work_left

    def fade_uv(self, t, span, target):
        return self.fade_color(t, span, "uv", target)

    def fade_white(self, t, span, target):
        return self.fade_color(t, span, "white", target)

    def fadeout(self, t, span):
        work_left = False
        work_left |= self.fade_rgb(t, span, self.MIN_RED, self.MIN_GREEN, self.MIN_BLUE)
        work_left |= self.fade_uv(t, span, self.MIN_UV)
        work_left |= self.fade_white(t, span, self.MIN_WHITE)
        return work_left

class Fade(object):
    def __init__(self, span, original_value, target_value):
        self.span = span
        self.original_value = original_value
        self.target_value = target_value
        self.last_value = original_value

    def calc(self, t):
        assert(self.span == 5)
        value = mmath.travel(t, self.span, self.original_value, self.target_value)
        self.last_value = value
        return value

    def __ne__(self, other):
        return not self == other

    def __eq__(self, other):
        return other.span == self.span and other.target_value == self.target_value
