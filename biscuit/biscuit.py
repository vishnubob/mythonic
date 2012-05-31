#!/usr/bin/env python

import sys
import serial
import time

class HardwareChain(object):
    def __init__(self, port, board_count, write_delay=.001):
        self.port = port
        self.board_count = board_count
        self.touch_index = 0
        self.touch_buffer = [0] * self.board_count
        self.light_buffer = [0] * (6 * self.board_count)
        self.write_delay = write_delay

    def set_light_value(self, idx, val):
        val >>= 1
        self.light_buffer[idx] = min(0x7f, max(val, 0))

    def beacon(self, addr):
        cmd = 0x80 | ord('B')
        port.write(chr(cmd))
        time.sleep(self.write_delay)
        port.write(chr(addr))

    def refresh(self, addr):
        cmd = 0x80 | ord('L')
        port.write(chr(cmd))
        time.sleep(self.write_delay)
        port.write(chr(addr))
        time.sleep(self.write_delay)
        print self.light_buffer
        for val in self.light_buffer:
            port.write(chr(val))
            time.sleep(self.write_delay)

    def touch(self, addr):
        cmd = 0x80 | ord('T')
        port.write(chr(cmd))
        time.sleep(self.write_delay)
        port.write(chr(addr))
        # XXX: timeout
        val = port.read(1)
        time.sleep(self.write_delay)
        return val

class TouchAverage(object):
    def __init__(self, hc):
        self.hc = hc


port = serial.Serial(sys.argv[1], baudrate=1000000, parity=serial.PARITY_EVEN)
hc = HardwareChain(port, 1, .001)

for x in range(5):
    hc.beacon(0)
    time.sleep(.5)

while 1:
    for x in range(0xff):
        hc.set_light_value(0, x)
        hc.refresh(0)
        print ord(hc.touch(0))
        time.sleep(.01)
    for x in range(0xff, 0, -1):
        hc.set_light_value(0, x)
        hc.refresh(0)
        print ord(hc.touch(0))
        time.sleep(.01)
