# function requiring (still?) improvement!
def as_python_name(s):
    return  '_' + ''.join(tuple(c if (c.isalpha() or c.isnumeric()) else '_' for c in s))
