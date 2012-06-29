#!/usr/bin/env python

import os
import midi

path = "reasonable_test.mid"
mf = midi.read_midifile(path)

for (idx, track) in enumerate(mf):
    fn = "reasonable_test_%d.mid" % idx
    new_pattern = midi.Pattern(resolution=mf.resolution)
    track[-1].tick = 0
    new_pattern.append(track[:])
    midi.write_midifile(fn, new_pattern)
