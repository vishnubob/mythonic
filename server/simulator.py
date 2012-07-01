import colorsys
import sys

import biscuit
import pygame

from manager import Coordinator
from music import make_looper
import ss

TEST_TRACK = "../music_raw/dewb_4bar/8 bar dance.mid"

screen = pygame.display.set_mode((640, 480)) #make screen

pygame.display.flip()

class SimulatedHC(object):
    _touched = False
    ch = [0, 0, 0, 0, 0, 0]

    def set_light(self, addr, idx, x):
        ch = self.ch
        ch[idx] = x
        pygame.draw.rect(screen, (ch[0], ch[2], ch[3]), (0, 0, 100, 100))
        pygame.draw.rect(screen, (ch[4], ch[4], ch[4]), (100, 0, 100, 100))
        purple_hsv = colorsys.rgb_to_hsv(170, 0, 250)
        uv_rgb = colorsys.hsv_to_rgb(purple_hsv[0], purple_hsv[1], ch[5])
        pygame.draw.rect(screen, uv_rgb, (200, 0, 100, 100))
        pygame.display.update()

    def get_touch_triggers(self):
        touched = self._touched
        self._touched = False
        return [[touched] * 4]

looper = make_looper([TEST_TRACK], 128, 0)
picture_frames = [ss.SSPictureFrame(looper, [0])]
patterns = []
#patterns = [[picture_frames[0]]]
effects_manager = ss.SSManager(picture_frames, patterns, None)
hc = SimulatedHC()
manager = Coordinator(hc, effects_manager)

while True:
    manager.think()
    looper.think()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            hc._touched = True
