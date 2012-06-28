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

DEFAULTS = {
    'only_boards': None,
    'count_boards': None,
    'write_touch_data': False,
}

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
    parser = argparse.ArgumentParser()
    parser.add_argument(dest="port", nargs=1, help="The port of the RS-485 dongle.")
    parser.add_argument('-o', '--only', dest="only_boards", help="comma seperated list of boards")
    parser.add_argument('-c', "--count", type=int, dest="count_boards", help="Count of contiguous boards")
    parser.add_argument('-d', "--data", dest="write_touch_data", action="store_true", help="Write raw touch data")
    parser.set_defaults(**DEFAULTS)
    args = parser.parse_args()
    args.port = args.port[0]
    return args

def main():
    args = get_cli()
    only_boards = None
    count_boards = None
    if args.only_boards and args.count_boards:
        print "only boards and count are mutually exclusive."
        sys.exit(-1)
    port = serial.Serial(args.port, baudrate=1000000, parity=serial.PARITY_EVEN)
    write_touch_data = args.write_touch_data
    if args.only_boards:
        only_boards = args.only_boards
        only_boards = [int(x) - 1 for x in set(only_boards.split(','))]
        only_boards.sort()
        hc = biscuit.HardwareChain(port, max(only_boards), write_delay=.001, only_boards=only_boards)
    if args.count_boards:
        count_boards = int(args.count_boards)
        hc = biscuit.HardwareChain(port, count_boards, write_delay=.001)
    manager = TestManager(hc, write_touch_data=write_touch_data)
    try:
        manager.run()
    except:
        manager.blackout()
        raise

class TestManager(biscuit.Manager):
    def __init__(self, hc, write_touch_data=False, *args, **kw):
        self.touch_data_f = None
        if write_touch_data:
            self.touch_data_f = open("touch_data.txt", 'w')
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

    def report_touch(self, triggers=None):
        if not triggers:
            triggers = self.hc.get_touch_triggers()
        avgs = self.hc.get_touch_averages()
        peeks = self.hc.get_touch_peeks()
        thresholds = self.hc.get_touch_thresholds()
        msg = ''
        for (idx, trig) in enumerate(triggers):
            msg += 'Frame #%d (trigger, avgs, thresholds, peeks)\r\n' % idx
            for ds in (triggers, avgs, thresholds, peeks):
                if ds == triggers:
                    vals = map(str, triggers[idx])
                else:
                    vals = [("%.2f" % val) for val in ds[idx]]
                vals = str.join(', ', vals)
                msg += vals + '\r\n'
            msg += '\r\n'
        self.report(msg)

    def write_touch_data(self):
        #vals = self.hc.get_touch_peeks()
        vals = self.hc.get_touch_averages()
        vals = [item for sublist in vals for item in sublist]
        vals = str.join(', ', map(str, [time.time()] + vals)) + '\n'
        self.touch_data_f.write(vals)

    def think(self):
        triggers = self.hc.get_touch_triggers()
        if self.touch_data_f:
            self.write_touch_data()
        touch_flag = None
        for (idx, vals) in enumerate(triggers):
            for val in vals:
                if val:
                    touch_flag = idx
                    break

        if touch_flag != None:
            self.report("TOUCH!")
            self.report_touch(triggers)
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
        elif ch == 't':
            self.report_touch()
        elif ch == 'q':
            pop_termios()
            self.report("quitting")
            raise RuntimeError, "Exit requested (no error)"
        #else:
        #    self.report("Unknown key!")

if __name__ == "__main__":
    main()
