#!/usr/bin/env python

import sys
import serial
import time

def main():
    port = serial.Serial(sys.argv[1], baudrate=1000000, parity=serial.PARITY_EVEN)
    hc = HardwareChain(port, 2, .001)
    hc.beacon(0)
    time.sleep(.5)
    hc.beacon(1)
    time.sleep(.5)
    man = Manager(hc)
    man.run()

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
    def __init__(self, size, fresh_ttl=60):
        self.size = size
        avglist = [0] * self.size
        self.idx = 0
        self.disabled = False
        self.fresh_ttl = fresh_ttl
        self.last_trigger = 0
        super(Average, self).__init__(avglist)

    def normalize(self, threshold=20):
        avg = self.average()
        self.threshold = avg + threshold
        print "%s new threshold set to %.2f" % (id(self), self.threshold)
    
    def push(self, val): 
        self[self.idx] = ord(val)
        self.idx = (self.idx + 1) % self.size

    def disable(self, timeout=5):
        self.disabled = True
        self.disabled_timeout = time.time() + timeout

    def is_disabled(self):
        if self.disabled and (time.time() > self.disabled_timeout):
            self.disabled = False
        return self.disabled

    def average(self, cheat_flag=False):
        data = self[:]
        if cheat_flag:
            del data[self.idx]
        return sum(data) / float(self.size)

    def peek(self):
        last_idx = (self.idx - 1) % self.size
        return self[last_idx]

    def trigger(self, disable=5):
        self.last_trigger += 1
        if self.is_disabled():
            return False
        if self.last_trigger > self.fresh_ttl:
            self.last_trigger = 0
            self.normalize()
        if self.average() < self.threshold:
            return False
        if disable:
            self.disable(disable)
        self.last_trigger = 0
        return True
            
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

    def peek(self):
        return [obj.peek() for obj in self.order]

    def normalize(self):
        return [obj.normalize() for obj in self.order]

    def go(self):
        self.order[self.idx].push(self.hc.get_touch_data(self.address))
        self.idx = (self.idx + 1) % 4

    def trigger(self):
        res = []
        for obj in self.order:
            if obj.is_disabled():
                res = [False] * 4
                break
            res.append(obj.trigger())
        return res

class HardwareChain(object):
    def __init__(self, port, length, write_delay=.001):
        self.port = port
        self.length = length
        self.write_delay = write_delay
        self.light_frames = [FrameLights(addr, self) for addr in range(self.length)]
        self.touch_frames = [FrameTouch(addr, 20, self) for addr in range(self.length)]
        self.frame_idx = 0

    def set_light(self, address, idx, val):
        self.light_frames[address].set_light(idx, val)

    def get_light(self, address, idx):
        return self.light_frames[address].get_light(idx)

    def get_touch_averages(self):
        return [obj.average() for obj in self.touch_frames]

    def get_touch_triggers(self):
        return [obj.trigger() for obj in self.touch_frames]

    def get_touch_peeks(self):
        return [obj.peek() for obj in self.touch_frames]

    def normalize_touch(self):
        return [obj.normalize() for obj in self.touch_frames]

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

class Manager(object):
    def __init__(self, hc):
        self.hc = hc

    def boot(self, cycles=100):
        # run the system for a while
        # fill the averages
        print "Booting"
        for x in range(cycles):
            self.cycle()
        self.hc.normalize_touch()
        print "BOOTED"

    def run(self):
        self.boot()
        while 1:
            self.cycle()
            self.think()

    def think(self):
        """
        Implements business logic.
        """
        for vals in self.hc.get_touch_triggers():
            for val in vals:
                if val:
                    print array
                    print self.hc.get_touch_averages()
                    print self.hc.get_touch_peeks()
                    print

    def cycle(self):
        # check to see if there is any input
        self.hc.refresh()


if __name__ == '__main__':
    main()
