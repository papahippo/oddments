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
    # The following statement is arguably unnecessary but has two advantages:
    # 1. It ensures that the function still works if e.g. a tuple is passed
    #    rather than a list; we need to be able to 'pop' elements.
    # 2. It avoids destroying the caller's list. The caller could work around
    #    such a 'feature' but it would nonetheless be bad style in my book.
    #
    ss = list(ss)
    ss_new = [] # start our answer as an empty list
    while ss:   # i.e. until there's no more left to take
        ss_new.append(ss.pop(0)) # take one from start:
        if ss:
            # at least one left so now take one from end:
            ss_new.append(ss.pop())
            # or more explicit but equivalent: ss_new.append(ss.pop(-1))
    return ss_new
    
# Above this line is the actual function.
# --------------------------------------------------------------
# Below this line is all test code.
if __name__ == '__main__':
    # I want to test with an empty list and with non-empty lists with odd and
    # even lengths in order to believe 'to_and_fro' really works ok:
    #
    for list_size, reason in ((0, 'empty'),
                              (4, 'even-sized'),
                              (7, 'odd-sized')):
        # I also want to test my claim that 'to_and_fro' works equally well for
        # lists and tuples.
        #
        for use_tuple in (False, True):
            # construct strings with easily recognizable order:
            #
            sequence_type_name = ('list', 'tuple')[use_tuple]
            orig_seq = ["    case '%s' using %s - string #%d"
                %(reason, sequence_type_name, i+1) for i in xrange(list_size)]
            
            # if one didn't need the original strings anymore, onecould assign
            # e.g seq = to_and_fro(seq); but we want to test that it is
            # possible to leave the original sequence unscathed.
            #
            if use_tuple:
                orig_seq = tuple(orig_seq)
            sorted_seq = to_and_fro(orig_seq)
            print ("\n\ncase %s (using %ss of strings)"
                   % (reason, sequence_type_name))
            for (which, when) in ((orig_seq, "original"),
                                  (sorted_seq, "to_and_fro sorted")):
                print ("\n  %s" % when)
                print ("\n".join(which))
