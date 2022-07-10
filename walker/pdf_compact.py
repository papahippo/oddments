#!/usr/bin/env python3
# WARNING: I have abandoned this approach 'for now'!
#
from PyPDF2 import PdfFileWriter, PdfFileReader
from PIL import Image

from walker import Walker

class Pdf_compact(Walker):

    name_ =  "converter of images embedded within a PDF to a more compact format"
    myExts = ('.pdf',)
    prefix_ = 'compact-'

    threshold_ = 50
    copies_ = 1

    def process_keyword_arg(self, a):
        if a in ('-t', '--threshold'):
            self.threshold = int(self.next_keyword_arg(50))
            return a
        if a in ('-h', '--help'):
            print("utility to convert images within a PDF to a more compact format\n"
                "syntax:  pdf_compact.py [options] [paths]\n"
                  "special options for pdf_compact are (shown quoted but must be entered unquoted!):\n"
                  "'--threshold'   or equivalently '-t'\n"
                  "means interpret the next argument as the black threshold for conversion to mono ('lineart')\n"
                  )
        return Walker.process_keyword_arg(self, a)

    def handle_item(self, root_, item_, is_dir):
        if is_dir or not Walker.handle_item(self, root_, item_, is_dir):
            return
        input = PdfFileReader(open(self.full_source_name, 'rb'), strict=False)
        output = PdfFileWriter()
        np = input.getNumPages()
        self.vprint(1, "input PDF contains %d page(s)" % np)
        for i in range(self.copies_):
            for page in [input.getPage(i) for i in range(0, input.getNumPages())]:
                xObject = page['/Resources']['/XObject'].getObject()

                for obj in xObject:
                    if xObject[obj]['/Subtype'] == '/Image':
                        size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                        data = xObject[obj].getData()
                        if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                            mode = "RGB"
                        else:
                            mode = "P"

                        if xObject[obj]['/Filter'] == '/FlateDecode':
                            img = Image.frombytes(mode, size, data)
                            img.save(obj[1:] + ".png")
                        elif xObject[obj]['/Filter'] == '/DCTDecode':
                            img = open(obj[1:] + ".jpg", "wb")
                            img.write(data)
                            img.close()
                        elif xObject[obj]['/Filter'] == '/JPXDecode':
                            img = open(obj[1:] + ".jp2", "wb")
                            img.write(data)
                            img.close()
                # bi_image.save(outputFileName)
                #samples = bi_image.tobytes()
                #rect = bi_image[0].rect
                #self.vprint(1, "rect =", rect)

        outCount = output.getNumPages()
        # outName =  f"{root_}/{self.prefix_}{self.stem_}{self.ext_}"  # ?? imgcount removed...
        output.write(open(self.full_output_name, 'wb'))
        print (f"written {outCount} pages to {self.full_output_name}")
        return True


if __name__ == '__main__':
    Pdf_compact().main()
