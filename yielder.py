#!/usr/bin/python3
"""
expermiental stuff to use my phileas stuff outside cherrpy context without
leading to horrible code!
"""
from phileas import _html40 as h

def stringify(hobj):
    """
    This may become a 'str' method of the element class but let's not get ahead of ourselves!
    """
    return ''.join(str(el) for el in hobj)

def main():
    hit = (h.html | ("\n",
              h.head | (
              ),
              h.body | (
                  h.p | '1st para',
                  h.p | '2nd para',
              )
          )
    )
    print(stringify(hit))

if __name__ == '__main__':
    main()
