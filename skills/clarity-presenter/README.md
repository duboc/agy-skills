# Clarity Presenter (`clarity-presenter`)

Build structured, mixed-audience presentations combining the **SCQA** (*Situation-Complication-Question-Answer*) narrative framework with **Assertion-Evidence** slide design and **Dual-Perspective** paired slides (white technical slides + dark business slides) in a **Google Cloud look & feel**, pure self-contained HTML output, local **LibreOffice (`soffice --headless`)** asset generation (`.pptx`, `.docx`, `.xlsx`), and native upload to **Google Workspace (`Slides`, `Docs`, `Sheets`)**.

## Overview

`clarity-presenter` bridges engineers and business stakeholders in a single coherent deck:
1. **SCQA Narrative Arc**: Ground the room in the *Situation*, quantify the *Complication*, pose one central *Question*, and deliver the *Answer* (`references/scqa-framework-guide.md`).
2. **Dual-Perspective Assertion-Evidence Slides**: Pair technical mechanism assertions (`<section class="slide">`, white background) with business outcome assertions (`<section class="slide invert">`, dark `#202124` background) backed by inline `<svg>` diagrams and metrics (`references/assertion-evidence-guide.md` & `references/dual-perspective-guide.md`).
3. **Pure Google Cloud HTML First**: Author self-contained 16:9 HTML directly (`assets/gcloud-slides-template.html` + `assets/gcloud-theme.css`) with zero Marp dependency.
4. **Local LibreOffice Asset Creation**: Convert the HTML via `scripts/export_to_google_workspace.py` (`soffice --headless`) into a local `.pptx` (for Slides), `.docx` (for Docs), or `.xlsx` (for Sheets), and render `.pdf` for visual QA.
5. **Google Workspace Upload**: Upload the local Office asset to Google Drive API v3 with automatic conversion to native **Google Slides**, **Google Docs**, or **Google Sheets**.

## How It Differs from `zen-presenter`

| Aspect | `zen-presenter` | `clarity-presenter` |
| :--- | :--- | :--- |
| **Words per slide** | 10–18 words | 15–25 words |
| **Headlines** | Short provocative statement or hero number | 8–15 word falsifiable sentence assertion (`<h2>`) |
| **Bullets** | Never | Sparingly (max 3 single-level items) |
| **Narrative Structure** | 3-Act Tension → Dark Pivot → Resolution (plus optional 4-layer research spine) | McKinsey SCQA (`Situation → Complication → Question → Answer`) |
| **Audience Pairing** | Unified visual storytelling | Dual-perspective: Technical (white) + Business (dark `invert`) pairs |
| **Best For** | Keynotes, persuasive pitches, executive storytelling | Architecture proposals, RFC readouts, mixed engineering + VP reviews |

## Installation

### Workspace scope
```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- clarity-presenter
```

### User scope
```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- clarity-presenter --scope user
```

## Exporting HTML via LibreOffice to Google Workspace

```bash
# Export HTML deck to local .pptx via LibreOffice and upload to Google Slides
python3 skills/clarity-presenter/scripts/export_to_google_workspace.py clarity-deck.html \
  --platform slides \
  --output ./clarity-deck.pptx \
  --title "Cloud Run Active-Active SCQA Proposal" \
  --upload

# Export SCQA executive readout HTML to local .docx and upload to Google Docs
python3 skills/clarity-presenter/scripts/export_to_google_workspace.py scqa-brief.html \
  --platform docs \
  --output ./scqa-brief.docx \
  --title "Cloud Run Active-Active SCQA Brief" \
  --upload

# Export Dual-Perspective Concept Matrix HTML table to local .xlsx and upload to Google Sheets
python3 skills/clarity-presenter/scripts/export_to_google_workspace.py concept-matrix.html \
  --platform sheets \
  --output ./concept-matrix.xlsx \
  --title "Dual-Perspective Concept Mapping" \
  --upload
```

## Included Files

| File | Description |
| :--- | :--- |
| [`SKILL.md`](SKILL.md) | Core workflow, SCQA + assertion-evidence rules, and 5-pillar security guardrails |
| [`scripts/export_to_google_workspace.py`](scripts/export_to_google_workspace.py) | Converts Google Cloud `.html` via headless LibreOffice (`.pptx`, `.docx`, `.xlsx`) and uploads to Google Slides, Docs, or Sheets |
| [`assets/gcloud-theme.css`](assets/gcloud-theme.css) | Google Cloud 16:9 HTML presentation stylesheet |
| [`assets/gcloud-slides-template.html`](assets/gcloud-slides-template.html) | Starter 16:9 Google Cloud SCQA dual-perspective HTML template |
| [`references/assertion-evidence-guide.md`](references/assertion-evidence-guide.md) | Sentence headline writing rules, falsifiability test, and evidence types |
| [`references/scqa-framework-guide.md`](references/scqa-framework-guide.md) | SCQA narrative structure, content mapping, and technical examples |
| [`references/dual-perspective-guide.md`](references/dual-perspective-guide.md) | Technical-to-business translation patterns and audience balance adaptation |
| [`references/visual-themes.md`](references/visual-themes.md) | Dual-perspective Google Cloud HTML/CSS theme presets |
| [`references/diagram-guide.md`](references/diagram-guide.md) | Inline `<svg>` diagrams as assertion evidence |
| [`references/html-libreoffice-workspace-pipeline.md`](references/html-libreoffice-workspace-pipeline.md) | Detailed HTML → LibreOffice → Google Workspace (`Slides`, `Docs`, `Sheets`) pipeline |
