#!/usr/bin/env python3
# This was intended as a cleaner compacter approach to conversion of grey scale or RGB
# images within PDFs to lineart/bivalue than that afforded by 'pdf_walker.py'.
# WARNING: I have abandoned this approach 'for now'!
#
import sys, os, subprocess
from walker import Walker

class Pdf_compact(Walker):

    name_ =  "converter of images embedded within a PDF to more compact format"
    tag_ = '-compact'
    threshold = 0.5
    resolution = 300

    def process_keyword_arg(self, a):
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

        if a in ('-h', '--help'):
            print("utility to convert images within a PDF to a more compact format\n"
                "syntax:  pdf_compact.py [options] [paths]\n"
                  "special options for pdf_compact are (shown quoted but must be entered unquoted!):\n"
                  "'--threshold'   or equivalently '-t'\n"
                  "means interpret the next argument as the black threshold for conversion to mono ('lineart')\n"
                  "this may be entered as e.g. 0.6 or equivalently 60%. The default is 0.5 (50%)\n"
                  "'--resolution'   or equivalently '-r'\n"
                  "means interpret the next argument as the resolution to use. The default is 300.\n"
                  )
        Walker.process_keyword_arg(self, a)

    def handle_item(self, root_, item_, is_dir):
        self.vprint(1, root_, item_)
        Walker.handle_item(self, root_, item_, is_dir)
        stem_, ext_ = os.path.splitext(item_)
        if is_dir or ext_.lower() not in ('.pdf',) or stem_.endswith(self.tag_):
            return None
        repair_cmd = ('gs -q -dNOPAUSE -dBATCH -dUseCropBox -sOutputFile=%s/%s%s.pdf' %(root_, stem_, self.tag_) +
                      ' -r%u -sDEVICE=tiffg4 -c "{ %.2f gt { 1 } { 0 } ifelse} settransfer" -f '
                      % (self.resolution, self.threshold)
                      + self.shl_pathname)
        #    ' -c "{ .5 gt { 1 } { 0 } ifelse} settransfer" -f %s' % self.shl_pathname)
        self.vprint(1, "repair_cmd=", repair_cmd)
        subprocess.call(repair_cmd, shell=True)

        return True


if __name__ == '__main__':
    Pdf_compact().main()
