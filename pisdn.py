#!/usr/bin/python3
"""
My ISDN work has stopped for good, now that even I don't use it at home anymore - and it's
going to be obsolete soon. This code is retained for... no good reason(?)

WARNING: temporarily(?) dicontinuing the ctypes approach; see 'pymisdn.py'.
I'm incubating my python isdn monitor stuff here.. I'll move it toits own project if it reallly gets going!
This project is stalled because of problems binding tosocket of family AF_ISDN. The python scoket library
only seems to like AF_INET and AF_INET6.
"""
import sys, os, socket, fcntl, array, ctypes

sa_family_t = ctypes.c_ushort;

class IsdnStructure(ctypes.LittleEndianStructure):
    _pack_ = 1
    def __str__(self):
        return '\n'.join(
            ["\t%s = %s" %(_f[0], getattr(self, _f[0]))
             for _f in self._fields_]
        )

class SockAddr_mISDN(IsdnStructure):
    _fields_ = [
        ("family",       sa_family_t),
        ("dev",          ctypes.c_ubyte),
        ("channel",      ctypes.c_ubyte),
        ("sapi",         ctypes.c_ubyte),
        ("tei",          ctypes.c_ubyte),
    ]

class ABI_version(IsdnStructure):
    """
    """
    _fields_ = [
        ("major_version",       ctypes.c_uint32,  8),
        ("minor_version",       ctypes.c_uint32,  8),
        ("release",             ctypes.c_uint32, 14),
        ("_spare_1",            ctypes.c_uint32,  1),
        ("is_git.misdn.eu_ver", ctypes.c_uint32,  1),
    ]

class ChannelMap(ctypes.c_ubyte*16):
    def __str__(self):
        return '0x'+ ''.join(reversed(['%02x' % i8 for i8 in self]))


class DeviceInfo(IsdnStructure):
    """
    """
    _fields_ = [
        ("id",                  ctypes.c_uint32),
        ("D_protocols",         ctypes.c_uint32),
        ("B_Protocols",         ctypes.c_uint32),
        ("protocol",            ctypes.c_uint32),
        ("channelMap",          ChannelMap),
        ("nB_chans",            ctypes.c_uint32),
        ("name",                ctypes.c_char*20),
    ]
    
socket.PF_ISDN = 34
IMGETVERSION = 0x80044942
IMGETCOUNT   = 0x80044943
IMGETDEVINFO = 0x80044944

dch_echo = True

print("running '%s' to monitor ISDN activity" % sys.argv.pop(0))
#print(socket.PF_ISDN, socket.SOCK_RAW, socket.PF_RDS)
mySocket = socket.socket(socket.PF_ISDN, socket.SOCK_RAW, 0)
#print (dir(socket))
print (mySocket)

pISDN_version = ABI_version(1, 1, 291)
mISDN_version = ABI_version()
deviceInfo = DeviceInfo()

rc = (fcntl.ioctl(mySocket, IMGETVERSION, mISDN_version))
print ('\npISDN_version\n', pISDN_version)
print ('\nmISDN_version\n', mISDN_version)

count_ = ctypes.c_uint32(0)
#count_ = Count_only(0)
rc = fcntl.ioctl(mySocket, IMGETCOUNT, count_)
count = count_.value
print ("%s controller(s) found" % count)
for ic in range(count):
    print ("controller #%s" % ic)
    rc = fcntl.ioctl(mySocket, IMGETDEVINFO, deviceInfo)
    print (deviceInfo)

mySocket.close()

mySocket = socket.socket(socket.PF_ISDN, socket.SOCK_DGRAM, deviceInfo.protocol)

sockAddr_mISDN = SockAddr_mISDN()

# try to bind on D/E channel first, fallback to D channel on error
for channel in reversed(list(range(dch_echo+1))):  # (1,0) or just (0,)
    pass
while (1):
    break