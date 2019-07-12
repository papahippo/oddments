#!/usr/bin/env python3
# this is kind of obsolete. pdf_neat.py does the same and more; so watch this space for empty space!
#
import copy, sys, os
from PyPDF2 import PdfFileWriter, PdfFileReader

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
