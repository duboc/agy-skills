# MARP Syntax Guide

Quick reference for MARP Markdown syntax used in Zen Presenter decks.

## Frontmatter Directive

Every MARP deck starts with a YAML frontmatter block:

```markdown
---
marp: true
theme: uncover
class: lead
color: white
backgroundColor: black
---
```

### Available Themes

| Theme | Description | Best For |
|-------|-------------|----------|
| `gcloud` | Google Cloud styling with structured layouts (custom) | Professional, clean design (default) |
| `default` | Clean, neutral styling | General purpose |
| `uncover` | Bold, full-bleed image support | Zen presentations with images |
| `gaia` | Modern, colorful | Playful or vibrant decks |

**Note:** The `gcloud` theme is a custom CSS theme provided by this skill. See the "Custom Themes" section below for setup instructions.

### Global Directives

| Directive | Purpose | Example |
|-----------|---------|---------|
| `marp: true` | Enable MARP processing | Required in every deck |
| `theme` | Set the slide theme | `theme: uncover` |
| `class` | Set default slide class | `class: lead` |
| `color` | Set default text color | `color: white` |
| `backgroundColor` | Set default background | `backgroundColor: #000` |
| `paginate` | Show slide numbers | `paginate: false` (default for Zen) |
| `header` | Set header text | Avoid for Zen decks |
| `footer` | Set footer text | Avoid for Zen decks |

## Slide Separation

Slides are separated by `---` on its own line:

```markdown
---

# First Slide

---

# Second Slide

---
```

## Background Images

### Full-bleed Background

```markdown
![bg](https://source.unsplash.com/featured/?mountain)
```

### With Brightness Filter

```markdown
![bg brightness:0.3](https://source.unsplash.com/featured/?ocean)
```

### With Blur

```markdown
![bg blur:3px](https://source.unsplash.com/featured/?forest)
```

### Combined Filters

```markdown
![bg brightness:0.3 blur:2px](https://source.unsplash.com/featured/?city)
```

### Background Sizing

| Syntax | Effect |
|--------|--------|
| `![bg](url)` | Cover (fills slide, may crop) |
| `![bg contain](url)` | Fit within slide |
| `![bg fit](url)` | Scale to fit |
| `![bg auto](url)` | Original size |

### Background Position

```markdown
![bg right](url)    <!-- Image on right half -->
![bg left](url)     <!-- Image on left half -->
![bg right:40%](url) <!-- Image takes 40% on right -->
```

### Multiple Backgrounds

```markdown
![bg](url1)
![bg](url2)
```

This creates a split layout with images side by side.

## Image Filters Reference

| Filter | Values | Effect |
|--------|--------|--------|
| `brightness` | `0.0`–`1.0` | Darken image (lower = darker) |
| `blur` | `1px`–`20px` | Blur the image |
| `contrast` | `0.0`–`2.0` | Adjust contrast |
| `grayscale` | `0.0`–`1.0` | Convert to grayscale |
| `opacity` | `0.0`–`1.0` | Adjust transparency |
| `sepia` | `0.0`–`1.0` | Apply sepia tone |

## Text Formatting

### Heading Levels for Slides

```markdown
# Large Impact Text        <!-- Use for main statements -->
## Secondary Text           <!-- Use for supporting phrases -->
### Smaller Accent Text     <!-- Use sparingly -->
```

### Emphasis

```markdown
**Bold** for key words
*Italic* for subtle emphasis
```

### Text Alignment

Per-slide class directives:

```markdown
<!-- _class: lead -->     <!-- Centered text (recommended for Zen) -->
<!-- _class: invert -->   <!-- Inverted colors -->
```

### Custom Positioning with HTML

For precise control (use sparingly):

```markdown
<div style="text-align: center; margin-top: 40%;">

# Your Text Here

</div>
```

## Per-Slide Directives

Override global settings for individual slides using HTML comments:

```markdown
<!-- _backgroundColor: #1a1a2e -->
<!-- _color: #e94560 -->
<!-- _class: lead -->

# This slide has custom colors
```

## Unsplash Source URL Patterns

### Featured Photos by Keyword

```
https://source.unsplash.com/featured/?KEYWORD
https://source.unsplash.com/featured/?KEYWORD1,KEYWORD2
```

### Specific Dimensions

```
https://source.unsplash.com/1920x1080/?KEYWORD
```

### Random Photo by Keyword

```
https://source.unsplash.com/random/?KEYWORD
```

## Export Commands

| Command | Output |
|---------|--------|
| `marp deck.md` | HTML file |
| `marp deck.md --pdf` | PDF file |
| `marp deck.md --pptx` | PowerPoint file |
| `marp deck.md --html` | HTML with inline assets |
| `marp deck.md --preview` | Open in browser |

## Custom Themes

Marp supports custom CSS themes. This skill includes the `gcloud` theme (`assets/gcloud-theme.css`).

### Custom Theme CSS Structure

A custom Marp theme CSS file must start with a `@theme` comment:

```css
/* @theme your-theme-name */

@import 'default';

/* Your custom styles */
h1 {
  color: #4285F4;
}
```

The `@import` line inherits from a built-in theme (`default`, `uncover`, or `gaia`).

### Using Custom Themes in VS Code

1. Copy the theme CSS file to your workspace (e.g., `gcloud-theme.css`).
2. Open VS Code workspace settings (F1 → "Preferences: Open Workspace Settings").
3. Search for "Marp: Themes".
4. Add the relative path to the CSS file (e.g., `./gcloud-theme.css`).
5. Use `theme: gcloud` in the Markdown frontmatter.

### Using Custom Themes with Marp CLI

Pass the `--theme` flag:

```bash
marp deck.md --html --theme ./gcloud-theme.css
marp deck.md --pdf --theme ./gcloud-theme.css
```

### Slide Type Classes (gcloud theme)

The `gcloud` theme provides per-slide classes for visual variety without background images:

```markdown
<!-- _class: title -->     <!-- Title slide with gradient bar -->
<!-- _class: section -->   <!-- Blue background section divider -->
<!-- _class: lead -->      <!-- Centered content -->
<!-- _class: stats -->     <!-- Numbers with blue accent -->
<!-- _class: speaker -->   <!-- Speaker bio layout -->
<!-- _class: quote -->     <!-- Large quotation -->
<!-- _class: invert -->    <!-- Dark background -->
<!-- _class: closing -->   <!-- Closing slide with gradient bar -->
```

Use `<!-- _class: ... -->` to set the class for a single slide (note the underscore prefix for per-slide directives).

## MARP CLI Installation

```bash
npm install -g @marp-team/marp-cli
```

Or use npx without installing:

```bash
npx @marp-team/marp-cli deck.md --html
```
