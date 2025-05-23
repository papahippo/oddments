#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" dive into archive and perform maintenance or analysis or report tasks on all files"""
import sys, os, shlex, glob

class Walker:
    # N.B. The argument parsing and similar stuff from this class has been used as a basis for class 'Large';
    # see 'arghandler.py'. I'm leaving walker.py asis for now though!

    name_ = "dummy walker"
    verbosity = recurse = 0
    prefix_ = ''   # maybe None better but this lazier
    myExts = ()
    newExt = ''

    def vprint(self, this_verbosity, *pp, **kw):
        if self.verbosity >= this_verbosity:
            return print(*pp, **kw)

    def handle_item(self, root_, item_, is_dir):
        # Subclasses of Walker are not compelled to call this; but it can be convenient!
        # Subclasses which intend to operate on directories as such - not just their files in them -
        # should prvide their own ''handle_item.
        # if is_dir:
        #     return None
        parentage, child = os.path.split(item_)
        self.stem_, self.ext_ = os.path.splitext(child)
        if self.myExts and self.ext_.lower() not in self.myExts:
            return False
        if self.prefix_ and self.stem_.startswith(self.prefix_):
            return False
        if os.path.isabs(item_):
            root_ = ''
        self.vprint(2, self.name_, 'isdir=%u' % is_dir, root_, item_)
# the use of 'shell_source_name'  and 'shell_dest_name' is being phased out in combination with the long overdue
# migration awaay from the use of shell=True in subporcess calls.
        self.full_source_name = os.path.join(root_, item_)
        self.vprint(2, f'full_source_name = {self.full_source_name}')
        self.shell_source_name = shlex.quote(self.full_source_name)
        self.full_dest_name =  os.path.join(parentage, root_ , self.prefix_ + self.stem_ + (self.newExt or self.ext_))
        self.vprint(2, f'full_dest_name = {self.full_dest_name}')
        self.shell_dest_name = shlex.quote(self.full_dest_name)
        self.vprint(2, f'shell_dest_name = {self.shell_dest_name}')
        #os.system("ls -l %s" % os.path.normpath(self.shell_source_name))
        return True

    def walk(self, target):
        if not os.path.isdir(target):
            self.vprint(1, "processing explicit filename:", target)
            self.handle_item(os.getcwd(), target, False)
            return

        self.vprint(1, "walking through target:", target)
        for root_, dirs_, files_ in os.walk(target, topdown=True):
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
        sReal, *rest = str(v).split('%')
        real = float(sReal)
        if rest:
            if len(*rest):
                raise ValueError("invalid real/percentage value")
            real /= 100.0
        return real

    def next_int_arg(self, default):
        return int(self.next_arg(default))

    def process_keyword_arg(self, a):
        if a in ('-v', '--verbose'):
            self.verbosity += 1
            return a
        if a in ('-q', '--quiet'):
            self.verbosity -= 1
            return a
        # making recursion optional and not the default; work in progress!
        # if a in('-R', '--recurse'):
        #    self.recurse = 1
        #    return a
        if a in('-p', '--prefix'):
            self.prefix_ = self.next_arg()
            return a
        # unrecognized args follow through to....
        print(
                "\n"
                "all utilities based around the 'Walker' class (also) accept the arguments (don't enter the quotes!):\n"
                "'--help' or equivalently '-h'\n"
                "\trequests help information about this command."
                "\n"
                "'--verbose' or equivalently '-v'\n"
                "\trequests verbose operation, i.e. more textual output; repeat this argument for even more!"
                "\n"
                "'--quiet' or equivalently '-q'\n"
                "\trequests quiet operation, i.e. less textual output;"
              )
        if a in ('-h', '--help'):
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
        targets = (sum(map(glob.glob, sys.argv), []) if sys.argv
                   else ['.'])
        self.vprint(1, "running '%s' on... '%s'" %(prog_path, ', '.join(targets)))
        for target in targets:
            self.walk(target)


if __name__ == '__main__':
    Walker().main()  # our class is both a base class and a dummy class
