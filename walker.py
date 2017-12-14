#!/usr/bin/python3
" dive into music archive and perform maintenance or analyis or report tasks on all files"
import sys, os, re, shlex
from subprocess import Popen, PIPE, TimeoutExpired, call, check_output
from phileas import _html40 as h

class shared:
    verbosity = 0
    ps_filename = '/tmp/pdf_fix.ps'
    pdf_filename = ''
    tmp_pdf_filename = '/tmp/pdf_fix.pdf'

def vprint(this_verbosity, *pp, **kw):
    if shared.verbosity >= this_verbosity:
        return print(*pp, **kw)

def check_images(effort):
    proc = Popen("pdfimages -list %s" % shared.pdf_filename, stdout=PIPE, stderr=PIPE, shell=True, close_fds=True)
    try:
        outs, errs = proc.communicate(timeout=15)
    except TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()
    out_lines = outs.decode(sys.stdout.encoding).split('\n')
    err_lines = errs.decode(sys.stderr.encoding).split('\n')
    if len(err_lines)>1:
        vprint(3, "warning: (buggy old?) pdfimages gave errors on %s" % shared.pdf_filename)
        # return None
    if len(out_lines)<2:
        vprint(1, "not a proper PDF? %s" % shared.pdf_filename)
        return None  # => no images
    headings = re.split(r'\s+', out_lines.pop(0))
    _hyphens = out_lines.pop(0)
    if not out_lines:
        vprint(1, "no images in %s" % shared.pdf_filename)
        return None  # => no images
    for l in out_lines:
        if len(l)<3:
            continue
        vprint(3, l)
        values = re.split(r'\s+', l)
        field =dict(zip(headings, values[1:]))
        vprint(3, "field['object']", field['object'])
        if field['object']=='[inline]':  # or field['enc']!='ccitt':
            vprint(1, "%s contains in-line or not ccitt-encoded image(s)" % shared.pdf_filename)
            call("pdf2ps %s %s" % (shared.pdf_filename, shared.ps_filename), shell=True)
            call("ps2pdf %s %s" % (shared.ps_filename, shared.pdf_filename), shell=True)
            return True
        if field['color']!='gray' or int(field['bpc'])!=1:
            vprint(1, "%s is %u bit(s) %s (not 1 bit gray)" % (shared.pdf_filename, int(field['bpc']), field['color']))
            # call("convert %s -monochrome -threshold 50 %s" % (shared.pdf_filename, shared.tmp_pdf_filename), shell=True)
            # unfinished!
            #call("cp %s %s"  % (shared.tmp_pdf_filename, shared.pdf_filename), shell=True)
            return True
    vprint(2, "%s is fine!" % shared.pdf_filename)
    return False


def process_pdf():
    for effort in range(2):
        if not check_images(effort):
            vprint(3, "%s is ok!" % shared.pdf_filename)
            return
    vprint (0, "%s is still not right after 'fix'." % shared.pdf_filename)

def pdf_walk(path):
    for root, dirs, files in os.walk(path):
        for file_ in files:
            name_, ext_ = os.path.splitext(file_)
            if ext_.lower() not in ('.pdf',):
                continue
            vprint (2, "found '%s'" % file_)
            rel_filename = os.path.join(root, file_)
            shared.pdf_filename = shlex.quote(rel_filename)
            process_pdf()

def main():
    prog_path = sys.argv.pop(0)
    shared.verbosity = sum([a in ('-v', '--verbose') for a in sys.argv])
    pdf_walk(sys.argv and (not sys.argv[0].startswith('-')) and sys.argv.pop(0) or '.')
if __name__ == '__main__':
    print (os.getcwd())
    main()
