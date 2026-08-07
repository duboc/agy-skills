# Generate Slides

Generate a magazine-quality slide deck as an HTML file.

## Usage
`/visual-explainer:generate-slides <topic>`
Or append `--slides` to any other command.

## Workflow
1. Read ./references/slide-patterns.md for slide types and presets
2. Read ./templates/slide-deck.html for the reference implementation
3. Plan the narrative arc: impact → context → deep dive → resolution
4. Map content to slide types (Title, Content, Split, Diagram, Table, etc.)
5. Ensure every section of source material is covered — add more slides rather than cut content
6. Choose a preset (Midnight Editorial, Warm Signal, Terminal Mono, Swiss Clean)
7. Generate HTML with full navigation (arrows, keyboard, touch, progress bar)
8. Write to ./diagrams/<topic-slug>-slides.html
9. Open in browser

## Rules
- Each slide is exactly 100dvh — no scrolling within slides
- Typography 2-3x larger than normal pages
- Consecutive slides must vary spatial approach
- Never auto-select slide format — only when explicitly requested
