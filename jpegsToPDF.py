#!/usr/bin/env python3
import copy, sys, os
from walker import Walker
import img2pdf

class JpegsToPDF(Walker):

    name_ =  "multiple jpegs to single multi-page PDF converter"
    pendingJpegFileNames = []

    def goes_to_same_PDF(self, stem_):
        return False  # STUB implementation for initial test with single-page docs

    def cleanup(self):
        if self.pendingJpegFileNames:
            pdfFileName = '%s/%s.pdf' % (self.root_, self.stem_, )
            print("writing %s" % pdfFileName)
            with open(pdfFileName, 'wb') as out:
                out.write(img2pdf.convert([jpegFile for jpegFile in self.pendingJpegFileNames]))
            self.pendingJpegFileNames = []

    def handle_item(self, root_, item_, is_dir):
        print(root_, item_)
        Walker.handle_item(self, root_, item_, is_dir)
        self.root_ = root_
        stem_, ext_ = os.path.splitext(item_)
        if is_dir or ext_.lower() not in ('.jpg', 'jpeg'):
            return None
        if not self.goes_to_same_PDF(stem_):
            self.cleanup()
        self.stem_ = stem_
        self.pendingJpegFileNames.append('%s/%s' %(root_, item_))
        return True


if __name__ == '__main__':
    JpegsToPDF().main()
