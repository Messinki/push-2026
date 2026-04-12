from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement
from _Framework.InputControlElement import MIDI_CC_TYPE, MIDI_NOTE_TYPE

ENCODER_MAP_MODE = Live.MidiMap.MapMode.relative_smooth_two_compliment


class Elements(object):
    """All MIDI element definitions for Push2026."""

    def __init__(self):
        # -- Transport --
        self.play_button = ButtonElement(True, MIDI_CC_TYPE, 0, 85, name='Play_Button')
        self.metronome_button = ButtonElement(True, MIDI_CC_TYPE, 0, 9, name='Metronome_Button')
        self.tap_tempo_button = ButtonElement(True, MIDI_CC_TYPE, 0, 3, name='Tap_Tempo_Button')

        # -- Grabbed buttons (silent, available to M4L) --
        self.record_button = ButtonElement(True, MIDI_CC_TYPE, 0, 86, name='Record_Button')
        self.new_button = ButtonElement(True, MIDI_CC_TYPE, 0, 87, name='New_Button')
        self.duplicate_button = ButtonElement(True, MIDI_CC_TYPE, 0, 88, name='Duplicate_Button')
        self.redo_button = ButtonElement(True, MIDI_CC_TYPE, 0, 89, name='Redo_Button')
        self.undo_button = ButtonElement(True, MIDI_CC_TYPE, 0, 90, name='Undo_Button')
        self.device_button = ButtonElement(True, MIDI_CC_TYPE, 0, 110, name='Device_Button')
        self.browse_button = ButtonElement(True, MIDI_CC_TYPE, 0, 111, name='Browse_Button')
        self.track_button = ButtonElement(True, MIDI_CC_TYPE, 0, 112, name='Track_Button')
        self.clip_button = ButtonElement(True, MIDI_CC_TYPE, 0, 113, name='Clip_Button')
        self.volume_button = ButtonElement(True, MIDI_CC_TYPE, 0, 114, name='Volume_Button')
        self.pan_send_button = ButtonElement(True, MIDI_CC_TYPE, 0, 115, name='Pan_Send_Button')
        self.quantize_button = ButtonElement(True, MIDI_CC_TYPE, 0, 116, name='Quantize_Button')

        # -- Tempo encoders (grabbed on ch0, native Push sends CC14/CC15) --
        self.tempo_coarse = EncoderElement(MIDI_CC_TYPE, 0, 14, ENCODER_MAP_MODE,
            name='Tempo_Coarse')
        self.tempo_fine = EncoderElement(MIDI_CC_TYPE, 0, 15, ENCODER_MAP_MODE,
            name='Tempo_Fine')

        # -- Function buttons (grabbed on ch0, re-channeled to ch2 for M4L) --
        self.drum_function_buttons = _make_cc_buttons(
            'Drums', [105, 104, 103, 102, 23, 22, 21, 20], channel=2)
        self.sampler_function_buttons = _make_cc_buttons(
            'Sampler', [109, 108, 107, 106, 27, 26, 25, 24], channel=2)

        # -- Tempo touch buttons (grabbed so they don't pass through) --
        self.tempo_coarse_touch = ButtonElement(True, MIDI_NOTE_TYPE, 0, 10,
            name='Tempo_Coarse_Touch')
        self.tempo_fine_touch = ButtonElement(True, MIDI_NOTE_TYPE, 0, 9,
            name='Tempo_Fine_Touch')

        # -- Dial touch buttons (grabbed on ch0, re-channeled to ch10 for M4L) --
        self.dial_touch_buttons = _make_note_buttons(
            'Dial_Button', [7, 6, 5, 4, 3, 2, 1, 0, 8], channel=10)

        # -- Dials (grabbed on ch0, re-channeled to ch2 for M4L) --
        self.dials = _make_encoders(
            'Dial', [78, 77, 76, 75, 74, 73, 72, 71, 79], channel=2)


def _make_cc_buttons(name, ccs, channel):
    buttons = []
    for i, cc in enumerate(ccs):
        button = ButtonElement(True, MIDI_CC_TYPE, 0, cc)
        button.name = name + '_F' + str(i + 1)
        button.set_channel(channel)
        buttons.append(button)
    return buttons


def _make_note_buttons(name, notes, channel):
    buttons = []
    for i, note in enumerate(notes):
        button = ButtonElement(True, MIDI_NOTE_TYPE, 0, note)
        button.name = name + '_' + str(i + 1)
        button.set_channel(channel)
        buttons.append(button)
    return buttons


def _make_encoders(name, ccs, channel):
    encoders = []
    for i, cc in enumerate(ccs):
        enc = EncoderElement(MIDI_CC_TYPE, 0, cc, map_mode=ENCODER_MAP_MODE)
        enc.name = name + '_' + str(i + 1)
        enc.set_channel(channel)
        encoders.append(enc)
    return encoders
