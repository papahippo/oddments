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
dev = sane.open(devices[0][0])
print (dev.optlist)
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
all_png_files = []
name = 'scanned'
while 1:
    pdf_name = name + '.pdf'
    new_page_num = 1+len(all_png_files)
    new_png_name = '%s-page%03u.png' %(name, new_page_num)
    print("enter '+' to scan '%s', 'q' to quit, or a decimal numer (1-99) to change black-white threshold (currently %d):"
          %(new_png_name, dev.threshold))
    print("or enter name (no suffix) to change name from '%s':" % name)
    if all_png_files:
        print ("or enter '=' to accept and save %u accumulated pages as %s:"
               % (len(all_png_files), pdf_name))
        print("or enter '-' to forget lastest scanned page:")
    answer = sys.stdin.readline().strip()
    if answer == 'q':
        dev.close()
        sys.exit(0)
    if answer == '+':
        dev.start()
        im = dev.snap()

        im.save(new_png_name)
        all_png_files.append(new_png_name)
        continue
    if answer == '-':
        if all_png_files:
            all_png_files.pop()
        continue
    if answer == '=':
        cmd = "convert %s %s" % (' '.join(all_png_files), pdf_name)
        print ("executing command '%s'..." %cmd)
        os.system(cmd)
        print("... done!")
        all_png_files = []  # clear the decks!
        continue
    if answer.isnumeric():
        dev.threshold = int(answer)
        continue
    name = answer
#
# leve de ouwe meuk:
# im = im.convert('L')
# im = im.point(lambda x: x > 150)
