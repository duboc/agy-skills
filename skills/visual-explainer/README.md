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
| **HTML generation** | Self-contained HTML files with inline CSS and JavaScript |
| **Mermaid diagrams** | Flowcharts, sequence diagrams, ER diagrams, state machines, mind maps, class diagrams, C4 |
| **Data tables** | Styled tables with sticky headers, alternating rows, status indicators |
| **Slide decks** | Magazine-quality presentations with 10 slide types |
| **Architecture visualization** | CSS Grid cards, Mermaid topology, hybrid patterns for complex systems |
| **CSS styling** | Curated aesthetics (Blueprint, Editorial, Paper/ink, Terminal), forbidden anti-patterns |
| **Responsive design** | Sticky sidebar TOC on desktop, horizontal scrollable bar on mobile |

## Commands

| Command | What it does |
|---------|-------------|
| `generate-web-diagram` | Generate an HTML diagram for any topic |
| `generate-visual-plan` | Generate a visual implementation plan for a feature |
| `generate-slides` | Generate a magazine-quality slide deck |
| `diff-review` | Visual diff review with architecture comparison and code review |
| `plan-review` | Compare a plan against the codebase with risk assessment |
| `project-recap` | Mental model snapshot for context-switching back to a project |
| `fact-check` | Verify accuracy of a document against actual code |
| `share` | Deploy an HTML page to Vercel and get a live URL |

## Installation

### Option B: One-liner

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- visual-explainer
```

For user-scope installation (available across all projects):

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- visual-explainer --scope user
```

### Option C: Manual

```bash
cp -r skills/visual-explainer ~/.gemini/config/skills/visual-explainer
```

## References

| File | Description |
|------|-------------|
| **references/css-patterns.md** | CSS layout patterns, SVG connectors, and prose page elements |
| **references/libraries.md** | Font pairings, Mermaid theming guide, and typography by content voice |
| **references/responsive-nav.md** | Section navigation with sticky sidebar TOC and mobile horizontal bar |
| **references/slide-patterns.md** | Slide deck patterns and slide type definitions |

## Templates

| File | Description |
|------|-------------|
| **templates/architecture.html** | Text-heavy architecture overview with CSS Grid cards |
| **templates/mermaid-flowchart.html** | Mermaid diagram shell with zoom controls and click-to-expand |
| **templates/data-table.html** | Styled data table with sticky headers and status indicators |
| **templates/slide-deck.html** | Slide deck template with 100dvh slides and 10 slide types |
