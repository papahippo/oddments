#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" dive into archive and perform maintenance or analysis or report tasks on all files"""
import sys, os, shlex


class Walker:
    name_ = "dummy walker"
    verbosity = recurse = 0

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
        os.system("ls -l %s" % os.path.normpath(self.shl_pathname))
        return False

    def walk(self, target):
        if not os.path.isdir(target):
            self.vprint(1, "processing explicit filename:", target)
            self.handle_item(os.getcwd(), target, False)
            return

        self.vprint(1, "walking through target:", target)
        for root_, dirs_, files_ in os.walk(target):
            for items_, isdir_ in ((dirs_, True), (files_, False),):
                for item_ in items_:
                    self.handle_item(root_, item_, isdir_)
        self.cleanup()

    def cleanup(self):
        pass

    def main(self):
        #print (os.getcwd())
        prog_path = sys.argv.pop(0)
        while sys.argv and sys.argv[0].startswith('-'):
            a = sys.argv.pop(0)
            if a in ('-v', '--verbose'):
                self.verbosity += 1
                continue
            # making recursion optional and not the default is a "to do .. maybe" action!
            #elif a in('-r', '--recurse'):
            #    self.recurse = 1
            #    continue
            else:
                print ("keyword '%s' not understood." % a)
                sys.exit(991)
        targets = [arg for arg in sys.argv if not arg.startswith('-')] or '.'
        self.vprint(1, "running", prog_path)
        for target in targets:
            self.walk(target)


if __name__ == '__main__':
    Walker().main()  # our class is both a base class and a dummy class
