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
    sExtra = ''

    def process_keyword_arg(self, a):
        if a in ('-p', '--prefix'):
            prefix = sys.argv.pop(0)
            return a
        if a in ('-r', '--rotated'):
            self.sExtra += f'--angle {self.next_arg("180")}'
            return a
        if a in ('-s', '--scale'):
            self.sExtra += f'--scale {self.next_float_arg("90%")}'
            return a
        if a in ('-h', '--help'):
            print("utility to reduce letter-size PDF's to A4 size.\n"
                 "syntax:  pdf_walker.py [options] [paths]\n"
                  "special options for pdf_walker.py are: (shown quoted but must be entered unquoted!)\n"
                  "'--prefix'   or equivalently '-p'\n"
                  "  means interpret the next argument as the prefix to apply when deriving thte output filename.\n"
                  "'--rotate'   or equivalently '-r'\n"
                  "  means interpret the next argument as an angle to rotate in degrees (e.g. 180 for upside-down).\n"
                  "'--prefix'   or equivalently '-p'\n"
                  "  means interpret the next argument as the prefix to apply when deriving thte output filename.\n"
                  "'--scale'   or equivalently '-s'\n"
                  "  means interpret the next argument as the scaling to apply (in order to get nice but not too wide border).\n"
                  "this may be entered as e.g. 0.8 or equivalently 80%. The default is to apply no scaling\n"
                  )
        return Walker.process_keyword_arg(self, a)


    def handle_item(self, root_, item_, is_dir):
        print(root_, item_)
        Walker.handle_item(self, root_, item_, is_dir)
        stem_, ext_ = os.path.splitext(item_)
        if is_dir or ext_.lower() not in ('.pdf',) or stem_.startswith(self.prefix_):
            return None
        old_filename = os.path.join(root_, item_)
        new_filename = os.path.join(root_, self.prefix_ + item_).replace('-.', '.')

        # cmd = f"pdfjam --outfile {new_filename}  --angle 180 --paper a4paper --scale {self.scale_} {old_filename}"
        cmd = f"pdfjam --outfile {new_filename}  --paper a4paper {self.sExtra} {old_filename}"
        print("converting this %s file with a one-liner: '%s'" %(ext_, cmd))
        os.system(cmd)

if __name__ == '__main__':
    JamToA4().main()

