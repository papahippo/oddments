#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" this script adds comments to a pinfunc...h file  to make it easier to identify the
U-boot/linux gpio numbers associated with multi-functional port bits.
"""
import sys, os, re


def main():
    prog_name = sys.argv.pop(0)
    pinfunc_h_file = sys.argv.pop(0) if sys.argv else 'imx6q-pinfunc.h'
    out = open(pinfunc_h_file + '-annotated','w')
    print ("'%s' will add comments to '%s' to facilitate I/O port identification..."
           % (prog_name, pinfunc_h_file))
    out.write("/* comments auto-added using '%s' */\n" % prog_name)
    prev_stem = ''
    for line in open(pinfunc_h_file, 'r'):
        lin = line[:-1]  # drop the new line char
        parse = lin.split('__')
        if len(parse) > 1 and parse[0] != prev_stem:
            out.write('\n')  # blank ine between groups with same stem for readability.
            prev_stem = parse[0]
        mine = re.match('.*__GPIO(\d+)_IO(\d+).*', lin)
        if mine:
            i2d = list(map(int, mine.groups()))
            i1d = i2d[1] + 32*(i2d[0]-1)
            lin += "  /* = gpio%d */" % i1d
            #print(lin)
        out.write(lin + '\n')
    out.close()


if __name__ == '__main__':
    main()
