#!/usr/bin/python3
# from __future__ import print_function
import sys, os
import sane
import numpy
from PIL import Image

#
# Change these for 16bit / grayscale scans
#
depth = None
mode = 'lineart'  # ''color'

#
# Initialize sane
#
ver = sane.init()
print('SANE version:', ver)

#
# Get devices
#
devices = sane.get_devices()
print('Available devices:', devices)

#
# Open first device
#
dev = sane.open(devices[1][0])

#
# Set some options
#
params = dev.get_parameters()
if 0:
    try:
        dev.depth = depth
    except:
        print('Cannot set depth, defaulting to %d' % params[3])
if 1:
    try:
        dev.mode = mode
    except:
        print('Cannot set mode, defaulting to %s' % params[0])

if 0:
    try:
        dev.br_x = 320.
        dev.br_y = 240.
    except:
        print('Cannot set scan area, using default')

params = dev.get_parameters()
print('Device parameters:', params)
print('original resolution =', dev.resolution)
dev.resolution = 300
print('changed resolution =', dev.resolution)
# dev.threshold=75
# params = dev.get_parameters()
# print('after threshold change: Device parameters:', params)
# Start a scan and get and PIL.Image object
#

while 1:
    print("enter filename: (control-C to quit)")
    fn = sys.stdin.readline().strip()
    if ',' in fn:
        fn, sth = fn.split(',')
        if sth:
            dev.threshold = int(sth)
    dev.start()
    im = dev.snap()
    # im = im.convert('L')
    # im = im.point(lambda x: x > 150)
    name, ext = os.path.splitext(fn)
    png_name = name + '.png'
    im.save(png_name)
    if ext != '.png':
        os.system("convert %s %s" % (png_name, fn))
