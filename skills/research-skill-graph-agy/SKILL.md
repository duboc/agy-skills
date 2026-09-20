---
name: research-skill-graph-agy
description: Use whenever the user wants to research a topic, investigate a question, do a deep-dive, validate a claim, explore a trend, or produce decision-grade analysis on the local filesystem.
---

# Research Skill Graph (Local Filesystem Edition)

## Overview

The **Research Skill Graph** turns a single research question into a structured, multi-angle analysis written as interconnected local markdown notes inside a hidden `.research/` directory in the project root. Each research project runs through 6 structured lenses that deliberately disagree with each other — the tension between them is the source of insight.

## Core Principle

Each lens must rethink the question from its own angle, not just add more facts. The technical lens and the contrarian lens should read like two researchers who fundamentally disagree. 

**Never resolve contradictions by picking a winner** — document both viewpoints and identify the exact parameters/conditions under which each is right.

---

## Workflow Comparison

| System Element | Obsidian Implementation | Hidden `.research/` Directory Implementation |
| :--- | :--- | :--- |
| **Root Directory** | `<vault>/` | `<project-root>/.research/` |
| **System Discovery** | Checking for `.obsidian/` folder | Scanning for `.research/` folder |
| **Interlinking** | Wikilinks (`[[Note Name]]`) | Standard relative Markdown links (`[Anchor Text](../relative/path.md)`) |
| **Environment** | Obsidian Desktop/Mobile App | Standard local IDEs, CLI tools, and basic markdown renderers |

---

## Workflow Step-by-Step

### Step 1 — Locate and Understand the Workspace

Before doing anything else, inspect the active project workspace directory:
1. **Target Workspace Enforcement**: Always create and write `.research/` directly in the root of the active workspace directory where the user initiated the research conversation. If the user explicitly provided a specific folder path, use that; otherwise, always default to the current working directory (`CWD`). NEVER write `.research/` files to temporary directories, user home directory, or outside the active project.
2. **Structural Scan**: List top-level folders in the active workspace and search for an existing `.research/` directory.
3. **Inspect System Files**: Check for `index.md`, `research-log.md`, `projects/`, and `knowledge/` inside `.research/`.
4. **Report Findings**: Inform the user before scaffolding:
   > "I see you have an existing research graph in this workspace with projects X and Y. I will integrate the new research into your existing `.research/projects/` folder."
   Allow the user to confirm routing before writing files.
5. **Adapt, Don't Overwrite**: If custom templates or files exist in `.research/`, read them first and merge into established conventions. Never overwrite or delete existing notes.

---

### Step 2 — Scaffold Missing Pieces

If `.research/` or any core files are missing, initialize them using the templates provided in this skill's `templates/` folder:

```text
<project-root>/.research/
├── index.md               # Global command center and entry point
├── research-log.md        # Running log of all completed/active projects
├── methodology/           # Research frameworks & protocols
│   ├── research-frameworks.md
│   ├── source-evaluation.md
│   ├── synthesis-rules.md
│   └── contradiction-protocol.md
├── lenses/                # Reference templates for the 6 lenses
│   ├── technical.md
│   ├── economic.md
│   ├── historical.md
│   ├── geopolitical.md
│   ├── contrarian.md
│   └── first-principles.md
├── projects/              # Active and historical research topics (one subfolder per topic)
├── sources/               # Source templates and processed bibliography files
└── knowledge/             # Knowledge-compounding index files
    ├── concepts.md        # Shared definitions and conceptual framework mappings
    └── data-points.md     # Quantitative database of validated hard numbers
```

---

### Step 3 — Set up the Project

For each new research question:
1. **Create Project Subfolder**: `.research/projects/<kebab-case-topic>/`
2. **Initialize Project `index.md`**: Populate metadata including:
   - Research Question
   - Scope & Boundary Conditions
   - Time Horizon
   - Output Goal
3. **Cross-Link Prior Context**: Scan `.research/research-log.md` and `.research/knowledge/concepts.md` for prior research. Link related projects in `index.md` using relative markdown links (e.g., `[Prior Topic](../../projects/prior-topic/index.md)`).
4. **Select Framework & Depth**: Choose a research framework from `.research/methodology/research-frameworks.md`:
   - **Type**: Verification / Causal / Scenario / Decision
   - **Depth**: Quick Scan / Standard / Deep Dive
5. **Notify User**: State the selected framework and depth, and allow the user to override if desired.

---

### Step 4 — Run the 6 Lenses (Strict Sequential Execution)

Execute all 6 lenses **one at a time in exact order** (`technical` → `economic` → `historical` → `geopolitical` → `contrarian` → `first-principles`). 

For each lens:
1. Read `.research/lenses/<lens>.md` to internalize its core questions and voice.
2. Conduct targeted web searches and fetch Tier 1 & Tier 2 primary/secondary sources per `.research/methodology/source-evaluation.md`.
3. Write findings directly to `.research/projects/<topic>/lens-<name>.md` containing:
   - Claims & Arguments
   - Supporting Evidence & Source Tiering
   - Confidence Calibration (`CLAIM` / `EVIDENCE` / `CONFIDENCE` / `DEFEASIBILITY TRIGGER`)
   - Explicit Contradictions with Prior Lenses
4. **Append Quantitative Data**: Add verified numerical data and statistics to `.research/knowledge/data-points.md` with complete attribution.
5. **Append Concepts**: Add new domain terms and conceptual models to `.research/knowledge/concepts.md`.
6. **Log Primary Sources**: Create detailed source notes in `.research/sources/<source-id>.md`.
7. **Adopt Distinct Voice**:
   - **Technical**: Clinical, dry, highly numerical, mechanistic.
   - **Economic**: Incentives, unit economics, market forces, capital allocation.
   - **Historical**: Precedents, cycles, long arcs, path dependency.
   - **Geopolitical**: State power, regulatory regimes, trade flows, national security.
   - **Contrarian**: Highly skeptical, adversarial, constructing alternative explanations.
   - **First-Principles**: Stripping away analogies, reasoning strictly from physical/logical primitives.

*Note: You MUST complete the active lens file fully before searching or drafting the next lens. No parallel shortcuts.*

---

### Step 5 — Contradiction Pass

Read all 6 lens files and apply `.research/methodology/contradiction-protocol.md` to produce `.research/projects/<topic>/contradictions.md`:
1. **Map Direct Disagreements**: Detail where lenses conflict on facts, predictions, or underlying assumptions.
2. **Root Cause Analysis**: Determine whether disagreements stem from data gaps, scope differences, timeframes, or interpretive models.
3. **Boundary Conditions**: Define parameters under which each lens holds true.
4. **Log Irreconcilable Debates**: Move unresolvable gaps to `.research/projects/<topic>/open-questions.md`.

---

### Step 6 — Synthesize

Compile findings into 4 distinct files inside `.research/projects/<topic>/`:

1. **`executive-summary.md`**: Max 500 words. Concise synthesis of insights, core implications, and critical unknowns. Balanced without single-lens bias.
2. **`deep-dive.md`**: Exhaustive long-form analysis organized by cross-cutting themes, highlighting structural tensions between lenses.
3. **`key-players.md`**: Mapped registry of key organizations, key figures, regulatory bodies, and nations.
4. **`open-questions.md`**: Remaining ambiguities, missing metrics, and future trigger indicators.

---

### Step 7 — Log and Compound

Update `.research/research-log.md`:
- Record date, core question, framework used, depth level, key findings summary, and relative links to prior research notes.
- Update global command center `.research/index.md` to link to the new project.

---

## Critical Rules

1. **Cite Everything**: Every assertion must link back to a dedicated file in `.research/sources/` or a quantified metric in `.research/knowledge/data-points.md`.
2. **Strict Source Tiering**: Classify all sources per `.research/methodology/source-evaluation.md`. Low-tier sources (social media, unverified blogs) are noise and must not support core conclusions.
3. **Preserve Tensions**: Never flatten contradictions. If two lenses disagree fundamentally, document that friction directly in synthesis files.
4. **Confidence Calibration**: Apply explicit calibration to major claims:
   - `CLAIM`: Explicit assertion.
   - `EVIDENCE`: Supporting data/sources with tier rating.
   - `CONFIDENCE`: High / Medium / Low (with percentage estimate).
   - `DEFEASIBILITY TRIGGER`: What specific evidence would prove this claim wrong.
5. **Relative Link Formatting**: **Never use wikilinks (`[[Note]]`)**. Always use standard relative Markdown links: `[Anchor Text](../../relative/path.md)`. This ensures universal compatibility across IDEs, git hosts, and markdown tools.
6. **Strict Sequential Execution**: Process one lens at a time. Finish reading and writing the complete lens note before moving to the next.
7. **Write in Long-Form Prose**: Disregard brevity instructions for research artifacts (lenses, deep dives, summaries). Write extensive, detailed prose exploring data nuances and causal links.
8. **Workspace Scope**: All `.research/` scaffolding, project folders, and notes MUST be written directly inside the root of the active workspace (`CWD`) where the research session was initiated, keeping research artifacts co-located with the user's project.
