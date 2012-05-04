from spectacle import Repeat

class Interaction(object):
    "Interaction with a picture frame"

    __slots__ = ["picture_frame", "time_code"]

    def __init__(self, picture_frame, time_code):
        self.picture_frame = origin
        self.time_code     = time_code

class Touch(Interaction):
    "Represents a picture frame being touched"

    __slots__ = ["up", "down", "left", "right"]

    def __init__(self, picture_frame, time_code, up, down, left, right):
        super(Touch, self).__init__(picture_frame, time_code)

        self.up    = up
        self.down  = down
        self.left  = left
        self.right = right

# see mythonic.py for wired version
class PictureFrame(object):
    "A picture frame with lighting"

    __slots__ = ["_red", "_green", "_blue", "_uv", "_white"]

    MAX_RED = 0xff 
    MIN_RED = 0x0

    MAX_GREEN = 0xff
    MIN_GREEN = 0x0

    MAX_BLUE = 0xff
    MIN_BLUE = 0x0

    MAX_UV = 0xff
    MIN_UV = 0x0

    MAX_WHITE = 0xff
    MIN_WHITE = 0x0

    MAX_HUE        = max(MAX_RED, MAX_GREEN, MAX_BLUE)
    MAX_VALUE      = max(MAX_RED, MAX_GREEN, MAX_BLUE)
    MAX_SATURATION = max(MAX_RED, MAX_GREEN, MAX_BLUE)

    def __init__(self):
        self._red   = 0
        self._green = 0
        self._blue  = 0
        self._uv    = 0
        self._white = 0

    def get_red(self):
        return self._red;
    def set_red(self, intensity):
        if intensity > self.MAX_RED or intensity < self.MIN_RED:
            raise ValueError("Exceeds maximum red intensity")
        self._red = intensity
    red = property(get_red, set_red)

    def get_green(self):
        return self._green;
    def set_green(self, intensity):
        if intensity > self.MAX_GREEN or intensity < self.MIN_GREEN:
            raise ValueError("Exceeds maximum green intensity")
        self._green = intensity
    green = property(get_green, set_green)

    def get_blue(self):
        return self._blue;
    def set_blue(self, intensity):
        if intensity > self.MAX_BLUE or intensity < self.MIN_BLUE:
            raise ValueError("Exceeds maximum blue intensity")
        self._blue = intensity
    blue = property(get_blue, set_blue)

    def get_uv(self):
        return self._uv;
    def set_uv(self, intensity):
        if intensity > self.MAX_UV or intensity < self.MIN_UV:
            raise ValueError("Exceeds maximum UV intensity")
        self._uv = intensity
    uv = property(get_uv, set_uv)

    def get_white(self):
        return self._white;
    def set_white(self, intensity):
        if intensity > self.MAX_WHITE or intensity < self.MIN_WHITE:
            raise ValueError("Exceeds maximum white intensity")
        self._white = intensity
    white = property(get_white, set_white)

    def increase_all(self, increase=1, ceiling=max(MAX_RED, MAX_GREEN, MAX_BLUE)):
        return self.increase_red(increase, ceiling) and \
            self.increase_green(increase, ceiling)  and \
            self.increase_blue(increase, ceiling)   and \
            self.increase_uv(increase, ceiling)     and \
            self.increase_white(increase, ceiling)

    def decrease_all(self, decrease=1, floor=min(MIN_RED, MIN_GREEN, MIN_BLUE)):
        return self.decrease_red(decrease, floor) and \
            self.decrease_green(decrease, floor)  and \
            self.decrease_blue(decrease, floor)   and \
            self.decrease_uv(decrease, floor)     and \
            self.decrease_white(decrease, floor)

    def increase_red(self, increase=1, ceiling=MAX_RED):
        return self._increase_or_ceiling(self.get_red, self.set_red, increase, ceiling)
    def decrease_red(self, decrease=1, floor=MIN_RED):
        return self._decrease_or_floor(self.get_red, self.set_red, decrease, floor)

    def increase_green(self, increase=1, ceiling=MAX_GREEN):
        return self._increase_or_ceiling(self.get_green, self.set_green, increase, ceiling)
    def decrease_green(self, decrease=1, floor=MIN_GREEN):
        return self._decrease_or_floor(self.get_green, self.set_green, decrease, floor)

    def increase_blue(self, increase=1, ceiling=MAX_BLUE):
        return self._increase_or_ceiling(self.get_blue, self.set_blue, increase, ceiling)
    def decrease_blue(self, decrease=1, floor=MIN_BLUE):
        return self._decrease_or_floor(self.get_blue, self.set_blue, decrease, floor)

    def increase_uv(self, increase=1, ceiling=MAX_UV):
        return self._increase_or_ceiling(self.get_uv, self.set_uv, increase, ceiling)
    def decrease_uv(self, decrease=1, floor=MIN_UV):
        return self._decrease_or_floor(self.get_uv, self.set_uv, decrease, floor)

    def increase_white(self, increase=1, ceiling=MAX_WHITE):
        return self._increase_or_ceiling(self.get_white, self.set_white, increase, ceiling)
    def decrease_white(self, decrease=1, floor=MIN_WHITE):
        return self._decrease_or_floor(self.get_white, self.set_white, decrease, floor)

    def _increase_or_ceiling(self, get_light, set_light, increase, ceiling):
        "Increase the intensity of the given light by the given intensity"
        intensity = get_light() + increase
        if intensity > ceiling:
            set_light(ceiling)
            return False
        set_light(intensity)
        return True

    def _decrease_or_floor(self, get_light, set_light, decrease, floor):
        "Decrease the intensity of the given light by the given intensity"
        intensity = get_light() + decrease
        if intensity < floor:
            set_light(floor)
            return False
        set_light(intensity)
        return True

#
# Spectacle specific to picture frames
#
#class Fade(Repeat)
class FadeBlack(Repeat):
    def __init__(self, picture_frame, duration):
        p = picture_frame
        brightest = max(p.red, p.green, p.blue, p.uv, p.white)
        super(FadeBlack, self).__init__(p.decrease_all, brightest, duration)
