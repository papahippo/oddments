#!/usr/bin/python
"""
quicky to correct an image that was scanned in at a slight angle.
"""
from PIL import Image
im = Image.open("./images/Wim-duet-1.png")
im_new = im.rotate(-3.2, expand=True, fillcolor="white")
im_new.save('./images/im_new.png', 'png')
im_mono = im_new.convert('1')
im_mono.save('./images/im_mono.png', 'png')
