# Research Skill Graph (`research-skill-graph-agy`)

Turn a research question into a structured, multi-angle analysis stored as interconnected Markdown notes inside a `.research/` directory in your project root.

---

## Overview

The `research-skill-graph-agy` skill evaluates technical, market, and strategic questions through six independent analytical lenses (`technical`, `economic`, `historical`, `geopolitical`, `contrarian`, and `first-principles`). Rather than forcing premature consensus, the workflow preserves disagreements between lenses and identifies the boundary conditions under which each perspective holds true.

---

## Key Capabilities

- **6-Lens Sequential Evaluation**: Analyzes every research topic across Technical, Economic, Historical, Geopolitical, Contrarian, and First-Principles dimensions.
- **Explicit Contradiction Protocol**: Documents competing claims side by side and isolates the quantitative thresholds or assumptions that separate them.
- **Compounding Local Knowledge Graph**: Maintains a persistent `.research/` directory with relative Markdown links, shared concept indices (`knowledge/concepts.md`), and validated quantitative metrics (`knowledge/data-points.md`).
- **Source Tiering**: Evaluates primary and secondary evidence using explicit source-quality criteria (`methodology/source-evaluation.md`).

---

## Directory Architecture

```text
<project-root>/.research/
├── index.md                         # Global research index and navigation hub
├── research-log.md                  # Chronological log of active and completed studies
├── methodology/                     # Frameworks, source tiering, and synthesis protocols
├── lenses/                          # Prompts and evaluation criteria for the 6 lenses
├── projects/<topic>/                # Topic-specific lens outputs and synthesis report
├── sources/                         # Annotated bibliography and primary source notes
└── knowledge/                       # Cross-project concepts and quantitative data points
```

---

## Quickstart Prompts

- *"Research the latency, cost, and reliability trade-offs between Gemini Live WebSockets and WebRTC edge relays."*
- *"Run a 6-lens deep dive on multi-tenant Firestore architectures for high-throughput live events."*

---

## Installation

### Workspace scope

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- research-skill-graph-agy
```

### User scope (global)

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- research-skill-graph-agy --scope user
```
