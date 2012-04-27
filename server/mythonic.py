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

    script_name, light_client, music_client_port, tty = sys.argv
    music_client, music_port = map(int, music_client_port.split(":"))
    
    # The personal running the show
    music_conductor = MusicConductor(music_client, music_port)
    light_conductor = LightConductor(light_client)
    director        = Director([music_conductor, light_conductor])

    # Create a stage with one box
    stage = Stage(tty, 1)

    # Start the mainloop. Time codes are worth 1/4th a second
    director.direct(stage, 0.25)

class Stage(object):
    "contains state information regarding the boxes and provides communication"

    def __init__(self, bus, box_count):
        self.bus = serial.Serial(bus)
        self.boxes = [Box(i) for i in range(box_count)]

    def refresh(self):
        self.refresh_lighting()

    def refresh_lighting(self):
        "Look at the lighting values of each box and send update accordingly"
        packets = []
        for i, box in enumerate(self.boxes):
            packets.append('W' + str.join('', map(chr, [i] + box.lights)))

        for ch in str.join('', packets):
            self.bus.write(ch)

    def next_feedback(self, time_code):
        "Process the next command should it exist."
        if self.bus.inWaiting() < 6:
            return None

        packet  = self.bus.read(6)
        command = packet[0]
        box     = self.boxes[int(packet[1])]
        v1, v2, v3, v4 = map(int, packet[2:5])

        if command == "T":
            box.last_touched = time_code
            return Touch(box, v1, v2, v3, v4)

        return None

class Feedback(object):
    "Feedback from our audiance/stage"

class Touch(Feedback):
    "Represents one of our boxes being touched"

    __slots__ = ["box", "up", "down", "left", "right"]

    def __init__(self, box, up, down, left, right):
        self.box   = box
        self.up    = up
        self.down  = down
        self.left  = left
        self.right = right

class Box(object):
    __slots__ = ["address", "last_touched"]

    def __init__(self, address):
        self.address = address
        self.last_touched = None

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

    def react(self, stage, time_code, feedback):
        "based on feedback, conduct the minions"

    def conduct(self, stage, time_code):
        "conduct the minions in away appropriate to the timecode"

class MusicConductor(Conductor):
    
    def __init__(self, midi_client, midi_port):
        seq = midi.sequencer.SequencerWrite(sequencer_resolution=120)
        seq.subscribe_port(midi_client, midi_port)
        seq.start_sequencer()
        self._music_seq = seq

    def conduct(self, stage, time_code):
        "sends scheduled music to our synth"

    def react(self, stage, time_code, feedback):
        "schedules music or reacts immediately to feedback"

class LightConductor(Conductor):
    
    def __init__(self, light_seq, serial_handle):
        self._serial_handle = serial_handle
        self._light_handle  = light_handle

    def conduct(self, stage, time_code):
        "updates the lighting values of our boxes then refreshes."
        stage.refresh_lighting()

    def react(self, stage, time_code, feedback):
        "reacts to feedback"

if __name__ == "__main__":
    main()
