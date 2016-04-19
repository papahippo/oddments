#!/usr/bin/python3
"""
I scanned some music which was in "letter" format with little or no margins. With careful placement of the orignal
on the scanner I ensured no part of the image was lost... but I need to distribute the music in A4 with margins
 (for filing in ring-binders).
Warnings:
     1. I added the sys.argc stuff just before posting on github without re-testing!
     2. The style does not conform to python commuity consensus of 'best practice'; e.g. %s stuff is old-fashioned.
"""

import sys,os
from PIL import Image, ImageOps
from os import listdir
from os.path import isfile, join

print("running '%s' to convert pdf's from latter to A4" % sys.argv.pop(0))
mypath = (sys.argv and sys.argv.pop(0)) or '/home/gill/MEW Archive/Lord of the dance/ScannedAtColins/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
myext = '.bmp'
for f in onlyfiles:
    base, ext = os.path.splitext(f)
    if ext != myext:
        print("skippping bacause extension not '%s': %s" %(myext, f))
        continue
    img = Image.open(mypath+f, "r")
    w, h =img.size
    full_a4_w = int((w * 210)/ (8.5 * 25.4))
    full_a4_h = int((w * 297)/ (11.0 * 25.4))
    print((full_a4_w, full_a4_h))
    margin = int(full_a4_w / 20)
    img_w = full_a4_w - 2*margin
    img_h = full_a4_h - 2*margin
    essential_image = img.resize((img_w, img_h))
    bordered_img = ImageOps.expand(essential_image, border=margin, fill=(255, 255, 255))
    print(f, "scanned area =", (w, h ),"  ok_area =", (img_w, img_h),
          "total size =", bordered_img.size)
    new_filename = 'a4_' + f + '.jpeg'
    print("saving to... ", new_filename)
    bordered_img.save(new_filename)