#!/usr/bin/env python3
import copy, math, sys
from PyPDF2 import PdfFileWriter, PdfFileReader
#input = PdfFileReader(sys.stdin)
input = PdfFileReader(open('in.pdf', 'rb'))
output = PdfFileWriter()
for p in [input.getPage(i) for i in range(0,input.getNumPages())]:
    # p.scaleBy(math.sqrt(2))
    q = copy.copy(p)
    (w, h) = p.mediaBox.upperRight
    p.mediaBox.upperRight = (w, h/2)
    q.mediaBox.lowerRight = (w, h/2)
    #p.mediaBox.upperRight = (w/2, h)
    #q.mediaBox.upperLeft = (w/2, h)
    output.addPage(p)
    output.addPage(q)
#output.write(sys.stdout)
output.write(open('out2.pdf', 'wb'))
