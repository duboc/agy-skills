# Visual Theme Presets for Clarity Presenter

Pre-defined visual theme combinations for the Design Consultation workflow. Each preset defines how both technical and business perspective slides appear, preserving the dual-perspective alternation pattern.

## Key Constraint: Dual-Perspective Preservation

Every clarity-presenter theme must define two visual modes:

1. **Technical perspective** — lighter background for "how it works" slides
2. **Business perspective** — darker/accent background for "why it matters" slides

The alternation pattern (tech → biz → tech → biz) is what makes clarity decks effective for mixed audiences. Themes modify the colors and mood of both perspectives, never eliminating the distinction.

## Theme Presets

### Google Cloud (Default)

Standard Google Cloud identity. White technical slides, dark business slides, blue section dividers. The most versatile preset.

| Attribute | Technical Slides | Business Slides |
|-----------|-----------------|-----------------|
| Background | White (`#FFFFFF`) | Dark grey (`#202124`) or Blue (`#4285F4`) |
| Text color | Dark (`#202124`) | White |
| Accent | Google Blue (`#4285F4`) | Light Blue (`#5C92F6`) |
| Class | *(default)* | `invert` or `section` |

| Attribute | Value |
|-----------|-------|
| Mood | Professional |
| Audience balance | Balanced (default) |
| Typography | Assertion headlines (h2) |
| Theme | `gcloud` |
| Font | Inter, Google Sans, Roboto |

**Frontmatter:**
```markdown
---
marp: true
theme: gcloud
---
```

**Section dividers:** `<!-- _class: section -->` (blue)
**Question slide:** `<!-- _class: lead -->`
**Image keywords (when enabled):** technology, cloud, infrastructure, code, server, network

**Example deck structure:**
```
Slide 1: <!-- _class: title --> — Title + subtitle
Slide 2: (default) — Situation: assertion + evidence
Slide 3: <!-- _class: section --> — Complication divider
Slide 4: (default) — Technical complication assertion
Slide 5: <!-- _class: invert --> — Business complication assertion
Slide 6: <!-- _class: lead --> — Central question
Slide 7: <!-- _class: section --> — Answer divider
Slide 8: (default) — Technical answer assertion
Slide 9: <!-- _class: invert --> — Business answer assertion
Slide 10: <!-- _class: closing --> — Call to action
```

---

### Executive Blue

Formal, polished. Navy tones with gold accents on business slides. Conveys authority and strategic thinking.

| Attribute | Technical Slides | Business Slides |
|-----------|-----------------|-----------------|
| Background | Pale blue-grey (`#F0F4F8`) | Navy (`#1B2A4A`) |
| Text color | Dark navy (`#1B2A4A`) | White |
| Accent | Steel blue (`#3A6EA5`) | Gold (`#C9A94F`) |
| Class | *(default)* with `_backgroundColor` | `invert` with `_backgroundColor` |

| Attribute | Value |
|-----------|-------|
| Mood | Professional, formal |
| Audience balance | Business-heavy recommended |
| Best for | Board presentations, executive reviews, strategy decks |
| Theme | `gcloud` |

**Frontmatter:**
```markdown
---
marp: true
theme: gcloud
style: |
  section {
    background-color: #F0F4F8;
    color: #1B2A4A;
  }
  section strong {
    color: #3A6EA5;
  }
  section.invert {
    background-color: #1B2A4A;
    color: #FFFFFF;
  }
  section.invert strong {
    color: #C9A94F;
  }
  section.section {
    background-color: #1B2A4A;
    color: #FFFFFF;
  }
  section.closing::after,
  section.title::after {
    background: linear-gradient(to right, #3A6EA5 25%, #1B2A4A 25%, #1B2A4A 50%, #C9A94F 50%, #C9A94F 75%, #3A6EA5 75%);
  }
---
```

**Image keywords (when enabled):** boardroom, skyline, executive, corporate, strategy, summit, horizon

---

### Data-Driven

Analytical and precise. Teal accents for technical slides, orange for business metrics. Designed for presentations heavy on data and quantitative claims.

| Attribute | Technical Slides | Business Slides |
|-----------|-----------------|-----------------|
| Background | White (`#FFFFFF`) | Charcoal (`#2D2D2D`) |
| Text color | Dark (`#333333`) | White |
| Accent | Data teal (`#00897B`) | Metric orange (`#FF6D00`) |
| Class | *(default)* | `invert` |

| Attribute | Value |
|-----------|-------|
| Mood | Analytical, precise |
| Audience balance | Balanced recommended |
| Best for | Data/analytics presentations, metric reviews, performance reports |
| Theme | `gcloud` |

**Frontmatter:**
```markdown
---
marp: true
theme: gcloud
style: |
  section {
    color: #333333;
  }
  section strong {
    color: #00897B;
  }
  section.invert {
    background-color: #2D2D2D;
    color: #FFFFFF;
  }
  section.invert strong {
    color: #FF6D00;
  }
  section.section {
    background-color: #00897B;
    color: #FFFFFF;
  }
  section.stats h2 {
    color: #00897B;
  }
---
```

**Tips:** Favor the `stats` class for evidence slides with quantitative assertions. Use orange accents on business slides to draw attention to financial metrics.

**Image keywords (when enabled):** data, analytics, dashboard, metrics, chart, graph, numbers

---

### Cloud Architecture

Technical-focused. Clean whites for architecture diagrams, dark slate for operational impact. Code blocks and diagrams render well on both perspective types.

| Attribute | Technical Slides | Business Slides |
|-----------|-----------------|-----------------|
| Background | White (`#FFFFFF`) | Dark slate (`#1E293B`) |
| Text color | Near-black (`#0F172A`) | Slate grey (`#CBD5E1`) |
| Accent | Sky blue (`#0EA5E9`) | Emerald (`#10B981`) |
| Class | *(default)* | `invert` |

| Attribute | Value |
|-----------|-------|
| Mood | Technical, detailed |
| Audience balance | Technical-heavy recommended |
| Best for | Architecture reviews, system design proposals, migration plans |
| Theme | `gcloud` |

**Frontmatter:**
```markdown
---
marp: true
theme: gcloud
style: |
  section {
    color: #0F172A;
  }
  section strong {
    color: #0EA5E9;
  }
  section.invert {
    background-color: #1E293B;
    color: #CBD5E1;
  }
  section.invert strong {
    color: #10B981;
  }
  section.section {
    background-color: #0EA5E9;
    color: #FFFFFF;
  }
  section pre {
    background-color: #0F172A;
  }
---
```

**Tips:** Technical slides often use code blocks and diagram embeds — this theme keeps them readable. Business slides use emerald accents to signal positive outcomes (cost savings, risk reduction).

**Image keywords (when enabled):** architecture, blueprint, circuit, structure, network, cloud, infrastructure

---

### Innovation Pitch

Inspiring and forward-looking. High contrast between light technical slides and deep purple business slides. Creates dramatic visual shifts that hold attention during proposals.

| Attribute | Technical Slides | Business Slides |
|-----------|-----------------|-----------------|
| Background | Light grey (`#FAFAFA`) | Deep purple-black (`#1A1025`) |
| Text color | Dark (`#2D2D2D`) | White |
| Accent | Electric violet (`#7C3AED`) | Warm amber (`#F59E0B`) |
| Class | *(default)* | `invert` |

| Attribute | Value |
|-----------|-------|
| Mood | Inspiring, forward-looking |
| Audience balance | Balanced recommended |
| Best for | Innovation proposals, new initiative introductions, product vision decks |
| Theme | `gcloud` |

**Frontmatter:**
```markdown
---
marp: true
theme: gcloud
style: |
  section {
    background-color: #FAFAFA;
    color: #2D2D2D;
  }
  section strong {
    color: #7C3AED;
  }
  section.invert {
    background-color: #1A1025;
    color: #FFFFFF;
  }
  section.invert strong {
    color: #F59E0B;
  }
  section.section {
    background-color: #7C3AED;
    color: #FFFFFF;
  }
  section.lead {
    background-color: #FAFAFA;
    color: #7C3AED;
  }
---
```

**Tips:** The violet-to-amber shift between perspectives creates a memorable visual pattern. The Question slide uses violet text on light background for maximum impact.

**Image keywords (when enabled):** innovation, future, horizon, launch, spark, light, rocket, breakthrough

---

### Compliance & Security

Measured and authoritative. Conservative palette with trust blue accents. Business slides use dual accent colors: red for risks/gaps, green for compliance/pass.

| Attribute | Technical Slides | Business Slides |
|-----------|-----------------|-----------------|
| Background | Off-white (`#F8F8F8`) | Dark grey (`#1F2937`) |
| Text color | Dark (`#1F2937`) | Light grey (`#E5E7EB`) |
| Accent | Trust blue (`#1D4ED8`) | Red (`#DC2626`) for risks, Green (`#059669`) for compliance |
| Class | *(default)* | `invert` |

| Attribute | Value |
|-----------|-------|
| Mood | Measured, authoritative, conservative |
| Audience balance | Business-heavy recommended |
| Best for | Security reviews, compliance assessments, risk reports, audit preparation |
| Theme | `gcloud` |

**Frontmatter:**
```markdown
---
marp: true
theme: gcloud
style: |
  section {
    background-color: #F8F8F8;
    color: #1F2937;
  }
  section strong {
    color: #1D4ED8;
  }
  section.invert {
    background-color: #1F2937;
    color: #E5E7EB;
  }
  section.invert strong {
    color: #DC2626;
  }
  section.invert em {
    color: #059669;
  }
  section.section {
    background-color: #1D4ED8;
    color: #FFFFFF;
  }
---
```

**Tips:** On business slides, use `**bold**` for risks and gaps (renders in red) and `*italic*` for compliance items (renders in green). This dual-accent pattern lets you present risk assessments visually without extra graphics.

**Image keywords (when enabled):** security, shield, lock, fortress, compliance, audit, defense

## Using Presets

When a user's choices during the Design Consultation match a preset, apply the preset's frontmatter and configuration.

### How Themes Work

All presets build on the `gcloud` base theme. They override its defaults using a `style` block in the MARP frontmatter. No additional CSS files are needed — the overrides are self-contained in the deck's YAML header.

The pattern:
1. Start with `theme: gcloud` (always)
2. Add `style: |` block with CSS overrides for colors
3. Technical slides use the default `section` styles
4. Business slides use `section.invert` overrides
5. Section dividers use `section.section` overrides

### Defaults

If the user says "you decide" or "surprise me," use the **Google Cloud** preset. It produces a clean, professional deck that works for any audience.

### Custom Mixing

If no preset matches exactly, compose a custom theme by mixing attributes from the closest presets. Always maintain:

- **Contrast between perspectives** — technical and business slides must be visually distinct
- **Light technical, dark business** — this is the core pattern; never reverse it
- **One accent per perspective** — too many colors reduce clarity
- **Consistent section dividers** — match the overall color scheme

### With Images

When the user opts in to background images, any preset can be combined with `![bg brightness:X]` directives:

- Technical slides: `brightness:0.8` to `brightness:0.95` (keep light)
- Business slides: `brightness:0.2` to `brightness:0.4` (keep dark)
- Maintain the light/dark distinction even with images
