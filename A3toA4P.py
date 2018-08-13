#!/usr/bin/python3
" dive into music archive and perform maintenance or analyis or report tasks on all files"
import sys, os, re
from subprocess import call

from walker import Walker, main

class A3toA4P(Walker):

    name_ =  "2xA4 pages on A3 to separate A4 portrait pages converter"
    tag_ = '-A4P'

    def handle_item(self, root_, item_, is_dir):
        print(root_, item_)
        Walker.handle_item(self, root_, item_, is_dir)
        stem_, ext_ = os.path.splitext(item_)
        if is_dir or ext_.lower() not in ('.pdf',) or stem_.endswith(self.tag_):
            return None
        call("pdfposter '%s/%s' '%s/%s%s%s' -m a4 -p 2x1a4" %(root_, item_, root_, stem_, self.tag_, ext_), shell=True)
        return True


if __name__ == '__main__':
    main(A3toA4P)
