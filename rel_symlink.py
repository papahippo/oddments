#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, os

print(sys.argv)
prog_name = sys.argv.pop(0)
if not sys.argv:
    print(f"syntax: {prog_name} <source file> [<dest directory>]")
    sys.exit(990)
source = sys.argv.pop(0)
parentage, short_name = os.path.split(source)
dest = sys.argv.pop(0) if sys.argv else os.getcwd()

if not os.path.isdir(dest):
    print(f"error! {dest} is not a directory!")
    sys.exit(990)
relative_path = os.path.relpath(source, start=dest)
#abs_link_location = os.path.abspath(self.full_source_name)
print ("equivalent relative path from %s is %s" % (dest, relative_path))
os.symlink(relative_path, os.path.join(dest, short_name))


