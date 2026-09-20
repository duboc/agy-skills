# Zen Presenter

A Agy skill for generating MARP presentation decks that follow the **Presentation Zen** philosophy — minimal text, high visual impact, and storytelling-driven design. Uses Google identity styling and outputs self-contained HTML with optional PowerPoint export.

## What It Does

This skill transforms any topic into a visually striking slide deck by applying Garr Reynolds' Presentation Zen principles. It guides Agy through:

1. **Topic discovery** — Captures the subject, audience, and core takeaway.
2. **Design consultation** — Asks about background images (optional), mood, and typography preferences before generating anything.
3. **Story arc planning** — Structures the deck as a narrative: hook, tension, exploration, climax, resolution.
4. **Zen slide generation** — Produces MARP Markdown with a target of 10 words per slide, retaining essential context and sources, zero bullet points, and either full-bleed Unsplash backgrounds or clean theme-based design.
5. **HTML rendering** — Converts the MARP deck to a self-contained HTML file via Marp CLI that can be presented directly in any browser.
6. **PowerPoint offer** — Asks the user if they want to export to `.pptx` via Marp CLI.

## When Does It Activate?

The skill activates when you ask Agy to create presentations, slides, or decks. Keywords include:

| Trigger | Example |
|---------|---------|
| Create a presentation | "Create a presentation about cloud architecture" |
| Generate slides | "Generate slides for my team meeting on observability" |
| Build a deck | "Build a MARP deck about Kubernetes best practices" |
| Zen presentation | "Make a Zen-style presentation about leadership" |
| MARP slides | "Create MARP slides about AI safety" |

## Topics Covered

| Area | Details |
|------|---------|
| **Presentation Zen** | Restraint (Kanso), Naturalness (Shizen), Emptiness (Ma), signal-to-noise ratio |
| **MARP Markdown** | Frontmatter directives, background images, filters, themes, custom themes, export commands |
| **Visual Design** | Mood presets, typography styles, image metaphor selection, slide type classes |
| **Story Structure** | Narrative arcs, audience adaptation, hook-tension-climax-resolution |
| **Google Identity** | Google colors (blue, red, yellow, green), Inter/Google Sans fonts, gradient bar accents |
| **Background Images** | Optional — user chooses whether to use full-bleed Unsplash images or clean theme-based design |
| **Diagrams** | Pre-rendered SVG embedding, Mermaid CLI workflow, Kroki URL rendering, minimal diagram guidelines |

## Installation

### Option B: One-liner

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- zen-presenter
```

For user-scope installation (available across all projects):

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- zen-presenter --scope user
```

### Option C: Manual

```bash
cp -r skills/zen-presenter ~/.gemini/config/skills/zen-presenter
```

## Usage Examples

Once installed, the skill activates when you ask Agy to create presentations.

### Basic deck generation

```
Create a presentation about microservices architecture for a developer conference.
```

### With audience context

```
I need a Zen-style presentation about data privacy for an executive audience.
The one takeaway should be: "Privacy is a competitive advantage, not a cost."
```

### Clean design (no background images)

```
Generate slides about cloud-native architecture, no background images.
Professional mood, around 8 slides.
```

### With background images

```
Create a presentation about sustainable engineering with full-bleed nature
images, calm mood, and white text on dark backgrounds. Around 8 slides.
```

### Quick deck with defaults

```
Make a quick Zen presentation about why Kubernetes matters. You decide the look and feel.
```

## Google Identity Theme

The skill includes a custom Marp CSS theme (`gcloud-theme.css`) styled after the Google identity. Features:

- **Inter / Google Sans** font family
- **Google color palette** (blue, red, yellow, green)
- **Slide type classes** for visual variety without images: `title`, `section`, `lead`, `stats`, `speaker`, `quote`, `invert`, `closing`
- **Google gradient bar** on title and closing slides
- Clean, professional look suitable for most audiences

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
| **marp-syntax-guide.md** | Complete MARP Markdown syntax reference — frontmatter, background images, filters, themes, custom themes, export commands |
| **zen-design-principles.md** | Presentation Zen philosophy — restraint, naturalness, emptiness, visual metaphor guide, story arc structure |
| **visual-themes.md** | Visual theme presets and slide type class reference |
| **diagram-guide.md** | Diagram embedding workflows — pre-rendered SVG, Kroki URLs, Mermaid CLI, style guidelines for minimal diagrams |

## Included Assets

| File | Description |
|------|-------------|
| **gcloud-theme.css** | Custom Marp CSS theme with Google identity styling and slide type classes |
| **deck-template.md** | Starter template using the gcloud theme (clean design, no images) |
| **deck-template-images.md** | Starter template with full-bleed Unsplash background images |
