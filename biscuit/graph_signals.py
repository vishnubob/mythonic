#!/usr/bin/env python

import sys

# matplotlib
PLOTS_ENABLED = True
try:
    import matplotlib
    matplotlib.use('AGG')
    import numpy as np
    import matplotlib.mlab as mlab
    import matplotlib.pyplot as plt
    import pylab
except ImportError:
    print "Warning: skipping import of plots (missing a module like matplotlib, pylab)."
    PLOTS_ENABLED = False

def plot(data, fofn, title, xlabel, ylabel, log=False):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    if log:
        ax.set_yscale('log')
    for dm in data:
        ax.plot(dm)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig(fofn)

f = open("touch_data.txt")
data = []
for line in f:
    line = line.strip()
    line = map(float, line.split(',')[1:])
    data.append(line)

data = zip(*data)
frames = len(data) / 4
for frame in range(frames):
    _data = data[frame*4:(frame+1) * 4]
    fn = "touch_avg_frame%d.png" % (frame + 1)
    title = "Average Touch Signal for frame %d" % (frame + 1)
    plot(_data, fn, title, "Time", "Touch Signal")

