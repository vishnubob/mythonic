#!/bin/sh

# Use mididumphw to discover where fluid synth is listening
# Unless you've already started a midi device, it's probably listening
# on 128:0

# Use ALSA drivers, dump midi events, use first arg as soundfont
fluidsynth -a alsa -d $1
