# HTML -> LibreOffice -> Google Workspace Pipeline (`Slides`, `Docs`, `Sheets`)

Both presentation skills (`clarity-presenter` and `zen-presenter`) enforce a deterministic 3-stage pipeline that **always generates self-contained Google Cloud HTML first**, uses **headless LibreOffice (`soffice --headless`)** to build and verify the local Office/ODF asset file, and uploads to **Google Drive API v3** with native Google Workspace `mimeType` conversion.

## Stage 1: Author Pure Google Cloud HTML (`.html`)

Never use `@marp-team/marp-cli`. Write a self-contained `.html` file using the official Google Cloud visual identity tokens (`assets/gcloud-theme.css` / `assets/gcloud-slides-template.html`):

| Target Platform | HTML Structure | Google Cloud Styling Rules |
| :--- | :--- | :--- |
| **Google Slides (`slides`)** | `<section class="slide [title\|section\|invert\|lead\|stats\|quote\|closing]">` with `<h2>` assertion headlines, visual evidence, and `<aside class="notes">` | 16:9 (`1280×720`), white technical slides (`#FFFFFF`), dark/blue business slides (`#202124` / `#4285F4`), 4-color bottom gradient bar on `title` and `closing` slides |
| **Google Docs (`docs`)** | Semantic `<article>` with SCQA sections (`Situation`, `Complication`, `Question`, `Answer`), `<table bgcolor="#4285F4">` headers, and callout banners | Inline CSS + HTML `bgcolor` attributes so LibreOffice Writer preserves Google Cloud colors, callout banners, and `Roboto Mono` code blocks |
| **Google Sheets (`sheets`)** | Semantic `<table>` containing the Dual-Perspective Concept Mapping Matrix (`Concept | Technical Assertion | Business Assertion | Evidence Metric`) | Header cells styled with `background-color: #4285F4; color: #FFFFFF; font-weight: bold` and alternating `#F8F9FA` rows |

---

## Stage 2: Create Local Asset via Headless LibreOffice (`soffice --headless`)

Always create the local Office asset file on disk before uploading to Google Workspace. Execute inside an isolated `0700` working directory (`mktemp -d "${HOME}/.cache/gcloud-workspace-export.XXXXXX"` or `tempfile.TemporaryDirectory()`):

### Option A: Automated Exporter Script (Recommended)

```bash
set -euo pipefail
umask 077
WORK_DIR="$(mktemp -d "${HOME}/.cache/gcloud-workspace-export.XXXXXX")"
chmod 700 "$WORK_DIR"
trap 'rm -rf "$WORK_DIR"' EXIT

# 1. Slides (.html -> LibreOffice .pptx + optional Google Slides upload)
python3 scripts/export_to_google_workspace.py clarity-deck.html \
  --platform slides \
  --output ./clarity-deck.pptx \
  --title "SCQA Architecture Proposal"

# 2. Docs (.html -> LibreOffice .docx + optional Google Docs upload)
python3 scripts/export_to_google_workspace.py scqa-narrative.html \
  --platform docs \
  --output ./scqa-narrative.docx \
  --title "SCQA Executive Narrative"

# 3. Sheets (.html -> LibreOffice .xlsx + optional Google Sheets upload)
python3 scripts/export_to_google_workspace.py dual-perspective-matrix.html \
  --platform sheets \
  --output ./dual-perspective-matrix.xlsx \
  --title "Dual-Perspective Concept Mapping"
```

### Option B: Direct Headless LibreOffice Commands & Visual PDF QA

When invoking `soffice` directly, always pass argument arrays (`shell=False`) and render a `.pdf` to visually inspect slide layout, contrast, and text wrapping:

```bash
set -euo pipefail
umask 077
WORK_DIR="$(mktemp -d "${HOME}/.cache/gcloud-workspace-export.XXXXXX")"
chmod 700 "$WORK_DIR"
trap 'rm -rf "$WORK_DIR"' EXIT

# Convert presentation FODP/ODP to local .pptx and .pdf for visual QA
soffice --headless --convert-to pptx --outdir "$WORK_DIR" "$WORK_DIR/clarity-deck.fodp"
soffice --headless --convert-to pdf --outdir "$WORK_DIR" "$WORK_DIR/clarity-deck.pptx"

# Convert SCQA narrative HTML brief to local .docx
soffice --headless --writer --convert-to "docx:MS Word 2007 XML" --outdir "$WORK_DIR" scqa-narrative.html

# Convert Dual-Perspective HTML table to local .xlsx
soffice --headless --calc --infilter="html:HTML (StarCalc)" --convert-to xlsx --outdir "$WORK_DIR" dual-perspective-matrix.html
```

---

## Stage 3: Upload Local Asset to Google Workspace (`Slides`, `Docs`, `Sheets`)

Pass `--upload` to `scripts/export_to_google_workspace.py` to upload the LibreOffice-generated local file (`.pptx`, `.docx`, or `.xlsx`) to Google Drive API v3 (`https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart`) with automatic Workspace conversion:

| `--platform` | Local LibreOffice Asset | Target Google Workspace `mimeType` | Resulting Google Workspace URL |
| :--- | :--- | :--- | :--- |
| `slides` | `<name>.pptx` | `application/vnd.google-apps.presentation` | `https://docs.google.com/presentation/d/<FILE_ID>/edit` |
| `docs` | `<name>.docx` | `application/vnd.google-apps.document` | `https://docs.google.com/document/d/<FILE_ID>/edit` |
| `sheets` | `<name>.xlsx` | `application/vnd.google-apps.spreadsheet` | `https://docs.google.com/spreadsheets/d/<FILE_ID>/edit` |

### Authentication Hygiene
- The uploader resolves credentials from `$GCLI_ACCESS_TOKEN_PATH` (enforcing `0600` file permissions), `~/.cache/gdoc-spec/access_token`, or `gcloud auth print-access-token`.
- If OAuth credentials are not configured in the current environment, deliver both the self-contained `.html` file and the LibreOffice-generated local `.pptx` / `.docx` / `.xlsx` asset, and state clearly that live Google Workspace upload requires an active OAuth token.
