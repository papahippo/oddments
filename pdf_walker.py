#!/usr/bin/python3
" dive into music archive and perform maintenance or analyis or report tasks on all files"
import sys, os, re
from subprocess import Popen, PIPE, TimeoutExpired, call, check_output

from walker import Walker, main

class PdfWalker(Walker):

    name_ =  "PDF walker/fixer"
    ps_filename = '/tmp/pdf_fix.ps'
    tmp_pdf_filename = '/tmp/pdf_fix.pdf'

    def check_images(self, effort):
        proc = Popen("pdfimages -list %s" % self.shl_filename, stdout=PIPE, stderr=PIPE, shell=True, close_fds=True)
        try:
            outs, errs = proc.communicate(timeout=15)
        except TimeoutExpired:
            proc.kill()
            outs, errs = proc.communicate()
        out_lines = outs.decode(sys.stdout.encoding).split('\n')
        err_lines = errs.decode(sys.stderr.encoding).split('\n')
        if 0: # err_lines:
            print("(buggy old?) pdfimages gave errors on %s" % self.shl_filename)
            return None
        if len(out_lines)<2:
            self.vprint(1, "not a proper PDF? %s" % self.shl_filename)
            return None  # => no images
        headings = re.split(r'\s+', out_lines.pop(0))
        _hyphens = out_lines.pop(0)
        if not out_lines:
            self.vprint(1, "no images in %s" % self.shl_filename)
            return None  # => no images
        for l in out_lines:
            if len(l)<3:
                continue
            self.vprint(3, l)
            values = re.split(r'\s+', l)
            field =dict(zip(headings, values[1:]))
            self.vprint(3, "field['object']", field['object'])
            if field['object']=='[inline]':  # or field['enc']!='ccitt':
                self.vprint(1, "%s contains in-line or not ccitt-encoded image(s)" % self.shl_filename)
                call("pdf2ps %s %s" % (self.shl_filename, self.ps_filename), shell=True)
                call("ps2pdf %s %s" % (self.ps_filename, self.shl_filename), shell=True)
                return True
            if field['color']!='gray' or int(field['bpc'])!=1:
                self.vprint(1, "%s is %u bit(s) %s (not 1 bit gray)" % (self.shl_filename, int(field['bpc']), field['color']))
                call("convert %s -monochrome -threshold 50 %s" % (self.shl_filename, self.tmp_pdf_filename), shell=True)
                # unfinished!
                #call("cp %s %s"  % (self.tmp_shl_filename, self.shl_filename), shell=True)
                return True
        self.vprint(2, "%s is fine!" % self.shl_filename)
        return False


    def handle_file(self, root_, file_):
        Walker.handle_file(self, root_, file_)
        name_, ext_ = os.path.splitext(file_)
        if ext_.lower() not in ('.pdf',):
            return None
        for effort in range(2):
            if not self.check_images(effort):
                return True
        self.vprint (1, "%s is still not right after 'fix'." % self.shl_filename)


if __name__ == '__main__':
    main(PdfWalker)
