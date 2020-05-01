#!/usr/bin/python3
" dive into music archive and perform maintenance or analyis or report tasks on all files"
import sys, os
from subprocess import call

from walker.walker import Walker, main

class Topsy(Walker):

    name_ =  "180 degree PDF flipper"
    prefix_ = 'ok-'
    myExts = ('.pdf',)

    def handle_item(self, root_, item_, is_dir):
        if not Walker.handle_item(self, root_, item_, is_dir):
            return
        call(f"pdftk '{root_}/{item_}' cat 1-enddown output '{root_}/{self.prefix_}{item_}", shell=True)
        return True

if __name__ == '__main__':
    main(Topsy)
