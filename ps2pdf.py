#!/usr/bin/env python3
import sys
import locale
import ghostscript

try:
    prog, input_ps_file, output_pdf_file = sys.argv
except ValueError:
    print("syntax:   ps2pdf.py <input_ps_file> <output_pdf_file>")
    sys.exit(999)
args = [
    prog,
    "-dCompatibilityLevel=1.4 ", "-q",
    "-dNOPAUSE", "-dBATCH", "-dSAFER",
    "-sDEVICE=pdfwrite",
    "-sstdout=%stderr",
    f"-sOutputFile={output_pdf_file}",
    f"-f{input_ps_file}"
]
print(f"using 'ghostscript' to convert {input_ps_file} to {output_pdf_file}")
# arguments have to be bytes, encode them
encoding = locale.getpreferredencoding()
args = [a.encode(encoding) for a in args]

ghostscript.Ghostscript(*args, stdout=open('ps2pdf.out', 'wb'), stderr=open('ps2pdf.err', 'wb'))
ghostscript.gs.exit(ghostscript.__instance__)
