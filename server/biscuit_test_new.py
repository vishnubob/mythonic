#!/usr/bin/env python

import sys
import time
import select
import argparse
import select
import serial
import termios
import biscuit
import tty

OLD_STDIN = None
def push_termios():
    global OLD_STDIN
    fd = sys.stdin.fileno()
    OLD_STDIN = termios.tcgetattr(fd)
    tty.setraw(fd)

def pop_termios():
    global OLD_STDIN
    fd = sys.stdin.fileno()
    termios.tcsetattr(fd, termios.TCSAFLUSH, OLD_STDIN)

def get_cli():
    port = None
    ports = []
    addresses = []
    try:
        for arg in sys.argv[1:]:
            if port == None:
                port = serial.Serial(arg, baudrate=1000000)
                continue
            else:
                boards = arg.split(',')
                addresses += map(int, boards)
                ports += [port] * len(boards)
                port = None
        if port or not (ports or addresses):
            print "Invalid number of arguments"
            raise "WTF"
    except:
        print "Usage: %s /dev/port1 1,12,8 [/dev/port2 2,9,6]" % sys.argv[0]
        sys.exit(-1)
    return (ports, addresses)

def main():
    (ports, addresses) = get_cli()
    hc = biscuit.HardwareChain(ports, addresses, write_delay=.001)
    manager = TestManager(hc)
    try:
        manager.run()
    except:
        manager.blackout()
        raise

class TestManager(biscuit.Manager):
    def __init__(self, hc, *args, **kw):
        self.touch_data_f = None
        super(TestManager, self).__init__(hc, *args, **kw)

    def __del__(self):
        if self.touch_data_f:
            self.touch_data_f.flush()
            self.report("saving!")
            self.touch_data_f.close()
            
    def readch(self):
        val = None
        (i, o, e) = select.select([sys.stdin], [], [], 0.0001)
        for s in i:
            if s == sys.stdin:
                val = sys.stdin.read(1)
                break
        return val

    def run(self):
        self.value = 0
        self.address = 0
        push_termios()
        try:
            super(TestManager, self).run()
        finally:
            pop_termios()

    def report(self, txt):
        print "%s\r" % txt

    def think(self):
        triggers = self.hc.get_touch_triggers()
        touch_flag = None
        for (idx, trigger) in enumerate(triggers):
            if trigger:
                touch_flag = idx
                break

        if touch_flag != None:
            self.report("TOUCH!")
            self.hc.set_light(touch_flag, 4, 0xff)
            for x in range(5):
                self.cycle()
            time.sleep(.1)
            self.hc.set_light(touch_flag, 4, 0)

        ch = self.readch()
        if ch in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            self.value = self.value * 10 + int(ch)
        elif ch == 'z':
            self.value = 0
        elif ch == 'a':
            self.address = self.value
            msg = "address set to %s" % self.address
            self.report(msg)
            self.value = 0
        elif ch == 'r':
            self.hc.set_light(self.address, 0, 0)
        elif ch == 'R':
            self.hc.set_light(self.address, 0, 0xff)
        elif ch == 'g':
            self.hc.set_light(self.address, 2, 0)
        elif ch == 'G':
            self.hc.set_light(self.address, 2, 0xff)
        elif ch == 'b':
            self.hc.set_light(self.address, 3, 0)
        elif ch == 'B':
            self.hc.set_light(self.address, 3, 0xff)
        elif ch == 'w':
            self.hc.set_light(self.address, 4, 0)
        elif ch == 'W':
            self.hc.set_light(self.address, 4, 0xff)
        elif ch == 'u':
            self.hc.set_light(self.address, 5, 0)
        elif ch == 'U':
            self.hc.set_light(self.address, 5, 0xff)
        elif ch == 'T':
            for ch in range(6):
                if ch == 1:
                    continue
                self.hc.set_light(self.address, ch, 0xff)
                for x in range(10):
                    self.cycle()
                time.sleep(.5)
                self.hc.set_light(self.address, ch, 0)
        elif ch == 'q':
            pop_termios()
            self.report("quitting")
            raise RuntimeError, "Exit requested (no error)"
        #else:
        #    self.report("Unknown key!")

if __name__ == "__main__":
    main()
