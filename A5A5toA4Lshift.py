#!/usr/bin/env python3
# ad hoc variant of A5A5toA4L.py
import copy, sys, os
from PyPDF2 import PdfFileWriter, PdfFileReader

from walker import Walker

class A5A5toA4L(Walker):

    name_ =  "2xA5 landscape (on 1 A4 page) to 2 A4 landscape pages converter"
    tag_ = '-A4LS'
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
            print('##', p.mediaBox)
            print('!!!!!!', w, h)
            p.mediaBox.lowerRight = (w, h / 2)
            p.mediaBox.upperLeft = (-50, h)
            q.mediaBox.upperRight = (w, h / 2)
            q.mediaBox.lowerLeft = (-50, 0)
            if not self.lower_only:
                output.addPage(p)
            if not self.upper_only:
                output.addPage(q)
        output.write(open('%s/%s%s%s' %(root_, stem_, self.tag_, ext_,), 'wb'))
        return True


if __name__ == '__main__':
    A5A5toA4L().main()
