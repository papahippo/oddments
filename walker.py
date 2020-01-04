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

    def next_arg(self, default=None):
        if not sys.argv:
            return default
        arg = sys.argv.pop(0)
        if arg == '--':
            return default
        return arg

    def next_keyword_arg(self):
        arg = self.next_arg()
        if not arg:
            return
        if arg[0]=='-':
            return arg
        sys.argv.insert(0, arg)

    def next_float_arg(self, default):
        v = self.next_arg(default)
        parts = str(v).split('%')
        real = float(parts.pop(0))
        if parts:
            real /= 100.0
        if parts.pop(0) or parts:
            raise ValueError("invalid real/percentrage value")
        return real

    def process_keyword_arg(self, a):
        if a in ('-v', '--verbose'):
            self.verbosity += 1
            return a
        # making recursion optional and not the default is a "to do .. maybe" action!
        # elif a in('-r', '--recurse'):
        #    self.recurse = 1
        #    continue
        if a in ('-h', '--help'):
            print("all utilities based around the 'Walker' class (also) accept the arguments (don't enter the quotes!):\n"
                  "'--verbose'   or equivalently '-v'\n"
                  "which may be repeated for even more verbosity (explanatory textual output)."
                  )
            sys.exit(0)
        print("keyword '%s' not understood." % a)
        sys.exit(991)

    def process_next_keyword_arg(self):
        a = self.next_keyword_arg()
        if a is not None:
            return self.process_keyword_arg(a)
    def main(self):
        #print (os.getcwd())
        prog_path = sys.argv.pop(0)
        while self.process_next_keyword_arg():
            pass
        targets = sys.argv or ['.']
        self.vprint(1, "running '%s' on '%s'" %(prog_path, ' '.join(sys.argv)))
        for target in targets:
            self.walk(target)


if __name__ == '__main__':
    Walker().main()  # our class is both a base class and a dummy class
