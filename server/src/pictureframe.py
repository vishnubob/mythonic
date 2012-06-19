import colorsys

from biscuit import FrameLights

class PictureFrame(object):
    """
    A picture frame with lighting a touch sensitivity.
    """

    MAX_RED = 0xff
    MIN_RED = 0x0
    RED_IDX = 0

    MAX_GREEN = 0xff
    MIN_GREEN = 0x0
    GREEN_IDX = 2

    MAX_BLUE = 0xff
    MIN_BLUE = 0x0
    BLUE_IDX = 3

    MAX_WHITE = 0xff
    MIN_WHITE = 0x0
    WHITE_IDX = 4

    MAX_UV = 0xff
    MIN_UV = 0x0
    UV_IDX = 5

    def __init__(self, address, hc, track):
       self.address = address
       self.hc = hc
       self.track = track

    def __str__(self):
        return "PictureFrame(addr={0}, red={1}, green={2}, blue={3}, uv={4}, white={5})".format(
            self.address, self.red, self.green, self.blue, self.uv, self.white)

    def get_red(self):
        return self.hc.get_light(self.address, self.RED_IDX)
    def set_red(self, intensity):
        if intensity > self.MAX_RED or intensity < self.MIN_RED:
            raise ValueError("red intensity " + str(intensity) + " is out of bounds")
        self.hc.set_light(self.address, self.RED_IDX, intensity)
    red = property(get_red, set_red)

    def get_green(self):
        return self.hc.get_light(self.address, self.GREEN_IDX)
    def set_green(self, intensity):
        if intensity > self.MAX_GREEN or intensity < self.MIN_GREEN:
            raise ValueError("green intensity " + str(intensity) + " is out of bounds")
        self.hc.set_light(self.address, self.GREEN_IDX, intensity)
    green = property(get_green, set_green)

    def get_blue(self):
        return self.hc.get_light(self.address, self.BLUE_IDX)
    def set_blue(self, intensity):
        if intensity > self.MAX_BLUE or intensity < self.MIN_BLUE:
            raise ValueError("blue intensity " + str(intensity) + " is out of bounds")
        self.hc.set_light(self.address, self.BLUE_IDX, intensity)
    blue = property(get_blue, set_blue)

    def get_white(self):
        return self.hc.get_light(self.address, self.WHITE_IDX)
    def set_white(self, intensity):
        if intensity > self.MAX_WHITE or intensity < self.MIN_WHITE:
            raise ValueError("white intensity " + str(intensity) + " is out of bounds")
        self.hc.set_light(self.address, self.WHITE_IDX, intensity)
    white = property(get_white, set_white)

    def get_uv(self):
        return self.hc.get_light(self.address, self.UV_IDX)
    def set_uv(self, intensity):
        if intensity > self.MAX_UV or intensity < self.MIN_UV:
            raise ValueError("uv intensity " + str(intensity) + " is out of bounds")
        self.hc.set_light(self.address, self.UV_IDX, intensity)
    uv = property(get_uv, set_uv)

    def blackout(self):
        self.set_red(self.MIN_RED)
        self.set_green(self.MIN_GREEN)
        self.set_blue(self.MIN_BLUE)
        self.set_uv(self.MIN_UV)
        self.set_white(self.MIN_WHITE)
