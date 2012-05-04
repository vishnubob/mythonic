#!/usr/bin/env python

import sys
import time
import serial
import midi
import midi.sequencer

def main():
    if len(sys.argv) != 4:
        script_name = sys.argv[0]
        print "Usage:   {0} <midi light client> <music client:port> <tty>".format(sys.argv[0])
        print "Example: {0} 129 128:0 /dev/ttyUSB0".format(sys.argv[0])
        exit(2)

    script_name, control_client, music_client_port, tty = sys.argv
    music_client, music_port = map(int, music_client_port.split(":"))
    
    # The personale running the show
    music_conductor = MusicConductor(music_client, music_port)
    light_conductor = LightConductor(light_client)
    director        = Director([music_conductor, light_conductor])

    # Create a stage with one picture_frame
    stage = Stage(tty, 1)

    # Start the mainloop. Time codes are worth 1/4th a second
    director.direct(stage, 0.25)

class PictureFrame(object):
    "A picture frame with lighting"

    __slots__ = ["red", "green", "blue", "uv", "white"]

    def __init__(self):
        self.address = address
        self.last_touched = None

class WiredPictureFrame(PictureFrame):
    "A picture frame with support for our protocol"

    def __init__(self, address):
        self.address = address
    
    def lights_by_channel(self):
        "light intensities ordered by their corresponding channels on board"
        [self.red, self.green, self.blue, self.uv, self.white]

    def packet(self):
        return 'W' + str.join('', map(chr, [self.address] + self.lights_by_channel()))

class Storyboard(list):
    "A series of picture frames"

class WiredStoryboard(Storyboard):
    "A series of MAGICAL picture frames"

    def __init__(self, bus, frames):
        self.bus = bus
        super(WiredStoryboard, self).__init__(frames)

    def refresh_lighting(self):
        "Look at the lighting values of each picture_frame and send update accordingly"
        packets = [frame.packet() for frame in self.picture_frames]
        for ch in str.join('', packets):
            self.bus.write(ch)

    def receive_feedback(self, time_code):
        ""
        if self.bus.inWaiting() < 6:
            return None

        packet  = self.bus.read(6)
        command = packet[0]
        picture_frame = self.picture_frames[int(packet[1])]
        v1, v2, v3, v4 = map(int, packet[2:5])

        if command == "T":
            picture_frame.last_touched = time_code
            return Touch(picture_frame, v1, v2, v3, v4)

        return None

class Feedback(object):
    "Feedback from our audiance/stage"

class Touch(Feedback):
    "Represents one of our picture_frames being touched"

    __slots__ = ["picture_frame", "up", "down", "left", "right"]

    def __init__(self, picture_frame, up, down, left, right):
        self.picture_frame = picture_frame
        self.up    = up
        self.down  = down
        self.left  = left
        self.right = right

class Director(object):

    def __init__(self, conductors):
        self._conductors = conductors

    def direct(self, stage, period_size):
        "mainloop. Notifies conductors of feedback and time changes"
        time_code = 1
        last_update = time.time()
        while True:
            if time.time() - time.last_update >= period_size:
                time_code = time_code + 1
                for conductor in self.conductors:
                    conductor.conduct(stage, time_code)
            
            feedback = stage.next_feedback()
            if not feedback is None:
                for conductor in self.conductors:
                    conductor.react(stage, time_code, feedback)

class Conductor(object):

    def react(self, stage, feedback):
        "based on feedback, conduct the minions"

    def conduct(self, stage, time_code):
        "conduct the minions in a way appropriate to the timecode"

class MusicConductor(Conductor):
    
    def __init__(self, midi_client, midi_port):
        seq = midi.sequencer.SequencerWrite(sequencer_resolution=120)
        seq.subscribe_port(midi_client, midi_port)
        seq.start_sequencer()
        self._music_seq = seq

    def conduct(self, stage, time_code, time_change):
        "sends scheduled music to our synth"

    def react(self, stage, time_code, feedback):
        "schedules music or reacts immediately to feedback"

class LightConductor(Conductor):
    
    def __init__(self, light_seq, serial_handle):
        self._serial_handle = serial_handle
        self._light_handle  = light_handle

    def conduct(self, stage, time_code):
        "updates the lighting values of our picture_frames then refreshes."
        stage.refresh_lighting()

    def react(self, stage, time_code, feedback):
        "reacts to feedback"

if __name__ == "__main__":
    main()
