import colorsys

from biscuit import FrameLights

class PictureFrame(object):
    "A picture frame with lighting"

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

    def __init__(self, address, hc):
       self.lights = FrameLights(address, hc)

    def get_red(self):
        return self.lights.get_light(0)
    def set_red(self, intensity):
        if intensity > self.MAX_RED or intensity < self.MIN_RED:
            raise ValueError("red intensity " + str(intensity) + " is out of bounds")
        self.lights.set_light(0, intensity)
    red = property(get_red, set_red)

    def get_green(self):
        return self.lights.get_light(1)
    def set_green(self, intensity):
        if intensity > self.MAX_GREEN or intensity < self.MIN_GREEN:
            raise ValueError("green intensity " + str(intensity) + " is out of bounds")
        self.lights.set_light(1, intensity)
    green = property(get_green, set_green)

    def get_blue(self):
        return self.lights.get_light(2)
    def set_blue(self, intensity):
        if intensity > self.MAX_BLUE or intensity < self.MIN_BLUE:
            raise ValueError("blue intensity " + str(intensity) + " is out of bounds")
        self.lights.set_light(2, intensity)
    blue = property(get_blue, set_blue)

    def get_uv(self):
        return self.lights.get_light(3)
    def set_uv(self, intensity):
        if intensity > self.MAX_UV or intensity < self.MIN_UV:
            raise ValueError("uv intensity " + str(intensity) + " is out of bounds")
        self.lights.set_light(3, intensity)
    uv = property(get_uv, set_uv)

    def get_white(self):
        return self.lights.get_light(4)
    def set_white(self, intensity):
        if intensity > self.MAX_WHITE or intensity < self.MIN_WHITE:
            raise ValueError("white intensity " + str(intensity) + " is out of bounds")
        self.lights.set_light(4, intensity)
    white = property(get_white, set_white)

    def blackout(self):
        self.set_red(self.MIN_RED)
        self.set_green(self.MIN_GREEN)
        self.set_blue(self.MIN_BLUE)
        self.set_uv(self.MIN_UV)
        self.set_white(self.MIN_WHITE)
