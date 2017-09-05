#!/usr/bin/env python3
"""
quickie to  convert csv mail address list to someting tath can be pasted into new mail.
"""
import sys, os

inname = sys.argv[1]
outname = os.path.splitext(inname)[0]+'.adr'
with open(inname, 'r') as infile:
    with open(outname, 'w') as outfile:
        for line in infile: # .readlines():
            fields = line.split(',')
            full_mail_address = fields[2]+'<'+fields[4]+'>,\n'
            outfile.write(full_mail_address)
