#!/usr/bin/python3
"""
quicky (?I hope) to read a log file as it is being written.
"""
import sys, os, time, struct


class EyeSDNFile:
    tell_tale_bytes = 'EyeSDN'.encode('utf8') + bytes([0xff])

    def __init__(self, name, mode='rb', block_size=1024):
        if not 'b' in mode:
            raise ValueError("must use binary (e.g. 'rb' or 'wb') mode for EyeSDN files")
        self.actual_file = open(name, mode=mode)
        self.block_size = block_size
        if 'r' in mode:
            starter = self.actual_file.read(7)
            if  starter != self.tell_tale_bytes:
                raise IOError("file does not start with '%s'" % self.tell_tale_bytes)
        if 'w' in mode:
            self.actual_file.write(self.tell_tale_bytes)
        self.carry_bytes = b''

    def read_packet(self):
        while 1:
            i = self.carry.find(0xff)
            if i >= 0:
                packet = self.carry_bytes[:i]
                self.carry_bytes = self.carry_bytes[i+1:]
                break
def main():
    prog = sys.argv.pop(0)
    log =  EyeSDNFile(sys.argv and sys.argv.pop() or 'isdnws.log', 'rb')

if __name__ == '__main__':
    main()


if 0:
    with EyeSDNFile(fileName, 'rb') as f:
        if f.read(6) != tell_tale_bytes:
            raise ValueError("log doesn't start with '%s'" % tell_tale_bytes)

        while 1:
            header = f.read(13)
            if header:
                print(len(header), "bytes read")
                if header[0] != 0xff:
                    raise ValueError("header doesn't start with 0xff")
                header = bytes([0]) + header [1:]
                usecs, secs, origin, length = struct.unpack('>LxLxbH', header)
                print(usecs, secs, origin, length)
                local_time_then = time.localtime(secs)
                print(time.strftime('%Y-%b-%d %H:%M:%S.', local_time_then) + ('%06u' % usecs))
                packet = f.read(length)
                print([hex(b) for b in header] + [' ---']+[hex(b) for b in packet])
                continue
            time.sleep(0.2)