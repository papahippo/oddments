#!/usr/bin/python
import math
import sys,  os
import time

import numpy
import pygame
import pyaudio
try:
    import analyse
except:
    print("'analyse' module not available. will just use FFT method.")
    analyse = None
from terpsichore import *
from pygame.locals import *

class Fortuna440(object):
    zoom, basePitch = 16, 88
    beyond_clef = 96
    background_colour = (25, 25, 25)
    screen_size = width, height = 1024, 768
    sampleRate = 44100
    sampleSize = 4096 #16384
    staff_lines = []
    pianoKeyDepth = 96
    horizLength = 64
    x9_trace = width - (pianoKeyDepth+horizLength+26)
    state = 0
    useFFT = analyse is None
    volumeThreshold  = 8
    
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('fortuna440')
        # myDir,  mySourceFile  = os.path.split(__file__)
        myDir = os.getcwd()  # quick hack when resurrecting this code!
        icon = pygame.transform.scale(pygame.image.load(myDir+'/images/Treble_clef_inv.png'), (32, 32))
        pygame.display.set_icon(icon)
        pygame.key.set_repeat(50, 20)
        pygame.event.set_allowed((pygame.KEYDOWN, pygame.QUIT))

        self.bigFont = pygame.font.Font("freesansbold.ttf", 32)
        self.littleFont = pygame.font.Font("freesansbold.ttf", 12)

        try:
            self.inputDeviceIndex = eval(sys.argv[1])
        except IndexError:
            self.inputDeviceIndex = 4

        # Initialize PyAudio
        self.pyaud = pyaudio.PyAudio()

        self.stream = None

        self.tt = numpy.array([])
        self.pp = numpy.array([],  dtype=float)
            

    def pitch2y(self, pitch):
        return (self.basePitch-pitch)*self.zoom

    def iter(self):
        for evt in pygame.event.get():
            if evt.type == pygame.KEYDOWN:
                if not evt.key:
                    continue
                ko = evt.key
                #ko = ord(evt.key)
                #ko = ord(evt.unicode)
                print(hex(ko))
                if ko in (K_ESCAPE, K_q):
                    sys.exit()
                elif (ko == K_m) and analyse:
                    self.useFFT = not self.useFFT
                elif ko == K_LEFTBRACKET:
                    if self.volumeThreshold:
                        self.volumeThreshold -= 1
                    print("LESS!")
                elif ko == K_RIGHTBRACKET:
                    self.volumeThreshold += 1
                elif ko in (K_EQUALS, K_KP_PLUS):
                    if self.zoom<=1024:
                        self.zoom *= 2
                elif ko in (K_MINUS, K_KP_MINUS):
                    #print("zoom out!")
                    if self.zoom>1:
                        self.zoom /= 2
                elif ko == K_UP:
                    self.basePitch += 1
                elif ko == K_DOWN:
                    self.basePitch -= 1
                elif ko in (K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7):
                    self.inputDeviceIndex = ko-K_0
                    if self.stream is not None:
                        self.stream.close()
                        self.stream = None
            if evt.type == pygame.QUIT:
                sys.exit()


        if self.stream is None:
            # Open input stream, 16-bit mono at 44100 Hz
            # On my system, device 1 is a USB microphone, your number may differ.
            # Open sound input before pygame, otherwise pygame hogs sounds
            self.latest_volume = 0
            try:
                self.stream = self.pyaud.open(
                    format = pyaudio.paInt16,
                    channels = 1,
                    rate = 44100,
                    input_device_index = self.inputDeviceIndex,
                    frames_per_buffer=4096,
                    input = True)
                self.latest_note = "Valid input device but no note yet"
            except OSError:
                self.latest_note = "This input device is not available on this system"
            #sys.exit(0)
            pygame.display.init()

            self.screen = pygame.display.set_mode(self.screen_size)
        if self.stream:
            try:
                # Read raw microphone data
                rawSamples = self.stream.read(self.sampleSize)
            except:
                print ("warning: dropped frame?")
                return
            # Convert raw data to NumPy array
            samples = numpy.fromstring(rawSamples, dtype=numpy.int16)
            # Show the volume and pitch
            if self.useFFT:
                avgNote, volume = default_voice.DeriveNote(samples)
                pitch = avgNote and avgNote.GetPitch()
            else:
                pitch = analyse.musical_detect_pitch(samples, samplerate=self.sampleRate)
                avgNote = default_voice.GetNote(pitch)
                volume = analyse.loudness(samples) + 24
        else:
            pygame.time.wait(200)
            avgNote, pitch, volume = None, None, None
        self.screen.fill(self.background_colour)
# BEGIN QUCIK FIX!
#        if pitch is not None:
#            pitch -=3 # defaulkt to Eb horn!
# END QUCIK FIX!

        if pitch and (97>pitch>=20) and volume and (volume>= self.volumeThreshold):
            print(avgNote, volume)
            self.latest_volume = volume            
            self.latest_note = avgNote
            self.pp = numpy.append(self.pp, pitch)

        for iPitch in range(32, 97):
            print("iPitch =", iPitch)
            note = default_voice.GetNote(iPitch)
            notelet= self.littleFont.render(str(note.real_name), 0, (180, 180, 80))
            name, pitch = note.real_name, note.pitch
            lineWidth = 2 
            if note in self.staff_lines:
                colour = (220, 220, 220)
                lineWidth = 3
            elif note is Note.A4:
                colour = (120, 100, 0)
            elif pitch==0:
                colour = (150, 50, 50)
            else:
                colour = ((96, 120)[len(name)==2], 30, 30)
            py = self.pitch2y(iPitch)
            pygame.draw.line(self.screen, colour, (0, py), (self.x9_trace+self.horizLength/2, py), lineWidth)
            self.screen.blit(notelet, (self.x9_trace+self.horizLength+8, py-6))
            whiteDepth = self.pianoKeyDepth
            if len(note.real_name)!=2: # ugly way to identify 'black' note!
                whiteDepth /= 2
            pygame.draw.rect(self.screen, (220, 220, 220), (self.width-whiteDepth, py-(self.zoom/2 -1), whiteDepth, self.zoom-1))
                
        for clef in (Clef.Bass, Clef.Treble):
            self.staff_lines += clef.lines
            symbol = clef.symbol
            #print("symbol=", symbol)
            if not symbol:
                continue
            surface = pygame.transform.scale(pygame.image.load(symbol), (clef.scaleHint*8, clef.scaleHint*self.zoom))
            coords = (0, self.pitch2y(clef.lines[-1].GetPitch()))
            self.screen.blit(surface, coords)
        chan_text = self.bigFont.render("Input device %u, method %s" %(self.inputDeviceIndex, ('AMDF','FFT')[self.useFFT]), 0, (0, 250, 0))
        self.screen.blit(chan_text, (50, 10))
        note_text = self.bigFont.render(str(self.latest_note) + " volume=%u(>=%u?)" %(self.latest_volume, self.volumeThreshold), 0, (0, 250, 0))
        self.screen.blit(note_text, (50, 70))
        if len(self.pp)>2:
            yy = self.pitch2y(self.pp)[self.beyond_clef-self.x9_trace:] # first index always negative!
            xx = numpy.arange(self.x9_trace-len(yy),  self.x9_trace)
            xxyy = numpy.array([xx, yy])
            xyxy = numpy.swapaxes(xxyy, 0, 1)
            # print(xyxy)
            pygame.draw.lines(self.screen, (150, 250, 50), 0, xyxy, 2)
            pygame.draw.line(self.screen, (250, 250, 50), (self.x9_trace, yy[-1]),  (self.x9_trace+self.horizLength, yy[-1]), 2)
        pygame.draw.rect(self.screen, (0, 150, 0), (0, 0, 1, 768))

                
        pygame.display.flip()

if __name__=="__main__":
    # os.chdir(os.path.split(__file__)[0])
    f440 = Fortuna440()
    while f440.stream is not False:
        f440.iter()
    del f440
