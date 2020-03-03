#!/usr/bin/env python3
# N.B. This is flawed. Thre recently added rotation stuff seems to work but the margin stuff doesn't!

import sys, os
from PyPDF2.pdf import PdfFileWriter, PdfFileReader, PageObject
from walker import Walker

class Pdf_neat(Walker):

    name_ =  "apply/adjust margins of PDF containing A4 scanned pages."
    tag_ = '-neat'
    top_margin = 0
    left_margin = 0
    bottom_margin = 0
    right_margin = 0
    clockwise = None
    anticlockwise = None
    copies = 1

    def process_keyword_arg(self, a):
        if a[1:].isnumeric():
            self.copies = int(a[1:])
            return a
        if a in ('-T', '--top-margin'):
            self.top_margin = int(sys.argv.pop(0))
            return a
        if a in ('-L', '--left-margin'):
            self.left_margin = int(sys.argv.pop(0))
            return a
        if a in ('-B', '--bottom-margin'):
            self.bottom_margin = int(sys.argv.pop(0))
            return a
        if a in ('-R', '--right-margin'):
            self.right_margin = int(sys.argv.pop(0))
            return a
        if a in ('-C', '--clockwise'):
            self.clockwise = sys.argv and int(sys.argv.pop(0)) or 180
            return a
        if a in ('-A', '--anticlockwise'):
            self.anticlockwise = sys.argv and int(sys.argv.pop(0)) or 180
            return a
        if a in ('-h', '--help'):
            print("utility to apply or adjust margins of (usually A4) pages within a PDF\n"
                "syntax:  pdf_neat.py [options] [paths]\n"
                  "special options for pdf_neat.py are (shown quoted but must be entered unquoted!):\n"
                  #"'--top-margin <int>'   or equivalently '-T <int>'\n"
                  #"'--left-margin <int>'   or equivalently '-L <int>'\n"
                  #"'--bottom-margin <int>'   or equivalently '-B <int>'\n"
                  #"'--right-margin <int>'   or equivalently '-R <int>'\n"
                  "'--clockwise <int>'   or equivalently '-C <int>'\n"
                  "'--anticlockwise <int>'   or equivalently '-A <int>'\n"
                  "(either of the above can be used with <int>=180 to fix wrong way up scanning!)\n"
                  "an arguments like '-2' means concatenate (in this case 2) copies of the resulting PDF\n"
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
        for ic in range(self.copies):
            for p in [input.getPage(i) for i in range(0, input.getNumPages())]:
                print (p.mediaBox)
                #for box in (p.mediaBox, p.cropBox, p.bleedBox,
                #            p.trimBox, p.artBox):
                if 0:
                    for box in (p.mediaBox,):
                        box.lowerLeft = (box.getLowerLeft_x() - self.left_margin,
                                         box.getLowerLeft_y() - self.bottom_margin)
                        box.upperRight = (box.getUpperRight_x() + self.right_margin,
                                          box.getUpperRight_y() + self.top_margin)

                if self.clockwise is not None:
                    p.rotateClockwise(180)
                if self.anticlockwise is not None:
                    p.rotateCounterClockwise(180)
                print (p.mediaBox,'\n')
                if 1:
                    output.addPage(p)
                else:
                    q = PageObject.createBlankPage(input)
                    #q.mergeScaledTranslatedPage(p, )
                    q.mergeScaledPage(p, (0.8))
                    output.addPage(q)
        output.write(open('%s/%s%s%s' %(root_, stem_, self.tag_, ext_,), 'wb'))
        return True


if __name__ == '__main__':
    Pdf_neat().main()
ghost