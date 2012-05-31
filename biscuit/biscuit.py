#!/usr/bin/env python

import sys
import serial
import time

class FrameLights(object):
    def __init__(self, address, hc):
        self.address = address
        self.hc = hc
        self.pages = [[0] * 6 for x in range(2)]
        self.page_idx = 0

    def set_light(self, idx, val):
        val = max(0, min(val, 0xff))
        self.pages[self.page_idx][idx] = val

    def get_light(self, idx):
        return self.pages[self.page_idx][idx]

    def flip(self):
        self.next_page = int(not self.page_idx)
        self.pages[self.next_page] = self.pages[self.page_idx][:]
        self.page_idx = self.next_page
    
    def dirty(self):
        return self.pages[0] != self.pages[1]

    def __iter__(self):
        return iter(self.pages[self.page_idx])

    def go(self):
        if self.dirty():
            self.hc.send_light_data(self.address, self)
        self.flip()

class Average(list):
    def __init__(self, size):
        self.size = size
        avglist = [0] * self.size
        self.idx = 0
        super(Average, self).__init__(avglist)
    
    def push(self, val): 
        self[self.idx] = ord(val)
        self.idx = (self.idx + 1) % self.size

    def average(self):
        return sum(self) / float(self.size)

class FrameTouch(object):
    def __init__(self, address, size, hc):
        self.address = address
        self.size = size
        self.hc = hc
        self.up = Average(self.size)
        self.down = Average(self.size)
        self.left = Average(self.size)
        self.right = Average(self.size)
        self.order = [self.up, self.down, self.left, self.right]
        self.idx = 0

    def average(self):
        subavg = [obj.average() for obj in self.order]
        #subavg.append(sum(subavg) / float(len(subavg)))
        return subavg

    def go(self):
        self.order[self.idx].push(self.hc.get_touch_data(self.address))
        self.idx = (self.idx + 1) % 4

class HardwareChain(object):
    def __init__(self, port, length, write_delay=.001):
        self.port = port
        self.length = length
        self.write_delay = write_delay
        self.light_frames = [FrameLights(addr, self) for addr in range(self.length)]
        self.touch_frames = [FrameTouch(addr, 8, self) for addr in range(self.length)]
        self.frame_idx = 0

    def set_light(self, address, idx, val):
        self.light_frames[address].set_light(idx, val)

    def get_light(self, address, idx):
        return self.light_frames[address].get_light(idx)

    def get_touch_averages(self):
        return [obj.average() for obj in self.touch_frames]

    def beacon(self, addr):
        cmd = 0x80 | ord('B')
        port.write(chr(cmd))
        time.sleep(self.write_delay)
        port.write(chr(addr))

    def refresh(self):
        touch_data = self.touch_frames[self.frame_idx]
        touch_data.go()
        time.sleep(.01)
        light_data = self.light_frames[self.frame_idx]
        light_data.go()
        self.frame_idx = (self.frame_idx + 1) % self.length

    def send_light_data(self, address, light_data):
        cmd = 0x80 | ord('L')
        port.write(chr(cmd))
        time.sleep(self.write_delay)
        port.write(chr(address))
        time.sleep(self.write_delay)
        light_data = list(light_data)
        print light_data
        for val in light_data:
            if (val & 0x1):
                val += 1
            val >>= 1
            val = min(0x7f, max(val, 0))
            port.write(chr(val))
            time.sleep(self.write_delay)

    def get_touch_data(self, addr):
        cmd = 0x80 | ord('T')
        port.write(chr(cmd))
        time.sleep(self.write_delay)
        port.write(chr(addr))
        # XXX: timeout
        val = port.read(1)
        time.sleep(self.write_delay)
        return val

class VirtualSerialPort(object):
    def __init__(self, port, hc):
        self.port = serial.Serial(port, baudrate=57600)
        self.hc = hc

    def cycle(self):
        # check to see if there is any input
        if self.port.inWaiting():
            self.handle_input()
        self.hc.refresh()

    def handle_input(self):
        cmd = self.port.read(1)
        if cmd == 'L':
            data = self.port.read(6 * self.hc.length)
            data = [chr(x) for x in data]
            for addr in range(self.hc.length):
                for light in range(6):
                    self.hc.set_light(addr, light, data[addr * 6 + light])
        elif cmd == 'T':
            avg = self.hc.get_touch_averages()
            data = ''
            for frame in avg:
                for val in frame:
                    data += chr(val)
            self.port.write(data)

port = serial.Serial(sys.argv[1], baudrate=1000000, parity=serial.PARITY_EVEN)
hc = HardwareChain(port, 1, .001)

for x in range(1):
    hc.beacon(0)
    time.sleep(.5)

def up_down():
    for x in range(0xff):
        hc.set_light_value(0, x)
        hc.refresh(0)
        tavg.think()
        time.sleep(.01)
    for x in range(0xff, 0, -1):
        hc.set_light_value(0, x)
        hc.refresh(0)
        tavg.think()
        time.sleep(.01)

while 1:
    hc.refresh()
    avg = hc.get_touch_averages()
    val = int(avg[0][-1])
    if val > 30:
        hc.set_light(0, 0, hc.get_light(0, 0) + 1)
    else:
        hc.set_light(0, 0, hc.get_light(0, 0) - 1)
