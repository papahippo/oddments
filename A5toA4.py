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
from os import listdir
from os.path import isfile, join

print("running '%s' to convert lots of scanned PDFs from 'top-half-A4-portrait' to A4 landscape." % sys.argv.pop(0))
mypath = (sys.argv and sys.argv.pop(0)) or './'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
myexts = '.pdf',
dest_suffix = '-XL'

for f in onlyfiles:
    base, ext = os.path.splitext(f)
    if ext not in myexts:
        print("skippping %s because extension not in '%s'" %(f, myexts))
        continue
    if base.endswith(dest_suffix):
        print("skippping %s because name indicates it is already in desired format." %f)
        continue
    old_filename = mypath + f
    temp_filename = '/tmp/a5toa4.pdf'
    new_filename = mypath + base + dest_suffix + '.pdf'
    # cmd = "pdfjam --outfile %s  --paper a4paper --scale 0.9 %s" %(new_filename, old_filename)
    # cmd = "cpdf %s -scale-contents 0.9  -o %s" %(old_filename, new_filename)
    cmd = "pdfposter -p2x1a4 %s %s" %(old_filename, temp_filename)
    print("enlarging with one-liner: '%s'" %cmd)
    os.system(cmd)
    cmd = "pdftk %s cat 1-1 output %s" %(temp_filename, new_filename)
    print("dropping second page (unwanted) with one-liner: '%s'" %cmd)
    os.system(cmd)
