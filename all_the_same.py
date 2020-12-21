#!/usr/bin/python3
"""
Answer to question on Facebook
"""
import numpy

a = numpy.array([5, 5, 5, 6, 5])
print (numpy.all(a==5))
a[3] = 5
print (numpy.all(a==5))
