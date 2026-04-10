from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.InputControlElement import MIDI_NOTE_TYPE


class PadComponent(ControlSurfaceComponent):
    """
    Maps a rectangular region of Push 1 pads to MIDI notes.

    The Push is oriented upside-down. Coordinates are (col, row), 1-indexed,
    from the user's perspective:
      (1, 1) = user's bottom-left -> physical pad 99
      (8, 8) = user's top-right  -> physical pad 36

    Layouts:
      ascending         - notes increase left-to-right, then bottom-to-top
      ascending_columns - notes increase bottom-to-top, then left-to-right
      mirror_right      - right half is drum rack layout, left half mirrors it
    """

    def __init__(self, bottom_left, top_right, starting_note, channel, color,
                 layout, *a, **k):
        super(PadComponent, self).__init__(*a, **k)
        col1, row1 = bottom_left
        col2, row2 = top_right
        self._col1 = col1
        self._row1 = row1
        self._width = col2 - col1 + 1
        self._height = row2 - row1 + 1
        self._starting_note = starting_note
        self._channel = channel
        self._color = color
        self._layout = layout
        self._pads = self._create_pads()

    def _pad_number(self, col, row):
        """Physical pad MIDI note for a grid position (0-indexed offsets from bottom-left)."""
        return 100 - (self._col1 + col) - (self._row1 + row - 1) * 8

    def _create_pads(self):
        pads = {}
        for row in range(self._height):
            for col in range(self._width):
                pad_num = self._pad_number(col, row)
                button = ButtonElement(True, MIDI_NOTE_TYPE, 0, pad_num)
                button.name = self.name + '_Pad' + str(pad_num)
                pads[(col, row)] = button
        return pads

    def update(self):
        super(PadComponent, self).update()
        if self.is_enabled():
            self._apply_layout()

    def _configure_pad(self, col, row, note, color=None):
        button = self._pads[(col, row)]
        button.set_identifier(note)
        button.set_channel(self._channel)
        c = color if color is not None else self._color
        midi_val = c.midi_value if hasattr(c, 'midi_value') else c
        button.send_value(midi_val)

    def _apply_layout(self):
        getattr(self, '_layout_' + self._layout)()

    def _layout_ascending(self):
        for row in range(self._height):
            for col in range(self._width):
                note = self._starting_note + col + row * self._width
                self._configure_pad(col, row, note)

    def _layout_ascending_columns(self):
        for row in range(self._height):
            for col in range(self._width):
                note = self._starting_note + row + col * self._height
                self._configure_pad(col, row, note)

    def _layout_mirror_right(self):
        half = self._width // 2
        mirror_color = self._color.shade(1) if hasattr(self._color, 'shade') else self._color
        for row in range(self._height):
            for col in range(self._width):
                if col >= half:
                    note = self._starting_note + row * 4 + (col - half)
                    self._configure_pad(col, row, note)
                else:
                    note = self._starting_note + row * 4 + (half - 1 - col)
                    self._configure_pad(col, row, note, color=mirror_color)
