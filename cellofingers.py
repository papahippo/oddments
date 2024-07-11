#!/usr/bin/python3
"""
select left hand fingering for cello. Send corresponding note
to output port... and ad hoc variations on that theme!
"""
import sys, os, time, random, signal
from terpsichore import *
import mido
from arghandler import ArgHandler


def program_pedals():
    # unbuffered reading of keyboard input in python is ... well not as straighforward as
    # I had hoped. So, I program my twin-pedal footswitch to generate (left) control-C =>KeyboardInterrupt
    # and (right) ENTER, both of which can be detected without too much jiggery-pokery.
    #
    return os.system("sudo footswitch -1 -m ctrl -k c -2 -k enter")


class TimeoutException(BaseException):
    pass


def handler(signum, frame):
    raise TimeoutException

signal.signal(signal.SIGALRM, handler)


def back_pedal(prompt='', timeout=None, obj=sys.stdin):
    """
Wait 'timeout' seconds (None => indefinitely) for action from footswitch.
returns True => left-pedal or False => right pedal or None => timeout.
    """
    if prompt:
        print(prompt)
    if timeout:
        signal.alarm(timeout)
    try:
        c = obj.read(1)
        answer = False
    except TimeoutException:
        # print("TimeoutException")
        answer = None
    except KeyboardInterrupt:
         # print("KeyboardInterrupt")
        answer = True

    if timeout:
        signal.alarm(0)
    # print(f"pedal returns <{answer}>")
    return answer

class CelloFingers(ArgHandler):
    strings = None
    play_time = 2.0
    before_secs = 0
    after_secs = 0
    midi_port = -1
    recap_time = False
    instrument = Instrument.cello
    instrument_name = 'Cello'

    def process_keyword_arg(self, a):
        if a in ('-I', '--instrument'):
            self.instrument_name = self.next_arg()
            self.instrument = instrument_by_name[self.instrument_name]
            return a
        if a in ('-s', '--strings'):
            self.strings = sys.argv.pop(0)
            return a
        if a in ('-b', '--before-secs'):
            self.before_secs = self.next_int_arg()
            return a
        if a in ('-a', '--after-secs'):
            self.after_secs = self.next_int_arg()
            return a
        if a in ('-m', '--midi-port'):
            self.midi_port= self.next_arg()  # more processing of this later!
            return a
        if a in ('-r', '--recap-time'):
            self.recap_time = self.next_float_arg()
            return a
        if a in ('-h', '--help'):
            print("utility/game to train recognizing of musical tones of instrument .\n"
                  " and playing them on the instrument\n"
                 "syntax:  cellofingers.py [options]\n"
                  "special options for cellofingers.py are: (shown quoted but can and should be entered unquoted in most cases!)\n"
                  "'--strings'     or equivalently '-s'\n"
                  "\tmeans interpret the next argument as letters referring to strings of the instrument, e.g. 'A' or 'AD'.\n"
                  "\n"
                  "'--instrument'     or equivalently '-i'\n"
                  "\tmeans interpret the next argument as an instrument name, e.g. 'cello' or 'string bass'.\n"
                  "\n"
                  "'--play-time'   or equivalently '-p'\n"
                  "\tmeans interpret the next argument as how many seconds (can be float) to sound the note for.\n"
                  "\n"
                  "'--before-secs'   or equivalently '-b'\n"
                  "\tmeans interpret the next argument as how many seconds (integer) to wait before revealing the 'answer'.\n"
                  "\n"
                  "'--after-secs'   or equivalently '-a'\n"
                  "\tmeans interpret the next argument as how many seconds (integer) to wait after revealing the 'answer'.\n"
                  "\n"
                  "'--midi-port'   or equivalently '-m'\n"
                  "\tmeans interpret the next argument as identifying which midi port to use. This may be\n"
                  "\tentered as a a string (this will tend to contain one of more space characters so it's handy to put singe quotes\n"
                  "\taround the name. Alternatively, a numerical index within the list of available mdidi iports may be entered.\n"
                  "\tThe default (-1) takes the last defined port which tends to relate to a midi synthesizedre if one has been congigured."
                  "\n"
                  "'--recap-time' or equivalently '-r'\n"
                  "\tmeans: before each note, play the previous note for this long (float, seconds) as a 'recap'.\n"
                  "\n"
                  )
        return ArgHandler.process_keyword_arg(self, a)

    def process_args(self):
        ArgHandler.process_args(self)

    def main(self):
        self.process_all_keyword_args()
        self.no_more_positional_args()

        program_pedals()

        try:
            self.midi_port = mido.get_output_names()[int(self.midi_port)]
        except ValueError:
            pass
        print(f"running '{self.program_name}' assuming fingers on '{self.strings}' string;using MIDI port '{self.midi_port}'")

        self.string_notes = self.instrument.get_string_notes(letters=self.strings)

        fingers_and_their_pitch_offsets = list(enumerate([0, 2, 3, 4, 5]))  # beginners only!

        with mido.open_output(self.midi_port, autoreset=True) as port:
            print(f"changing program to {self.instrument.midi_program} for instrument '{self.instrument}'")
            select_instrument_sound = mido.Message('program_change', program=self.instrument.midi_program, time=0)
            print(f"selecting MIDI program {self.instrument.midi_program}")
            port.send(select_instrument_sound)
            prev_pitch = None
            while 1:  # until a deliberate minor deluge of ^C's busts our signal handling!
                finger, pitch_offset = random.choice(fingers_and_their_pitch_offsets)
                the_string = random.choice(self.string_notes)
                pitch = the_string.GetPitch() + pitch_offset
                note = notes_by_Pitch[pitch][0]  # 0 => favour sharps over flats
                while 1: # i.e. until we move on to the next note via 'break'
                    if prev_pitch and self.recap_time:
                        port.send(mido.Message('note_on', note=prev_pitch))
                        time.sleep(self.recap_time)
                        port.send(mido.Message('note_off', note=prev_pitch))
                    port.send(mido.Message('note_on', note=pitch))
                    time.sleep(self.play_time)
                    port.send(mido.Message('note_off', note=pitch))
                    if back_pedal(prompt="which note? left= play it again, right or just wait = skip this note", timeout=self.before_secs):
                        continue  # True (ctl_C) means "don't tell me yet, repeat the same note"
                    print(f"\n{note}\n\nstring {the_string.real_name}, finger: {finger}  {note}",
                      f"interval={pitch-prev_pitch if prev_pitch else ''}")
                    if not back_pedal(prompt="left= let me try again, right or just wait = proceed to next note", timeout=self.after_secs):
                        break  # move on to produce another note
                prev_pitch = pitch
        print("That's all folks!!")

if __name__=="__main__":
    CelloFingers().main()
