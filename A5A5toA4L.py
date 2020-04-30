#!/usr/bin/env python3
import fitz, os

from walker import Walker

class A5A5toA4L(Walker):

    name_ =  "2xA5 landscape (on 1 A4 page) to 2 A4 landscape pages converter"
    tag_ = '-A4L'
    lower_only = 0
    upper_only = 0

    def process_keyword_arg(self, a):
        if a in ('-L', '--lower-only'):
            self.lower_only += 1
            return a
        if a in ('-U', '--upper-only'):
            self.upper_only += 1
            return a
        if a in ('-h', '--help'):
            print("utility to convert 1 or 2 A5L images on a A4P page to separate A$ landscape images\n"
                "syntax:  A5A5toA4L [options] [paths]\n"
                  "special options for A5A5toA4L are (shown quoted but must be entered unquoted!):\n"
                  "'--upper-only'   or equivalently '-U'\n"
                  "'--lower-only'   or equivalently '-L'\n"
                  )
        return Walker.process_keyword_arg(self, a)

    def handle_item(self, root_, item_, is_dir):
        print(root_, item_)
        Walker.handle_item(self, root_, item_, is_dir)
        stem_, ext_ = os.path.splitext(item_)
        if is_dir or ext_.lower() not in ('.pdf',) or stem_.endswith(self.tag_):
            return None
        print(f'{root_}/{item_}')
        src = fitz.open(f'{root_}/{item_}')
        dest = fitz.open()  # output initally empty!
        for spage in src:  # for each page in input
            xref = 0  # force initial page copy to output
            r = spage.rect  # input page rectangle
            d = fitz.Rect(spage.CropBoxPosition,  # CropBox displacement if not
                          spage.CropBoxPosition)  # starting at (0, 0)
            # --------------------------------------------------------------------------
            # example: cut input page into 2 x 2 parts
            # --------------------------------------------------------------------------
            rTop = r - (0, 0, 0, r.height * 0.5)
            rBottom = r + (0, r.height * 0.5, 0, 0)

            for rx in [rect for rect, exclude in
                       ((rTop, self.lower_only), (rBottom, self.upper_only)) if not exclude]:
                rx += d  # add the CropBox displacement
                page = dest.newPage(-1,  # new output page with rx dimensions
                                   width=r.height,  # r.width,
                                   height=r.width)  # r.height)
                #        width = rx.width,
                #        height = rx.height)
                xref = page.showPDFpage(page.rect,  # fill all new page with the image
                                        src,  # input document
                                        spage.number,  # input page number
                                        clip=rx,  # which part to use of input page
                                        # rotate = 90.0,
                                        reuse_xref=xref)  # copy input page once only

        # that's it, save output file
        dest.save(f"{stem_}{self.tag_}{ext_}",
                 garbage=4,  # eliminate duplicate objects
                 deflate=True)  # compress stuff where possible
        return True


if __name__ == '__main__':
    A5A5toA4L().main()
