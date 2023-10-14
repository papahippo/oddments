#!/usr/bin/env python3
# N.B. This is flawed. Thre recently added rotation stuff seems to work but the margin stuff doesn't!

import sys, os
from pypdf import PdfWriter, PdfReader, PageObject
from walker import Walker

XSANE_STANDARD_TITLE = "XSane scanned image"

class Pdf_meta(Walker):

    name_ =  "apply/adjust margins of PDF containing A4 scanned pages."
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
                  "special options for pdf_meta.py are (shown quoted but must be entered unquoted!):\n"
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
        meta = reader.metadata
        if meta is None:
            self.vprint(1, "no metadata!")
            new_meta = {}
        else:
            self.vprint(2, meta.author)
            self.vprint(2, meta.creator)
            self.vprint(2, meta.producer)
            self.vprint(2, meta.subject)
            self.vprint(1, meta.title)
            self.vprint(1, meta.creation_date)
            new_meta = meta.copy()
        new_meta['/Title']= "aha!"
        self.vprint(2, new_meta)
        writer.add_metadata(new_meta)
        for page in reader.pages:
                writer.add_page(page)

        # writer.write(open(self.full_dest_name, 'wb'))
        return True


if __name__ == '__main__':
    Pdf_meta().main()
