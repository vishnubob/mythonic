from time import time, sleep
from os import path, getcwd
from Pd import Pd
import serial
import sys

chain_length = 2

patch = "/Users/ghall/code/mythonic/pd/instrument-mode-python.pd"

class FrameManager(object):
    def __init__(self, port, length):
        self.port = serial.Serial(port, 57600)
        self.length = length
        self.pd = Pd(nogui=False, open=patch)
        self.pd.lightdata = self.send_lights

    def get_touches(self):
        data = 'T'
        self.port.write(data)
        vals = map(ord, self.port.read(self.length * 4))
        res = []
        for frame in range(chain_length):
            touched = False
            for side in range(4):
                idx = frame * 4 + side
                if vals[idx] > 100:
                    touched = True
                    break
            res.append(touched)
        return res

    def touch_update(self):
        touches = self.get_touches()
        print touches
        for (frame_idx, touch) in enumerate(touches):
            if not touch:
                continue
            print "sending touch for %d" % frame_idx
            self.pd.Send(["touch", frame_idx])

    def send_lights(self, *data):
        #print "Got some light data bitches"
        data = 'L'
        for val in data:
            data += chr(int(val))
        self.port.send(data)

    def run(self):
        try:
            while 1:
                self.touch_update()
                self.pd.Update()
        except:
            self.pd.Exit()
            raise

port = sys.argv[1]
fm = FrameManager(port, 2)
fm.run()

