#!/usr/bin/python3
"""
I'm incubating my python isdn monitor stuff here.. I'll move it toits own project if it reallly gets going!
"""
import sys, os, socket, fcntl, struct, array

# def composeFuncCode(fucNum, )
# ... on hold; currently using magic 32-bit constants!

PF_ISDN = AF_ISDN = 34

class ISocket(socket.socket):
    tag = 'I'


    def __init__(self, family=PF_ISDN, type=socket.SOCK_RAW, proto=0, fileno=None):
        socket.socket.__init__(self, family, type, proto, fileno)

    def ioctl(self, funcCode, fmt, *values):
        size = struct.calcsize(fmt)
        # funcCode = funcNum + (ord(self.tag)<<8) + (size<<16) + 0x80000000;
        buf = bytearray(size)
        if values:
            struct.pack_into(fmt, buf, 0, *values)
        print (type(buf), buf)
        print ("size =", size, "funcCode=", hex(funcCode))
        rc = fcntl.ioctl(self, funcCode, buf)
        if rc:
            raise IOError("can't get mISDN version")
        # print (buf)
        return struct.unpack(fmt, buf)

    def get_mISDN_Version(self):
        return self.ioctl(0x80044942, 'BBH')

    def get_device_count(self):
        return self.ioctl(0x80044943, 'L')

    def get_device_info(self, device_index):
        return self.ioctl(0x80044944, 'LLLL16sL20s', device_index, 0, 0, 0, bytes(' ', 'utf8'), 0, bytes('', 'utf8'))

def main():
    iSocket = ISocket()
    # print(iSocket)
    version = iSocket.get_mISDN_Version()
    print("version (Major.minor.release) = %s.%s.%s" % version)
    device_count, = iSocket.get_device_count()
    print("device count =", device_count)

    for device_index in range(device_count):
        print ("device_index %s" % device_index)
        device_info = iSocket.get_device_info(device_index)
        _id, Dprotocols, Bprotocols, protocol, bytes_channelMap, nrBchan, bytes_device_name = device_info
        print (device_info)
        device_name = bytes_device_name.decode('utf8')
        print(device_name)
    iSocket.close()

    iSocket = ISocket(PF_ISDN, socket.SOCK_DGRAM, protocol)

    dch_echo = 0  # can be set to 1 by arg in loghex.c from which this is largely cribbed!
    card_no = 0 # ditto
    # try to bind on D/E channel first, fallback to D channel on error
    #
    for channel in reversed(list(range(dch_echo+1))):  # (1,0) or just (0,)
        print(iSocket.bind((AF_ISDN, card_no)))
        break




    while (1):
        break

if __name__ == "__main__":
    main()

