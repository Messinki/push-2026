from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ControlSurface import ControlSurface
from _Framework.TransportComponent import TransportComponent
from _Framework.BackgroundComponent import BackgroundComponent
from _Framework.Layer import Layer
from _Framework.ModesComponent import ModesComponent
from .elements import Elements
from .pad_component import PadComponent
from . import colors


class Push2026(ControlSurface):

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        with self.component_guard():
            self._elements = Elements()
            self._create_pad_components()
            self._create_transport()
            self._create_tempo()
            self._create_background()
            self._create_modes()

    def _create_pad_components(self):
        self._drum_pads = PadComponent(
            (3, 1), (8, 4), 36, 6, colors.DRUMS,
            'mirror_right', name='Drum_Pads', is_enabled=False)
        self._beat_repeat_pads = PadComponent(
            (1, 1), (2, 4), 36, 7, colors.BEAT_REPEAT,
            'ascending_columns', name='Beat_Repeat_Pads', is_enabled=False)
        self._sampler_1_pads = PadComponent(
            (1, 5), (4, 8), 36, 8, colors.SAMPLER_1,
            'ascending', name='Sampler_1_Pads', is_enabled=False)
        self._sampler_2_pads = PadComponent(
            (1, 5), (4, 8), 36, 9, colors.SAMPLER_2,
            'ascending', name='Sampler_2_Pads', is_enabled=False)

    def _create_transport(self):
        self._transport = TransportComponent()
        self._transport.set_play_button(self._elements.play_button)
        self._transport.set_metronome_button(self._elements.metronome_button)
        self._transport.set_tap_tempo_button(self._elements.tap_tempo_button)

    def _create_tempo(self):
        self._elements.tempo_coarse.add_value_listener(self._on_tempo_coarse_value)
        self._elements.tempo_fine.add_value_listener(self._on_tempo_fine_value)

    def _on_tempo_coarse_value(self, value):
        delta = value if value < 64 else value - 128
        self.song().tempo = max(20, min(999, self.song().tempo + delta))

    def _on_tempo_fine_value(self, value):
        delta = value if value < 64 else value - 128
        self.song().tempo = max(20, min(999, self.song().tempo + delta * 0.1))

    def disconnect(self):
        self._elements.tempo_coarse.remove_value_listener(self._on_tempo_coarse_value)
        self._elements.tempo_fine.remove_value_listener(self._on_tempo_fine_value)
        ControlSurface.disconnect(self)

    def _create_background(self):
        self._background = BackgroundComponent(name='Background')
        self._background.layer = Layer(
            record_button=self._elements.record_button,
            new_button=self._elements.new_button,
            duplicate_button=self._elements.duplicate_button,
            redo_button=self._elements.redo_button,
            undo_button=self._elements.undo_button,
            device_button=self._elements.device_button,
            browse_button=self._elements.browse_button,
            track_button=self._elements.track_button,
            clip_button=self._elements.clip_button,
            volume_button=self._elements.volume_button,
            pan_send_button=self._elements.pan_send_button,
            quantize_button=self._elements.quantize_button,
        )

    def _create_modes(self):
        self._pad_modes = ModesComponent(name='Pad_Modes')
        self._pad_modes.add_mode('default', [
            self._drum_pads,
            self._beat_repeat_pads,
            self._sampler_1_pads,
            self._sampler_2_pads,
        ])
        self._pad_modes.selected_mode = 'default'
