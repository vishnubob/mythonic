import pprint
import select
import sys
import time

import midi
import midi.sequencer

from music import make_looper

def main():
    if len(sys.argv) < 4:
        script_name = sys.argv[0]
        print "Usage: %s <midi client> <midi port> <file1, ...>" % script_name
        sys.exit(1)

    print "Press # track then enter to toggle track"
    client = int(sys.argv[1])
    port = int(sys.argv[2])
    file_paths = sys.argv[3:]

    if len(file_paths) <= 0:
        print "No MIDI files specified"
        sys.exit(1)

    looper = make_looper(file_paths, client, port)

    while True:
        track_idx = read_toggle()
        if track_idx is not None:
            if track_idx >= len(looper.tracks):
                print "Track %d does not exist!" % track_idx
                continue
            if looper.tracks[track_idx].playing:
                looper.stop(track_idx)
            else:
                looper.play(track_idx)
        looper.think()

def readch():
    val = None
    (i, o, e) = select.select([sys.stdin], [], [], 0.0001)
    for s in i:
        if s == sys.stdin:
            val = sys.stdin.read(1)
            break
    return val

def read_toggle():
    val = readch()
    if val is None or not val.isdigit():
        return None

    while True:
        nxt = readch()
        if nxt is None or not nxt.isdigit():
            return int(val)
        val += nxt

if __name__ == "__main__":
    main()
