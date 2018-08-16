#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" sandpit for parsing ostensibly man-readable output """
import sys, os, re



def main():
    out = open('imx6dl-pinfunc_plus.h' ,'w')
    out.write("/* comments audo-added using '%s' */\n" % sys.argv[0])
    prev_stem = ''
    for line in open('/home/lmyerscough/src/um-kernel/linux/arch/arm/boot/dts/imx6dl-pinfunc.h', 'r'):
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
