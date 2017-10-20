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
dev.resolution = 600
print('changed resolution =', dev.resolution)
# dev.threshold=75
# params = dev.get_parameters()
# print('after threshold change: Device parameters:', params)
# Start a scan and get and PIL.Image object
#
page_files = []
name = 'scanned'
while 1:
    pdf_name = name + '.pdf'
    print("enter '+' to scan page %n, 'q' to quit, or a decimal numer (1-99) to change black-white threshold (currently %d):"
          %(1+len(page_files), dev.threshold))
    if page_files:
        print ("or enter '=' to accept and save %u accumulated pages as %s, or enter '-' to forget lastest scanned page"
               %(pdf_name, len(page_files))
        print("or enter name (no suffix) to change name from '%s':" % name)
    answer = sys.stdin.readline().strip()
    if answer == 'q':
        sys.exit(0)
    if answer == '+':
        dev.start()
        im = dev.snap()
        png_name = '%s-page%03u.png' %(name, 1 + len(page_files))
        im.save(png_name)
        page_files.append(png_name)
        continue
    if answer == '-':
        if page_files:
            page_files.pop()
        continue
    if answer == '=':

    if answer.isnumeric():
        dev.threshold = int(answer)
        continue

    # im = im.convert('L')
    # im = im.point(lambda x: x > 150)
    name, ext = os.path.splitext(fn)
    if ext != '.png':
        os.system("convert %s %s" % (png_name, fn))
