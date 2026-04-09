# Color System (`pushbase.colors`)

Import from `pushbase.colors`. Never copy this file into the script.

```python
from pushbase.colors import RgbColor, Pulse, Blink, FallbackColor, Basic, Rgb, BiLed, LIVE_COLORS_TO_MIDI_VALUES
```

## Key Classes

| Class | Purpose |
|---|---|
| `RgbColor(midi_value)` | Static RGB pad/button color. Index-based (0–127). |
| `FallbackColor(default, fallback_midi)` | Uses RGB color on RGB interface, falls back to a plain MIDI value on non-RGB. |
| `Pulse(color1, color2, speed)` | Animates between two colors. `speed` ∈ `{4, 6, 12, 24, 48}` (BPM fractions). |
| `Blink(color1, color2, speed)` | Hard blink between two colors. Same speed values as Pulse. |
| `TransparentColor` | No-op draw — leaves LED unchanged. |

## Named Color Palettes

- **`Rgb`** — named `RgbColor` constants: `Rgb.RED`, `Rgb.GREEN`, `Rgb.BLUE`, `Rgb.WHITE`, `Rgb.BLACK`, `Rgb.YELLOW`, `Rgb.CYAN`, `Rgb.MAGENTA`, `Rgb.PINK`, etc. (18 named colors)
- **`Basic`** — `FallbackColor` presets for non-RGB buttons: `Basic.OFF`, `Basic.HALF`, `Basic.FULL`, `Basic.FULL_BLINK_SLOW`, etc.
- **`BiLed`** — presets for bi-color LEDs (green/red/yellow/amber + blink variants): `BiLed.GREEN`, `BiLed.RED`, `BiLed.YELLOW`, `BiLed.AMBER`, and their `_HALF`, `_BLINK_SLOW`, `_BLINK_FAST` variants.

## Mapping Live Colors → Push MIDI Values

`LIVE_COLORS_TO_MIDI_VALUES` — dict mapping Live's integer RGB color values (as returned by `clip.color` or `track.color`) to Push MIDI color indices. Use this to make pad colors match clip/track colors.
