#!/usr/bin/python3
"""
quicky (?I hope) to read a log file as it is being written.
"""
import sys, os, time, struct

program = sys.argv.pop(0)
fileName = sys.argv and sys.argv.pop() or 'isdnws.log'

tell_tale_bytes = 'EyeSDN'.encode('utf8')

with open(fileName, 'rb') as f:
    if f.read(6) != tell_tale_bytes:
        raise ValueError("log doesn't start with '%s'" % tell_tale_bytes)

    while 1:
        header = f.read(13)
        if header:
            print(len(header), "bytes read")
            if header[0] != 0xff:
                raise ValueError("log doesn't start with 0xff")
            header = bytes([0]) + header [1:]
            usecs, secs, origin, length = struct.unpack('>LxLxbH', header)
            print(usecs, secs, origin, length)
            local_time_then = time.localtime(secs)
            print(time.strftime('%Y-%b-%d %H:%M:%S.', local_time_then) + ('%06u' % usecs))
            break  # while testing! continue
        time.sleep(0.2)