from event import *
import time

class Mode(object):

    def __init__(self, picture_frames, mediator):
        self.picture_frames = picture_frames
        self.mediator = mediator
        self.last_started = None

    def get_time_passed(self):
        return time.time() - self.last_started
    time_passed = property(get_time_passed)

    def start(self):
        self.last_started = time.time()

    def handle_event(self, event):
        "handle a happening"

    def think(self):
        "modify picture frames produce events"

    def send_mediator(self, event):
        self.mediator.handle_event(event)
