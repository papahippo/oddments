#!/usr/bin/python3
" dive into music archive and perform maintenance or analyis or report tasks on all files"
import sys, os, re, shlex
from subprocess import Popen, PIPE, TimeoutExpired, call, check_output
from phileas import _html40 as h
class shared:
    verbosity = 0

def vprint(this_verbosity, *pp, **kw):
    if shared.verbosity >= this_verbosity:
        return print(*pp, **kw)

def images_ok_in(ok_filename):

    #output = check_output("pdfimages -list %s" % ok_filename, shell=True, close_fds=True)
    #print(str(output))
    #return
    #return call("pdfimages -list %s" % ok_filename, shell=True, close_fds=True)
    proc = Popen("pdfimages -list %s" % ok_filename, stdout=PIPE, stderr=PIPE, shell=True, close_fds=True)
    try:
        outs, errs = proc.communicate(timeout=15)
    except TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()
    out_lines = outs.decode(sys.stdout.encoding).split('\n')
    err_lines = errs.decode(sys.stderr.encoding).split('\n')
    if 0: # err_lines:
        print("(buggy old?) pdfimages gave errors on %s" % ok_filename)
        return None
    for l in out_lines:
        print(l)


def pdf_walk(path):
    for root, dirs, files in os.walk(path):
        for file_ in files:
            name_, ext_ = os.path.splitext(file_)
            if ext_.lower() not in ('.pdf',):
                continue
            rel_filename = os.path.join(root, file_)
            ok_filename = shlex.quote(rel_filename)
            # print( rel_filename, "->", ok_filename)
            if images_ok_in(ok_filename):
                print ("%s is fine!" % ok_filename)

def main():
    prog_path = sys.argv.pop(0)
    pdf_walk(sys.argv and sys.argv.pop(0) or '.')
if __name__ == '__main__':
    print (os.getcwd())
    main()
