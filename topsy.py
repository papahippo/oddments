#!/usr/bin/python3
" dive into music archive and perform maintenance or analyis or report tasks on all files"
import sys, os, re
from subprocess import call

from walker import Walker, main

class Topsy(Walker):

    name_ =  "180 degree PDF flipper"

    def handle_item(self, root_, item_, is_dir):
        print(root_, item_)
        Walker.handle_item(self, root_, item_, is_dir)
        name_, ext_ = os.path.splitext(item_)
        if is_dir or ext_.lower() not in ('.pdf',):
            return None
        call("pdftk '%s/%s' cat 1-enddown output '../%s'" %(root_, item_, item_), shell=True)
        return True

    def walk(self, target):
        if not os.path.abspath(target).endswith('Topsy'):
            print("error: files should be in sub-directory called 'Topsy'!")
            sys.exit(1)
        Walker.walk(self, target)
if __name__ == '__main__':
    main(Topsy)
