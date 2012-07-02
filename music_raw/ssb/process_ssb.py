#!/usr/bin/env python

import os

import midi

path = "ssb.mid"
mf = midi.read_midifile(path)

def handle_drum_track(track):
    track.make_ticks_abs()
    drumset = set()
    drumhash = {}
    channel = 0
    for event in track:
        if isinstance(event, midi.NoteOnEvent):
            drumset.add(event.data[0])

    for note in drumset:
        drumhash[note] = midi.Pattern(resolution=mf.resolution)
        _track = midi.Track()
        drumhash[note].append(_track)

    for event in track:
        if isinstance(event, midi.NoteEvent):
            drumhash[event.pitch][0].append(event.copy())
        else:
            for key in drumhash:
                drumhash[key][0].append(eval(repr(event)))

    for key in drumhash:
        fn = "drum_%s.mid" % key
        drumhash[key].make_ticks_rel()
        midi.write_midifile(fn, drumhash[key])

track = mf[0]
for track in mf:
    for event in track:
        if isinstance(event, midi.TrackNameEvent):
            name = str.join('', map(chr, event.data))
            if name.startswith("Redrum"):
                handle_drum_track(track)
                break

