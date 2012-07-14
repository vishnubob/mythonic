import math

def segment(t, span, start, end):
    increment = (end - start) / float(span)
    return ((t * increment - start) % (end - start)) + start

def triangle(i, maximum):
    return maximum - abs(i % (2 * maximum) - maximum)

def sawtooth(i, maximum):
    return i % maximum

def sin_abs(i, invert=False):
    value = abs(math.sin(i))
    if invert:
        value = abs(value - 1) 
    return value
