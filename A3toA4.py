#!/usr/bin/python3
" dive into music archive and perform maintenance or analyis or report tasks on all files"
import sys, os, re
from subprocess import call

from walker import Walker, main

class A3toA4(Walker):

    name_ =  "A3 to A4 converter"

    def handle_item(self, root_, item_, is_dir):
        print(root_, item_)
        Walker.handle_item(self, root_, item_, is_dir)
        name_, ext_ = os.path.splitext(item_)
        if is_dir or ext_.lower() not in ('.pdf',):
            return None
        call("pdfposter '%s/%s' '../%s' -m a4 -p 2x1a4" %(root_, item_, item_), shell=True)
        return True

    def walk(self, target):
        if not os.path.abspath(target).endswith('A3'):
            print("error: files should be in sub-directory called 'A3'!")
            sys.exit(1)
        Walker.walk(self, target)
if __name__ == '__main__':
    main(A3toA4)
