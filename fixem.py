#!/usr/bin/python
"""
quicky to correct an image that was scanned in at a slight angle.
"""
from PIL import Image
import sys

prog = sys.argv.pop(0)
werk_naam = sys.argv.pop(0) if sys.argv else "Vivaldi Zomer"
print(f"running '{prog}' to rescale sheet music pages and convert them to PDFs")
for stem in (1, 2, 3, 4):
    partij_naam = f"{werk_naam}-{stem}"
    print(f"{stem=}")
    bladzijde_dict = {}
    for bladzijde_index in ('a', 'b'):
        bladzijde_naam = f"{partij_naam}{bladzijde_index}.jpg"
        print(f"\treading: {bladzijde_naam=}")
        A4_PORTRAIT = (595, 842)
        bladzijde_img = Image.open(bladzijde_naam).resize(A4_PORTRAIT) # , reducing_gap=1.0)  # , resample=Image.Resampling.BICUBIC)
        bladzijde_dict[bladzijde_index] = bladzijde_img
    PDF_naam = f"{partij_naam}.pdf"
    print(f"\twriting: {PDF_naam=}")
    bladzijde_dict['a'].save(PDF_naam, save_all=True, append_images=(bladzijde_dict['b'],))
