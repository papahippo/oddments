#!/usr/bin/env python3
import fitz, os

from walker import Walker

class A5A5toA4L(Walker):

    name_ =  "2xA5 landscape (on 1 A4 page) to 2 A4 landscape pages converter"
    prefix_ = 'A4L-'
    myExts = ('.pdf',)
    lower_only = False
    upper_only = False
    split = 0.5

    def process_keyword_arg(self, a):
        if a in ('-L', '--lower-only'):
            self.lower_only = True
            return a
        if a in ('-U', '--upper-only'):
            self.upper_only = True
            return a
        if a in ('-S', '--split'):
            self.split = self.next_float_arg(0.5)
            return a
        if a in ('-h', '--help'):
            print("utility to convert 1 or 2 A5L images on a A4P page to separate A$ landscape images\n"
                "syntax:  A5A5toA4L [options] [paths]\n"
                  "special options for A5A5toA4L are (shown quoted but must be entered unquoted!):\n"
                  "'--upper-only'   or equivalently '-U'\n"
                  "'--lower-only'   or equivalently '-L'\n"
                  "'--split'   or equivalently '-S'\n"
                  "means interpret the next argument as how far down the page to split the page.\n"
                  "this may be entered as e.g. 0.6 or equivalently 60%. The default is 0.5 (50%).\n"
                  "note that value other than 0.5 distort the vertical scaling of the output pages."
                  )
        return Walker.process_keyword_arg(self, a)

    def handle_item(self, root_, item_, is_dir):
        if is_dir or not Walker.handle_item(self, root_, item_, is_dir):
            return
        src = fitz.open(self.full_source_name)
        dest = fitz.open()  # output initally empty!
        for spage in src:  # for each page in input
            xref = 0  # force initial page copy to output
            r = spage.rect  # input page rectangle
            d = fitz.Rect(spage.CropBoxPosition,  # CropBox displacement if not
                          spage.CropBoxPosition)  # starting at (0, 0)
            # --------------------------------------------------------------------------
            # example: cut input page into 2 x 2 parts
            # --------------------------------------------------------------------------
            rTop = r - (0, 0, 0, r.height*(1-self.split))
            rBottom = r + (0, r.height*self.split, 0, 0)

            for rx in [rect for rect, exclude in
                       ((rTop, self.lower_only), (rBottom, self.upper_only)) if not exclude]:
                rx += d  # add the CropBox displacement
                page = dest.new_page(-1,  width=842, height=595) # = A4L
                                   #  #width=r.height,  # r.width,
                                   # height=r.width)  # r.height)
                #        width = rx.width,
                #        height = rx.height)
                xref = page.show_pdf_page(page.rect,  # fill all new page with the image
                                        src,  # input document
                                        spage.number,  # input page number
                                        clip=rx,  # which part to use of input page
                                        # rotate = 90.0,
                                        reuse_xref=xref)  # copy input page once only

        # that's it, save output file
        dest.save(self.full_dest_name,
                 garbage=4,  # eliminate duplicate objects
                 deflate=True)  # compress stuff where possible
        return True


if __name__ == '__main__':
    A5A5toA4L().main()
