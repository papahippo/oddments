#!/usr/bin/env python3
import copy, sys, os
from PyPDF2 import PdfFileWriter, PdfFileReader

from walker import Walker, main

class A5A5toA4(Walker):

    name_ =  "2xA5 landscape (on 1 A4 page) to 2 A4 pages converter"

    def handle_item(self, root_, item_, is_dir):
        print(root_, item_)
        Walker.handle_item(self, root_, item_, is_dir)
        name_, ext_ = os.path.splitext(item_)
        if is_dir or ext_.lower() not in ('.pdf',):
            return None
        input = PdfFileReader(open('%s/%s' %(root_, item_), 'rb'))
        output = PdfFileWriter()
        for p in [input.getPage(i) for i in range(0, input.getNumPages())]:
            q = copy.copy(p)
            (w, h) = p.mediaBox.upperRight
            p.mediaBox.upperRight = (w, h / 2)
            q.mediaBox.lowerRight = (w, h / 2)
            output.addPage(p)
            output.addPage(q)
        # output.write(sys.stdout)
        output.write(open('%s/%s-A4%s' %(root_, name_, ext_,), 'wb'))
        return True

if __name__ == '__main__':
    main(A5A5toA4)
