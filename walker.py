#!/usr/bin/python3
" dive into music archive and perform maintenance or analyis or report tasks on all files"
import sys, os, re, shlex
from subprocess import Popen, PIPE, TimeoutExpired, call, check_output
from phileas import _html40 as h

class shared:
    verbosity = 3
    ps_filename = '/tmp/pdf_fix.ps'
    #pdf_filename = ''

def vprint(this_verbosity, *pp, **kw):
    if shared.verbosity >= this_verbosity:
        return print(*pp, **kw)

def fix_images_in_pdf():
    call("pdf2ps %s %s" %(shared.pdf_filename, shared.ps_filename), shell=True)
    call("ps2pdf %s %s" %(shared.ps_filename, shared.ok_filename), shell=True)

def images_ok():

    #output = check_output("pdfimages -list %s" % ok_filename, shell=True, close_fds=True)
    #print(str(output))
    #return
    #return call("pdfimages -list %s" % ok_filename, shell=True, close_fds=True)
    proc = Popen("pdfimages -list %s" % shared.ok_filename, stdout=PIPE, stderr=PIPE, shell=True, close_fds=True)
    try:
        outs, errs = proc.communicate(timeout=15)
    except TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()
    out_lines = outs.decode(sys.stdout.encoding).split('\n')
    err_lines = errs.decode(sys.stderr.encoding).split('\n')
    if 0: # err_lines:
        print("(buggy old?) pdfimages gave errors on %s" % shared.ok_filename)
        return None
    if len(out_lines)<2:
        vprint(1, "not a proper PDF? %s" % shared.ok_filename)
        return None  # => no images
    headings = re.split(r'\s+', out_lines.pop(0))
    _hyphens = out_lines.pop(0)
    if not out_lines:
        vprint(1, "no images in %s" % shared.ok_filename)
        return None  # => no images
    for l in out_lines:
        if len(l)<3:
            continue
        print(l)
        values = re.split(r'\s+', l)
        field =dict(zip(headings, values[1:]))
        print("field['object']", field['object'])
        if field['object']=='[inline]':
            vprint(2, "%s contains in-line image(s)" % shared.ok_filename)
            return False  # => not-ok image(s)
    print("%s is fine!" % shared.ok_filename)
    return True


def process_pdf():
    if images_ok() is not False:
        return
    fix_images_in_pdf()
    if images_ok() is not True:
        print ("%s is still not right after 'fix'." % shared.ok_filename)

def pdf_walk(path):
    for root, dirs, files in os.walk(path):
        for file_ in files:
            name_, ext_ = os.path.splitext(file_)
            if ext_.lower() not in ('.pdf',):
                continue
            rel_filename = os.path.join(root, file_)
            shared.ok_filename = shlex.quote(rel_filename)
            # print( rel_filename, "->", ok_filename)
            process_pdf()

def main():
    prog_path = sys.argv.pop(0)
    pdf_walk(sys.argv and sys.argv.pop(0) or '.')
if __name__ == '__main__':
    print (os.getcwd())
    main()
