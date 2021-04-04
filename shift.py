#!/usr/bin/python3
"""
select left hand fingering for cello. Send corresponding note
to output port... and ad hoc variations on that theme!
"""
import sys, os, time, keyboard


def main():
    prev = False
    count = 0
    for i in range(500):
        pressed = keyboard.is_pressed('shift')
        if pressed == prev:
            count +=1
        else:
            if not pressed:
                print (count, end=' ')
            count = 0
        prev = pressed
        time.sleep(0.02)
if __name__=="__main__":
    main()
