# Visual Explainer

Generate beautiful, self-contained HTML pages that visually explain systems, code changes, plans, and data.

## When Does It Activate?

The skill activates when you ask for visual explanations or when complex tabular data would benefit from browser rendering.

| Trigger | Example |
|---------|---------|
| Diagram | "Draw a diagram of the authentication flow" |
| Architecture overview | "Show me the system architecture" |
| Diff review | "Review this diff visually" |
| Plan review | "Compare this plan against the codebase" |
| Project recap | "Give me a project recap for context-switching" |
| Comparison table | "Compare these three frameworks" |
| Visual explanation | "Visually explain how the event pipeline works" |
| Complex table rendering | Automatically triggered when rendering 4+ rows or 3+ columns |

## Topics Covered

| Area | Details |
|------|---------|
| **HTML generation** | Self-contained HTML files with inline CSS, responsive layouts, and zero-dependency scripts |
| **Interactive diagrams** | Pan & Zoom canvas, node inspector slide-out drawer, step-by-step scrubber, 1-click SVG/PNG export |
| **Dynamic data tables** | Live search filtering, multi-column click-to-sort, status filter pills, expandable row details, and CSV/Markdown export |
| **Visual diff review** | Side-by-side vs unified diff viewer, KPI metrics, file risk indicators, syntax highlighting |
| **Architecture visualization** | Tier filters, card connection highlighters, Prism code snippets with copy buttons, dark/light theme toggles |
| **Slide decks** | Magazine-quality presentations with 10 slide types |
| **CSS styling** | Curated aesthetics (Blueprint, Editorial, Paper/ink, Slate, Terminal, Google Cloud) |

## Commands

| Command | What it does |
|---------|-------------|
| `generate-web-diagram` | Generate an HTML diagram with Pan/Zoom, Node Inspector, and PNG/SVG export |
| `generate-visual-plan` | Generate a visual implementation plan with step scrubber and syntax-highlighted code |
| `generate-slides` | Generate a magazine-quality slide deck |
| `diff-review` | Visual diff review with side-by-side comparisons, impact map, and risk KPIs |
| `plan-review` | Compare a plan against the codebase with risk assessment |
| `project-recap` | Mental model snapshot for context-switching back to a project |
| `fact-check` | Verify accuracy of a document against actual code |
| `share` | Deploy an HTML page to Vercel and get a live URL |

## Installation

### Method 1: One-liner with curl (Recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- visual-explainer
```

For user-scope installation (available globally across all projects):

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- visual-explainer --scope user
```

### Method 2: Manual Copy

```bash
# Workspace scope
cp -r skills/visual-explainer .agents/skills/visual-explainer

# User scope
cp -r skills/visual-explainer ~/.gemini/config/skills/visual-explainer
```

## References

| File | Description |
|------|-------------|
| **references/css-patterns.md** | CSS layout patterns, SVG connectors, inspector drawers, and prose elements |
| **references/libraries.md** | Font pairings, Pan-Zoom engine, SVG/PNG export utilities, Prism.js CDN, and Mermaid theming |
| **references/responsive-nav.md** | Section navigation with sticky sidebar TOC and mobile horizontal bar |
| **references/slide-patterns.md** | Slide deck patterns and slide type definitions |

## Templates

| File | Description |
|------|-------------|
| **templates/mermaid-flowchart.html** | Interactive diagram shell with Pan/Zoom, Node Inspector, Step Scrubber, Theme Switcher, and SVG/PNG Export |
| **templates/data-table.html** | Dynamic data table with live search, multi-column sort, status pills, and CSV/Markdown export |
| **templates/architecture.html** | Architecture overview with layer filters, hover dependency highlighters, Prism syntax, and copy buttons |
| **templates/diff-review.html** | Pull request and diff review with side-by-side split view, KPI cards, and risk metrics |
| **templates/slide-deck.html** | Slide deck template with 100dvh slides and 10 slide types |
