# Clarity Presenter

A Agy skill for generating MARP presentation decks using the **SCQA** (Situation-Complication-Question-Answer) narrative framework with **assertion-evidence** slide design and **dual-perspective** paired slides for mixed technical and business audiences. Uses Google identity styling and outputs self-contained HTML with optional PowerPoint export.

## What It Does

This skill transforms any technical topic into a structured slide deck that bridges engineers and stakeholders. It guides Agy through:

1. **Topic discovery** — Captures the subject, audience, key concepts (3-5), and core takeaway.
2. **Design consultation** — Asks about background images, audience balance, and mood preferences.
3. **SCQA story arc planning** — Maps content to the Situation-Complication-Question-Answer narrative framework.
4. **Dual-perspective concept mapping** — Plans technical (how) and business (why) assertion headlines for each concept.
5. **Assertion-evidence slide generation** — Produces MARP Markdown with sentence headlines (8-15 words), not topic labels, backed by visual evidence.
6. **HTML rendering** — Converts the MARP deck to a self-contained HTML file via Marp CLI that can be presented directly in any browser.
7. **PowerPoint offer** — Asks the user if they want to export to `.pptx` via Marp CLI.

## When Does It Activate?

The skill activates when you ask Agy to create structured, dual-audience presentations. Keywords include:

| Trigger | Example |
|---------|---------|
| SCQA presentation | "Create an SCQA presentation about our API migration" |
| Assertion-evidence deck | "Build an assertion-evidence deck about Kubernetes adoption" |
| Technical and business | "I need slides that explain service mesh to both engineers and VPs" |
| Dual perspective | "Create a dual-perspective presentation about our data platform" |
| Structured deck | "Generate a structured deck about cloud security for a mixed audience" |
| Clarity presentation | "Make a clarity presentation about our microservices strategy" |

## How It Differs from Zen Presenter

| Aspect | Zen Presenter | Clarity Presenter |
|--------|--------------|-------------------|
| **Words per slide** | Max 10 | 15-25 |
| **Headlines** | Single words or short phrases | 8-15 word sentence assertions |
| **Bullets** | Never | Sparingly (max 3 items) |
| **Structure** | Narrative arc (hook → climax → resolution) | SCQA (situation → complication → question → answer) |
| **Audience** | Single perspective | Dual: technical + business paired slides |
| **Visual variety** | Theme classes for rhythm | White (technical) vs dark (business) alternation |
| **Best for** | Keynotes, inspiration, storytelling | Technical proposals, architecture reviews, strategy decks |

## Topics Covered

| Area | Details |
|------|---------|
| **SCQA Framework** | Situation-Complication-Question-Answer narrative structure from McKinsey |
| **Assertion-Evidence** | Michael Alley's method — sentence headlines backed by visual evidence |
| **Dual Perspectives** | Technical (how) + business (why) translation patterns |
| **MARP Markdown** | Frontmatter directives, themes, slide classes, export commands |
| **Google Identity** | Google colors, Inter/Google Sans fonts, gradient bar accents |
| **Visual Themes** | 6 presets with dual-perspective color schemes, CSS variable overrides, audience-adapted mood and accent colors |
| **Diagrams** | Pre-rendered SVG embedding, Mermaid CLI workflow, Kroki URL rendering, diagrams as visual evidence for assertions |

## Installation

### Option B: One-liner

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- clarity-presenter
```

For user-scope installation (available across all projects):

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- clarity-presenter --scope user
```

### Option C: Manual

```bash
cp -r skills/clarity-presenter ~/.gemini/config/skills/clarity-presenter
```

## Usage Examples

Once installed, the skill activates when you ask Agy to create structured, dual-audience presentations.

### Basic SCQA deck

```
Create a presentation about migrating from monolith to microservices
for a mixed audience of engineers and engineering directors.
```

### With key concepts specified

```
Create an SCQA deck about our API gateway migration. Key concepts:
authentication, rate limiting, and observability. The audience is
our platform team and product leadership.
```

### Technical-heavy audience

```
Build an assertion-evidence presentation about Kubernetes autoscaling
for our SRE team and their engineering manager. Technical-heavy balance.
```

### Business-heavy audience

```
I need a structured deck about data platform consolidation for the CTO
and finance team. Focus on cost and risk. Business-heavy balance.
```

### Quick deck with defaults

```
Make a clarity presentation about why we should adopt a service mesh.
You decide the look and feel.
```

## Google Identity Theme

The skill includes a custom Marp CSS theme (`gcloud-theme.css`) styled after the Google identity. Features:

- **Inter / Google Sans** font family
- **Google color palette** (blue, red, yellow, green)
- **Slide type classes** for visual variety: `title`, `section`, `lead`, `stats`, `quote`, `invert`, `closing`
- **White/dark alternation** for distinguishing technical and business slides
- Clean, professional look suitable for mixed audiences
- **6 visual theme presets** (see `references/visual-themes.md`) that customize the gcloud base theme for specific use cases like executive reviews, data analytics, architecture decks, innovation pitches, and compliance assessments. All presets preserve the dual-perspective white/dark alternation pattern.

### Setting up the custom theme in VS Code

1. Copy `gcloud-theme.css` to your workspace
2. Open workspace settings (F1 → "Preferences: Open Workspace Settings")
3. Search "Marp: Themes" and add the path `./gcloud-theme.css`
4. Use `theme: gcloud` in your Markdown frontmatter

### Using with Marp CLI

```bash
# Render to self-contained HTML
npx @marp-team/marp-cli@latest slides.md --html --theme ./gcloud-theme.css -o slides.html

# Export to PowerPoint
npx @marp-team/marp-cli@latest slides.md --theme ./gcloud-theme.css --pptx -o slides.pptx

# Export to PDF
npx @marp-team/marp-cli@latest slides.md --pdf --theme ./gcloud-theme.css -o slides.pdf
```

## Included References

| File | Description |
|------|-------------|
| **assertion-evidence-guide.md** | Sentence headline writing rules, evidence types, falsifiability test, good vs bad headline examples |
| **scqa-framework-guide.md** | SCQA narrative structure, content mapping, 3 complete technical examples, anti-patterns |
| **dual-perspective-guide.md** | 12+ technical-to-business translation patterns, audience balance adaptation, writing process for paired headlines |
| **visual-themes.md** | 6 visual theme presets adapted for dual-perspective SCQA decks — Google Cloud, Executive Blue, Data-Driven, Cloud Architecture, Innovation Pitch, Compliance & Security |
| **diagram-guide.md** | Diagram embedding workflows — pre-rendered SVG, Kroki URLs, Mermaid CLI, diagrams as assertion evidence |

## Included Assets

| File | Description |
|------|-------------|
| **gcloud-theme.css** | Custom Marp CSS theme with Google identity styling and slide type classes |
| **deck-template.md** | Starter template demonstrating SCQA structure with dual-perspective paired slides |
