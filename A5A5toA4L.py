#!/usr/bin/env python3
import copy, sys, os
from PyPDF2 import PdfFileWriter, PdfFileReader, pdf

from walker import Walker

root2 = 2.0**0.5


class A5A5toA4L(Walker):

    name_ =  "2xA5 landscape (on 1 A4 page) to 2 A4 landscape pages converter"
    tag_ = '-A4L'
    lower_only = 0
    upper_only = 0

    def process_keyword_arg(self, a):
        if a in ('-L', '--lower-only'):
            self.lower_only += 1
            return a
        if a in ('-U', '--upper-only'):
            self.upper_only += 1
            return a
        if a in ('-h', '--help'):
            print("utility to convert 1 or 2 A5L images on a A4P page to separate A$ landscape images\n"
                "syntax:  A5A5toA4L [options] [paths]\n"
                  "special options for A5A5toA4L are (shown quoted but must be entered unquoted!):\n"
                  "'--upper-only'   or equivalently '-U'\n"
                  "'--lower-only'   or equivalently '-L'\n"
                  )
        return Walker.process_keyword_arg(self, a)

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
            #p.scaleBy(1.4142)
            #p.rotateCounterClockwise(90)
            print('#p1', p.mediaBox)
            #p.mediaBox.lowerRight = (w, h / 2)
            q.mediaBox.upperRight = (w, h / 2)
            if not self.lower_only:
                r = pdf.PageObject.createBlankPage(input)
                r.mergeRotatedScaledPage(p, 90.0, root2)
                output.addPage(r)
            if 0:  # not self.upper_only:
                q.scale(root2, root2)
                output.addPage(q)
        output.write(open('%s/%s%s%s' %(root_, stem_, self.tag_, ext_,), 'wb'))
        return True


if __name__ == '__main__':
    A5A5toA4L().main()
