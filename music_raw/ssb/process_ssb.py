#!/usr/bin/env python

import os
import midi

path = "ssb.mid"
mf = midi.read_midifile(path)

def save_track(track, filename, channel):
    print "Creating %s for channel %d" % (filename, channel)
    track.make_ticks_abs()
    noteset = set()
    notehash = {}
    offset = min([event.tick for event in track if isinstance(event, midi.NoteOnEvent)])
    for event in track:
        if isinstance(event, midi.NoteOnEvent):
            noteset.add(event.data[0])

    out = midi.Pattern(resolution=mf.resolution)
    out.append(midi.Track())

    for event in track:
        event.channel = channel
        if isinstance(event, midi.NoteEvent):
            new_event = event.copy()
            out[0].append(new_event)
        else:
            out[0].append(event)

    out.make_ticks_rel()
    midi.write_midifile(filename, out)

def handle_drum_track(track, prefix, channel):
    print "Creating %s*.mid for channel %d" % (prefix, channel)
    track.make_ticks_abs()
    drumset = set()
    drumhash = {}
    for event in track:
        event.channel = channel
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
        fn = "%s%d.mid" % (prefix, key)
        drumhash[key].make_ticks_rel()
        midi.write_midifile(fn, drumhash[key])

track = mf[0]
for track in mf:
    for event in track:
        if isinstance(event, midi.TrackNameEvent):
            name = str.join('', map(chr, event.data))
            filename = name.replace(" ", "_").lower() + ".mid" 
            if name == "Drums 1":
                handle_drum_track(track, "drums_1_", 0)
            elif name == "Drums 2":
                handle_drum_track(track, "drums_2_", 1)
            elif name == "Drums 3":
                handle_drum_track(track, "drums_3_", 2)
            elif name == "Bass":
                save_track(track, filename, 3)
            elif name == "Pad":
                save_track(track, filename, 4)
            elif name == "Lead 1":
                save_track(track, filename, 5)
            elif name == "Lead 2":
                save_track(track, filename, 6)
            elif name == "Lead 3":
                save_track(track, filename, 7)
