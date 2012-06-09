#!/usr/bin/env python

import sys
import serial
import time

from mythonic import SSManager

def main():
    port = serial.Serial(sys.argv[1], baudrate=1000000, parity=serial.PARITY_EVEN)
    hc = HardwareChain(port, 2, .001)
    hc.beacon(0)
    time.sleep(.5)
    hc.beacon(1)
    time.sleep(.5)
    man = SSManager(hc)
    man.run()

if __name__ == '__main__':
    main()
