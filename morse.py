#!/usr/bin/python3
"""
morse code detection.
This is ultimately intended for use with a button connected to an 'orange pi'
(other fruits are available!) but this protoype works with the 'alt' key of a PC.
"""
import sys, os, time, keyboard


class Morse:
    class Error(BaseException):
        pass

    class Break(BaseException):
        '''
        treat a serously oversized pulse as a 'break condition' (analogous to the treatment of
        successive zero bits past the stop bit on RS232 communication.
        '''
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
    ignore_first = 1
    dot_nax = 4
    dash_max = 12
    within_char_max = 12
    key_to_poll = 'alt'  # previously 'shift'

    def init_dicts(self):
        self.morse_to_char = {}
        self.char_to_morse = {}
        for (char, morse) in self.char_and_morse:
            self.morse_to_char[morse] = char
            self.char_to_morse[char] = morse

    def __init__(self):
        self.init_dicts()

    def poll(self):
        return keyboard.is_pressed(self.key_to_poll)

    def wait_for(self, sense, how_long):
        for i in range(how_long):
            time.sleep(self.secs_resolution)
            if self.poll()!=sense:
                continue
            if i < self.ignore_first:
                print ('<', end=" ")
                continue
            print(i if sense else -i, end=" ")
            return True

        else: # completed all iterations without returning!
            return False

    def get_dot_or_dash(self):
        if not self.wait_for(True, self.within_char_max):
            return None  # => end of character
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
            if s_dot_dash == '':
                continue
            print(f"\n{s_dot_dash:>6}", end=' ')
            try:
                return self.morse_to_char[s_dot_dash]
            except KeyError:
                raise Morse.Error(f"invalid morse code {s_dot_dash}")

    def print_table(self):
        for i, (char, morse_code) in enumerate(self.char_and_morse):
            print(f"{char} = {morse_code:6}", end='  ' if (i+1) % 4 else '\n')
        print()

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
            print(f' = {my_char}')
        if my_char == '?':
            morse.print_table()


if __name__ == "__main__":
    main()
