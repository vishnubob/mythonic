#!/usr/bin/env python

import serial
import signal
import sys
import time

from mythonic import SSManager
from biscuit import HardwareChain

PFRAME_COUNT = 3

def main():
    port = serial.Serial(sys.argv[1], baudrate=1000000, parity=serial.PARITY_EVEN)
    hc = HardwareChain(port, PFRAME_COUNT, .001)
    hc.beacon(0)
    time.sleep(.5)
    hc.beacon(1)
    time.sleep(.5)
    hc.beacon(2)
    time.sleep(.5)

    man = SSManager(hc, PFRAME_COUNT)

    def signal_handler(signal, frame):
        man.blackout()
        for i in range(PFRAME_COUNT * 2):
            man.cycle()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    man.run()

if __name__ == '__main__':
    main()
