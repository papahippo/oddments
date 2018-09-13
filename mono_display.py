#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" overtaken by events? """
import sys, os, numpy



def main():
    out = open('/dev/fb0','wb')
    out.write(numpy.ndarray([0xffff0000]*4096))
    out.close()
if __name__ == '__main__':
    main()
