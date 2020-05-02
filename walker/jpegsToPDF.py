#!/usr/bin/env python3
import os
from walker import Walker
import img2pdf

class JpegsToPDF(Walker):

    name_ =  "multiple jpegs to single multi-page PDF converter"
    myExts = ('.jpg', 'jpeg')

    pendingJpegFileNames = []

    def goes_to_same_PDF(self, item_):
        return False  # STUB implementation for initial test with single-page docs

    def cleanup(self):
        if self.pendingJpegFileNames:
            pdfFileName = f'{self.root_}/{self.stem_}.pdf'
            print("writing %s" % pdfFileName)
            with open(pdfFileName, 'wb') as out:
                out.write(img2pdf.convert([jpegFile for jpegFile in self.pendingJpegFileNames]))
            self.pendingJpegFileNames = []

    def handle_item(self, root_, item_, is_dir):
        if not Walker.handle_item(self, root_, item_, is_dir):
            return
        if not self.goes_to_same_PDF(item_):
            self.cleanup()
        self.pendingJpegFileNames.append(self.full_source_name)
        return True


if __name__ == '__main__':
    JpegsToPDF().main()
