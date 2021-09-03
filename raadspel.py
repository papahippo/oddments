#!/usr/bin/python3
"""
The old-fashioned conjuring trick, whereby the contestant must choose a number and say which
lists his chosen number appears in, whereupon you instantly tell him which number it is.
This script just prints out the lists; the game works off-line!
Output is to stdout, so you will usually want to redirect to a file, e.g.:
        python3 raadspel.py >raadsel.out
"""
from collections import OrderedDict
MAX_BITS = 10  # overkill!
MAX_NUMBER = 100  # 63 or 127 might be more logical but might give the game away too easily!


def main():
    # using an (ordered) dictionary is more usually associated with sparse lists than the dense one we'll
    # be creating, but it avoids potential pitfals when declaring lists of lists in python.
    #
    lijsten = OrderedDict()

    # Accumulate numbers with bit 0, 1, ... set into respective lists:
    #
    for i in range(1, 1+MAX_NUMBER):
        i2 = i  # a copy to mess around with
        for j in range(MAX_BITS):
            if i2 & 1:  # if bit j of i is set...
                lijsten.setdefault(j, []).append(i)
            i2 >>=1  # and the next bit, please!
            if not i2:
                break  # a minor optimisation

    for j, l in lijsten.items():
        print(f"Lijst {chr(ord('A')+j)}\n=======")

        # print 20 per line with margin for conveniently folding to reveal list titles and
        # first number of each list (1, 2, 4, ...) but not much else:
        #
        print(*[("  " if k % 20 else '\n  ') + f"{i:<3}" for k, i in enumerate(l)])
        print('\n')


if __name__ == "__main__":
    main()
