#!/usr/bin/env python3
"""
Experimental work for ultimate employment within cherrypy web page!
"""
import os, sys
# from entity.company import OutgoingItem


class ImportPath(object):
    """
    Step into a directory temporarily.
    """

    def __init__(self, path):
        self.import_path = path

    def __enter__(self):
        sys.path.insert(0, self.import_path)

    def __exit__(self, *args):
        sys.path.pop(0)


def main():
    with ImportPath('/home/gill/Hippos/_2018/Acco2018/Q1/'):
        import outgoings
        print (outgoings)
        print("hello?")
        outgoings.OutgoingItem.export()


if __name__=='__main__':
    main()