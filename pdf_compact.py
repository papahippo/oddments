#!/usr/bin/env python3
# WARNING: I have abandoned this approach 'for now'!
#
import copy, sys, os
import fitz
from PIL import Image

from walker import Walker

class A5A5toA4L(Walker):

    name_ =  "converter of images embedded within a PDF to more compact format"
    tag_ = '-compact'
    threshold = 50

    def process_keyword_arg(self, a):
        if a in ('-t', '--threshold'):
            self.threshold = int(sys.argv.pop(0))
            return
        if a in ('-h', '--help'):
            print("utility to convert images within a PDF to a more compact format\n"
                "syntax:  pdf_compact.py [options] [paths]\n"
                  "special options for pdf_compact are (shown quoted but must be entered unquoted!):\n"
                  "'--threshold'   or equivalently '-t'\n"
                  "means interpret the next argument as the black threshold for conversion to mono ('lineart')\n"
                  )
        Walker.process_keyword_arg(self, a)

    def handle_item(self, root_, item_, is_dir):
        self.vprint(1, root_, item_)
        Walker.handle_item(self, root_, item_, is_dir)
        stem_, ext_ = os.path.splitext(item_)
        if is_dir or ext_.lower() not in ('.pdf',) or stem_.endswith(self.tag_):
            return None
        input = fitz.open('%s/%s' %(root_, item_))
        self.vprint(1, "input PDF contains %d page(s)" % len(input))
        imgcount = 0
        output = fitz.open()
        rgb = 'rgb'
        gray = 'P'
        for i in range(len(input)):
            imglist = input.getPageImageList(i)
            for img in imglist:
                xref = img[0]  # xref number
                pix = fitz.Pixmap(input, xref)  # make pixmap from image
                pilimg = Image.frombuffer(gray, [pix.width, pix.height], pix.samples,
                                       'raw', gray, 0, 1)
                imgcount += 1
                bi_image = pilimg.point(lambda p: p > self.threshold and 255)
                outputFileName = '%s/%s-%d.tif'  %(root_, stem_, imgcount)
                self.vprint(1, 'Writing %s' % outputFileName)
                bi_image.save(outputFileName)
                #samples = bi_image.tobytes()
                #rect = bi_image[0].rect
                #self.vprint(1, "rect =", rect)

        self.vprint(1, "input PDF contains %d image(s)" % imgcount)
        return True


if __name__ == '__main__':
    A5A5toA4L().main()
