#!/usr/bin/env python3
import sys
from walker import Walker
import img2pdf

class JpegsToPDF(Walker):

    name_ =  "multiple jpegs to single multi-page PDF converter"
    myExts = ('.jpg', 'jpeg')
    newExt = '.pdf'

    dry_run = False

    pendingFileNamePairs = []

    def process_keyword_arg(self, a):
        if a in ('-d', '--dry-run'):
            self.dry_run = True
            return a
        if a in ('-h', '--help'):
            print("utility to convert JPEGs to PDF. (rough and ready - beware!)\n"
                 "syntax:  jpegsToPDF.py [options] [paths]\n"
                  "special options for jpegsToPDF.py are: (shown quoted but must be entered unquoted!)\n"
                  "'--dry-run'   or equivalently '-d'\n"
                  "  means determine which PDFs to make from which jpegs don't actually create them.\n"
                  )
        return Walker.process_keyword_arg(self, a)


    def goes_to_same_PDF(self, item_):
        return False  # STUB implementation for initial test with single-page docs

    def cleanup(self):
        if self.pendingFileNamePairs:
            print(f"processing {self.pendingFileNamePairs}")
            if not self.dry_run:
                with open(self.pendingFileNamePairs[0][1], 'wb') as out:
                    out.write(img2pdf.convert([jpegName for (jpegName, PdfName) in self.pendingFileNamePairs]))
            self.pendingFileNamePairs = []

    def handle_item(self, root_, item_, is_dir):
        if is_dir or not Walker.handle_item(self, root_, item_, is_dir):
            return
        if not self.goes_to_same_PDF(item_):
            self.cleanup()
        
        self.pendingFileNamePairs.append((self.full_source_name, self.full_dest_name))
        return True


if __name__ == '__main__':
    JpegsToPDF().main()
