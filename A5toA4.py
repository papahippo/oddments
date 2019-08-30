#!/usr/bin/python3
import sys,os
from os import listdir
from os.path import isfile, join
#Note to self: maybe I shouldd rework this to use my 'Walker'
#  class
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
    if base.endswith(dest_suffix) or base.endswith('-A4L'):
        print("skippping %s because name indicates it is already in desired format." %f)
        continue
    old_filename = mypath + f
    temp_filename = '/tmp/a5toa4.pdf'
    new_filename = mypath + base + dest_suffix + '.pdf'
    # cmd = "pdfjam --outfile %s  --paper a4paper --scale 0.9 %s" %(new_filename, old_filename)
    # cmd = "cpdf %s -scale-contents 0.9  -o %s" %(old_filename, new_filename)
    cmd = "pdfposter -p2x1a4 %s %s" %(old_filename, new_filename)
    print("enlarging with one-liner: '%s'" %cmd)
    os.system(cmd)
    #cmd = "pdftk %s cat 1-1 output %s" %(temp_filename, new_filename)
    #print("dropping second page (unwanted) with one-liner: '%s'" %cmd)
    #os.system(cmd)
