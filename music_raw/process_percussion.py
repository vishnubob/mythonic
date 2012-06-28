#!/usr/bin/env python

import os

import midi

path = os.path.dirname(__file__) + "/Percussion_Dance_Rhythm.mid"
mf = midi.read_midifile(path)
drumset = set()

track = mf[0]
for event in track:
    if event.__class__ == midi.events.NoteOnEvent:
        drumset.add(event.data[0])

print drumset
drumhash = {}
for note in drumset:
    drumhash[note] = midi.Pattern(resolution=mf.resolution)
    _track = midi.Track()
    drumhash[note].append(_track)

for event in track:
    if event.__class__ in (midi.events.NoteOnEvent, midi.events.NoteOffEvent):
        drumhash[event.data[0]][0].append(event)
    else:
        for key in drumhash:
            drumhash[key][0].append(event)

for key in drumhash:
    fn = "drum_%s.mid" % key
    midi.write_midifile(fn, drumhash[key])

