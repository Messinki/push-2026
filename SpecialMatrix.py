from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ButtonElement import ButtonElement
from _Framework.InputControlElement import MIDI_NOTE_TYPE
from pushbase.colors import RgbColor, Pulse, Blink, FallbackColor, Basic, Rgb, BiLed


def _shade_color(color, shade_level=1):
    """Return a shaded (darker) version of color if it's an RgbColor, else return color unchanged."""
    if isinstance(color, RgbColor):
        return color.shade(shade_level)
    return color


class SpecialMatrix:
    """
    Maps a rectangular region of Push 1 pads to MIDI notes.

    The Push is oriented upside-down. Coordinates are (col, row), 1-indexed,
    from the user's perspective:
      (1, 1) = user's bottom-left → physical pad 99
      (8, 8) = user's top-right  → physical pad 36

    Usage:
        Full 8x8 grid, notes starting at 36, MIDI channel 1.

        Named color:   matrix = SpecialMatrix((1,1),(8,8), starting_note=36, channel=1, color=Rgb.CYAN)
        Raw integer:   matrix = SpecialMatrix((1,1),(8,8), starting_note=36, channel=1, color=127)
        Custom index:  matrix = SpecialMatrix((1,1),(8,8), starting_note=36, channel=1, color=RgbColor(45))

        matrix.pitch_ascending()          # default mode
        matrix.mirror_right()             # left half mirrors right half
        matrix.pitch_ascending_columns()  # notes go bottom-to-top within each column
    """

    def __init__(self, bottom_left, top_right, starting_note, channel, color):
        """
        Args:
            bottom_left:   (col, row) of the bottom-left corner in user-space, e.g. (1, 1)
            top_right:     (col, row) of the top-right corner in user-space, e.g. (8, 8)
            starting_note: MIDI note assigned to the bottom-left pad
            channel:       MIDI channel (0-indexed)
            color:         LED color value
        """
        col1, row1 = bottom_left
        col2, row2 = top_right
        self._col1   = col1
        self._row1   = row1
        self._width  = col2 - col1 + 1
        self._height = row2 - row1 + 1
        self.starting_note = starting_note
        self.channel = channel
        self.color   = color

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _pad_number(self, col_offset, row_offset):
        """Physical pad MIDI number for a position (0-indexed from the bottom-left corner; row increases upward)."""
        col = self._col1 + col_offset
        row = self._row1 + row_offset
        return 100 - col - (row - 1) * 8

    def _assign(self, pad, note, color=None):
        button = ButtonElement(True, MIDI_NOTE_TYPE, 0, pad)
        button.name = u'Pad' + str(pad)
        button.set_identifier(note)
        button.set_channel(self.channel)
        c = color if color is not None else self.color
        midi_val = c.midi_value if hasattr(c, 'midi_value') else c
        button.send_value(midi_val)

    # ------------------------------------------------------------------
    # Modes
    # ------------------------------------------------------------------

    def pitch_ascending(self):
        """
        Default mode. Notes increase left→right across each row, then upward row by row.

        Example for a 4×2 region (starting_note=36):
            40  41  42  43   ← top row
            36  37  38  39   ← bottom row
        """
        for row in range(self._height):
            for col in range(self._width):
                note = self.starting_note + col + row * self._width
                self._assign(self._pad_number(col, row), note)

    def pitch_ascending_columns(self):
        """
        Notes increase bottom→top within each column, then rightward column by column.

        Example for a 4×2 region (starting_note=36):
            37  39  41  43   ← top row
            36  38  40  42   ← bottom row
        """
        for row in range(self._height):
            for col in range(self._width):
                note = self.starting_note + row + col * self._height
                self._assign(self._pad_number(col, row), note)

    def mirror_right(self):
        """
        Right half maps to drum rack layout (rows of 4); left half mirrors it.

        Drum racks arrange notes in rows of 4:
            48 49 50 51
            44 45 46 47
            40 41 42 43
            36 37 38 39

        For a 6×4 region (starting_note=36), right half is 3 wide:
            Left (mirror)  Right (drum rack)
            50 49 48       48 49 50
            46 45 44       44 45 46
            42 41 40       40 41 42
            38 37 36       36 37 38
        """
        half = self._width // 2
        mirror_color = _shade_color(self.color)
        for row in range(self._height):
            for col in range(self._width):
                if col >= half:
                    note = self.starting_note + row * 4 + (col - half)
                    self._assign(self._pad_number(col, row), note)
                else:
                    note = self.starting_note + row * 4 + (half - 1 - col)
                    self._assign(self._pad_number(col, row), note, color=mirror_color)
