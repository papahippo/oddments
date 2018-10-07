#!/usr/bin/env python3
"""
Yet another PDF maipualtion utility. This can be tweaked at source, e.g scaling A5 input by 1.41 to produce decent
size A4 output.
"""
import copy, sys, os
from PyPDF2 import PdfFileWriter, PdfFileReader

from walker import Walker

class CustomToA4(Walker):

    name_ =  "customPDF converter for pages that aren't quite A4"
    tag_ = '-A4'

    def handle_item(self, root_, item_, is_dir):
        print(root_, item_)
        Walker.handle_item(self, root_, item_, is_dir)
        stem_, ext_ = os.path.splitext(item_)
        if is_dir or ext_.lower() not in ('.pdf',) or stem_.endswith(self.tag_):
            return None
        input = PdfFileReader(open('%s/%s' %(root_, item_), 'rb'))
        output = PdfFileWriter()
        for p in [input.getPage(i) for i in range(0, input.getNumPages())]:
            (w, h) = p.mediaBox.upperRight
            print("w=%d h=%d" %(w, h))
            # p.mediaBox.lowerLeft = (100, 550)
            # p.mediaBox.upperRight = (1600, 2750)
            #p.mediaBox.lowerLeft = (30, 30)
            #p.mediaBox.upperRight = (w-30, h-30)
            p.scale(1.41, 1.41)
            output.addPage(p)
        output.write(open('%s/%s%s%s' %(root_, stem_, self.tag_, ext_,), 'wb'))
        return True


if __name__ == '__main__':
    CustomToA4().main()
