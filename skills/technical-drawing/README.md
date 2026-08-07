# Technical Drawing (SVG)

Create precise, dimensioned technical drawings in SVG — orthographic views (side/end/top), scale-accurate objects, dimension lines (cotas), leader-line callouts, FOV cones, and equipment/space layouts.

---

## Features

- **Math-First Drafting**: Every coordinate is derived from real-world measurements and a defined scale parameter block — no eyeballing or arbitrary stretching.
- **Dimension Lines (Cotas) & Callouts**: Standardized arrow-ended dimension markers, internal dashed offset lines, and clean leader callouts.
- **Optical & Physical Geometry**: Accurate formulas for field-of-view (FOV) coverage cones, angular spans, occlusion shadows, clearances, and cantilever checks.
- **Orthographic Views**: Side (elevation, long axis), end (elevation, short axis), and top (plan) projections with consistent multi-view scaling.
- **Semantic Palettes**: Neutral standalone and Google-brand palettes with strict semantic color assignments (Blue=subject, Green=context, Yellow=sensing/FOV, Red=alerts, Grey=support).
- **Responsive Corrections**: Modifying a measurement updates the parameter block, recalculates derived values, updates affected views, and explains physical impacts.

---

## Skill Structure

```text
technical-drawing/
├── SKILL.md                          # Main skill prompt and core drafting workflow
├── README.md                         # Skill overview and documentation
└── references/
    ├── conventions.md                # Layout skeleton, cota/leader/FOV snippets, and text rules
    ├── geometry.md                   # Scale selection, parameter blocks, and geometric formulas
    └── palette-google.md             # Google brand palette and Material grey ramp semantic mapping
```

---

## Usage Examples

Trigger this skill by asking:
- *"Draw a side view of a camera mounted 1.2 m above a 1.4 m workbench with dimension lines."*
- *"Create an orthographic drawing of this equipment setup showing clearances."*
- *"Visualize the FOV cone of a 78° lens over this workspace."*
- *"Desenhe a vista superior e lateral dessa bancada com as cotas."*
- *"Adjust the table width to 1.60 m and update the coverage calculations."*

---

## Installation

### Workspace Scope

Install to `.agents/skills/technical-drawing/` in your current project:

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- technical-drawing
```

### User Scope (Global)

Install to `~/.gemini/config/skills/technical-drawing/` for availability across all projects:

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- technical-drawing --scope user
```
