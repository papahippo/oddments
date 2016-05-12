#!/usr/bin/python3
"""
I'm incubating my python isdn monitor stuff here.. I'll move it toits own project if it reallly gets going!
"""
import sys, os, socket, fcntl, array, ctypes

class EasyStructure(ctypes.LittleEndianStructure):
    def __str__(self):
        return '\n'.join(
            ["%s = 0x%x" %(_f[0], getattr(self, _f[0]))
             for _f in self._fields_]
        )

class ABI_version(EasyStructure):
    """
    """
    _pack_ = 1
    _fields_ = [
        ("major_version",       ctypes.c_uint32,  8),
        ("minor_version",       ctypes.c_uint32,  8),
        ("release",             ctypes.c_uint32, 14),
        ("_spare_1",            ctypes.c_uint32,  1),
        ("is_git.misdn.eu_ver", ctypes.c_uint32,  1),
    ]


socket.PF_ISDN = 34
IMGETVERSION = 0x80044942
print("running '%s' to monitor ISDN activity" % sys.argv.pop(0))
#print(socket.PF_ISDN, socket.SOCK_RAW, socket.PF_RDS)
mySocket = socket.socket(socket.PF_ISDN, socket.SOCK_RAW, 0)
#print (dir(socket))
print (mySocket)
mISDN_version = ABI_version() # array.array('b', [0]*8)
print (fcntl.ioctl(mySocket, IMGETVERSION, mISDN_version))
print (mISDN_version)
#print (dir(mISDN_version))
#print (mISDN_version)
