#!/usr/bin/python3
"""
quicky kind of simulaton of FPGA walking.
commercial project so no context details!
"""
import sys, os
def main():
    prog = sys.argv.pop(0)
    tWalk = 570
    # iSince = number of ticks passed since bank switch
    for iSince in range(30):
        # we want to have written a complete mesage sector before the FPGA starts sending it.
        tEnd = (iSince+1) * 20
        # where will the FPGA be reading at that time.
        # 'for now' think of messages as 11 segment (2*config+1*ascii+8*binary) clumps
        # The FPGA takes 570ms to process 32 clumps.
        # so the integral number of clumps transmitted at tEnd is:
        xDone = (tEnd * 32) /tWalk
        iSafe = int(xDone + 1)
        if iSafe >=32:
            comment = "write this mesage to OTHER bank!"
            iSafe -= 32
        elif iSince==0:
            comment = "0 doesn't actually occur"
        else:
            comment = "write this message to current bank"
        print ("iSince =", iSince, "xDone =", xDone, "iSafe = ",iSafe, comment)
    print ("last case will not always occur.\nsometimes 28 and sometimes 29 ticks will occur between banks swiches")
if __name__ == '__main__':
    main()
