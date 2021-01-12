from math import inf, sqrt


def constrain(val, min_val=-inf, max_val=inf):
    return min(max_val, max(min_val, val))


def distance(x1, y1, x2, y2):
    return sqrt((x2-x1)**2 + (y2-y1)**2)


def rgb_to_hex(r, g, b):
    return '#%02x%02x%02x' % (r, g, b)
