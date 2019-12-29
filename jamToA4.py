#!/usr/bin/python3
"""
This is a hastily reworked version of LetterToA4.py, whose comment is retained below.
It now uses the 'Walker' class; see 'walker.py' in this diretory.
I scanned some music which was in "letter" format with little or no margins. With careful placement of the orignal
on the scanner I ensured no part of the image was lost... but I need to distribute the music in A4 with margins
 (for filing in ring-binders).
"""
import sys,os
from walker import Walker


class JamToA4(Walker):

    prefix_ = 'a4-'
    scale_ = 0.90

    def process_keyword_arg(self, a):
        if a in ('-p', '--prefix'):
            prefix = sys.argv.pop(0)
        if a in ('-s', '--scale'):
            parts = sys.argv.pop(0).split('%')
            self.scale_ = float(parts.pop(0))
            if not parts:
                return
            self.scale_ /= 100.0
            if not parts.pop(0) and not parts:
                return
            raise ValueError("bad threshold value")
        if a in ('-h', '--help'):
            print("utility to reduce letter-size PDF's to A4 size.\n"
                 "syntax:  pdf_walker.py [options] [paths]\n"
                  "special options for pdf_walker.py are: (shown quoted but must be entered unquoted!)\n"
                  "'--prefix'   or equivalently '-p'\n"
                  "means interpret the next argument as the prefix to apply when deriving thte outputp filename.\n"
                  "'--scale'   or equivalently '-s'\n"
                  "means interpret the next argument as the scaling to apply (in order to get nicew but not too wide border).\n"
                  "this may be entered as e.g. 0.8 or equivalently 80%. The default is 0.9 (90%)\n"
                  )
        Walker.process_keyword_arg(self, a)


    def handle_item(self, root_, item_, is_dir):
        print(root_, item_)
        Walker.handle_item(self, root_, item_, is_dir)
        stem_, ext_ = os.path.splitext(item_)
        if is_dir or ext_.lower() not in ('.pdf',) or stem_.startswith(self.prefix_):
            return None
        old_filename = os.path.join(root_, item_)
        new_filename = os.path.join(root_, self.prefix_ + item_).replace('-.', '.')

        # cmd = f"pdfjam --outfile {new_filename}  --angle 180 --paper a4paper --scale {self.scale_} {old_filename}"
        cmd = f"pdfjam --outfile {new_filename}  --paper a4paper --scale {self.scale_} {old_filename}"
        print("converting this %s files with a one-liner: '%s'" %(ext_, cmd))
        os.system(cmd)

if __name__ == '__main__':
    JamToA4().main()

