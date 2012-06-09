from time import time, sleep
from os import path, getcwd
from Pd import Pd
import serial

port = serial.Serial(port, 57600)
chain_length = 2

patch = "/Users/ghall/code/mythonic/pd/instrument-mode.pd"

class FrameMaager(object):
    def __init__(self, port, length):
        self.port = port
        self.length = length
        self.pd = Pd(nogui=False, open=patch)
        self.pd.lightdata = self.send_light_data

    def touched(self):
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
        for (frame_idx, touch) in enumerate(touches):
            if not touch:
                continue
            pd.Send(["touch", feame_idx])

    def send_lights(self, *data):
        data = 'L'
        for val in data:
            data += chr(int(val))
        self.port.send(data)

    def run(self):
        try:
            while 1:
                self.touch_update()
        except:
            self.pd.Exit()
            raise

port = sys.argv[1]
fm = FrameManager(port, 2)
fm.run()

