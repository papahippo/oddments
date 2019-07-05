#!/usr/bin/env python3
import copy, sys, os
from PyPDF2 import PdfFileWriter, PdfFileReader

from walker import Walker

class A5A5toA4L(Walker):

    name_ =  "2xA5 landscape (on 1 A4 page) to 2 A4 landscape pages converter"
    tag_ = '-A4L'
    skip_upper = 0
    skip_lower = 0

    def process_keyword_arg(self, a):
        if a in ('-U', '--skip-upper'):
            self.skip_upper += 1
            return
        if a in ('-L', '--skip-lower'):
            self.skip_lower += 1
            return
        Walker.process_keyword_arg(self, a)

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
            (w, h) = p.mediaBox.upperRight
            p.mediaBox.lowerRight = (w, h / 2)
            q.mediaBox.upperRight = (w, h / 2)
            if not self.skip_upper:
                output.addPage(p)
            if not self.skip_lower:
                output.addPage(q)
        output.write(open('%s/%s%s%s' %(root_, stem_, self.tag_, ext_,), 'wb'))
        return True


if __name__ == '__main__':
    A5A5toA4L().main()
