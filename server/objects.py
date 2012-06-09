#!/usr/bin/env python

import sys
import time
import colorsys
import serial

class PictureFrame(object):
    LED_COUNT = 6
    MAX_LED_VAL = 0xFF
    MIN_LED_VAL = 0
    RED_CHANNEL = 0
    GREEN_CHANNEL = 2
    BLUE_CHANNEL = 3
    WHITE_CHANNEL = 4
    UV_CHANNEL = 5

    def __init__(self):
        self._leds = [0] * self.LED_COUNT

    def get_red(self): 
        return self._leds[self.RED_CHANNEL]
    def set_red(self, val):
        self._leds[self.RED_CHANNEL] = max(self.MIN_LED_VAL, min(self.MAX_LED_VAL, int(val)))
    red = property(get_red, set_red)

    def get_green(self): 
        return self._leds[self.GREEN_CHANNEL]
    def set_green(self, val):
        self._leds[self.GREEN_CHANNEL] = max(self.MIN_LED_VAL, min(self.MAX_LED_VAL, int(val)))
    green = property(get_green, set_green)
        
    def get_blue(self): 
        return self._leds[self.BLUE_CHANNEL]
    def set_blue(self, val):
        self._leds[self.BLUE_CHANNEL] = max(self.MIN_LED_VAL, min(self.MAX_LED_VAL, int(val)))
    blue = property(get_blue, set_blue)

    def get_white(self): 
        return self._leds[self.WHITE_CHANNEL]
    def set_white(self, val):
        self._leds[self.WHITE_CHANNEL] = max(self.MIN_LED_VAL, min(self.MAX_LED_VAL, int(val)))
    white = property(get_white, set_white)

    def get_uv(self): 
        return self._leds[self.UV_CHANNEL]
    def set_uv(self, val):
        self._leds[self.UV_CHANNEL] = max(self.MIN_LED_VAL, min(self.MAX_LED_VAL, int(val)))
    uv = property(get_uv, set_uv)

    def get_hsv(self):
        red = self.red / float(self.MAX_LED_VAL) 
        green = self.green / float(self.MAX_LED_VAL) 
        blue = self.blue / float(self.MAX_LED_VAL) 
        rgb = (red, green, blue)
        hsv = colorsys.rgb_to_hsv(*rgb)
        return hsv
    def set_hsv(self, hsv):
        rgb = colorsys.hsv_to_rgb(*hsv)
        self.red = self.MAX_LED_VAL * rgb[0]
        self.green = self.MAX_LED_VAL * rgb[1]
        self.blue = self.MAX_LED_VAL * rgb[2]
    hsv = property(get_hsv, set_hsv)

    def get_rgb(self):
        return (self.red, self.green, self.blue)
    def set_rgb(self, rgb):
        self.red = rgb[0]
        self.green = rgb[1]
        self.blue = rgb[2]

    rgb = property(get_rgb, set_rgb)
    def clear(self):
        self.rgb = (0, 0, 0)
        self.uv = 0
        self.white = 0

    def packet(self):
        return str.join('', map(chr, self._leds))

class Stage(list):
    def __init__(self, bus, *args):
        self.bus = bus
        super(Stage, self).__init__(*args)

    def refresh(self):
        data = 'L' + str.join('', [frame.packet() for frame in self])
        self.bus.flush()
        self.bus.write(data)

    def poll_input(self):
        if not self.bus.inWaiting():
            return

        ch = self.bus.read(1)
        if ch == 'T':
            channel = ord(self.bus.read(1))
            print "TOUCH", channel

        return None

class Effect(object):
    def __init__(self, stage):
        self.stage = stage

    def think(self):
        pass

class Rainbow(Effect):
    def __init__(self, *args):
        super(Rainbow).__init__(*args)
        self.ttl = 10
        self.slices = len(self.stage)
        self.subres = 25
        self.resolution = self.subres * self.slices
        self.clockhand = 0

    def think(self):
        self.clockhand += 1
        for (idx, frame) in enumerate(self.stage):
            hue = idx * self.subres + self.clockhand
            hue %= 1.0
            

class Factory(object):
    def __init__(self, frame_count, sbcls=None, sbcls_args=()):
        self.frame_count = frame_count
        self.sbcls = sbcls
        if self.sbcls == None:
            self.sbcls = Storyboard

    def build(self):
        sb = self.sbcls(*self.sbcls_args)
        for fc in range(frame_count):
            pf = PictureFrame()
            sb.append(pf)
        return sb

if __name__ == "__main__":
    bus = serial.Serial(sys.argv[1], 250000)
    Factory(7, WiredStoryboard, (bus, ))
    sb = Factory.build()
    sb[0].red = 0xff
    sb.refresh_lighting()
