#!/usr/bin/env python3
# N.B. This is flawed. Thre recently added rotation stuff seems to work but the margin stuff doesn't!

import sys, os
from pdfrw import PdfReader, PdfWriter, IndirectPdfDict
from walker import Walker

XSANE_STANDARD_TITLE = "XSane scanned image"

class Pdf_meta(Walker):

    name_ =  "Fix anomalies - or other inconvenient data! - in PDF metadata."
    myExts = ('.pdf',)
    prefix_ = 'meta-'
    fix = False

    def process_keyword_arg(self, a):
        if a in ('-X', '--fix-xsane'):
            self.fix_xsane = True
            return a
        if a in ('-h', '--help'):
            print(f"utility to apply or adjust margins of (usually A4) pages within a PDF\n"
                "syntax:  pdf_neat.py [options] [paths]\n"
                  "special options for pdf_reader.Info.py are (shown quoted but must be entered unquoted!):\n"
                  "'--fix-xsane   or equivalently '-X'\n"
                  "'remove the tile '{XSANE_STANDARD_TITLE}' if present\n"
                  )
        return Walker.process_keyword_arg(self, a)

    def handle_item(self, root_, item_, is_dir):
        if is_dir or not Walker.handle_item(self, root_, item_, is_dir):
            return
        self.vprint(1, "item..", item_)
        reader = PdfReader(open(self.full_source_name, 'rb'))
        self.vprint(2, "page count", len(reader.pages))
        writer = PdfWriter()
        writer.addpages(reader.pages)
        writer.Info = reader.Info
        if writer.Info is None:
            self.vprint(1, f"no metadata in '{item_}'!")
            writer.Info = IndirectPdfDict()
        else:
            self.vprint(2, writer.Info.Creator)
            self.vprint(2, writer.Info.Producer)
            self.vprint(2, writer.Info.Subject)
            self.vprint(1, writer.Info.Title)
            self.vprint(1, writer.Info.CreationDate)
        writer.Info.Title= "aha!"
        self.vprint(2, writer.Info)
        writer.write(open(self.full_dest_name, 'wb'))
        return True


if __name__ == '__main__':
    Pdf_meta().main()
