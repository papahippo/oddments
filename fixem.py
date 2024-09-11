#!/usr/bin/python
"""
quicky to correct an image that was scanned in at a slight angle.
"""
from PIL import Image
import sys

prog = sys.argv.pop(0)
thresh = int(sys.argv.pop(0)) if sys.argv else 235 # default

img = Image.open("./images/Vivaldi Zomer-1a.jpg")
fn = lambda x : 255 if x > thresh else 0
bw = img.convert('L').point(fn, mode='1')
bw.save('./images/bw.pdf')
img.save('./images/rgb.pdf')

if 0:
    im_new = im.rotate(-3.2, expand=True, fillcolor="white")
    im_new.save('./images/im_new.png', 'png')
    im_mono = im_new.convert('1')
    im_mono.save('./images/im_mono.png', 'png')
