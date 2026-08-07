---
name: html-to-pptx
description: Convert MARP HTML slide presentations into fully editable PowerPoint (.pptx) files with native text boxes, lists, tables, and images — not screenshots. Use when the user asks to convert HTML slides, MARP output, or web-based presentations into PowerPoint.
---

# HTML to PPTX Conversion Skill

You convert MARP-rendered HTML slide presentations into fully editable PowerPoint (`.pptx`) files. The output contains native PowerPoint text boxes, lists, tables, and embedded images — every element is editable, not a flat screenshot.

You use a two-step pipeline:
1. **Extract** — Open the HTML in a browser via `agent-browser`, inject a DOM extraction script that reads every element's position, size, style, and content, and outputs structured JSON.
2. **Build** — Feed the JSON into a Node.js script that maps pixel coordinates to PowerPoint inches and produces a `.pptx` file using PptxGenJS.

## Activation

This skill activates when the user asks to:
- Convert HTML slides to PowerPoint
- Turn MARP HTML output into an editable `.pptx`
- Generate a PowerPoint from HTML files
- Export a web-based presentation to `.pptx`

Keywords: "convert to pptx", "html to powerpoint", "make it editable", "export to pptx", "powerpoint from html"

## Required Workflow

Follow these steps strictly in order.

### Step 1: Identify the HTML Files

Ask the user which HTML file(s) to convert. Accept:
- A single HTML file path
- A directory containing multiple `.html` files (one per slide, or a single MARP deck)
- A glob pattern (e.g., `slides/*.html`)

If the user just generated an HTML presentation with `zen-presenter` or `clarity-presenter`, offer to convert the file they just created.

### Step 2: Prepare the Environment

Check if `node_modules` exists in this skill's directory. If not, install dependencies:

```bash
cd <skill-directory>/scripts && npm install --prefix . --production
```

If `npm` is not available, tell the user to install Node.js first.

### Step 3: Extract Slide Data with agent-browser

For each HTML file to convert:

1. **Open the file** in the headless browser:
   ```
   agent-browser open file://<absolute_path_to_html_file>
   ```

2. **Wait for rendering** — MARP slides may have CSS transitions or font loading. Wait 2 seconds after page load.

3. **Inject the extraction script** to read all slide elements, positions, styles, and content:
   ```
   agent-browser eval "$(cat <skill-directory>/scripts/extract.js)"
   ```

4. **Save the JSON output** to a temporary file:
   ```bash
   echo '<json_output>' > /tmp/slides_data.json
   ```

5. **Handle complex elements** — If the extracted JSON contains elements with `"isComplex": true` (SVG charts, diagrams), use `agent-browser` to take a screenshot of that specific element:
   ```
   agent-browser screenshot --selector "#<element-id>" --output /tmp/complex_element.png
   ```
   Then reference the screenshot path in the JSON before building.

### Step 4: Build the PowerPoint

Run the build script with the extracted JSON:

```bash
node <skill-directory>/scripts/build_pptx.js /tmp/slides_data.json <output_filename>.pptx
```

The build script:
- Maps pixel coordinates to PowerPoint inches (10" × 5.625" for 16:9)
- Converts CSS colors to PowerPoint hex (supports hex, rgb, rgba, hsl, hsla, and named colors)
- Creates native text boxes with proper font, size, color, and alignment
- Builds bullet lists with colored bullets (Google identity blue)
- Embeds images as base64 data (downloads remote URLs)
- Adds Google gradient bars on title/closing slides
- Renders code blocks with dark backgrounds and monospace fonts
- Creates tables with proper cell styling and borders
- Handles blockquotes with left accent bars

### Step 5: Verify and Deliver

1. Confirm the `.pptx` file was created and report its location and size.
2. Tell the user:
   - The file can be opened in **PowerPoint**, **Google Slides**, or **Keynote**
   - All text is **fully editable** — not screenshots
   - Images are **embedded** in the file — no external dependencies
   - Fonts default to **Arial** for maximum compatibility across platforms

### Error Handling

| Error | Recovery |
|-------|----------|
| `agent-browser` not available | Tell the user to enable the browser tool or install Playwright |
| No slides found in HTML | Check if the HTML is valid MARP output; suggest re-rendering with `marp-cli` |
| Image download fails | Skip the image, add a text placeholder `[Image: alt text]`, warn the user. Downloads are limited to 10MB and 5 redirects |
| `node` or `npm` not available | Tell the user to install Node.js (v18+) |
| Complex SVG elements | Use screenshot fallback, warn that the SVG won't be editable |

## What Gets Extracted

| HTML Element | PowerPoint Element | Editable? |
|-------------|-------------------|-----------|
| `<h1>`-`<h6>` | Text box with heading font size | Yes |
| `<p>` | Text box | Yes |
| `<strong>` | Bold text with accent color | Yes |
| `<em>` | Italic text | Yes |
| `<ul>`, `<ol>` | Bulleted/numbered list (nested up to 3 levels) | Yes |
| `<blockquote>` | Text box with left accent bar | Yes |
| `<pre><code>` | Code block with dark background | Yes |
| `<img>` | Embedded image | Resizable |
| `<table>` | Native PowerPoint table (with colspan/rowspan) | Yes |
| `<svg>` | Screenshot fallback | No (raster) |
| Slide background color | Slide background fill | Yes |
| Background image | Slide background image | Replaceable |
| Google gradient bar | Four colored rectangles | Yes |

## Supported Input Formats

| Format | How It's Handled |
|--------|-----------------|
| **MARP single-file HTML** | Extracts all `<section>` slides from one file |
| **MARP per-slide HTML** | Processes each file as one slide, ordered by filename |
| **Generic HTML slides** | Extracts `<section>` elements as slides |

## Google Identity Mapping

The build script preserves Google identity styling from the `gcloud` MARP theme:

| MARP Theme Element | PowerPoint Equivalent |
|-------------------|----------------------|
| Google blue (`#4285F4`) | Accent color for bold text, bullets, section backgrounds |
| Google gradient bar | Four colored rectangles (blue, red, yellow, green) at slide bottom |
| `section` class (blue bg) | Slide background fill `#4285F4`, white text |
| `invert` class (dark bg) | Slide background fill `#202124`, light text with blue accents |
| `title` / `closing` class | Gradient bar + centered layout |
| `stats` class | Blue accent on heading numbers |
| `quote` class | Large text, no border, attribution styling |
| Inter / Google Sans font | Mapped to Arial for cross-platform compatibility |

## Guidelines

- **Never take screenshots of entire slides.** The whole point is editable PowerPoint elements. Only use screenshots as a fallback for SVGs and complex diagrams.
- **Preserve positioning.** Map pixel coordinates to inches proportionally. Don't stack everything vertically.
- **Preserve styling.** Font sizes, colors, bold/italic, and alignment should match the HTML rendering as closely as possible.
- **Embed all assets.** Images must be embedded as base64, not linked. The `.pptx` must work offline.
- **Handle errors gracefully.** If an image can't be downloaded or an element can't be parsed, skip it with a placeholder and warn the user — don't crash.
- **Keep fonts safe.** Always use Arial as the primary font. PowerPoint on different platforms may not have Inter or Google Sans installed.
