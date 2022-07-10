#!/usr/bin/python3
" dive into music archive and perform maintenance or analyis or report tasks on all files"
import os
from subprocess import call

from walker import Walker

class A3toA4P(Walker):

    name_ =  "2xA4 pages on A3 to separate A4 portrait pages converter"
    prefix_ = 'A4P-'
    myExts = ('.pdf',)

    def handle_item(self, root_, item_, is_dir):
        if is_dir or not Walker.handle_item(self, root_, item_, is_dir):
            return
        call(f'pdfposter {self.shell_source_name} {self.shell_dest_name} -m a4 -p 2x1a4', shell=True)
        return True


if __name__ == '__main__':
    A3toA4P().main()
