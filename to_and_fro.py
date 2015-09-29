#/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 17:59:40 2015 in answer to the question on Linked-in:
LIST REORDER

HI GUYES
I AM A VERY BRGINNER IN PYTHON AND I HAVE A SMALL QUESTION :
IF I HAVE A LIST OF STRINGS AND I WANT TO REARRANGE IT BY TAKING THE VERY Ist ELEMENT THEN THE VERY LAST ONE , THEN THE SECOND FROM THE BEGINNING AND THE SECOND FROM THE END AND SO ON ..
WOULD YOU PLEASE GUIDE ME
THANKS
@author: Larry Myerscough (aka papahippo)
"""

def to_and_fro(ss):
    """
    'sort' a sequence (e.g. a list) of strings by taking 1st, then last,
    then 2nd, then last-but-one and so on.
    """
    ss = list(ss)  # make sure we have a list; don't change caller's original.
    ss_new = [] # start our answer as an empty list
    while ss:   # i.e. until there's no more left to take
        ss_new.append(ss.pop(0)) # take one from start:
        if ss:
            # at least one left so now take one from end:
            ss_new.append(ss.pop())
            # or more explicit but equivalent: ss_new.append(ss.pop(-1))
    return ss_new
    
# Above this line is the actual function.
# Below this line is all test code.
if __name__ == '__main__':
    for list_size, reason in ((0, 'empty'),
                              (4, 'even-sized'),
                              (7, 'odd-sized')):
        orig_seq = ["    case '%s' string #%d" %(reason, i+1)
                        for i in xrange(list_size)]
        sorted_seq = to_and_fro(orig_seq)
        print ("\n\ncase %s" % reason)
        for (which, when) in ((orig_seq, "before"),
                              (sorted_seq, "after")):
            print ("\n  %s" % when)
            print ("\n".join(which))

        