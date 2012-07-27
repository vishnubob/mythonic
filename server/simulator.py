#!/usr/bin/env python

import colorsys
import serial
import sys

import pygame

import biscuit
import manager
import mmath
import pictureframe
import server
import ss

from music import make_looper

BOX_HEIGHT = 50
BOX_WIDTH = 100

def main():
    midi_client = 14
    midi_port = 0
    port = serial.Serial(None, baudrate=1000000, bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=False, rtscts=False, dsrdtr=False)
    looper = make_looper(server.MIDI_TRACKS, midi_client, midi_port)
    picture_frames = server.PICTURE_FRAMES
    hc = PyGHardwareChain([port] * len(picture_frames), [pf.real_address for pf in picture_frames])
    sb = pictureframe.Storyboard(picture_frames, server.track_listing(server.MIDI_TRACKS))
    manager = PyGManager(hc, sb, looper)
    manager.run()

class PyGHardwareChain(biscuit.HardwareChain):

    def __init__(self, ports, addresses):
        super(PyGHardwareChain, self).__init__(ports, addresses)
        length = len(self.addresses)
        self._touched = [False] * length
        self.screen = pygame.display.set_mode((BOX_WIDTH * 3, length * BOX_HEIGHT))
        pygame.display.flip()

    def draw_light(self, address, column, rgb):
        y = address * BOX_HEIGHT
        x = column * BOX_WIDTH
        pygame.draw.rect(self.screen, rgb, (x, y, BOX_WIDTH, BOX_HEIGHT))

    #def set_light(self, addr_idx, color_idx, val):

    def send_light_data(self, address, light_data):
        ch = light_data.pages[light_data.page_idx]
        y = address * BOX_HEIGHT
        # RGB
        self.draw_light(address, 0, (ch[0], ch[2], ch[3]))
        # White
        self.draw_light(address, 1, (ch[4], ch[4], ch[4]))
        # UV
        purple_hsv = colorsys.rgb_to_hsv(170, 0, 250)
        uv_rgb = colorsys.hsv_to_rgb(purple_hsv[0], purple_hsv[1], ch[5])
        self.draw_light(address, 2, uv_rgb)
        # Update!
        pygame.display.update()

    # I coppied original refresh function, except for touch stuff
    def refresh(self):
        light_data = self.light_frames[self.frame_idx]
        light_data.go()
        self.frame_idx = (self.frame_idx + 1) % self.length

    def get_touch_triggers(self):
        touched = self._touched
        self._touched = [False] * len(self.addresses)
        return touched

class PyGManager(ss.SSManager):

    def __init__(self, hc, storyboard, looper):
        self.test_story = TestStory(storyboard)
        super(PyGManager, self).__init__(hc, storyboard, looper)

    def pos_to_addr(self, pos):
         return self.hc.addresses[int(pos[1]/float(BOX_HEIGHT))]

    def think(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                addr = self.pos_to_addr(event.pos)
                self.hc._touched[addr] = True
        super(PyGManager, self).think()

class TestStory(manager.Story):
    def setup(self, t):
        work_left = False
        for pf in self.storyboard:
            work_left |= pf.fade_rgb(t, 5, 0, 128, 128)
        return work_left

    def plot(self, t):
        work_left = False
        for pf in self.storyboard:
            work_left |= pf.fade_rgb(t, 5, 255, 255, 128)
        return work_left

    def teardown(self, t):
        work_left = False
        for pf in self.storyboard:
            work_left |= pf.fadeout(t, 5)
        return work_left

if __name__ == "__main__":
    main()
