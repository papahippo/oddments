#/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 17:59:40 2015
@author: Larry Myerscough (aka papahippo)
"""

def muple(t):
    """
    simple function to show how tuples can be manipulated (if that's what you
    expect - otherwise 'mutilated' may be a better word) in called functions.
    """
    t*=2
    
# Above this line is the actual function.
# Below this line is all test code.
if __name__ == '__main__':
    t = (1,2)
    muple(t)
    print (t)

        