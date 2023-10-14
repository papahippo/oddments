#!/usr/bin/env python3
# WARNING: I have abandoned this approach 'for now'!
#
import os, sys, subprocess
from walker import Walker

class Pdf_real_copy(Walker):

    name_ =  "copy PDFs following links"
    myExts = ('.pdf',)


    def process_keyword_arg(self, a):
        if a in ('-h', '--help'):
            print("utility to ccpy PDFs resolving symbolic links when necessary\n"
                "syntax:  pdf_real_copy.py [options] [paths]\n"
                  "no special options so far implemented):\n"
                  )
        return Walker.process_keyword_arg(self, a)

    def handle_item(self, root_, item_, is_dir):
            print (sys.argv)
            return

if __name__ == '__main__':
    Pdf_real_copy().main()
