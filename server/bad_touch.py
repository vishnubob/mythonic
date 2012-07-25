#!/usr/bin/env python

import biscuit
import serial
import random
import time

ADDRESSES = range(2)

def main():
    tty = serial.Serial("/dev/ttyUSB0", baudrate=1000000)
    m = CrashManager(biscuit.HardwareChain([tty] * len(ADDRESSES), ADDRESSES))
    print "Starting at %d" % (time.time())
    m.run()

class CrashManager(biscuit.Manager):
    last_update = time.time()

    def think(self):
        #print "[THINK %d]" % (time.time())
        for idx, trigger in enumerate(self.hc.get_touch_triggers()):
            if trigger:
                print "[TOUCH %d] position: %d, address: %d" % (time.time(), idx, self.hc.addresses[idx])
        if time.time() - self.last_update > 0.001:
            for idx, addr in enumerate(ADDRESSES):
                self.hc.set_light(idx, 0, int(random.random() * 255))
                self.hc.set_light(idx, 2, int(random.random() * 255))
                self.hc.set_light(idx, 3, int(random.random() * 255))
                self.hc.set_light(idx, 4, int(random.random() * 255))
                self.hc.set_light(idx, 5, int(random.random() * 255))
            self.last_update = time.time()

if __name__ == "__main__":
    main()
