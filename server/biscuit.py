#!/usr/bin/env python

import sys
import time
import random

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
        # THOERY: By always refreshing the lights,
        #         we might be able to re-write missed
        #         light messages
        #if True or self.dirty():
        if self.dirty():
            self.hc.send_light_data(self.address, self)
        self.flip()

class FrameTouch(object):
    def __init__(self, address, hc, quiescent_length=10, refresh_length=.3, trigger_threshold=1):
        self.address = address
        self.quiescent_length = quiescent_length
        self.hc = hc
        self.touch_trigger = False
        self.refresh_length = refresh_length
        self.last_refresh = random.random() + time.time()
        self.touch_ts = 0
        self.idx = 0
        self.trigger_count = 0
        self.trigger_threshold = trigger_threshold

    def go(self):
        if self.is_quiescent():
            return
        self.last_refresh = time.time()
        if self.hc.get_touch(self.address):
            self.set_trigger()
        else:
            self.trigger_count = max(self.trigger_count - 1, 0)

    def set_trigger(self):
        self.trigger_count += 1
        if self.trigger_count >= self.trigger_threshold:
            self.trigger_count = 0
            self.touch_trigger = True
            self.touch_ts = time.time()

    def is_quiescent(self):
        now = time.time()
        return (now < (self.last_refresh + self.refresh_length)) or \
                (now < (self.touch_ts + self.quiescent_length))

    def trigger(self):
        if self.touch_trigger:
            # reset the trigger
            self.touch_trigger = False
            return True
        return False

class HardwareChain(object):
    def __init__(self, ports, addresses, write_delay=.1, timeout_factor=50):
        self.write_delay = write_delay
        self.write_delay = .001
        self.timeout_factor = timeout_factor
        self.addresses = addresses
        self.ports = {}
        for idx, addr in enumerate(self.addresses):
            self.ports[addr] = ports[idx]
        # set the tiemout
        for port in list(set(self.ports.values())):
            port.timeout = (self.write_delay * self.timeout_factor)
        self.write_delay = .01
        self.light_frames = [FrameLights(addr, self) for addr in self.addresses]
        self.touch_frames = [FrameTouch(addr, self) for addr in self.addresses]
        self.frame_idx = 0

    def get_touch_triggers(self):
        return [obj.trigger() for obj in self.touch_frames]

    @property
    def length(self):
        return len(self.addresses)

    def set_light(self, address, idx, val):
        self.light_frames[address].set_light(idx, val)

    def get_light(self, address, idx):
        return self.light_frames[address].get_light(idx)

    # serial
    def refresh(self):
        light_data = self.light_frames[self.frame_idx]
        light_data.go()
        # THOERY: last box is working on setting up the lights
        #           move on to the next box for touch
        self.frame_idx = (self.frame_idx + 1) % self.length
        touch_data = self.touch_frames[self.frame_idx]
        touch_data.go()

    def beacon(self, address):
        cmd = 0x80 | ord('B')
        port = self.ports[address]
        port.write(chr(cmd))
        time.sleep(self.write_delay)
        port.write(chr(addr))

    def send_light_data(self, address, light_data):
        #print "LIGHT", address, list(light_data)
        #print "\r"
        cmd = 0x80 | ord('L')
        port = self.ports[address]
        port.write(chr(cmd))
        time.sleep(self.write_delay)
        port.write(chr(address))
        time.sleep(self.write_delay)
        light_data = list(light_data)
        extra_byte = 0
        for (idx, val) in enumerate(light_data):
            extra_byte = (extra_byte << 1) | (val & 0x1)
            val >>= 1
            port.write(chr(val))
            time.sleep(self.write_delay)
        port.write(chr(extra_byte))
        time.sleep(self.write_delay)

    def get_touch(self, address):
        #print "GET_TOUCH", address, '\r'
        cmd = 0x80 | ord('T')
        port = self.ports[address]
        port.write(chr(cmd))
        time.sleep(self.write_delay)
        port.write(chr(address))
        val = port.read(1)
        if not len(val):
            return False
        time.sleep(self.write_delay)
        val = ord(val)
        origval = val
        truefalse = val & 0x1
        val >>= 1
        #print "WOOP", "ADDR", address, "ORIG", bin(origval), "FLAG", bool(truefalse), "REM", val, "\r"
        if val != address:
            return False
        return truefalse == 1

class Manager(object):
    def __init__(self, hc):
        self.hc = hc
        self.initialized_at = time.time()

    def blackout(self):
        for lf in self.hc.light_frames:
            for i in range(6):
                lf.set_light(i, 0)
        # XXX: this is an ugly hack
        for i in range(100):
            self.cycle()
            time.sleep(.001)

    def beacon(self, pause=1, repeat=5):
        for addr in self.hc.addresses:
            for r in range(repeat):
                self.hc.beacon(addr)
                time.sleep(pause / 2.0)
            time.sleep(pause)

    def run(self):
        while 1:
            self.cycle()
            self.think()

    def think(self):
        pass

    def cycle(self):
        # check to see if there is any input
        self.hc.refresh()

if __name__ == '__main__':
    main()
