#!/usr/bin/env python3
import copy, math, sys
from PyPDF2 import PdfFileWriter, PdfFileReader
squareRootOf2 = 2**0.5

#input = PdfFileReader(sys.stdin)
input = PdfFileReader(open('in.pdf', 'rb'))
output = PdfFileWriter()
for p in [input.getPage(i) for i in range(0,input.getNumPages())]:
    # p.scaleBy(math.sqrt(2))
    q = copy.copy(p)
    (w, h) = p.mediaBox.upperRight
    p.mediaBox.upperRight = (w, h/2)
    q.mediaBox.lowerRight = (w, h/2)
    p.scale(squareRootOf2, squareRootOf2)
    q.scale(squareRootOf2, squareRootOf2)
    output.addPage(p)
    output.addPage(q)
#output.write(sys.stdout)
output.write(open('out2.pdf', 'wb'))
