#!/usr/bin/env python3
import copy, sys, os
from PyPDF2 import PdfFileWriter, PdfFileReader

from walker import Walker

class A5A5toA4L(Walker):

    name_ =  "A3 landscape (on 1 A3 page) to 2 A4 portrait pages converter"
    tag_ = '-A4L'

    def handle_item(self, root_, item_, is_dir):
        print(root_, item_)
        Walker.handle_item(self, root_, item_, is_dir)
        stem_, ext_ = os.path.splitext(item_)
        if is_dir or ext_.lower() not in ('.pdf',) or stem_.endswith(self.tag_):
            return None
        input = PdfFileReader(open('%s/%s' %(root_, item_), 'rb'))
        output = PdfFileWriter()
        for p in [input.getPage(i) for i in range(0, input.getNumPages())]:
            q = copy.copy(p)
            (x0, y0) = p.mediaBox.lowerLeft
            (x1, y1) = p.mediaBox.upperRight
            print ((x0, y0), (x1, y1))
            p.mediaBox.lowerLeft = (x0, y0)
            p.mediaBox.lowerRight = (x1/2, y0)
            p.mediaBox.upperLeft = (x0, y1)
            p.mediaBox.upperRight = (x1/2, y1)
            output.addPage(p)
            q.mediaBox.lowerLeft = (x1/2, y0)
            q.mediaBox.lowerRight = (x1, y0)
            q.mediaBox.upperLeft = (x1/2, y1)
            q.mediaBox.upperRight = (x1, y1)
            output.addPage(q)
        output.write(open('%s/%s%s%s' %(root_, stem_, self.tag_, ext_,), 'wb'))
        return True


if __name__ == '__main__':
    A5A5toA4L().main()
