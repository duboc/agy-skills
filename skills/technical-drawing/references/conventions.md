# Drafting conventions and reusable snippets

Copy-paste patterns for consistent technical drawings. All coordinates assume viewBox `0 0 680 H`.

## Layout skeleton

```xml
<svg width="100%" viewBox="0 0 680 460" role="img" xmlns="http://www.w3.org/2000/svg">
  <title>Short title of the drawing</title>
  <desc>One-sentence description of what the drawing shows, for accessibility.</desc>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6"
      markerHeight="6" orient="auto-start-reverse">
      <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5"
        stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>
  <!-- 1. reference plane (floor/wall) -->
  <!-- 2. matter: objects, structure -->
  <!-- 3. annotations: FOV, reference lines -->
  <!-- 4. cotas -->
  <!-- 5. callout labels (right margin) -->
</svg>
```

Zones: left edge x<75 → full-height cota; right margin x>520 → callout labels; bottom below floor line → horizontal cotas; content between.

## Reference plane (floor or wall)

```xml
<line x1="40" y1="400" x2="640" y2="400" stroke="GRAY_ANNOT" stroke-width="1"/>
```

## Dimension line (cota) patterns

Horizontal (below floor):
```xml
<line x1="250" y1="418" x2="560" y2="418" stroke="GRAY_ANNOT" stroke-width="0.8"
  marker-start="url(#arrow)" marker-end="url(#arrow)"/>
<text x="405" y="436" text-anchor="middle" class="ts">1,37–1,40 m</text>
```

Vertical (full height, left edge):
```xml
<line x1="68" y1="54" x2="68" y2="398" stroke="GRAY_ANNOT" stroke-width="0.8"
  marker-start="url(#arrow)" marker-end="url(#arrow)"/>
<text x="62" y="230" text-anchor="end" class="ts">2,10 m</text>
```

Internal distance (through open space — dashed, label offset to the side):
```xml
<line x1="340" y1="98" x2="340" y2="272" stroke="GRAY_ANNOT" stroke-width="0.8"
  stroke-dasharray="2 3" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
<text x="350" y="180" class="ts">1,1–1,3 m</text>
```

Rules: arrows at BOTH ends always; label gets 8px+ clear air; crossing other annotation lines is fine, crossing text never is. Chained cotas (segment + segment) sit on the same baseline y.

## Leader-line callout

```xml
<g>
  <line x1="362" y1="85" x2="514" y2="88" stroke="GRAY_ANNOT" stroke-width="0.5"/>
  <circle cx="362" cy="85" r="2" fill="GRAY_ANNOT"/>
  <text x="520" y="92" class="ts">Label text</text>
</g>
```

Anchor dot on the object; label in the right margin; leaders must not cross matter or other labels. Stack labels with ≥30px vertical spacing. Two-line labels: second `<text>` 18px below.

## FOV / coverage cone

```xml
<path d="M340 84 L216 276 L464 276 Z" fill="FOV_COLOR" opacity="0.14"/>
<line x1="340" y1="84" x2="216" y2="276" stroke="FOV_STROKE" stroke-width="0.8" stroke-dasharray="4 4"/>
<line x1="340" y1="84" x2="464" y2="276" stroke="FOV_STROKE" stroke-width="0.8" stroke-dasharray="4 4"/>
```

Optical axis (optional, for tilted cameras): single dashed line from lens to target center, `stroke-dasharray="2 4"`, width 0.6.

## Tilted object

```xml
<g transform="rotate(38 130 78)">
  <rect x="106" y="70" width="46" height="16" rx="4" fill="OBJ_FILL" stroke="OBJ_STROKE" stroke-width="0.5"/>
</g>
<circle cx="146" cy="92" r="2.5" fill="LENS_COLOR"/>  <!-- lens placed at rotated position -->
```

Rotate around the object's center. Emitter/lens points are separate elements placed at the post-rotation position so rays start exactly at them.

## Small protrusions (handles, knobs, brackets)

Draw at true scale as small rounded rects in structure gray. They matter for clearance/occlusion and users notice their absence:

```xml
<rect x="218" y="286" width="34" height="6" rx="3" fill="GRAY_STRUCT"/>
```

## Text classes

If CSS classes aren't available (standalone file), inline the equivalent:
- Title/heading (`th`): 15px, font-weight 500
- Small/label (`ts`): 13px
- font-family: system-ui, sans-serif; fill = text color from the active palette

## Multi-view sets

Same scale, same palette, same label vocabulary across all views. Title each view inside its main object or via prose, not floating headings. A measurement corrected in one view is recomputed in all views.
