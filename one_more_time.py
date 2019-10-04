import sys

class Extra:
    def __init__(self, myIterator, extra=None, *more_extras):
        self.myIterator = myIterator
        self.extra_values = list((extra,)+more_extras)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return next(self.myIterator)
        except StopIteration:
            try:
                return self.extra_values.pop(0)
            except IndexError:
                raise StopIteration

def main():
    this_file = sys.argv[-1]
    print(this_file)
    this_file_plus = Extra(open(this_file, 'r')) # , "one more line!\n", "and another!\n")
    for line in this_file_plus:
        print(line and line.strip() or "default extra!")

if __name__ == "__main__":
    main()
