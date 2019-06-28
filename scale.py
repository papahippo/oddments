#!/usr/bin/env python3
import numpy
points= numpy.array([850,75,958,137.5,958,262.5,
                    850,325,742,262.6,742,137.5],
                    dtype=numpy.float_)
tinies = points / 120
print(points)
print(tinies)
for ix, tiny in enumerate(tinies):
    print ("%.1f" %tiny, end=ix & 1 and '\n' or ', ')


