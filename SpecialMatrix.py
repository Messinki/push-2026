from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.ButtonElement import ButtonElement
from _Framework.InputControlElement import *



class SpecialMatrix:

    def __init__(self, width, height, starting_pad, starting_note, channel, color):
        self.width = width
        self.height = height
        self.starting_pad = starting_pad
        self.starting_note = starting_note
        self.channel = channel
        self.color = color


    def pitchAscending(self):
        for y in range(self.height):
            padheightshifter = y * 8
            noteheightshifter = y * self.width
            for x in range(self.width):
                pad = x + padheightshifter + self.starting_pad
                note = x + noteheightshifter + self.starting_note

                button = ButtonElement(True, MIDI_NOTE_TYPE, 0, pad)
                button.name = u'Pad' + str(pad)
                button.set_identifier(note)
                button.set_channel(self.channel)
                button.send_value(self.color)

    def pitchAscendingUpsideDown(self):
        for y in range(self.height):
            padheightshifter = y * 8
            noteheightshifter = y * self.width
            for x in range(self.width):
                pad = -x - padheightshifter + self.starting_pad
                note = x + noteheightshifter + self.starting_note

                button = ButtonElement(True, MIDI_NOTE_TYPE, 0, pad)
                button.name = u'Pad' + str(pad)
                button.set_identifier(note)
                button.set_channel(self.channel)
                button.send_value(self.color)

    def mirrorRight(self):
        for y in range(self.height):
            padheightshifter = y * 8
            noteheightshifter = y * self.width

            for x in range(self.width):
                pad = x + padheightshifter + self.starting_pad
                            
                half_width = self.width / 2
                note = x - half_width
                if note < 0:
                    note += 1
                note = int(abs(note)+half_width+self.starting_note+noteheightshifter)


                button = ButtonElement(True, MIDI_NOTE_TYPE, 0, pad)
                button.name = u'Pad' + str(pad)
                button.set_identifier(note)
                button.set_channel(self.channel)
                button.send_value(self.color)

    def mirrorRightUpsideDown(self):
        for y in range(self.height):
            padheightshifter = y * 8
            noteheightshifter = y * self.width

            for x in range(self.width):
                pad = -x - padheightshifter + self.starting_pad
                            
                half_width = self.width / 2
                note = x - half_width
                if note < 0:
                    note += 1
                note = int(abs(note)+half_width+self.starting_note+noteheightshifter)


                button = ButtonElement(True, MIDI_NOTE_TYPE, 0, pad)
                button.name = u'Pad' + str(pad)
                button.set_identifier(note)
                button.set_channel(self.channel)
                button.send_value(self.color)


