#!/usr/bin/env python3
import copy, sys, os
from PyPDF2 import PdfFileWriter, PdfFileReader

from walker import Walker

def main():
    progName = sys.argv.pop(0)
    for fileName in sys.argv:
        print ("running", progName, "on", fileName)
        input = PdfFileReader(open(fileName, 'rb'), strict=False)
        output = PdfFileWriter()
        for i in range(2):
            for p in [input.getPage(i) for i in range(0, input.getNumPages())]:
                output.addPage(p)
        outCount = output.getNumPages()
        outName = 'double-' + fileName
        output.write(open(outName, 'wb'))
        print ("written", outCount, "pages to", outName)


if __name__ == '__main__':
    main()
