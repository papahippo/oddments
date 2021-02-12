#!/usr/bin/python3
from furl import furl
import sys, os


def main():
    prog = sys.argv.pop(0)
    patient = sys.argv.pop(0) if sys.argv else "http://192.168.2.39:8080/abc_music/tune/view/samples/voices_X4#back"
    print(f"let's see how I can manipulate'{patient}' using furl via '{prog}'")
    uo = furl(patient)
    print(uo.remove(path=['view', 'samples', 'voices_X4']).add(path=('list', 'samples')))


if __name__=='__main__':
    main()
