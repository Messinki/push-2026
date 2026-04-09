# Push 2026 — Custom Ableton Push 1 MIDI Remote Script

## Overview

Custom MIDI remote script for **Ableton Push 1**. Replaces default Push behavior with
custom pad layouts, button mappings, encoder assignments, and custom modes.
User orients his push upsidedown.

## Push 1 MIDI Specification

- **Pads**: MIDI notes 36–99, channel 0 (8x8 grid, bottom-left = 36)
- **Buttons**: MIDI CC, channel 0 (see `../reference/Push/elements.py` for full mapping)
- **Encoders**: MIDI CC, relative mode (`relative_smooth_two_compliment`)
- **Tempo encoders**: CC 14/15 on channel 5
- **Display**: SysEx messages (see `../reference/Push/sysex.py`)
- **LED colors**: Use `pushbase.colors` — import from it, never copy. See `docs/colors.md`.

## Reference Docs (read on demand)

- [docs/colors.md](docs/colors.md) — color classes, named palettes, LIVE_COLORS_TO_MIDI_VALUES
