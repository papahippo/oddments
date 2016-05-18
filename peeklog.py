#!/usr/bin/python3
"""
quicky (?I hope) to read a log file as it is being written.
"""
import sys, os, time, struct


class EyeSDNFile:
    tell_tale_bytes = 'EyeSDN'.encode('utf8') + bytes([0xff])

    def __init__(self, name, mode='rb', block_size=1024, dither=False):
        if not 'b' in mode:
            raise ValueError("must use binary (e.g. 'rb' or 'wb') mode for EyeSDN files")
        self.actual_file = open(name, mode=mode)
        self.block_size = block_size
        self.dither= dither
        if 'r' in mode:
            starter = self.actual_file.read(7)
            if  starter != self.tell_tale_bytes:
                raise IOError("file does not start with '%s'" % self.tell_tale_bytes)
        if 'w' in mode:
            self.actual_file.write(self.tell_tale_bytes)
        self.carry_bytes = b''

    def read_packet(self):
        while 1:
            i = self.carry_bytes.find(0xff)
            # print ("index of 0xff =", i)
            if i >= 0:
                packet = self.carry_bytes[:i]
                self.carry_bytes = self.carry_bytes[i+1:]
                break
            new_bytes = self.actual_file.read(self.block_size)
            if new_bytes:
                self.carry_bytes += new_bytes
                continue
            if not self.dither:
                packet = self.carry_bytes
                self.carry_bytes = b''
                break
            time.sleep(self.dither)

        return (packet.replace(b'\xfe\xfd', b'\xff')
                      .replace(b'\xfe\xfc', b'\xfe'))

    def get_packet_parts(self):
        packet = self.read_packet()
        head = bytes([0]) + packet[:12]  # prefix null byte to facilitate unpacking
        usecs, secs, origin, length = struct.unpack('>LxLxbH', head)
        local_time_then = time.localtime(secs)
        body = packet[12:]
        print(time.strftime('%Y-%b-%d %H:%M:%S.', local_time_then) + ('%06u' % usecs))
        print([hex(b) for b in head] + [' ---'] + [hex(b) for b in body])
        if length != len(body):
            raise ValueError('actual length %s != advertized lengh %s'
                             %(len(body), length))
        return local_time_then, usecs, body

def main():
    prog = sys.argv.pop(0)
    log =  EyeSDNFile(sys.argv and sys.argv.pop() or 'isdnws.log', 'rb')
    while 1:
        local_time_then, usecs, body = log.get_packet_parts()

if __name__ == '__main__':
    main()
