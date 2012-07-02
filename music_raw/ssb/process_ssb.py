#!/usr/bin/env python

import os

import midi

path = "ssb.mid"
mf = midi.read_midifile(path)

def handle_pad(track):
    track.make_ticks_abs()
    noteset = set()
    notehash = {}
    channel = 0
    offset = min([event.tick for event in track if isinstance(event, midi.NoteOnEvent)])
    for event in track:
        if isinstance(event, midi.NoteOnEvent):
            noteset.add(event.data[0])

    out = midi.Pattern(resolution=mf.resolution)
    out.append(midi.Track())

    for event in track:
        event.channel = 3
        if isinstance(event, midi.NoteEvent):
            new_event = event.copy()
            out[0].append(new_event)
        else:
            out[0].append(event)

    out.make_ticks_rel()
    fn = "pads.mid"
    midi.write_midifile(fn, out)

def handle_bass(track):
    track.make_ticks_abs()
    noteset = set()
    notehash = {}
    channel = 0
    offset = min([event.tick for event in track if isinstance(event, midi.NoteOnEvent)])
    for event in track:
        if isinstance(event, midi.NoteOnEvent):
            noteset.add(event.data[0])

    out = midi.Pattern(resolution=mf.resolution)
    out.append(midi.Track())

    for event in track:
        event.channel = 2
        if isinstance(event, midi.NoteEvent):
            new_event = event.copy()
            out[0].append(new_event)
        else:
            out[0].append(event)

    out.make_ticks_rel()
    fn = "bass.mid"
    midi.write_midifile(fn, out)

def handle_lead(track):
    track.make_ticks_abs()
    noteset = set()
    notehash = {}
    channel = 0
    offset = min([event.tick for event in track if isinstance(event, midi.NoteOnEvent)])
    for event in track:
        if isinstance(event, midi.NoteOnEvent):
            noteset.add(event.data[0])

    for note in noteset:
        notehash[note] = midi.Pattern(resolution=mf.resolution)
        _track = midi.Track()
        notehash[note].append(_track)

    for event in track[:10]:
        print event
    print

    for event in track:
        if isinstance(event, midi.NoteEvent):
            event.channel = 1
            new_event = event.copy()
            print id(new_event), new_event.tick
            new_event.tick -= offset
            print id(new_event), new_event.tick
            print
            notehash[event.pitch][0].append(new_event)
        else:
            for key in notehash:
                event.channel = 1
                notehash[key][0].append(eval(repr(event)))

    print notehash.keys()
    for key in notehash:
        fn = "lead_%s.mid" % key
        for event in notehash[key][0][:10]:
            print id(event), event
        notehash[key].make_ticks_rel()
        print "##"
        for event in notehash[key][0][:10]:
            print id(event), event
        print
        midi.write_midifile(fn, notehash[key])

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
            elif name.startswith("SubTractor 5"):
                handle_lead(track)
                break
            elif name.startswith("SubTractor 1"):
                handle_bass(track)
                break
            elif name.startswith("SubTractor 4"):
                handle_pad(track)
                break

