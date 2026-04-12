# Push2026 — v2 Patterns and Recipes

Reference for the patterns actively used in Push2026. For the full v2 framework
overview see [docs/frameworks.md](../../docs/frameworks.md).

---

## How Grabbed Buttons Work (M4L)

Creating a `ButtonElement` grabs the MIDI CC/note from Live's default handling.
This is identical in v1 and v2 — the framework version doesn't change it.

In Push2026, unused grabbed buttons sit in a `BackgroundComponent` with a `Layer`
(which also resets their LEDs). M4L accesses controls through the `Live` API, not
raw MIDI, so grabbing is what *enables* M4L to see them.

---

## Mode Switching (ModesComponent + LatchingBehaviour)

`LatchingBehaviour` is the default: tap = switch permanently, hold + release = momentary
peek, returns to previous mode.

```python
from ableton.v2.control_surface.mode import ModesComponent, AddLayerMode
from ableton.v2.control_surface import Layer

self._pad_modes = ModesComponent(name="Pad_Modes")
self._pad_modes.add_mode("drums", self._drum_pads)
self._pad_modes.add_mode("sampler", self._sampler_pads)

self._pad_modes.layer = Layer(
    drums_button=self._elements.some_button,
    sampler_button=self._elements.another_button,
)
self._pad_modes.selected_mode = "drums"
```

### Adding a New Pad Mode

```python
# 1. Instantiate a PadComponent with the desired layout
self._new_pads = PadComponent(layout="pitch_ascending", channel=10, ...)

# 2. Register it as a mode — button wiring and enable/disable is automatic
self._pad_modes.add_mode("new_layout", self._new_pads)
```

---

## Shift Behavior (ComboElement)

`ComboElement` wraps a button + modifier. When the modifier is held, the shifted
element activates. Shifted elements get their own Layer (or AddLayerMode).

```python
from functools import partial
from ableton.v2.control_surface.elements import ComboElement

# In elements.py:
with_shift = partial(ComboElement, modifier=self.shift_button)
self.shifted_record_button = with_shift(control=self.record_button)
```

```python
# In main script — normal and shifted bindings in separate layers:
self._some_component.layer = Layer(
    record_button=self._elements.record_button          # normal
)
# Shifted behavior via AddLayerMode on a mode:
shifted_layer = AddLayerMode(self._some_component, Layer(
    record_button=self._elements.shifted_record_button  # active when shift held
))
```
