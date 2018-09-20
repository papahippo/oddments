#/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 17:59:40 2015
@author: Larry Myerscough (aka papahippo)
"""

def muple(t, l):
    """
    simple function to show how lists can be manipulated (if that's what you
    expect - otherwise 'mutilated' may be a better word) but tuples can't via called functions.
    """
    print ("at start of function:", t, l)
    t*=2
    l*=2
    print ("at end of function:", t, l)

# Above this line is the actual function.
# Below this line is all test code.
if __name__ == '__main__':
    t = (1,2)
    l = [1, 2]
    print ("before function call:", t, l)
    muple(t, l)
    print ("after function call:", t, l)

        