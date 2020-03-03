#!/usr/bin/python3
"""
select left hand fingering for chello. Send correspondign note
to output port.
"""

from __future__ import print_function
import sys
import time
import random
import terpsichore
import mido
from mido import Message

open_string_pitch_per_name = {'C':36, 'G':43, 'D':50, 'A': 57}

program_name = sys.argv and sys.argv.pop(0) or "unknown program"
on_time = sys.argv and float(sys.argv.pop(0)) or 1.5  # seconds
open_string_name = sys.argv and sys.argv.pop(0) or 'D'
port_name = sys.argv and sys.argv.pop(0) or 'TiMidity port 0'
print(f"running '{program_name}' assuming fingers on '{open_string_name}' string;using MIDI port '{port_name}'")

# A pentatonic scale
fingers_and_their_pitch_offsets = list(enumerate([0, 2, 3, 4, 5]))  # beginners only!

with mido.open_output(port_name, autoreset=True) as port:
    while True:
        finger, pitch_offset = random.choice(fingers_and_their_pitch_offsets)
        pitch = open_string_pitch_per_name[open_string_name] + pitch_offset
        note = terpsichore.notes_by_Pitch[pitch][0]  # 0 => favour sharps over flats
        print(f"fingering {finger}    {note}")
        time.sleep(0.1)
        on = Message('note_on', note=pitch)
        port.send(on)
        time.sleep(on_time)

        off = Message('note_off', note=pitch)
        port.send(off)
print("That's all folks!!")
