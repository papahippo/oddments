#!/usr/bin/python3
"""
I scanned some music which was in "letter" format with little or no margins. With careful placement of the orignal
on the scanner I ensured no part of the image was lost... but I need to distribute the music in A4 with margins
 (for filing in ring-binders).
Warnings:
     1. I added the sys.argc stuff just before posting on github without re-testing!
     2. The style does not conform to python commuity consensus of 'best practice'; e.g. %s stuff is old-fashioned.
     3. i used  '.bmp' file by accident (I was borrrowing my son's scanner because it supports letter format better).
     4. I had the same problem with lettr stuff scanned as PDFs; the solution for this is ratehr different, but I
        crammed it into this single source file!
"""

import sys,os
from PIL import Image, ImageOps
from os import listdir
from os.path import isfile, join

print("running '%s' to convert scanned images from 'letter' without margin to A4 with margin" % sys.argv.pop(0))
mypath = (sys.argv and sys.argv.pop(0)) or './'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
myexts = '.bmp', '.ppm', '.pdf'
dest_prefix = 'a4-'

if '/' in dest_prefix:
    try:
        os.mkdir(mypath + dest_prefix)
    except FileExistsError:
        pass
for f in onlyfiles:
    base, ext = os.path.splitext(f)
    if ext not in myexts:
        print("skippping bacause extension not in %s: %s" %(myexts, f))
        continue
    old_filename = mypath + f
    new_filename = mypath + dest_prefix + f
    if ext == '.pdf':
        cmd = "pdfjam --outfile %s  --paper a4paper --scale 0.93 %s" %(new_filename, old_filename)
        print("converting this %s files with a one-liner: '%s'" %(myexts, cmd))
        os.system(cmd)
        continue
    img = Image.open(old_filename, "r")
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
    print("saving to... ", new_filename)
    bordered_img.save(new_filename)
