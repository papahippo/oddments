#!/usr/bin/python3
" dive into music archive and perform maintenance or analyis or report tasks on all files"
import sys, os
from subprocess import call

from walker import Walker

class Topsy(Walker):

    name_ =  "180 degree PDF flipper"
    prefix_ = 'ok-'
    myExts = ('.pdf',)

    def handle_item(self, root_, item_, is_dir):
        if not Walker.handle_item(self, root_, item_, is_dir):
            return
        call(f"pdftk {self.shell_source_name} cat 1-enddown output {self.shell_dest_name}", shell=True)
        return True

if __name__ == '__main__':
    Topsy().main()
