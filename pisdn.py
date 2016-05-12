#!/usr/bin/python3
"""
I'm incubating my python isdn monitor stuff here.. I'll move it toits own project if it reallly gets going!
"""
import sys, os, socket, fcntl, array, ctypes

class Packet_part(ctypes.BigEndianStructure):
    """
    """
    _pack_ = 1
    _fields_ = []


socket.PF_ISDN = 34
IMGETVERSION = 0x80044942
print("running '%s' to monitor ISDN activity" % sys.argv.pop(0))
#print(socket.PF_ISDN, socket.SOCK_RAW, socket.PF_RDS)
mySocket = socket.socket(socket.PF_ISDN, socket.SOCK_RAW, 0)
#print (dir(socket))
print (mySocket)
versionArray = array.array('b', [0]*8)
print (fcntl.ioctl(mySocket, IMGETVERSION, versionArray))
print (versionArray)
