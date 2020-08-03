#!/usr/bin/python3
"""
select left hand fingering for cello. Send corresponding note
to output port... and ad hoc variations on that theme!
"""
import sys, os, time, random, select
from terpsichore import *
import mido

def program_pedals():
    # unbuffered reading of keyboard input in python is ... well not as straighforward as
    # I had hoped. So, I program my twin-pedal footswitch to generate (left) control-D = end-of-file
    # and (right) ENTER, both of which can be detected without too much jiggery-pokery.
    #
    return os.system("sudo footswitch -1 -m ctrl -k d -2 -k enter")

def pedal(timeout=None, obj=sys.stdin):
    """
Wait 'timeout' seconds (None => indefinitely) for action from footswitch.
returns '' => left-pedal or '\n' => right pedal or None => timeout.
    """
    print('pedal called!')
    inList, outsList, excList = select.select([obj], [], [], timeout)
    if inList:
        return inList[0].read(1)
    # return None # does this anyway!

def main():
    program_pedals()
    instrument = Instrument.Cello
    program_number = 43
    program_name = sys.argv and sys.argv.pop(0) or "unknown program"
    timeout = sys.argv and float(sys.argv.pop(0)) or None #    # 1.5  # seconds
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

    with mido.open_output(port_name, autoreset=True) as port:
        select_instrument_sound = mido.Message('program_change', program=instrument.midi_program, time=0)
        print(f"selecting MIDI program {instrument.midi_program}")
        port.send(select_instrument_sound)
        prev_pitch = None
        while 1:
            finger, pitch_offset = random.choice(fingers_and_their_pitch_offsets)
            pitch = string.GetPitch() + pitch_offset
            note = notes_by_Pitch[pitch][0]  # 0 => favour sharps over flats
            while 1:
                if prev_pitch:
                    port.send(mido.Message('note_on', note=prev_pitch))
                    time.sleep(1.0)
                    port.send(mido.Message('note_off', note=prev_pitch))
                port.send(mido.Message('note_on', note=pitch))
                time.sleep(1.0)
                port.send(mido.Message('note_off', note=pitch))
                if pedal(timeout=4.0) is '':
                    continue
                print(f"({open_string_name} string)  finger: {finger}  {note}",
                  f"interval={pitch-prev_pitch if prev_pitch else ''}")
                input_ = pedal(timeout=5.0)
                if  input_ is not '':
                    break
            if input is None:
                break
            prev_pitch = pitch
    print("That's all folks!!")

if __name__=="__main__":
    main()
