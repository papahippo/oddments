#!/usr/bin/python3
"""
The old-fashioned conjuring trick, whereby the contestant must say which lists his chosen
number appears in, whereupon you instantly tell him which number it is.
Output is to stdout, so you will usually want to redirect to a file, e.g.:
        python3 raadspel.py >raadsel.out
"""
MAX_LISTS = 10  # overkill!
MAX_NUMBER = 100  # 63 or 127 might be more logical but might give the game away too easily!


def main():
    # create (more than) enough empty lists to accommodate results:
    # (deviously codied to avoid reusing single list! (one of python's least loved features!)
    #
    lijsten = list(map(list, [()]*MAX_LISTS))  #

    # accumulate numbers with bit 0, 1, ... set into appropriate lists:
    #
    for i in range(1, 1+MAX_NUMBER):
        for j, l in enumerate(lijsten):
            if i & (1 << j):  # if bit j of i is set...
                l.append(i)

    for j, l in enumerate(lijsten):
        if not l:
            # if no number in range has this bit set, we're all done.
            break
        print(f"Lijst {chr(ord('A')+j)}\n=======")
        # print 20 per line with margin for conveniently folding to reveal list titles and
        # first number of each list (1, 2, 4, ...) but not much else:
        #
        print(*[("  " if k % 20 else '\n  ') + f"{i:<3}" for k, i in enumerate(l)])
        print('\n')


if __name__ == "__main__":
    main()
