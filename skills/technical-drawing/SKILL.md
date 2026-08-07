---
name: technical-drawing
description: >-
  Create precise, dimensioned technical drawings in SVG — orthographic views
  (side/end/top), scale-accurate objects, dimension lines (cotas), leader-line
  callouts, FOV cones, and equipment/space layouts. Use this whenever the user
  wants to draw, sketch, spec, or show a physical setup with measurements —
  camera rigs, mounts, tripods, tables, furniture, rooms, machines,
  installations, floor plans — or asks to adjust dimensions on an existing
  drawing. Trigger even without the words "technical drawing", e.g. "posição
  do equipamento", "desenho disso", "vista lateral/superior", "coloque as
  medidas", or when the user gives real-world measurements to visualize.
---

# Technical Drawing (SVG)

Produce drafting-style drawings where every object is placed by computed coordinates from real-world measurements. The drawing IS the math: fix a scale, convert meters to pixels, and derive everything. Never eyeball proportions and never stretch an existing drawing to "fit" new measurements — recompute from the parameter block.

## References (read before drawing)

- `references/conventions.md` — layout skeleton, cota/leader/FOV/tilt snippets to copy, text rules, multi-view rules. Read for every drawing.
- `references/geometry.md` — scale selection, parameter block format, FOV/coverage/occlusion/clearance formulas, worked example. Read whenever any value must be derived (almost always).
- `references/palette-google.md` — Google-brand palette with fixed semantic mapping. Read when the user wants Google colors or the audience is Google-internal.

## Core workflow

1. **Collect real measurements.** Dimensions, heights, distances, angles. Ranges (1,37–1,40 m): draw the midpoint, label the range. Missing critical measurement: use a documented standard value and say so in prose — never silently invent.
2. **Choose the view(s).** Orthographic only (side/end/top — see geometry.md). No fake 3D/isometric: it breaks measurement reading. If the user wants "how it looks", offer additional orthographic views.
3. **Fix the scale and write the parameter block** (geometry.md) before drawing anything.
4. **Compute all coordinates** from the parameter block using the geometry recipes.
5. **Draw in layers**: reference plane → matter → annotations → cotas → callout labels (conventions.md).
6. **Run the quality checklist** below before emitting.

## Palette selection

- **Inline visualization tool available** (widget/visualizer with design guidance): load its design guidance and use its CSS variables/classes. Semantic accents: one color for the subject, one for the context object, amber/yellow for FOV, neutral for structure.
- **Google-branded output**: use `references/palette-google.md` (fixed semantic mapping: Blue=subject, Green=context, Yellow=sensing, Red=problems only, Grey=support).
- **Neutral standalone** (.svg/.html/Markdown files, no branding): matter `#3D6B6B` + accent `#C86B4A`, structure `#B4B2A9`, annotations `#888780`, FOV `#EF9F27` @0.14, text `#3A3A36`, font `system-ui, sans-serif`.

All targets: `role="img"` + `<title>` + `<desc>` for accessibility; user's locale for units and decimal separators (`1,40 m` pt-BR / `1.40 m` en).

## Correction protocol

When the user corrects a measurement: return to the parameter block, recompute every derived value (positions, FOV intersections, clearances), redraw all affected views, and state in prose what changed as a consequence (e.g., "the new length raises the minimum camera height to X"). This is the skill's defining behavior — a correction updates conclusions, not just a rectangle.

## Quality checklist (before emitting)

1. Every drawn size traces to a real measurement × scale — no freehand proportions.
2. Cotas have arrows at both ends and legible labels with ≥8px clear air.
3. Dashed = non-matter, solid = matter — no exceptions.
4. Every derived value stated (height, angle, coverage, clearance) was actually computed and is consistent across drawing, labels, and prose.
5. Labels collide with nothing; right margin reserved for callouts; leaders cross no matter.
6. Physical sanity pass: supports reach required heights, clearances are positive, nothing floats, cantilevers have counterweights. If the user's requested arrangement has a flaw, draw it as asked and flag the flaw in prose.
7. Multi-view sets share scale, palette, and vocabulary; a corrected measurement propagated to every view.
