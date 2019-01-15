#!/usr/bin/env python3
import sys, os
from PyPDF2 import PdfFileWriter, PdfFileReader


class PDF_Bundle:
    input_name = 'How_to_train_your_dragon-partijen-A4L.pdf'
    output_name_stem = 'How_to_train_your_dragon-'
    output_name_suffix = '.pdf'
    division = [
        ('Sop_Sax', 2),
        ('Alt_Sax_1', 2),
        ('AltSax_2', 2),
        ('Tenor_Sax', 2),
        ('Bari_Sax', 2),
        ('Flugelhorn_1', 2),
        ('Flugelhorn_2', 2),
        ('Flugelhorn_3', 2),
        ('Horn_in_F_1', 2),
        ('Horn_in_F_2', 2),
        ('Horn_in_F_2-x', 2),
        ('Horn_in_F_2-y', 2),
        ('Trumpet_1', 2),
        ('Trumpet_2', 2),
        ('Trumpet_3', 2),
        ('Trombone_1', 2),
        ('Trombone_1', 2),

    ]
    def main(self):
        input = PdfFileReader(open('%s' %(self.input_name), 'rb'))
        output = None
        n = input.getNumPages()
        for i in range(0, n):
            p = input.getPage(i)
            if not output:
                try:
                    part_name, n_pages_per_part = self.division.pop(0)
                except IndexError:
                    print ("ran out of division specifiers after %d of %d pages!" % (i, n))
                output = PdfFileWriter()
            output.addPage(p)
            if output.getNumPages() == n_pages_per_part:
                output_name = '%s%s%s' % (self.output_name_stem, part_name, self.output_name_suffix)
                output.write(open(output_name, 'wb'))
                print ("written %d pages to '%s'." % (output.getNumPages(), output_name))
                output = None
        #if output:
        #    print("shortchagnged last part (%s): %d,%d" % (part_name, output.getNumPages(), n_pages_per_part))

        return True


if __name__ == '__main__':
    PDF_Bundle().main()
