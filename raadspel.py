#!/usr/bin/python3
"""
The old-fashioned conjuring trick, whereby the contestant must say which lists his chosen
number appears in, whereupon you instantly tell him which number it is.
"""
MAX_LISTS = 10  # overkill!
MAX_NUMBER = 100  # 63 or 127 might be more logical but might give the game away too easily.


def main():
    lijsten = [[] for _ in range(MAX_LISTS)]  # long-winded coding to avoid reusin gsingle list!

    # accumulate numbers with bit 0, 1, ... set into separate lists:
    for i in range(1, 1+MAX_NUMBER):
        for j, l in enumerate(lijsten):
            if i & (1 << j):
                l.append(i)

    for j, l in enumerate(lijsten):
        if not l:
            break
        print(f"Lijst {chr(ord('A')+j)}\n=======")
        print(*[("  " if k % 20 else '\n') + f"{i:<4}" for k, i in enumerate(l)])
        print('\n')


if __name__ == "__main__":
    main()
