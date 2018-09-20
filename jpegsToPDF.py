#!/usr/bin/env python3
import copy, sys, os
from PyPDF2 import PdfFileWriter
from PIL import Image
from walker import Walker


class JpegsToPDF(Walker):

    name_ =  "multiple jpegs to single multi-page PDF converter"
    tag_ = '-A4L'
    output = None

    def goes_to_same_PDF(self, stem_):
        return False  # STUB implementation for initial test with single-page docs

    def cleanup(self):
        if self.output and self.output.getNumPages():
            self.output.write(open('%s/%s.pdf' % (self.root_, self.stem_, ), 'wb'))
        self.output = None

    def handle_item(self, root_, item_, is_dir):
        print(root_, item_)
        Walker.handle_item(self, root_, item_, is_dir)
        self.root_ = root_
        stem_, ext_ = os.path.splitext(item_)
        if is_dir or ext_.lower() not in ('.jpg', 'jpeg'):
            return None
        input = Image.open('%s/%s' %(root_, item_))
        if not self.goes_to_same_PDF(stem_):
            self.cleanup()
            self.stem_ = stem_
            self.output = PdfFileWriter()
            self.output.addPage(input)
        return True


if __name__ == '__main__':
    JpegsToPDF().main()
