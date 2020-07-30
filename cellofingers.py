#!/usr/bin/python3
"""
select left hand fingering for chello. Send correspondign note
to output port... and ad hoc variations on that theme!
"""

from __future__ import print_function
import sys
import time
import random
from terpsichore import *
import mido
from mido import Message
from pynput.keyboard import Events
from queue import Empty

class KeyEvents(Events):
    # tweaking this class for my own convenience
    def get_key(self, action=Events.Release, timeout=None):
        try:
            while 1:
                event = self.get(timeout)
                if isinstance(event, action):
                    return event.key;
        except Empty:
            return None


def main():
    instrument = Instrument.Cello
    program_number = 43

    program_name = sys.argv and sys.argv.pop(0) or "unknown program"
    on_time = sys.argv and float(sys.argv.pop(0)) or None # 1.5  # seconds
    open_string_name = sys.argv and sys.argv.pop(0) or 'D'
    port_name = sys.argv and sys.argv.pop(0) or 'TiMidity port 0'
    print(f"running '{program_name}' assuming fingers on '{open_string_name}' string;using MIDI port '{port_name}'")

    for string in instrument.strings:
        if string.real_name.startswith(open_string_name):
            break
    else:
        print(f"A {instrument} with a '{open_string_name}' string?  I don't think so!")
        sys.exit(990)

    fingers_and_their_pitch_offsets = list(enumerate([0, 2, 3, 4, 5]))  # beginners only!

    with mido.open_output(port_name, autoreset=True) as port, KeyEvents() as events:
        select_instrument_sound = Message('program_change', program=instrument.midi_program, time=0)
        print(f"selecting MID program {instrument.midi_program}")
        port.send(select_instrument_sound)
        while True:
            finger, pitch_offset = random.choice(fingers_and_their_pitch_offsets)
            pitch = string.GetPitch() + pitch_offset
            note = notes_by_Pitch[pitch][0]  # 0 => favour sharps over flats
            print(f"({open_string_name} string)  finger: {finger}  {note}")
            time.sleep(0.1)
            on = Message('note_on', note=pitch)
            port.send(on)
            key = events.get_key(timeout=on_time)
            if key:
                print(f"{key}  (released) {type(key)}")
            off = Message('note_off', note=pitch)
            port.send(off)
    print("That's all folks!!")

if __name__=="__main__":
    main()
