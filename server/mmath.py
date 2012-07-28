import math

def travel(t, span, start=0, end=1):
    increment = (end - start) / float(span)
    unbound = start + (t * increment)
    return min(unbound, end) if end > start else max(unbound, end)

def segment(t, span, start=0, end=1):
    if end == start:
        return end
    increment = (end - start) / float(span)
    return ((t * increment - start) % (end - start)) + start

def triangle(i, span, start=0, end=1):
    span = span/2.0
    if int((i/span) % 2) == 0:
        return segment(i, span, start, end)
    else:
        return segment(i, span, end, start)

def sawtooth(i, maximum):
    return i % maximum

def sin_abs(i, invert=False):
    value = abs(math.sin(i))
    if invert:
        value = abs(value - 1)
    return value
