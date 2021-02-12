#!/usr/bin/env python3
"""
Yet another PDF maipualtion utility. This can be tweaked at source, e.g scaling A5 input by 1.41 to produce decent
size A4 output.
"""
import os
from PyPDF2 import PdfFileWriter, PdfFileReader

from walker import Walker

class CustomToA4(Walker):

    name_ =  "customPDF converter for pages that aren't quite A4"
    prefix_ = 'A4-'
    myExts = ('.pdf',)

    def handle_item(self, root_, item_, is_dir):
        if not Walker.handle_item(self, root_, item_, is_dir):
            return
        input = PdfFileReader(open(self.full_source_name, 'rb'))
        output = PdfFileWriter()
        for p in [input.getPage(i) for i in range(0, input.getNumPages())]:
            (w, h) = p.mediaBox.upperRight
            print("w=%d h=%d" %(w, h))
            #p.mediaBox.lowerLeft = (0, 400)
            p.mediaBox.upperRight = (float(w)*0.75, h)
            p.mediaBox.lowerLeft = (-20, 0)
            #.mediaBox.upperRight = (w-30, h-30)
            #p.mediaBox.upperRight = (w-30, h-30)
            #p.scale(1.41, 1.41)
            output.addPage(p)
        output.write(open(self.full_dest_name, 'wb'))
        return True


if __name__ == '__main__':
    CustomToA4().main()
