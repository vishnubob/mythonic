import sys

import biscuit
import pygame

import mythonic
import ss

screen = pygame.display.set_mode((640, 480)) #make screen

pygame.display.flip()

class SimulatedHC(object):
    _touched = False
    ch = [0, 0, 0, 0, 0, 0]

    def set_light(self, addr, idx, x):
        ch = self.ch
        ch[idx] = x
        pygame.draw.rect(screen, (ch[0], ch[2], ch[3]), (50, 50, 100, 100))
        pygame.display.update()

    def get_touch_triggers(self):
        touched = self._touched
        self._touched = False
        return [[touched] * 4]

picture_frames = [ss.SSPictureFrame()]
effects_manager = ss.SSManager(picture_frames, [], None)
hc = SimulatedHC()
manager = mythonic.DelegationManager(hc, effects_manager)

while True:
    manager.think()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            hc._touched = True
