#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, os, re

import walker

class SLinkWalker(walker.Walker):

    name_ =  "symbolic walker/fixer"

    def handle_item(self, root_, item_name, is_dir):
        Walker.handle_item(self, root_, item_name, is_dir)
        if not os.path.islink(self.composite_pathname):
            return
        source = os.readlink(self.composite_pathname)
        self.vprint (1, "%s is a symbolic link to %s" % (self.composite_pathname, source))
        relative_path =  os.path.relpath(source, start=root_)
        #abs_link_location = os.path.abspath(self.composite_pathname)
        print ("equivalent relative path from %s is %s" % (root_, relative_path))
        os.remove(self.composite_pathname)
        os.symlink(relative_path, self.composite_pathname)


if __name__ == '__main__':
    SLinkWalker().main()
