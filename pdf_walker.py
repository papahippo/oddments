#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" dive into music archive and perform maintenance or analysis or repair tasks on all PDFs
N.B. There is considerable overlap in functinality between this scriprt and oddments/pdf_compact.py
... but I am wary of burning bridges just yet!"""

import sys, os, re
from subprocess import Popen, PIPE, TimeoutExpired, call

from walker import Walker

class PdfWalker(Walker):

    name_ = "PDF walker/fixer"
    ps_filename = '/tmp/pdf_fix.ps'
    tmp_pdf_filename = '/tmp/pdf_fix.pdf'
    fix = 0
    resolution = 300
    threshold = 0.5

    def process_keyword_arg(self, a):
        if a in ('-f', '--fix'):
            self.fix += 1
            return
        if a in ('-r', '--resolution'):
            self.resolution = int(sys.argv.pop(0))
            return
        if a in ('-t', '--threshold'):
            parts = sys.argv.pop(0).split('%')
            self.threshold = float(parts.pop(0))
            if not parts:
                return
            self.threshold /= 100.0
            if not parts.pop(0) and not parts:
                return
            raise ValueError("bad threshold value")

        # making recursion optional and not the default is a "to do .. maybe" action!
        # elif a in('-r', '--recurse'):
        #    self.recurse = 1
        #    continue
        if a in ('-h', '--help'):
            print("utility to check images within a PDF and optionally 'fix' them.\n"
                 "syntax:  pdf_walker.py [options] [paths]\n"
                  "special options for pdf_walker.py are: (shown quoted but must be entered unquoted!)\n"
                  "'--threshold'   or equivalently '-t'\n"
                  "means interpret the next argument as the black threshold for conversion to mono ('lineart')\n"
                  "this may be entered as e.g. 0.6 or equivalently 60%. The default is 0.5 (50%)\n"
                  "'--resolution'   or equivalently '-r'\n"
                  "means interpret the next argument as the resolution to use. The default is 300.\n"
                  )
        Walker.process_keyword_arg(self, a)

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
                if not self.fix:
                    continue
                # This file is quite possibly created by 'xsane' which uses in-line data not embedded objects
                # for scan images. While not wrong, this has been known to give problems with e.g. poppler
                # whose logic used to assume that in-line images are always very small (?not 100% sure of this story).
                # anyway, they are easily corrected:
                #
                call("pdf2ps %s %s" % (self.shl_pathname, self.ps_filename), shell=True)
                call("ps2pdf %s %s" % (self.ps_filename, self.shl_pathname), shell=True)
                return True
            if field['color']!='gray' or int(field['bpc'])!=1:
                self.vprint(1, "%s is %u bit(s) %s (not 1 bit gray)" % (self.shl_pathname, int(field['bpc']), field['color']))
                if not self.fix:
                    continue
                # So we want to convert a PDF's image from e.g RGB or 8-bit grey to one-bit grey (=bivalue=B/W=lineart).
                # I'm not really happy with this 'ghostscript approach - not least because you often need to change
                # .../share/ghostscript/policy.xml' before it will work!
                # N.B. This is unnecessarily complicated. 'gs' can convert a multi-page PDF in one go.
                # See 'oddments/pdf_compact.py'.
                if not fixed_tifs:
                    repair_cmd = ('gs -q -dNOPAUSE -dBATCH -dUseCropBox -sOutputFile=temp_%d.tif' +
                           ' -r%u -sDEVICE=tiffg4 -c "{ %.2f gt { 1 } { 0 } ifelse} settransfer" -f '
                            % (self.resolution, self.threshold)
                                  +  self.shl_pathname)
                     #    ' -c "{ .5 gt { 1 } { 0 } ifelse} settransfer" -f %s' % self.shl_pathname)
                    self.vprint (1, "repair_cmd=", repair_cmd)
                    call(repair_cmd, shell=True)
                fixed_tifs.append('temp_%d.tif' % (1+len(fixed_tifs)))
                continue
                #call("convert %s -monochrome -threshold 50 %s" % (self.shl_pathname, self.tmp_pdf_filename), shell=True)
                # unfinished!
                #call("cp %s %s"  % (self.tmp_shl_pathname, self.shl_pathname), shell=True)
            self.vprint(2, "good image encountered")
        if fixed_tifs:
            reunite_cmd = 'convert ' + ' '.join(fixed_tifs)+ ' ' + self.shl_pathname
            self.vprint(1, "reunite_cmd=", reunite_cmd)
            call(reunite_cmd, shell=True)
            return True
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
