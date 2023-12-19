#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" dive into music archive and perform maintenance or analysis or repair tasks on all PDFs
N.B. There is considerable overlap in functionality between this script and oddments/pdf_compact.py
... but I am wary of burning bridges just yet!"""

import sys, os, re
import subprocess

from walker import Walker

class PdfWalker(Walker):

    name_ = "PDF walker/fixer"
    ps_filename = '/tmp/pdf_fix.ps'
    tmp_pdf_filename = '/tmp/pdf_fix.pdf'
    fix = 0
    resolution = 600
    threshold = 0.85

    def process_keyword_arg(self, a):
        if a in ('-f', '--fix'):
            self.fix += 1
            return a
        if a in ('-r', '--resolution'):
            self.resolution = int(self.next_arg())
            return a
        if a in ('-t', '--threshold'):
            self.threshold = self.next_float_arg(0.5)
            return a

        # making recursion optional and not the default is a "to do .. maybe" action!
        # elif a in('-r', '--recurse'):
        #    self.recurse = 1
        #    continue
        if a in ('-h', '--help'):
            print("utility to check images within a PDF and optionally 'fix' them.\n"
                 "syntax:  pdf_walker.py [options] [paths]\n"
                  "\n"
                  "special options for pdf_walker.py are: (shown quoted but must be entered unquoted!)\n"
                  "\n"
                  "'--fix'   or equivalently '-f'\n"
                  "\tmeans don't just inspect but also fix the PDFs whre necessary.\n"
                  "\n"
                  "'--threshold'   or equivalently '-t'\n"
                  "\tmeans interpret the next argument as the black threshold for conversion to mono ('lineart')\n"
                  f"\tthis may be entered as e.g. 0.6 or equivalently 60%. The default is {self.threshold} ({int(self.threshold*100)}%)\n"
                  "\n"
                  "'--resolution'   or equivalently '-r'\n"
                  "\n"
                  "\tmeans interpret the next argument as the resolution to use. The default is 300.\n"
                  )
        return Walker.process_keyword_arg(self, a)

    def check_images(self, effort):
        proc = subprocess.run(('pdfimages', '-list', self.full_source_name), capture_output=True, timeout=5)
        out_lines = proc.stdout.decode(sys.stdout.encoding).split('\n')
        err_lines = proc.stderr.decode(sys.stderr.encoding).split('\n')
        if len(out_lines)<2:
            self.vprint(1, "not a proper PDF? %s" % self.shell_source_name)
            return None  # => no images
        headings = re.split(r'\s+', out_lines.pop(0))
        out_lines.pop(0)  # skip line with just hyphens
        if not out_lines:
            self.vprint(1, "no images in %s" % self.shell_source_name)
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
                self.vprint(1, "%s contains in-line or not ccitt-encoded image(s)" % self.shell_source_name)
                if not self.fix:
                    continue
                # This file is quite possibly created by 'xsane' which uses in-line data not embedded objects
                # for scan images. While not wrong, this has been known to give problems with e.g. poppler
                # whose logic used to assume that in-line images are always very small (?not 100% sure of this story).
                # anyway, they are easily corrected:
                #
                subprocess.run(('pdf2ps', self.full_source_name, self.ps_filename))
                subprocess.run(('ps2pdf', self.ps_filename, self.full_source_name))
                return True
            if field['color']!='gray' or int(field['bpc'])!=1:
                self.vprint(0, "%s is %u bit(s) %s (not 1 bit gray)" % (self.shell_source_name, int(field['bpc']), field['color']))
                if not self.fix:
                    continue
                # So we want to convert a PDF's image from e.g RGB or 8-bit grey to one-bit grey (=bivalue=B/W=lineart).
                # I'm not really happy with this 'ghostscript approach - not least because you often need to change
                # .../share/ghostscript/policy.xml' before it will work!
                # N.B. This is unnecessarily complicated. 'gs' can convert a multi-page PDF in one go.
                # See 'oddments/pdf_compact.py'.
                if not fixed_tifs:
                    repair_args = ('gs', '-q', '-dNOPAUSE',  '-dBATCH', '-dUseCropBox', '-sOutputFile=temp_%d.tif',
                           f'-r{self.resolution}', '-sDEVICE=tiffg4',
                           '-c', f"{{ {self.threshold:.2f} gt {{ 1 }} {{ 0 }} ifelse}} settransfer", '-f',
                           self.full_source_name)
                    self.vprint (1, "repair_args=", repair_args)
                    subprocess.run(repair_args)
                fixed_tifs.append('temp_%d.tif' % (1+len(fixed_tifs)))
                continue
            self.vprint(2, "good image encountered")
        if fixed_tifs:
            if 0:  # too slow and memory consuming
                reunite_args = ['convert',] + fixed_tifs + [self.full_source_name,]
                self.vprint(1, "reunite_args=", reunite_args)
                subprocess.run(reunite_args)
            else:
                combine_args = ['tiffcp',] + fixed_tifs + ['combibed.tif',]
                self.vprint(1, "combine_args=", combine_args)
                subprocess.run(combine_args)

                convert_args = ['tiff2pdf', '-o', self.full_source_name,'combibed.tif', ]
                self.vprint(1, "reunite_args=", convert_args)
                subprocess.run(convert_args)
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
        self.vprint (1, "%s is still not right after 'fix'." % self.shell_source_name)


if __name__ == '__main__':
    PdfWalker().main()
