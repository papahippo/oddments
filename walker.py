#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" dive into archive and perform maintenance or analysis or report tasks on all files"""
import sys, os, shlex


class Walker:
    name_ = "dummy walker"

    def vprint(self, this_verbosity, *pp, **kw):
        if self.verbosity >= this_verbosity:
            return print(*pp, **kw)

    def handle_file(self, root_, filename_):
        self.vprint(2, self.name_, 'handle_file', root_, filename_)
        return False

    def handle_item(self, root_, item_name, is_dir):
        self.vprint(2, self.name_, 'isdir=%u' % is_dir, root_, item_name)
        self.composite_pathname = os.path.join(root_, item_name)
        self.shl_pathname = shlex.quote(self.composite_pathname)
        return False

    def walk(self, target):
        self.vprint(1, "walking through target:", target)
        for root_, dirs_, files_ in os.walk(target):
            for items_, isdir_ in ((dirs_, True), (files_, False),):
                for item_ in items_:
                    self.handle_item(root_, item_, isdir_)

    def main(self):
        #print (os.getcwd())
        prog_path = sys.argv.pop(0)
        self.verbosity = sum([a in ('-v', '--verbose') for a in sys.argv])
        targets = [arg for arg in sys.argv if not arg.startswith('-')] or '.'
        self.vprint(1, "running", prog_path)
        for target in targets:
            self.walk(target)


if __name__ == '__main__':
    Walker().main()  # our class is both a base class and a dummy class
