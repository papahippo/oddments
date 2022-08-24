#!/usr/bin/python3
"""
select left hand fingering for cello. Send corresponding note
to output port... and ad hoc variations on that theme!
"""
import sys, os, time, random, signal
from terpsichore import *
import mido
from large import Large


def program_pedals():
    # unbuffered reading of keyboard input in python is ... well not as straighforward as
    # I had hoped. So, I program my twin-pedal footswitch to generate (left) control-D = end-of-file
    # and (right) ENTER, both of which can be detected without too much jiggery-pokery.
    #
    return os.system("sudo footswitch -1 -k enter -2 -m ctrl -k c")


class TimeoutException(BaseException):
    pass


def handler(signum, frame):
    raise TimeoutException

signal.signal(signal.SIGALRM, handler)


def pedal(prompt='', timeout=None, obj=sys.stdin):
    """
Wait 'timeout' seconds (None => indefinitely) for action from footswitch.
returns '' => left-pedal or '\n' => right pedal or None => timeout.
    """
    if prompt:
        print(prompt)
    if timeout:
        signal.alarm(timeout)
    try:
        c = obj.read(1)
        answer = True
    except TimeoutException:
        answer = None
    except KeyboardInterrupt:
        answer = False

    if timeout:
        signal.alarm(0)
    print(f"pedal returns <{answer}>")
    return answer

class CelloFingers(Large):
    open_strings = 'D'
    user_secs = 3.0
    midi_port = -1

    def process_keyword_arg(self, a):
        if a in ('-S', '--open-string'):
            self.open_strings = sys.argv.pop(0)
            return a
        if a in ('-U', '--user-time'):
            self.user_secs = self.next_float_arg()
            return a
        if a in ('-P', '--midi-port'):
            self.midi_port= self.next_arg()  # more processing of this later!
            return a
        if a in ('-h', '--help'):
            print("utility to reduce letter-size PDF's to A4 size.\n"
                 "syntax:  pdf_walker.py [options] [paths]\n"
                  "special options for pdf_walker.py are: (shown quoted but must be entered unquoted!)\n"
                  "'--prefix'   or equivalently '-p'\n"
                  "  means interpret the next argument as the prefix to apply when deriving thte output filename.\n"
                  "'--rotate'   or equivalently '-r'\n"
                  "  means interpret the next argument as an angle to rotate in degrees (e.g. 180 for upside-down).\n"
                  "'--prefix'   or equivalently '-p'\n"
                  "  means interpret the next argument as the prefix to apply when deriving thte output filename.\n"
                  "'--scale'   or equivalently '-s'\n"
                  "  means interpret the next argument as the scaling to apply (in order to get nice but not too wide border).\n"
                  "this may be entered as e.g. 0.8 or equivalently 80%. The default is to apply no scaling\n"
                  )
        return Large.process_keyword_arg(self, a)

    def process_args(self):
        Large.process_args(self)
        print(f"remaining args: {sys.argv}")

    def main(self):
        self.process_all_keyword_args()
        self.no_more_positional_args()
        program_pedals()

        instrument = Instrument.Cello
        try:
            self.midi_port = mido.get_output_names()[int(self.midi_port)]
        except ValueError:
            pass
        print(f"running '{self.program_name}' assuming fingers on '{self.open_strings}' string;using MIDI port '{self.midi_port}'")

        self.string_notes = [instrument.get_string_note_from_letter(letter) for letter in self.open_strings]

        fingers_and_their_pitch_offsets = list(enumerate([0, 2, 3, 4, 5]))  # beginners only!

        with mido.open_output(self.midi_port, autoreset=True) as port:
            select_instrument_sound = mido.Message('program_change', program=instrument.midi_program, time=0)
            print(f"selecting MIDI program {instrument.midi_program}")
            port.send(select_instrument_sound)
            prev_pitch = None
            while 1:
                finger, pitch_offset = random.choice(fingers_and_their_pitch_offsets)
                the_string = random.choice(self.string_notes)
                pitch = the_string.GetPitch() + pitch_offset
                note = notes_by_Pitch[pitch][0]  # 0 => favour sharps over flats
                while 1:
                    if prev_pitch:
                        port.send(mido.Message('note_on', note=prev_pitch))
                        time.sleep(1.0)
                        port.send(mido.Message('note_off', note=prev_pitch))
                    port.send(mido.Message('note_on', note=pitch))
                    time.sleep(1.0)
                    port.send(mido.Message('note_off', note=pitch))
                    if pedal(prompt="left=again, right or none = proceed", timeout=4):
                        continue
                    print(f"string {the_string.real_name}, finger: {finger}  {note}",
                      f"interval={pitch-prev_pitch if prev_pitch else ''}")
                    if not pedal(prompt="left=again, right or none = proceed", timeout=4):
                        break
                prev_pitch = pitch
        print("That's all folks!!")

if __name__=="__main__":
    CelloFingers().main()
