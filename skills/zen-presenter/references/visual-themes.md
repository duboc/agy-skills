# Visual Theme Presets

Pre-defined visual theme combinations for the Design Consultation workflow. Each preset combines mood, typography, imagery, and color choices into a cohesive visual identity.

## Theme Presets

### Google Cloud (Default)

Clean, professional Google Cloud styling. Uses a custom Marp theme (`gcloud`) with structured slide types, Google colors, and Inter font. Best used **without** background images — relies on typography, color, and layout classes for visual impact.

| Attribute | Value |
|-----------|-------|
| Mood | Professional |
| Typography | Statement |
| Imagery | None (clean design) |
| Colors | Dark text on white, blue accents |
| Theme | `gcloud` (custom CSS) |
| Class | Varies by slide type |
| Font | Inter, Google Sans, Roboto |

**Frontmatter:**
```markdown
---
marp: true
theme: gcloud
---
```

**Slide type classes available:**
- `title` — Opening slide with large headline, Google gradient bar at bottom
- `section` — Blue background section divider
- `lead` — Centered emphasis content
- `stats` — Numbers and data with blue accent
- `speaker` — Speaker bio/introduction
- `quote` — Large quotation with attribution
- `invert` — Dark background with light text
- `closing` — Centered closing with Google gradient bar
- *(no class)* — Standard white content slide

**Color palette (CSS variables):**
- `--gcloud-blue: #4285F4`
- `--gcloud-red: #EA4335`
- `--gcloud-yellow: #FBBC05`
- `--gcloud-green: #34A853`
- `--gcloud-grey-900: #202124` (primary text)
- `--gcloud-grey-700: #5F6368` (secondary text)
- `--gcloud-light-blue: #5C92F6` (accent numbers)

**Example deck structure:**
```
Slide 1: <!-- _class: title --> — Title + subtitle
Slide 2: (default) — Context/problem statement
Slide 3: <!-- _class: section --> — Section divider
Slide 4: (default) — Key idea
Slide 5: <!-- _class: stats --> — Supporting data
Slide 6: <!-- _class: quote --> — Memorable quote
Slide 7: <!-- _class: closing --> — Call to action
```

**Setup:** Requires the `gcloud-theme.css` file to be registered in VS Code workspace settings under `markdown.marp.themes`, or passed via `--theme gcloud-theme.css` when using the Marp CLI.

---

### Keynote Zen

The classic Garr Reynolds look. Minimalist, high-impact, nature-inspired.

| Attribute | Value |
|-----------|-------|
| Mood | Calm |
| Typography | Statement |
| Imagery | Nature & Landscape |
| Colors | White on dark |
| Brightness | `0.3` |
| Theme | `uncover` |
| Class | `lead` |
| Font suggestion | Large `#` headings only |

**Frontmatter:**
```markdown
---
marp: true
theme: uncover
class: lead
color: white
---
```

**Image keywords:** zen, garden, mountain, ocean, forest, sky, horizon, meadow, lake, sunrise

---

### Corporate Bold

Professional but not boring. Uses architectural photography and strong contrast.

| Attribute | Value |
|-----------|-------|
| Mood | Bold |
| Typography | Statement |
| Imagery | Urban & Architecture |
| Colors | White on dark |
| Brightness | `0.3` |
| Theme | `uncover` |
| Class | `lead` |
| Font suggestion | `#` headings with occasional `##` |

**Frontmatter:**
```markdown
---
marp: true
theme: uncover
class: lead
color: white
---
```

**Image keywords:** architecture, skyline, building, geometric, concrete, glass, bridge, structure, urban, cityscape

---

### Warm Storyteller

Emotional, people-focused. For talks about culture, leadership, or human topics.

| Attribute | Value |
|-----------|-------|
| Mood | Inspiring |
| Typography | Quote-driven |
| Imagery | People & Emotion |
| Colors | White on dark |
| Brightness | `0.35` |
| Theme | `uncover` |
| Class | `lead` |
| Font suggestion | Mix of `#` and `##` with occasional `*italic*` |

**Frontmatter:**
```markdown
---
marp: true
theme: uncover
class: lead
color: white
---
```

**Image keywords:** people, hands, community, connection, faces, crowd, together, culture, emotion, team

---

### Clean Minimalist

Bright, airy, Scandinavian-inspired. For design and product presentations.

| Attribute | Value |
|-----------|-------|
| Mood | Calm |
| Typography | Minimal |
| Imagery | Abstract & Texture |
| Colors | Dark on light |
| Brightness | `0.9` |
| Theme | `default` |
| Class | `lead` |
| Font suggestion | Single `#` word or short phrase |

**Frontmatter:**
```markdown
---
marp: true
theme: default
class: lead
color: #1a1a1a
backgroundColor: #fafafa
---
```

**Image keywords:** minimal, white, texture, marble, paper, linen, clean, space, light, abstract

---

### Tech Neon

High-energy, modern. For tech demos, hackathons, and developer talks.

| Attribute | Value |
|-----------|-------|
| Mood | Bold |
| Typography | Statement |
| Imagery | Abstract & Texture |
| Colors | Accent color (cyan on dark) |
| Brightness | `0.2` |
| Theme | `uncover` |
| Class | `lead` |
| Font suggestion | `#` headings with `**bold**` accent words |

**Frontmatter:**
```markdown
---
marp: true
theme: uncover
class: lead
color: #00f0ff
backgroundColor: #0a0a0a
---
```

**Image keywords:** neon, circuit, code, digital, network, data, space, matrix, technology, cyberpunk

---

### Earth & Organic

Grounded, natural. For sustainability, wellness, or environmental topics.

| Attribute | Value |
|-----------|-------|
| Mood | Calm |
| Typography | Statement |
| Imagery | Nature & Landscape |
| Colors | White on dark |
| Brightness | `0.35` |
| Theme | `uncover` |
| Class | `lead` |
| Font suggestion | `#` headings, soft tone |

**Frontmatter:**
```markdown
---
marp: true
theme: uncover
class: lead
color: #f5f0e8
---
```

**Image keywords:** earth, soil, leaves, wood, river, moss, stone, rain, field, roots

---

### Playful Creative

Vibrant and energetic. For creative pitches, workshops, and brainstorms.

| Attribute | Value |
|-----------|-------|
| Mood | Playful |
| Typography | Minimal |
| Imagery | Abstract & Texture |
| Colors | Accent color (yellow on dark) |
| Brightness | `0.3` |
| Theme | `gaia` |
| Class | `lead` |
| Font suggestion | `#` with `**bold**` for pop |

**Frontmatter:**
```markdown
---
marp: true
theme: gaia
class: lead
color: #ffd166
backgroundColor: #1a1a2e
---
```

**Image keywords:** color, paint, splash, confetti, graffiti, art, creative, vibrant, pattern, kaleidoscope

## Using Presets

When a user selects options during the Design Consultation that match a preset, apply the preset's frontmatter and image keywords as a starting point. Adjust as needed based on the specific topic.

**Default behavior:** If the user says "you decide" or "surprise me," use the **Google Cloud** preset without background images. This produces a clean, professional deck that works well for most audiences.

**With images:** The Google Cloud theme can also be used with background images. When images are enabled, use `![bg brightness:0.3]` directives as normal — the theme styling will still apply to text, and slide type classes remain available.

**Without images (any theme):** When the user opts out of background images, any theme can be used in clean-design mode. Use slide type classes, alternate between white and accent backgrounds, and let typography carry the visual weight.

If a user's choices don't match any preset exactly, compose a custom theme by mixing attributes from the closest presets. Always maintain internal consistency:
- Dark backgrounds pair with light text
- Light backgrounds pair with dark text
- Brightness values must match the color scheme (when images are enabled)
- Image keywords should complement the mood (when images are enabled)
- Slide type classes create visual rhythm when images are disabled
