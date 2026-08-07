# Palette: Google

Use this palette when the user asks for "Google colors", the drawing targets Google-internal docs/decks, or the `google` palette is requested. Based on the Google brand primaries and the Material grey ramp.

## Core colors

| Token | Hex | Use in technical drawings |
|---|---|---|
| Google Blue 500 | `#4285F4` | Subject/hero object (the camera, the sensor — the thing being specified) |
| Blue 700 | `#1967D2` | Subject stroke/outline; emphasis text |
| Blue 50 | `#E8F0FE` | Subject fill (light), highlighted zones |
| Google Green 500 | `#34A853` | Main context object (the table, the machine, the room) |
| Green 700 | `#188038` | Context object stroke |
| Green 50 | `#E6F4EA` | Context object fill (light) |
| Google Yellow 500 | `#FBBC04` | FOV cones, beams, light, coverage areas (use with `opacity="0.16"` for fills) |
| Yellow 700 | `#F29900` | FOV ray strokes (dashed) |
| Google Red 500 | `#EA4335` | Alerts only: interference zones, blind spots, clearance violations, danger |
| Red 700 | `#C5221F` | Alert strokes/text |

## Greys (Material grey ramp)

| Token | Hex | Use |
|---|---|---|
| Grey 900 | `#202124` | Primary text, titles |
| Grey 700 | `#5F6368` | Secondary text, cota labels |
| Grey 500 | `#9AA0A6` | Annotation strokes: cotas, leaders, reference planes |
| Grey 300 | `#DADCE0` | Structure fills: poles, legs, brackets, protrusions |
| Grey 100 | `#F1F3F4` | Optional panel/background zones |
| Grey 50 | `#F8F9FA` | Page background if one is needed (prefer transparent) |

## Semantic mapping (fixed — don't improvise)

- **Blue = the thing being specified.** One per drawing. Fill Blue 50, stroke Blue 700, or solid Blue 500 for small objects.
- **Green = what it acts on / sits on.** Fill Green 50, stroke Green 700; body text inside in Grey 900.
- **Yellow = sensing/illumination volumes.** Never for matter.
- **Red = problems.** If nothing is wrong, no red appears. A drawing with red must explain the red in prose.
- **Grey = everything supporting.** Structure, cotas, leaders, floors.

Filled shapes get `stroke-width="0.5"` outlines in their 700 tone. Text: 15px/500-weight titles in Grey 900, 13px labels in Grey 700, font-family `'Google Sans', Roboto, system-ui, sans-serif`.

## Accessibility notes

- Yellow 500 text on white fails contrast — never use yellow for text; label FOV cones in Grey 700.
- Red/green colorblind safety: red and green never carry meaning alone — alerts are also dashed-outlined and labeled; context objects are also the largest shape.
- Keep the standalone-file fallback (neutral palette in SKILL.md) when the audience is not Google-branded.
