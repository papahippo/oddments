#!/usr/bin/python
import sys, subprocess
"""
Playing with the idea of doing sudo-related jiggery-pokery from within python
"""
this_script = sys.argv.pop(0)
verb = sys.argv.pop(0)
service_name = sys.argv.pop(0)
print(f"{sys.executable=}\n {sys.argv=}\n {this_script=}\n {verb=}\n {service_name=}\n")
args_to_subprocess = ['sudo', sys.executable] + sys.argv
print(f"{args_to_subprocess=}")
# this is work in progress! .. to be continued!
subp = subprocess.Popen(args_to_subprocess)