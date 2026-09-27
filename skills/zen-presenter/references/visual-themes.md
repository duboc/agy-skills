# Visual Theme Presets (Google Cloud HTML)

Pre-defined visual theme combinations for `zen-presenter`. All presets target a **Google Cloud look & feel** by default and are authored as pure, self-contained HTML (`<section class="slide ...">`) styled via CSS custom properties (`:root`).

## 1. Google Cloud (Default)

Clean, high-contrast Google Cloud visual identity using Google Sans / Roboto / Inter typography, the 4-color Google accent bar, and structured `<section class="slide">` classes.

| Attribute | Value |
| :--- | :--- |
| **Mood** | Professional |
| **Typography** | Statement (`<h1>` / `<h2>` claims, zero bullet lists) |
| **Colors** | Charcoal (`#202124`) on White (`#FFFFFF`), Google Blue (`#4285F4`) accents |
| **Font Family** | `'Google Sans', 'Roboto', 'Inter', Arial, sans-serif` |
| **Gradient Bar** | 4-color Google bar (`#4285F4`, `#EA4335`, `#FBBC05`, `#34A853`) on `title` and `closing` slides |

### CSS Variables (`:root`)

```css
:root {
  --gcloud-blue: #4285F4;
  --gcloud-red: #EA4335;
  --gcloud-yellow: #FBBC05;
  --gcloud-green: #34A853;
  --gcloud-grey-900: #202124;
  --gcloud-grey-700: #5F6368;
  --gcloud-grey-200: #E8EAED;
  --gcloud-grey-100: #F8F9FA;
  --gcloud-light-blue: #5C92F6;
  --gcloud-bg: #FFFFFF;
}
```

### Slide Type Classes (`<section class="slide ...">`)

| HTML Class | Visual Effect | Best Used For |
| :--- | :--- | :--- |
| `slide title` | Large headline, subtitle, 4-color Google bar at bottom | Opening cover slide |
| `slide section` | Google Blue (`#4285F4`) background, white text | Act dividers or high-energy transitions |
| `slide lead` | Vertically and horizontally centered statement | Core claim or pivot question |
| `slide stats` | Oversized `#4285F4` metric (`96px–128px`) + concise caption | Hero quantification slide |
| `slide quote` | Large quotation with `#5F6368` attribution | Stakeholder or customer evidence |
| `slide invert` | Dark charcoal (`#202124`) background, white text, `#5C92F6` accents | The Pivot slide separating Tension from Resolution |
| `slide closing` | Centered call-to-action with 4-color Google bar at bottom | Final slide returning to the opening metric |
| `slide` *(default)* | Clean white (`#FFFFFF`) background, `#202124` text | Tension and Resolution narrative slides |

---

## 2. Executive Navy Override

Formal navy and gold palette for board readouts and executive decision decks while preserving the 16:9 Google Cloud layout structure:

```css
:root {
  --gcloud-blue: #3A6EA5;
  --gcloud-grey-900: #1B2A4A;
  --gcloud-bg: #F8FAFC;
  --gcloud-light-blue: #C9A94F;
}
```

---

## 3. Cloud Architecture & SRE Override

High-contrast slate and sky-blue palette suited for deep infrastructure, Kubernetes, and reliability pitches:

```css
:root {
  --gcloud-blue: #0EA5E9;
  --gcloud-grey-900: #0F172A;
  --gcloud-bg: #FFFFFF;
  --gcloud-light-blue: #10B981;
}
```

---

## 4. Data & FinOps Override

Analytical teal and metric orange accents for quantitative benchmarks and cloud FinOps reviews:

```css
:root {
  --gcloud-blue: #00897B;
  --gcloud-grey-900: #202124;
  --gcloud-bg: #FFFFFF;
  --gcloud-light-blue: #FF6D00;
}
```

## Using Presets in Self-Contained HTML & LibreOffice Export

1. Always start from `assets/gcloud-slides-template.html` or embed `assets/gcloud-theme.css` inside a `<style>` tag so the `.html` deck is 100% self-contained.
2. When exporting via `scripts/export_to_google_workspace.py`, the slide classes (`title`, `section`, `invert`, `lead`, `stats`, `quote`, `closing`) automatically map to the corresponding 16:9 LibreOffice backgrounds and 4-color Google bars before uploading to Google Slides.
