#!/usr/bin/env python3
import copy, sys, os
from PyPDF2 import PdfFileWriter, PdfFileReader

from walker import Walker

class A5A5toA4P(Walker):

    name_ =  "2xA5 portrait (on 1 A4 page) to 2 A4 portrait pages converter"
    tag_ = '-A4P'

    def handle_item(self, root_, item_, is_dir):
        print(root_, item_)
        Walker.handle_item(self, root_, item_, is_dir)
        stem_, ext_ = os.path.splitext(item_)
        if is_dir or ext_.lower() not in ('.pdf',) or stem_.endswith(self.tag_):
            return None
        input = PdfFileReader(open('%s/%s' %(root_, item_), 'rb'))
        output = PdfFileWriter()
        pages = []
        for p in [input.getPage(i) for i in range(0, input.getNumPages())]:
            q = copy.copy(p)
            (w, h) = p.mediaBox.upperRight
            # print (w, h)
            p.mediaBox.upperRight = (w/2, h)
            p.mediaBox.lowerLeft = (0, 0)
            q.mediaBox.upperRight = (w, h)
            q.mediaBox.lowerLeft = (w/2, 0)
            pages.extend([p,q])
        for i in (1,2, 5,6, 9,10, 13,14, 17,18, 21,22, 25,26, 29,30, 33,34, 37,38, 41,42,43,
                  40,39, 36,35, 32,31, 28,27, 24,23, 20,19, 16,15, 12,11, 8,7, 4,3, 0):
            output.addPage(pages[i])
        output.write(open('%s/%s%s%s' %(root_, stem_, self.tag_, ext_,), 'wb'))
        return True


if __name__ == '__main__':
    A5A5toA4P().main()
