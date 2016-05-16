#!/usr/bin/python3
"""
quicky (?I hope) to read a log file as it is being written.
"""
import sys, os, time

program = sys.argv.pop(0)
fileName = sys.argv and sys.argv.pop() or '/home/gill/isdn/mISDNuser-21b8c52/capi20/.libs/isdnws.log'

tell_tale_bytes = 'EyeSDN'.encode('utf8')

with open(fileName, 'rb') as f:
    if f.read(6) != tell_tale_bytes:
        raise ValueError("log doesn't start with '%s'" % tell_tale_bytes)

    while 1:
        header = f.read(12)
        if header:
            print(len(header), "bytes read")
            break  # while testing! continue
        time.sleep(0.2)