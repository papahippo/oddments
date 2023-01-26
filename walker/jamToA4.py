#!/usr/bin/python3
"""
This is a hastily reworked version of LetterToA4.py, whose comment is retained below.
It now uses the 'Walker' class; see 'walker.py' in this diretory.
I scanned some music which was in "letter" format with little or no margins. With careful placement of the orignal
on the scanner I ensured no part of the image was lost... but I need to distribute the music in A4 with margins
 (for filing in ring-binders).
typically, we create subprocesses to run commands like:
pdfjam --scale 0.95 --a4paper --latex /usr/bin/lualatex Singin-Sax-Partituur.pdf
"""
import sys,subprocess
from walker import Walker


class JamToA4(Walker):

    prefix_ = 'a4-'
    myExts = ('.pdf',)

    argsExtra = ()

    def process_keyword_arg(self, a):
        if a in ('-p', '--prefix'):
            prefix = sys.argv.pop(0)
            return a
        if a in ('-r', '--rotated'):
            self.argsExtra += ('--angle', self.next_arg("180"))
            return a
        if a in ('-s', '--scale'):
            self.argsExtra += ('--scale', str(self.next_float_arg("90%")))
            return a
        if a in ('-o', '--offset'):
            self.argsExtra += ('--offset', f"{self.next_arg('0mm')} {self.next_arg('0mm')}")
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
                  "'--offset'   or equivalently '-o'\n"
                  "  means interpret the next two arguments as the x and y offset to apply.\n"
                  "this may be entered as e.g. ... 10mm 0mm ... (I'm not sure what other units are allowed.\n"
                  )
        return Walker.process_keyword_arg(self, a)


    def handle_item(self, root_, item_, is_dir):
        if is_dir or not Walker.handle_item(self, root_, item_, is_dir):
            return

        cmd_n_args = (("pdfjam", "--outfile", self.full_dest_name,  '--paper', '--a4paper')
                                + ('--latex', '/usr/bin/lualatex')
                                + self.argsExtra + (self.full_source_name,))
        self.vprint(1, f"converting this file with command and args: {cmd_n_args}")
        subprocess.run(cmd_n_args)

if __name__ == '__main__':
    JamToA4().main()

