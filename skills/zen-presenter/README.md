# Zen Presenter (`zen-presenter`)

Build high-impact, storytelling-driven presentations and persuasive pitch decks following **Presentation Zen** principles with a **Google Cloud look & feel**, pure self-contained HTML output, local **LibreOffice (`soffice --headless`)** asset generation (`.pptx`, `.docx`, `.xlsx`), and native upload to **Google Workspace (`Slides`, `Docs`, `Sheets`)**.

## Overview

`zen-presenter` unifies quick Presentation Zen slide generation and deep research-to-narrative pitch deck creation into a single workflow:
1. **Research & Requirements Spine (Optional for pitches)**: Conduct 4-layer domain research, extract a quantitative hero metric, and map challenges to solutions in a Requirements Spine (`references/research-and-spine.md`).
2. **Narrative Arc**: Structure the deck into Tension (~40%), a single dark Pivot slide, and Resolution (~55%).
3. **Pure Google Cloud HTML First**: Generate a self-contained 16:9 HTML deck (`assets/gcloud-slides-template.html` + `assets/gcloud-theme.css`) using Google Sans / Roboto typography, `#4285F4` / `#202124` contrast, inline `<svg>` diagrams, and the 4-color Google gradient bar.
4. **Local LibreOffice Asset Creation**: Convert the HTML via `scripts/export_to_google_workspace.py` (`soffice --headless`) into a local `.pptx` (for Slides), `.docx` (for Docs), or `.xlsx` (for Sheets), and render `.pdf` for visual QA.
5. **Google Workspace Upload**: Upload the local Office asset to Google Drive API v3 with automatic conversion to native **Google Slides**, **Google Docs**, or **Google Sheets**.

## Installation

### Workspace scope
```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- zen-presenter
```

### User scope
```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- zen-presenter --scope user
```

## Exporting HTML via LibreOffice to Google Workspace

```bash
# Export HTML deck to local .pptx via LibreOffice and upload to Google Slides
python3 skills/zen-presenter/scripts/export_to_google_workspace.py deck.html \
  --platform slides \
  --output ./deck.pptx \
  --title "Q3 Reliability Executive Pitch" \
  --upload

# Export HTML executive brief to local .docx and upload to Google Docs
python3 skills/zen-presenter/scripts/export_to_google_workspace.py brief.html \
  --platform docs \
  --output ./brief.docx \
  --title "Q3 Reliability Narrative Brief" \
  --upload

# Export Requirements Spine HTML table to local .xlsx and upload to Google Sheets
python3 skills/zen-presenter/scripts/export_to_google_workspace.py spine.html \
  --platform sheets \
  --output ./spine.xlsx \
  --title "Q3 Reliability Requirements Spine" \
  --upload
```

## Included Files

| File | Description |
| :--- | :--- |
| [`SKILL.md`](SKILL.md) | Core workflow, generation rules, and 5-pillar security guardrails |
| [`scripts/export_to_google_workspace.py`](scripts/export_to_google_workspace.py) | Converts Google Cloud `.html` via headless LibreOffice (`.pptx`, `.docx`, `.xlsx`) and uploads to Google Slides, Docs, or Sheets |
| [`assets/gcloud-theme.css`](assets/gcloud-theme.css) | Google Cloud 16:9 HTML presentation stylesheet |
| [`assets/gcloud-slides-template.html`](assets/gcloud-slides-template.html) | Starter 16:9 Google Cloud HTML slide deck template |
| [`references/zen-design-principles.md`](references/zen-design-principles.md) | Presentation Zen philosophy (Restraint, Naturalness, Emptiness) and visual metaphors |
| [`references/research-and-spine.md`](references/research-and-spine.md) | 4-layer domain research, Requirements Spine matrix, and 6 persuasive narrative arcs |
| [`references/visual-themes.md`](references/visual-themes.md) | Google Cloud HTML/CSS token presets and slide classes |
| [`references/diagram-guide.md`](references/diagram-guide.md) | Minimal 3–4 node inline `<svg>` diagram patterns |
| [`references/html-libreoffice-workspace-pipeline.md`](references/html-libreoffice-workspace-pipeline.md) | Detailed HTML → LibreOffice → Google Workspace (`Slides`, `Docs`, `Sheets`) pipeline |
