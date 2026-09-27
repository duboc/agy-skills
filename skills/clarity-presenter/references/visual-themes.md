# Visual Theme Presets for Clarity Presenter (Google Cloud HTML)

Pre-defined visual theme combinations for `clarity-presenter`. Every preset preserves the **dual-perspective alternation pattern** (light technical slides for *how it works*, dark or accent business slides for *why it matters*) inside pure, self-contained Google Cloud HTML (`<section class="slide ...">`).

## Key Constraint: Dual-Perspective Preservation

Every `clarity-presenter` theme defines two contrasting visual modes:
1. **Technical perspective (`<section class="slide">`)** — White/light background (`#FFFFFF`) for engineering mechanisms, architecture, and benchmarks.
2. **Business perspective (`<section class="slide invert">` or `<section class="slide section">`)** — Dark charcoal (`#202124`) or Google Blue (`#4285F4`) background for SLA, cost, risk, and revenue impact.

---

## 1. Google Cloud (Default)

Standard Google Cloud visual identity with white technical slides, dark charcoal business slides, Google Blue section dividers, and the 4-color Google gradient bar on `title` and `closing` slides.

| Attribute | Technical Slides (`class="slide"`) | Business Slides (`class="slide invert"`) |
| :--- | :--- | :--- |
| **Background** | White (`#FFFFFF`) | Charcoal (`#202124`) or Google Blue (`#4285F4` via `section`) |
| **Text Color** | Dark (`#202124`) | White (`#FFFFFF`) |
| **Accent (`<strong>`)** | Google Blue (`#4285F4`) | Light Blue (`#5C92F6`) |
| **Font Family** | `'Google Sans', 'Roboto', 'Inter', Arial, sans-serif` | `'Google Sans', 'Roboto', 'Inter', Arial, sans-serif` |

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

---

## 2. Executive Blue

Formal navy and gold palette for board reviews and strategy proposals:

| Attribute | Technical Slides | Business Slides |
| :--- | :--- | :--- |
| **Background** | Pale blue-grey (`#F0F4F8`) | Deep Navy (`#1B2A4A`) |
| **Text Color** | Dark navy (`#1B2A4A`) | White (`#FFFFFF`) |
| **Accent (`<strong>`)** | Steel blue (`#3A6EA5`) | Gold (`#C9A94F`) |

---

## 3. Data-Driven & FinOps

Analytical teal for technical slides and metric orange for business ROI slides:

| Attribute | Technical Slides | Business Slides |
| :--- | :--- | :--- |
| **Background** | White (`#FFFFFF`) | Charcoal (`#2D2D2D`) |
| **Text Color** | Dark (`#333333`) | White (`#FFFFFF`) |
| **Accent (`<strong>`)** | Data teal (`#00897B`) | Metric orange (`#FF6D00`) |

---

## 4. Cloud Architecture & SRE

Clean white for architecture diagrams and dark slate with emerald accents for operational outcomes:

| Attribute | Technical Slides | Business Slides |
| :--- | :--- | :--- |
| **Background** | White (`#FFFFFF`) | Dark slate (`#1E293B`) |
| **Text Color** | Near-black (`#0F172A`) | Slate grey (`#E2E8F0`) |
| **Accent (`<strong>`)** | Sky blue (`#0EA5E9`) | Emerald (`#10B981`) |

---

## 5. Compliance & Security

Conservative trust-blue palette where business slides highlight risks in red (`<strong>`) and compliance controls in green (`<em>`):

| Attribute | Technical Slides | Business Slides |
| :--- | :--- | :--- |
| **Background** | Off-white (`#F8F8F8`) | Dark grey (`#1F2937`) |
| **Text Color** | Dark (`#1F2937`) | Light grey (`#E5E7EB`) |
| **Accent** | Trust blue (`#1D4ED8`) | Red (`#DC2626`) for risk / Green (`#059669`) for compliance |
