import curses
import os

def main(win):
    win.nodelay(True)
    key=""
    win.clear()
    win.addstr("Detected key:")
    while 1:
        try:
           key = win.getkey()
           win.clear()
           win.addstr("Detected key:")
           win.addstr(str(key)+str(type(key)) )
           if key == os.linesep:
              break
           elif key=='KEY_LEFT':
              win.addstr('hurrah!')
        except Exception as e:
           # No input
           pass

curses.wrapper(main)
