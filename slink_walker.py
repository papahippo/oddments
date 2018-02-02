#!/usr/bin/python3
import sys, os, re
from subprocess import Popen, PIPE, TimeoutExpired, call, check_output

from walker import Walker, main

class SLinkWalker(Walker):

    name_ =  "symbolic walker/fixer"

    def handle_file(self, root_, file_):
        Walker.handle_file(self, root_, file_)
        if os.path.islink(self.rel_filename):
            self.vprint (1, "%s is a good symbolic link!" % self.rel_filename)


if __name__ == '__main__':
    main(SLinkWalker)
