---
name: visual-explainer
description: "Generate beautiful, self-contained HTML pages that visually explain systems, code changes, plans, and data. Use when the user asks for a diagram, architecture overview, diff review, plan review, project recap, comparison table, or any visual explanation of technical concepts. Also use proactively when you are about to render a complex ASCII table (4+ rows or 3+ columns) — present it as a styled HTML page instead."
---

# Visual Explainer
Generate self-contained HTML files for technical diagrams, visualizations, and data tables. Always open the result in the browser. Never fall back to ASCII art when this skill is loaded.

Proactive table rendering. When you're about to present tabular data as an ASCII box-drawing table in the terminal (comparisons, audits, feature matrices, status reports, any structured rows/columns), generate an HTML page instead. The threshold: if the table has 4+ rows or 3+ columns, it belongs in the browser. Don't wait for the user to ask — render it as HTML automatically and tell them the file path. You can still include a brief text summary in the chat, but the table itself should be the HTML page.

## Available Commands
Detailed prompt templates in ./commands/. In Pi, these are slash commands (/diff-review). In Claude Code, namespaced (/visual-explainer:diff-review). In Codex, use /prompts:diff-review (if installed to ~/.codex/prompts/) or invoke $visual-explainer and describe the workflow.

| Command | What it does |
|---------|-------------|
| generate-web-diagram | Generate an HTML diagram for any topic |
| generate-visual-plan | Generate a visual implementation plan for a feature |
| generate-slides | Generate a magazine-quality slide deck |
| diff-review | Visual diff review with architecture comparison and code review |
| plan-review | Compare a plan against the codebase with risk assessment |
| project-recap | Mental model snapshot for context-switching back to a project |
| fact-check | Verify accuracy of a document against actual code |
| share | Deploy an HTML page to Vercel and get a live URL |

## Workflow

### 1. Think (5 seconds, not 5 minutes)
Before writing HTML, commit to a direction. Don't default to "dark theme with blue accents" every time.

**Visual is always default.** Even essays, blog posts, and articles get visual treatment — extract structure into cards, diagrams, grids, tables.

Prose patterns (lead paragraphs, pull quotes, callout boxes) are accent elements within visual pages, not a separate mode. Use them to highlight key points or provide breathing room, but the page structure remains visual.

For prose accents, see "Prose Page Elements" in ./references/css-patterns.md. For everything else, use the standard freeform approach with aesthetic directions below.

**Who is looking?** A developer understanding a system? A PM seeing the big picture? A team reviewing a proposal? This shapes information density and visual complexity.

**What type of content?** Architecture, flowchart, sequence, data flow, schema/ER, state machine, mind map, class diagram, C4 architecture, data table, timeline, dashboard, or prose-first page. Each has distinct layout needs and rendering approaches (see Diagram Types below).

**What aesthetic?** Pick one and commit. The constrained aesthetics (Blueprint, Editorial, Paper/ink) are safer — they have specific requirements that prevent generic output. The flexible ones (IDE-inspired) require more discipline.

**Constrained aesthetics (prefer these):**
- Blueprint (technical drawing feel, subtle grid background, deep slate/blue palette, monospace labels, precise borders) — see websocket-implementation-plan.html for reference
- Editorial (serif headlines like Instrument Serif or Crimson Pro, generous whitespace, muted earth tones or deep navy + gold)
- Paper/ink (warm cream #faf7f5 background, terracotta/sage accents, informal feel)
- Monochrome terminal (green/amber on near-black, monospace everything, CRT glow optional)
- Google Cloud (white background, Google Sans font, Google brand four-color accents blue/red/yellow/green, clean corporate feel) — use for GCP architecture, migration plans, cloud-themed content. See preset-gcloud in ./references/slide-patterns.md

**Flexible aesthetics (use with caution):**
- IDE-inspired (borrow a real, named color scheme: Dracula, Nord, Catppuccin Mocha/Latte, Solarized Dark/Light, Gruvbox, One Dark, Rosé Pine) — commit to the actual palette, don't approximate

**Data-dense** (small type, tight spacing, maximum information, muted colors)

**Explicitly forbidden:**
- Neon dashboard (cyan + magenta + purple on dark) — always produces AI slop
- Gradient mesh (pink/purple/cyan blobs) — too generic
- Any combination of Inter font + violet/indigo accents + gradient text

Vary the choice each time. If the last diagram was dark and technical, make the next one light and editorial. The swap test: if you replaced your styling with a generic dark theme and nobody would notice the difference, you haven't designed anything.

### 2. Structure
Read the reference material before generating. Don't memorize it — read it each time to absorb the patterns.

- For text-heavy architecture overviews (card content matters more than topology): read ./templates/architecture.html
- For flowcharts, sequence diagrams, ER, state machines, mind maps, class diagrams, C4: read ./templates/mermaid-flowchart.html
- For data tables, comparisons, audits, feature matrices: read ./templates/data-table.html
- For slide deck presentations (when --slides flag is present or /generate-slides is invoked): read ./templates/slide-deck.html and ./references/slide-patterns.md
- For prose-heavy publishable pages (READMEs, articles, blog posts, essays): read the "Prose Page Elements" section in ./references/css-patterns.md and "Typography by Content Voice" in ./references/libraries.md
- For CSS/layout patterns and SVG connectors, read ./references/css-patterns.md.
- For pages with 4+ sections (reviews, recaps, dashboards), also read ./references/responsive-nav.md for section navigation with sticky sidebar TOC on desktop and horizontal scrollable bar on mobile.

**Choosing a rendering approach:**

| Content type | Approach | Why |
|-------------|----------|-----|
| Architecture (text-heavy) | CSS Grid cards + flow arrows | Rich card content (descriptions, code, tool lists) needs CSS control |
| Architecture (topology-focused) | Mermaid | Visible connections between components need automatic edge routing |
| Flowchart / pipeline | Mermaid | Automatic node positioning and edge routing |
| Sequence diagram | Mermaid | Lifelines, messages, and activation boxes need automatic layout |
| Data flow | Mermaid with edge labels | Connections and data descriptions need automatic edge routing |
| ER / schema diagram | Mermaid | Relationship lines between many entities need auto-routing |
| State machine | Mermaid | State transitions with labeled edges need automatic layout |
| Mind map | Mermaid | Hierarchical branching needs automatic positioning |
| Class diagram | Mermaid | Inheritance, composition, aggregation lines with automatic routing |
| C4 architecture | Mermaid | Use graph TD + subgraph for C4 (not native C4Context — it ignores themes) |
| Data table | HTML `<table>` | Semantic markup, accessibility, copy-paste behavior |
| Timeline | CSS (central line + cards) | Simple linear layout doesn't need a layout engine |
| Dashboard | CSS Grid + Chart.js | Card grid with embedded charts |

**Mermaid theming:** Always use theme: 'base' with custom themeVariables so colors match your page palette. Use layout: 'elk' for complex graphs. Override Mermaid's SVG classes with CSS for pixel-perfect control. See ./references/libraries.md for full theming guide.

**Mermaid containers:** Always center Mermaid diagrams with display: flex; justify-content: center;. Add zoom controls (+/−/reset/expand) to every .mermaid-wrap container. Include the click-to-expand JavaScript so clicking the diagram (or the ⛶ button) opens it full-size in a new tab.

⚠️ Never use bare `<pre class="mermaid">`. Always use the full diagram-shell pattern from templates/mermaid-flowchart.html.

**Mermaid scaling:** Diagrams with 10+ nodes render too small by default. For 10-12 nodes, increase fontSize in themeVariables to 18-20px and set INITIAL_ZOOM to 1.5-1.6. For 15+ elements, use the hybrid pattern (simple Mermaid overview + CSS Grid cards).

**Mermaid layout direction:** Prefer flowchart TD (top-down) over flowchart LR (left-to-right) for complex diagrams.

**Mermaid line breaks:** Use `<br/>` inside quoted labels. Never use escaped newlines like `\n`.

**Mermaid CSS class collision constraint:** Never define `.node` as a page-level CSS class. Use `.ve-card` instead.

### 3. Style

**Typography is the diagram.** Pick a distinctive font pairing from the list in ./references/libraries.md.

**Forbidden as --font-body:** Inter, Roboto, Arial, Helvetica, system-ui alone.

**Good pairings:**
- DM Sans + Fira Code (technical, precise)
- Instrument Serif + JetBrains Mono (editorial, refined)
- IBM Plex Sans + IBM Plex Mono (reliable, readable)
- Bricolage Grotesque + Fragment Mono (bold, characterful)
- Plus Jakarta Sans + Azeret Mono (rounded, approachable)

**Color tells a story.** Use CSS custom properties. Define at minimum: --bg, --surface, --border, --text, --text-dim, and 3-5 accent colors.

**Forbidden accent colors:** #8b5cf6 #7c3aed #a78bfa (indigo/violet), #d946ef (fuchsia), cyan-magenta-pink combination.

**Good accent palettes:**
- Terracotta + sage (#c2410c, #65a30d)
- Teal + slate (#0891b2, #0369a1)
- Rose + cranberry (#be123c, #881337)
- Amber + emerald (#d97706, #059669)
- Deep blue + gold (#1e3a5f, #d4a73a)

**Surfaces whisper, they don't shout.** Build depth through subtle lightness shifts (2-4% between levels).

**Backgrounds create atmosphere.** Don't use flat solid colors. Use subtle gradients, faint grid patterns, or gentle radial glows.

**Visual weight signals importance.** Use `<details>/<summary>` for sections that are useful but not primary.

**Surface depth creates hierarchy.** Vary card depth using ve-card--hero, ve-card, ve-card--recessed patterns.

**Animation earns its place.** Staggered fade-ins on page load. Mix fadeUp for cards, fadeScale for KPIs, drawIn for SVG connectors, countUp for hero numbers. Always respect prefers-reduced-motion.

**Forbidden animations:** Animated glowing box-shadows, pulsing/breathing effects, continuous animations after page load.

### 4. Deliver
Output location: Write to `./diagrams/`. Use descriptive filenames.

Open in browser:
- macOS: `open ./diagrams/filename.html`
- Linux: `xdg-open ./diagrams/filename.html`

## Diagram Types

### Architecture / System Diagrams
Three approaches depending on complexity:
- **Simple topology (under 10 elements):** Use Mermaid
- **Text-heavy overviews (under 15 elements):** CSS Grid with explicit row/column placement
- **Complex architectures (15+ elements):** Hybrid pattern — simple Mermaid overview + detailed CSS Grid cards

### Flowcharts / Pipelines
Use Mermaid. Prefer graph TD; use graph LR only for simple 3-4 node linear flows.

### Sequence Diagrams
Use Mermaid sequenceDiagram syntax.

### Data Flow Diagrams
Use Mermaid with edge labels for data descriptions.

### Schema / ER Diagrams
Use Mermaid erDiagram syntax.

### State Machines / Decision Trees
Use Mermaid stateDiagram-v2 for simple labels. Use flowchart TD for labels with special characters.

### Mind Maps / Hierarchical Breakdowns
Use Mermaid mindmap syntax.

### Class Diagrams
Use Mermaid classDiagram syntax. For simple entity boxes without OOP semantics, prefer erDiagram.

### C4 Architecture Diagrams
Use Mermaid flowchart syntax — NOT native C4. Use graph TD with subgraph blocks.

### Data Tables / Comparisons / Audits
Use real `<table>` elements. Use proactively for any 4+ rows or 3+ columns data.

Layout patterns: sticky thead, alternating rows, responsive wrapper, row hover highlight.

Status indicators: colored dots/badges (never emoji). Match=green, Gap=red, Partial=amber, Neutral=muted.

### Timeline / Roadmap Views
Vertical or horizontal timeline with central line. Content cards branching alternately.

### Dashboard / Metrics Overview
Card grid layout. Hero numbers large. Sparklines via inline SVG. Chart.js for real charts.

### Implementation Plans
Don't dump full files. Show file structure with descriptions, key snippets only, collapsible sections.

### Documentation
Transform content into visual elements: features→card grid, steps→numbered flow, APIs→table, architecture→diagram.

### Prose Accent Elements
Use sparingly: lead paragraph, pull quote, callout box, section divider.

### Slide Deck Mode
Opt-in only via /generate-slides or --slides flag. Read ./references/slide-patterns.md and ./templates/slide-deck.html before generating. Each slide is 100dvh, no scrolling. 10 slide types: Title, Section Divider, Content, Split, Diagram, Dashboard, Table, Code, Quote, Full-Bleed.

## File Structure
Every diagram is a single self-contained .html file:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Descriptive Title</title>
  <link href="https://fonts.googleapis.com/css2?family=...&display=swap" rel="stylesheet">
  <style>
    /* CSS custom properties, theme, layout, components — all inline */
  </style>
</head>
<body>
  <!-- Semantic HTML: sections, headings, lists, tables, inline SVG -->
  <script>/* Optional: Mermaid, Chart.js, or anime.js when used */</script>
</body>
</html>
```
