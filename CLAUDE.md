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

## File Structure

```
Push2026/
├── __init__.py          ← create_instance → Push2026
├── push2026.py          ← main ControlSurface class
├── elements.py          ← all MIDI element definitions (excludes pads and ComboElements — none yet)
├── colors.py            ← simple color constants (Rgb.MAGENTA, RgbColor(24), etc.)
└── pad_component.py     ← pad layouts as a v2-style Component
```

## Architecture Decisions

### What we use from v2

- **`Layer`** — declarative binding of elements to components
- **`ModesComponent`** + **`LatchingBehaviour`** — named modes, tap=switch / hold=momentary
- **`ComboElement`** — shift functionality (not wired yet — no shifted buttons)
- **`BackgroundLayer`** — grabs buttons that should be silent (for M4L)

### What we don't use from v2

- **Skin** — plain `colors.py` module with constants instead. Change `DRUMS` and `DRUMS_MIRROR` follows automatically.
- **Control descriptors** (`ButtonControl`, `@button.pressed`) — pad remapping does custom `set_channel()`/`set_identifier()` which doesn't fit descriptors. Direct element access instead.
- **Dependency injection** (`@depends`, `inject`) — unnecessary with one main script.
- **`listenable_property`** — not needed until components need to talk to each other.

### PadComponent gotcha

`PadComponent` inherits from `_Framework.ControlSurfaceComponent`, **not** `ableton.v2.control_surface.Component`.
Using v2 `Component` raises a `DependencyError` because `register_component` is not provided by our `_Framework.ControlSurface` base class.
`tomode()` still auto-wraps it into a `ComponentMode` correctly.

### Transport

Uses `_Framework.TransportComponent` with direct `set_*` calls — this is its API and it works fine alongside v2 patterns.

## Reference Docs (read on demand)

- [../docs/signal-flow.md](../docs/signal-flow.md) — hardware → elements → components → Live, parameter control approaches
- [docs/colors.md](docs/colors.md) — color classes, named palettes, LIVE_COLORS_TO_MIDI_VALUES
- [docs/patterns.md](docs/patterns.md) — v2 recipes: mode switching, shift (ComboElement), grabbed buttons, adding a mode