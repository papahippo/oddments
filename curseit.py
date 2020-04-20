import curses

screen = curses.initscr()
curses.noecho()
curses.curs_set(0)
screen.keypad(1)

while 1:
    screen.addstr("Press a key")
    key = screen.getch()
    if key == curses.KEY_LEFT:
        print("Left Arrow Key pressed")
    elif key == curses.KEY_RIGHT:
        print("Right Arrow Key pressed")
    else:
        print(key)