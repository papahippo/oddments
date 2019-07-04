#!/usr/bin/python3
# -*- coding: utf-8 -*-
" dive into music archive and perform maintenance or analyis or report tasks on all PDFs"
import sys, os, re
from subprocess import Popen, PIPE, TimeoutExpired, call

from walker import Walker

class PdfWalker(Walker):

    name_ = "PDF walker/fixer"
    ps_filename = '/tmp/pdf_fix.ps'
    tmp_pdf_filename = '/tmp/pdf_fix.pdf'

    def check_images(self, effort):
        proc = Popen("pdfimages -list %s" % self.shl_pathname, stdout=PIPE, stderr=PIPE, shell=True, close_fds=True)
        try:
            outs, errs = proc.communicate(timeout=15)
        except TimeoutExpired:
            proc.kill()
            outs, errs = proc.communicate()
        out_lines = outs.decode(sys.stdout.encoding).split('\n')
        err_lines = errs.decode(sys.stderr.encoding).split('\n')
        if 0: #  or err_lines:  # disabled, not sure why!?
            print("(buggy old?) pdfimages gave errors on %s" % self.shl_pathname)
            return None
        if len(out_lines)<2:
            self.vprint(1, "not a proper PDF? %s" % self.shl_pathname)
            return None  # => no images
        headings = re.split(r'\s+', out_lines.pop(0))
        out_lines.pop(0)  # skip line with just hyphens
        if not out_lines:
            self.vprint(1, "no images in %s" % self.shl_pathname)
            return None  # => no images
        fixed_tifs = []
        for l in out_lines:
            if len(l)<3:
                continue
            self.vprint(3, l)
            values = re.split(r'\s+', l)
            field =dict(zip(headings, values[1:]))
            self.vprint(3, "field['object']", field['object'])
            if field['object']=='[inline]':  # or field['enc']!='ccitt':
                self.vprint(1, "%s contains in-line or not ccitt-encoded image(s)" % self.shl_pathname)
                call("pdf2ps %s %s" % (self.shl_pathname, self.ps_filename), shell=True)
                call("ps2pdf %s %s" % (self.ps_filename, self.shl_pathname), shell=True)
                return True
            if field['color']!='gray' or int(field['bpc'])!=1:
                self.vprint(1, "%s is %u bit(s) %s (not 1 bit gray)" % (self.shl_pathname, int(field['bpc']), field['color']))
                if not fixed_tifs:
                    repair_cmd = ('gs -q -dSAFER -dNOPAUSE -dBATCH -dUseCropBox -sOutputFile=temp_%d.tif' +
                           ' -r300 -sDEVICE=tiffg4 -c "{ .5 gt { 1 } { 0 } ifelse} settransfer" -f ' +  self.shl_pathname)
                     #    ' -c "{ .5 gt { 1 } { 0 } ifelse} settransfer" -f %s' % self.shl_pathname)
                    self.vprint (1, "repair_cmd=", repair_cmd)
                    call(repair_cmd, shell=True)
                fixed_tifs.append('temp_%d.tif' % (1+len(fixed_tifs)))
                #call("convert %s -monochrome -threshold 50 %s" % (self.shl_pathname, self.tmp_pdf_filename), shell=True)
                # unfinished!
                #call("cp %s %s"  % (self.tmp_shl_pathname, self.shl_pathname), shell=True)
        if fixed_tifs:
            reunite_cmd = 'convert ' + ' '.join(fixed_tifs)+ ' ' + self.shl_pathname
            self.vprint(1, "reunite_cmd=", reunite_cmd)
            call(reunite_cmd, shell=True)
            return True
        self.vprint(2, "%s is fine!" % self.shl_pathname)
        return False


    def handle_item(self, root_, item_, is_dir):
        Walker.handle_item(self, root_, item_, is_dir)
        name_, ext_ = os.path.splitext(item_)
        if is_dir or ext_.lower() not in ('.pdf',):
            return None
        for effort in range(2):
            if not self.check_images(effort):
                return True
        self.vprint (1, "%s is still not right after 'fix'." % self.shl_pathname)


if __name__ == '__main__':
    PdfWalker().main()
