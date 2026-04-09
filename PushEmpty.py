from __future__ import absolute_import, print_function, unicode_literals
import Live
from .SpecialMatrix import SpecialMatrix
from _Framework.ControlSurface import ControlSurface
from _Framework.Skin import Skin

from _Framework.ButtonElement import ButtonElement, Color
from ableton.v2.base.dependency import *
from ableton.v2.control_surface.elements import encoder

from pushbase.colors import Rgb, Pulse, Blink
from pushbase.touch_encoder_element import TouchEncoderElement
from pushbase.elements import create_note_button
from pushbase import consts

from _Framework.ButtonMatrixElement import ButtonMatrixElement
from Launchpad.ConfigurableButtonElement import ConfigurableButtonElement
from _Framework.InputControlElement import *
from _Framework.EncoderElement import EncoderElement
from _Framework.TransportComponent import TransportComponent
from _Framework.EncoderElement import EncoderElement



class PushEmpty(ControlSurface):
    u""" Script for PushEmpty Controllers """

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        with self.component_guard():

            u"""Empty buttons that don't do anything but are grabbable"""
            #self.PlayButton=ButtonElement(True, MIDI_CC_TYPE, 0, 85, name='Play_Button')
            self.RecordButton=ButtonElement(True, MIDI_CC_TYPE, 0, 86, name='Record_Button')
            self.NewButton=ButtonElement(True, MIDI_CC_TYPE, 0, 87, name='New_Button')
            self.DuplicateButton=ButtonElement(True, MIDI_CC_TYPE, 0, 88, name='New_Duplicate_Button')
            self.UndoButton=ButtonElement(True, MIDI_CC_TYPE, 0, 90, name='Undo_Button')
            self.RedoButton=ButtonElement(True, MIDI_CC_TYPE, 0, 89, name='Redo_Button')
            self.QuantizeButton=ButtonElement(True, MIDI_CC_TYPE, 0, 116, name='Quantize_Button')

            self.DeviceButton=ButtonElement(True, MIDI_CC_TYPE, 0, 110, name='Device_Button')
            self.BrowseButton=ButtonElement(True, MIDI_CC_TYPE, 0, 111, name='Browse_Button')
            self.TrackButton=ButtonElement(True, MIDI_CC_TYPE, 0, 112, name='Track_Button')
            self.ClipButton=ButtonElement(True, MIDI_CC_TYPE, 0, 113, name='Clip_Button')
            self.VolumeButton=ButtonElement(True, MIDI_CC_TYPE, 0, 114, name='Volume_Button')
            self.PanSendButton=ButtonElement(True, MIDI_CC_TYPE, 0, 115, name='Pan_Send_Button')


            self.Tempo_Coarse=EncoderElement( MIDI_CC_TYPE, 5, 14, Live.MidiMap.MapMode.relative_smooth_two_compliment, name='Tempo_Coarse')
            self.Tempo_Fine=EncoderElement( MIDI_CC_TYPE, 5, 15, Live.MidiMap.MapMode.relative_smooth_two_compliment,  name='Tempo_Fine')

            self.transport_control()

            #def disconnect(self):   #this function is automatically called by live when the program is closed
		    #for pads in range(36, 99)



        
            padsBottomRight = [95,94,93,92,87,86,85,84,79,78,77,76,71,70,69,68]
            padsBottomLeft = [99,98,97,96,91,90,89,88,83,82,81,80,75,74,73,72]
    
            MirrorDrumNotes = [39,38,38,39,43,42,42,43,47,46,46,47,51,50,50,51]

            BLACK = 0
            DARK_GREY = 1
            GREY = 2
            WHITE = 3
            RED = 5
            AMBER = 9
            YELLOW = 13
            LIME = 17
            GREEN = 21
            SPRING = 25
            TURQUOISE = 29
            CYAN = 33
            SKY = 37
            OCEAN = 41
            BLUE = 45
            ORCHID = 49
            MAGENTA = 53
            PINK = 57

            




            pads1 = SpecialMatrix(4, 4, 95, 36, 6, 69).mirrorRightUpsideDown()     #Drumpads with mirrored pads
            pads2 = SpecialMatrix(4, 2, 63, 36, 7, 24).pitchAscendingUpsideDown() # beat repeat above drums
            pads3 = SpecialMatrix(4, 4, 99, 36, 8, 44).pitchAscendingUpsideDown()  #sampler
            pads4 = SpecialMatrix(4, 4, 67, 36, 9, 22).pitchAscendingUpsideDown()  #Another one
            


            
            def setup_function_buttons(name, pads, channel):
                for i in range(8):
                    button = ButtonElement(True, MIDI_CC_TYPE, 0, pads[i])
                    button.name = name + '_F' + str(i+1)
                    button.set_channel(channel)

            setup_function_buttons('Drums', [105,104,103,102,23,22,21,20], 2)
            setup_function_buttons('Sampler', [109,108,107,106,27,26,25,24], 2)



            def setup_dial_notes(notes, channel):
                for i in range(len(notes)):
                    button = ButtonElement(True, MIDI_NOTE_TYPE, 0, notes[i])
                    button.name = 'Dial_Button_' + str(i+1)
                    button.set_channel(channel)

            setup_dial_notes([7,6,5,4,3,2,1,0,8,9,10], 10)


            def setup_dials(dials, channel):
                for i in range(len(dials)):
                    button = EncoderElement( MIDI_CC_TYPE, 0, dials[i], map_mode=Live.MidiMap.MapMode.relative_smooth_two_compliment,)
                    button.name = 'Dial_' + str(i+1)
                    button.set_channel(channel)

            setup_dials([78,77,76,75,74,73,72,71,79], 2)


    def transport_control(self):
                
        transport = TransportComponent()

        transport.set_metronome_button(ButtonElement(True, MIDI_CC_TYPE, 0, 9, name='Metronome_Button'))
        transport.set_tap_tempo_button(ButtonElement(True, MIDI_CC_TYPE, 0, 3, name='Tap_Tempo_Button'))
        transport.set_play_button(ButtonElement(True, MIDI_CC_TYPE, 0, 85, name='Play_Button'))
      