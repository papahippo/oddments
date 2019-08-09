#!/usr/bin/env python3
import os, sys
import curses
from time import sleep

from subprocess import (run, PIPE)
class GPIO_pin:
    """
This is a horribly inefficient stand-in to use until I get a decent gpio access library working on
my orange pi one.
    """
    def __init__(self, num):
        self.num = num
        self.exported_name = '/sys/class/gpio/gpio%d' % num

    def export(self, sDirection=None, only_if_nec=True):
        if not (only_if_nec and os.path.exists(self.exported_name)):
            run('echo %d > /sys/class/gpio/export' % self.num, shell=True, stdout=PIPE)
        if sDirection:
            self.set_direction(sDirection)

    def set_direction(self, sDirection):
        run('echo %s > %s/direction' % (sDirection, self.exported_name), shell=True, stdout=PIPE)

    def get(self):
        cp = run("cat %s/value", shell=True, stdout=PIPE)
        return cp.stdout[0]==b'1\n'

    def set(self, val):
        run('echo %d > %s/value' % (int(val), self.exported_name), shell=True, stdout=PIPE)

pinC4 = GPIO_pin(68)
pinC7 = GPIO_pin(71)
for pin in  (pinC4, pinC7):
    pin.export('out')

def main():
    stdscr = curses.initscr()
    curses.cbreak()
    stdscr.keypad(1)

    stdscr.addstr(0, 10, "Hit 'q' to quit")
    stdscr.refresh()

    pinC4.set(0)
    key = ''
    while key != ord('q'):
        key = stdscr.getch()
        stdscr.addch(20, 25, key)
        stdscr.refresh()
        if key == ord('0'):
            stdscr.addstr(2, 20, "set PC4 low")
            pinC4.set(0)
        elif key == ord('1'):
            stdscr.addstr(2, 20, "set PC4 high")
            pinC4.set(1)
        else:
            stdscr.addstr(3, 20, "Huh?")

def old_main():
    pinC4.set(0)
    pinC7.set(0)
    sleep(0.02)
    pinC4.set(1)
    sleep(0.01)
    pinC7.set(1)
    sleep(0.01)

if __name__=='__main__':
    main()
