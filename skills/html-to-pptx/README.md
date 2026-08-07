# HTML to PPTX

A Agy skill that converts MARP HTML slide presentations into fully editable PowerPoint (`.pptx`) files. Every text element, list, table, and image becomes a native PowerPoint object — not a screenshot.

## What It Does

This skill uses a two-step pipeline to produce editable PowerPoint files from HTML slides:

1. **Extract** — Opens the HTML in a headless browser via `agent-browser`, injects a DOM extraction script that reads every element's position, size, computed style, and content. Outputs structured JSON.
2. **Build** — Feeds the JSON into a Node.js script that maps pixel coordinates to PowerPoint inches and produces a `.pptx` file using PptxGenJS with native text boxes, lists, tables, and embedded images.

## When Does It Activate?

The skill activates when you ask Agy to convert HTML slides to PowerPoint:

| Trigger | Example |
|---------|---------|
| Convert HTML to PPTX | "Convert my MARP HTML to an editable PowerPoint" |
| Export to PowerPoint | "Turn these HTML slides into a .pptx" |
| Make it editable | "I need an editable PowerPoint from this HTML deck" |
| After zen-presenter | "Now convert that presentation to an editable PPTX" |

## What's Editable?

| HTML Element | PowerPoint Element | Editable? |
|-------------|-------------------|-----------|
| `<h1>`-`<h6>` | Text box with heading font size | Yes |
| `<p>` | Text box | Yes |
| `<strong>` / `<em>` | Bold / italic text | Yes |
| `<ul>`, `<ol>` | Bulleted / numbered list (nested up to 3 levels) | Yes |
| `<blockquote>` | Text box with accent bar | Yes |
| `<pre><code>` | Code block (dark bg, monospace) | Yes |
| `<img>` | Embedded image | Resizable |
| `<table>` | Native PowerPoint table (colspan/rowspan) | Yes |
| `<svg>` | Screenshot fallback | No |
| Slide backgrounds | Slide background fill / image | Yes |
| Google gradient bar | Colored rectangles | Yes |

## How It Works with Presenter Skills

This skill is designed to work after `zen-presenter` or `clarity-presenter`:

```
1. User: "Create a Zen presentation about cloud architecture"
   → zen-presenter generates MARP Markdown + HTML

2. User: "Now convert that to an editable PowerPoint"
   → html-to-pptx extracts the HTML and builds a .pptx
```

The Google identity styling (colors, gradient bars, slide type classes) is preserved in the PowerPoint output.

## Prerequisites

- **Node.js** v18+ (for running the build script)
- **agent-browser** (Agy browser tool for DOM extraction)

## Installation

### Option A: Agy native

```bash
agy skills install https://github.com/duboc/agy-skills.git --path skills/html-to-pptx
```

### Option B: One-liner

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- html-to-pptx
```

For user-scope installation:

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- html-to-pptx --scope user
```

### Option C: Manual

```bash
cp -r skills/html-to-pptx ~/.gemini/config/skills/html-to-pptx
cd ~/.gemini/config/skills/html-to-pptx && npm install
```

## Usage Examples

### Convert a MARP HTML file

```
Convert my-presentation.html to an editable PowerPoint file.
```

### Convert after generating a presentation

```
I just created a Zen presentation. Now turn the HTML into an editable PPTX.
```

### Convert multiple HTML files

```
Convert all the .html files in the slides/ directory to a single PowerPoint.
```

## Included Scripts

| File | Description |
|------|-------------|
| **extract.js** | Browser-side DOM extraction script — reads MARP slide structure, element positions, computed styles, text content, images, nested lists, and table spans |
| **build_pptx.js** | Node.js script that converts extracted JSON to PowerPoint using PptxGenJS — maps coordinates, supports HSL/named colors, nested lists, colspan/rowspan tables, multiple inline styles, and hardened image downloads |
| **package.json** | Dependencies (PptxGenJS) |
