#!/usr/bin/python3
"""
I'm incubating my python isdn monitor stuff here.. I'll move it toits own project if it reallly gets going!
"""
import sys, os, socket, fcntl, struct, array

class ISocket(socket.socket):
    tag = 'I'


    def __init__(self, family=34, type=socket.SOCK_RAW, proto=0, fileno=None):
        socket.socket.__init__(self, family, type, proto, fileno)

    def ioctl(self, funcNum, fmt, *values):
        size = struct.calcsize(fmt)
        funcCode = funcNum + (ord(self.tag)<<8) + (4<<16) + 0x80000000;
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
        return self.ioctl(66, 'BBH')

    def get_device_count(self):
        return self.ioctl(67, 'L')

    def get_device_info(self, device_index):
        return self.ioctl(68, 'LLLL16sL20s', device_index, 0, 0, 0,
                          0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0,  0,
                          0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, )

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
        print (device_info)

    mySocket.close()

if __name__ == "__main__":
    main()

