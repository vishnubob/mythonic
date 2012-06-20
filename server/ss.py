#!/usr/bin/env python

import serial
import signal
import sys
import time

import midi.sequencer

from mythonic import SSManager
from biscuit import HardwareChain

PFRAME_COUNT = 3

def make_write_sequencer(client, port):
    seq = midi.sequencer.SequencerWrite(sequencer_resolution=120)
    seq.subscribe_port(client, port)
    seq.start_sequencer()
    return seq

def main():
    if len(sys.argv) != 4:
        script_name = sys.argv[0]
        print "Usage:   {0} <midi client> <midi port> <tty>".format(sys.argv[0])
        print "Example: {0} 128 0 /dev/ttyUSB0".format(sys.argv[0])
        exit(2)

    client = sys.argv[1]
    port = sys.argv[2]
    tty = sys.argv[3]

    tty = serial.Serial(tty, baudrate=1000000, parity=serial.PARITY_EVEN)
    hc = HardwareChain(tty, PFRAME_COUNT, .001)
    seq = make_write_sequencer(client, port)

    man = SSManager(seq, hc, PFRAME_COUNT)

    def signal_handler(signal, frame):
        man.blackout()
        for i in range(1000):
            man.cycle()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    man.run()

if __name__ == '__main__':
    main()
