#!/usr/bin/env python

import colorsys
import sys

import pygame

import biscuit
import ss
import pictureframe
import server

from music import make_looper

BOX_HEIGHT = 50
BOX_WIDTH = 100

def main():
    looper = make_looper(server.MIDI_TRACKS, server.MIDI_CLIENT, server.MIDI_PORT)
    picture_frames = server.PICTURE_FRAMES
    hc = PyGHardwareChain(len(picture_frames))
    manager = PyGManager(hc, pictureframe.Storyboard(picture_frames), looper)
    manager.run()

class PyGHardwareChain(biscuit.HardwareChain):

    def __init__(self, length):
        super(PyGHardwareChain, self).__init__(None, length)
        length = len(self.addresses)
        self._touched = [[False] * 4] * length
        self.screen = pygame.display.set_mode((BOX_WIDTH * 3, length * BOX_HEIGHT))
        pygame.display.flip()

    def draw_light(self, address, column, rgb):
        y = address * BOX_HEIGHT
        x = column * BOX_WIDTH
        pygame.draw.rect(self.screen, rgb, (x, y, BOX_WIDTH, BOX_HEIGHT))

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
        self._touched = [[False] * 4 for i in range(len(self.addresses))]
        return touched

class PyGManager(ss.SSManager):

    def pos_to_addr(self, pos):
         return int(pos[1]/float(BOX_HEIGHT))

    def think(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                addr = self.pos_to_addr(event.pos)
                self.hc._touched[addr][0] = True
        super(PyGManager, self).think()

if __name__ == "__main__":
    main()
