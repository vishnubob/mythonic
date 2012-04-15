#!/usr/bin/env python

import sys
import serial
import time
import midi
import midi.sequencer
import math

def main():
    if len(sys.argv) != 4:
        script_name = sys.argv[0]
        print "Usage:   {0} <midi client> <midi port> <tty>".format(sys.argv[0])
        print "Example: {0} 128 0 /dev/ttyUSB0".format(sys.argv[0])
        exit(2)

    client = sys.argv[1]
    port   = sys.argv[2]
    tty    = sys.argv[3]

    seq = midi.sequencer.SequencerRead(sequencer_resolution=120)
    seq.subscribe_port(client, port)
    seq.start_sequencer()

    biscuit = make_biscuit(tty)

    LightServer(seq, biscuit, 1).act()

def make_biscuit(port):
    biscuit = serial.Serial(port, 57600)
    while 1:
        biscuit.write('&')
        if biscuit.inWaiting():
            ch = biscuit.read(1)
            if ch == '!':
                biscuit.flushInput()
                break
    return biscuit

class Box(object):
    __slots__ = ["lights"]

    def __init__(self):
        self.lights = [0, 0, 0, 0, 0, 0]

    def set_light_intensity(self, light, value):
        # Channels of index 3 and 5 are blank
        if light == 3 or light == 5:
            light = 4

        self.lights[light] = value

    def packet(self):
        #print repr(self.lights)
        return 'W' + str.join('', map(chr, self.lights))

class LightServer(object):
    __slots__ = ["sequencer", "biscuit", "boxes"]
    
    def __init__(self, sequencer, biscuit, box_count):
        self.sequencer = sequencer
        self.biscuit   = biscuit
        self.boxes     = []
        for i in range(box_count):
            self.boxes.append(Box())

    def push_update(self):
        packets = [box.packet() for box in self.boxes]

        for ch in str.join('', packets):
            self.biscuit.write(ch)

    def set_light_intensity(self, light, intensity):
        box_index = int(math.floor(light / 5.0))
        box_light  = light - (box_index * 5)

        max_box_index = len(self.boxes) - 1
        if box_index > max_box_index:
           box_index = max_box_index

        box = self.boxes[box_index]
        #print "self.boxes[" + str(box_index) + "].set_light_intensity(" + str(box_light) + ", " + str(intensity) + ")"
        box.set_light_intensity(box_light, intensity)

    def handle(self, event):
        #print repr(event)

        if isinstance(event, midi.NoteOnEvent):
            self.set_light_intensity(event.pitch, event.velocity)
        elif isinstance(event, midi.NoteOffEvent):
            self.set_light_intensity(event.pitch, 0)
        elif isinstance(event, midi.AfterTouchEvent):
            ""
        elif isinstance(event, midi.ControlChangeEvent):
            ""

        self.push_update()

    def act(self):
        while True:
            event = self.receive()
            if event is not None:
                self.handle(event)

    def receive(self):
        return self.sequencer.event_read()

if __name__ == "__main__":
    main()
