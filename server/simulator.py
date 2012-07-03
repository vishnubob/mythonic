#!/usr/bin/env python

import colorsys
import sys

import biscuit
import pygame

from manager import Coordinator
from music import make_looper
from biscuit import HardwareChain
import ss

TEST_TRACK = "../music_raw/music_test/reasonable_test_2.mid"
BOX_HEIGHT = 100
BOX_WIDTH = 100
FRAME_COUNT = 3

screen = pygame.display.set_mode((BOX_WIDTH * 3, FRAME_COUNT * BOX_HEIGHT)) #make screen

pygame.display.flip()

class PyGHardwareChain(HardwareChain):

    def __init__(self, length):
        super(PyGHardwareChain, self).__init__(None, length)
        self._touched = [[False] * 4] * FRAME_COUNT

    def draw_light(self, address, column, rgb):
        y = address * BOX_HEIGHT
        x = column * BOX_WIDTH
        pygame.draw.rect(screen, rgb, (x, y, BOX_WIDTH, BOX_HEIGHT))

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

    # I copy&paste refresh, except for touch stuff
    def refresh(self):
        light_data = self.light_frames[self.frame_idx]
        light_data.go()
        self.frame_idx = (self.frame_idx + 1) % self.length

    def get_touch_triggers(self):
        touched = self._touched
        self._touched = [[False] * 4 for i in range(len(self.addresses))]
        return touched

class PyGCoordinator(Coordinator):

    def pos_to_addr(self, pos):
         return int(pos[1]/float(BOX_HEIGHT))

    def think(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                addr = self.pos_to_addr(event.pos)
                self.hc._touched[addr][0] = True
                print "Clicked", addr
        super(PyGCoordinator, self).think()

looper = make_looper([TEST_TRACK], 128, 0)
picture_frames = [ss.SSPictureFrame(looper) for i in range(FRAME_COUNT)]
patterns = []
#patterns = [[picture_frames[0]]]
effects_manager = ss.SSManager(picture_frames, patterns)
hc = PyGHardwareChain(FRAME_COUNT)
manager = PyGCoordinator(hc, effects_manager)
manager.run()
