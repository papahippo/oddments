#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

from walker import Walker

class SLinkWalker(Walker):

    name_ =  "symbolic walker/fixer"

    def handle_item(self, root_, item_name, is_dir):
        if not Walker.handle_item(self, root_, item_name, is_dir):
            return
        if not os.path.islink(self.full_source_name):
            return
        source = os.readlink(self.full_source_name)
        self.vprint (1, "%s is a symbolic link to %s" % (self.full_source_name, source))
        if not os.path.isabs(source):
            self.vprint(1, "this is already a good relative path, so will be left alone.")
            return
        relative_path = os.path.relpath(source, start=root_)
        #abs_link_location = os.path.abspath(self.full_source_name)
        print ("equivalent relative path from %s is %s" % (root_, relative_path))
        os.remove(self.full_source_name)
        os.symlink(relative_path, self.full_source_name)


if __name__ == '__main__':
    SLinkWalker().main()
