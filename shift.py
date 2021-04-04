#!/usr/bin/python3
"""
select left hand fingering for cello. Send corresponding note
to output port... and ad hoc variations on that theme!
"""
import sys, os, time, keyboard


class Morse:
    class Break(BaseException):
        pass

    class Error(BaseException):
        pass

    char_and_morse = [
        ('A', '.-'), ('B', '-...'), ('C', '-.-.'), ('D', '-..'), ('E', '.'), ('F', '..-.'),
        ('G', '--.'), ('H', '....'), ('I', '..'), ('J', '.---'),  ('K', '-.-'), ('L', '.-..'),
        ('M', '--'), ('N', '-.'), ('O', '---'), ('P', '.--.'), ('Q', '--.-'), ('R', '.-.'),
        ('S', '...'), ('T', '-'), ('U', '..-'), ('V', '...-'), ('W', '.--'), ('X', '-..-'),
        ('Y', '-.--'), ('Z', '--..'), ('.', '.-.-.-'), (',', '--..--'), ('?', '..--..'),
        ('1', '.----'), ('2', '..---'), ('3', '...--'), ('4', '....-'), ('5', '.....'),
        ('6', '-.....'), ('7', '--...'), ('8', '.---..'), ('9', '----.'), ('0', '-----'),
    ]
    secs_resolution = 0.03
    dot_nax = 4
    dash_max = 12
    within_char_max = 12

    def init_dicts(self):
        self.morse_to_char = {}
        self.char_to_morse = {}
        for (char, morse) in self.char_and_morse:
            self.morse_to_char[morse] = char
            self.char_to_morse[char] = morse

    def __init__(self):
        self.init_dicts()

    def poll(self):
        return keyboard.is_pressed('shift')

    def wait_for(self, sense, how_long, ignore_first=0):
        for i in range(how_long):
            time.sleep(self.secs_resolution)
            if self.poll()!=sense:
                continue
            if i < ignore_first:
                print ('<', end=" ")
                continue
            print(i if sense else -i, end=" ")
            return True

        else: # completed all iterations without returning!
            return False

    def get_dot_or_dash(self):
        if not self.wait_for(True, self.within_char_max):  # , ignore_first=1): # tune debounce later!
            return None # => end of character
        if self.wait_for(False, self.dot_nax):
            return '.'
        if self.wait_for(False, self.dash_max - self.dot_nax):
            print('+', end=" ")  # to distinguish in debug output
            return '-'
        raise Morse.Break('very long key press')

    def get_s_dot_dash(self):
        s_dot_dash = ''
        for i in range(8):  # more than max 'bits' per morse char
            dot_or_dash = self.get_dot_or_dash()
            if not dot_or_dash:
                return s_dot_dash
            s_dot_dash += dot_or_dash
        else:
            raise Morse.Error(f"more than 8 bits!?")

    def get_char(self):
        while 1:
            s_dot_dash = self.get_s_dot_dash()
            if s_dot_dash != '':
                print(s_dot_dash, end=' ')
                try:
                    return self.morse_to_char[s_dot_dash]
                except KeyError:
                    raise Morse.Error(f"invalid morse code {s_dot_dash}")

    def print_table(self):
        for i, (char, morse) in enumerate(self.char_and_morse):
            print(f"{char}={morse:6}", end='  ' if (i+1) % 4 else '\n')
def main():
    morse = Morse()
    while 1:
        my_char = None
        try:
            my_char = morse.get_char()
        except Morse.Error as me:
            print(f"morse code errr: {me}")
        except Morse.Break as mb:
            print(f"{mb}:\n ... treat this as regular doorbell push!")
        if my_char is not None:
            print(my_char)
        if my_char == '?':
            morse.print_table()

if __name__=="__main__":
    main()
