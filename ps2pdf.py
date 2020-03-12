#!/usr/bin/env python3
import sys
import locale
import ghostscript

args = [
    "ps2pdf",  # actual value doesn't matter
    "-dCompatibilityLevel=1.4 ", "-q",
    "-dNOPAUSE", "-dBATCH", "-dSAFER",
    "-sDEVICE=pdfwrite",
    "-sstdout=%stderr",
    "-sOutputFile=" + sys.argv[2],
    "-c", ".setpdfwrite",
    "-f", sys.argv[1]
]

# arguments have to be bytes, encode them
encoding = locale.getpreferredencoding()
#args = [a.encode(encoding) for a in args]
args = [a.encode('utf8') for a in args]

ghostscript.Ghostscript(*args)
ghostscript.gs.exit(ghostscript.__instance__)
