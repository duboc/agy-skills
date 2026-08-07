# zen-pitch

A skill for researching a market or problem domain, turning findings into a requirements spine, and building a Presentation Zen–style slide deck that tells the story of the challenge and how a proposed solution resolves it.

## Overview

Most slide decks fail not because of rendering, but because they were built before anyone established a compelling narrative. `zen-pitch` front-loads research, narrative arc planning, and requirements validation before writing any slide code.

### Pipeline Workflow

1. **SCOPE** → Interactive scoping for audience, objective, arc, and palette.
2. **RESEARCH** → Multi-layered domain search until the challenge is stated as a specific metric.
3. **SPINE** → Matrix mapping Challenge → Evidence → Solution requirements.
4. **NARRATIVE** → Storyboard claim-per-slide arc for sign-off before coding.
5. **BUILD** → Compile MARP slides using Presentation Zen design principles and `deck_kit.js`.
6. **QA & DELIVER** → Inspection and speaker notes handover.

## Activation Keywords

Activates when you ask Agy to:
- "Build a pitch deck for X"
- "Make a presentation showing how we solve Y"
- "Turn this research into a deck"
- "Create an executive readout or client presentation"

## Installation

### Method 1: One-liner with curl (Recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- zen-pitch
```

To install globally for your user profile:

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- zen-pitch --scope user
```

### Method 2: Manual Copy

Copy the skill folder into your workspace or user skills directory:
```bash
# Workspace scope
cp -r skills/zen-pitch .agents/skills/zen-pitch

# User scope
cp -r skills/zen-pitch ~/.gemini/config/skills/zen-pitch
```
