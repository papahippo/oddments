#!/usr/bin/python3
import sys, subprocess
def main():
    print(sys.argv[1:])
    return subprocess.call(sys.argv[1:])
if __name__ =='__main__':
    sys.exit(main())
