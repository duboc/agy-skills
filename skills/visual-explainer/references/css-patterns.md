# CSS Patterns Reference

Comprehensive CSS patterns for generating self-contained visual HTML pages.

---

## Layout Patterns

### CSS Grid Card Layouts

```css
/* 2-column card grid */
.ve-grid-2 {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

/* 3-column card grid */
.ve-grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

/* Responsive: collapse to 1 column on mobile, 2 on tablet */
@media (max-width: 1024px) {
  .ve-grid-3 { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 640px) {
  .ve-grid-3,
  .ve-grid-2 { grid-template-columns: 1fr; }
}
```

### Flexbox Centering and Alignment

```css
/* Center content both axes */
.ve-center {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Space-between row with vertical centering */
.ve-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

/* Vertical stack with gap */
.ve-stack {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
```

### Sticky Header / Footer

```css
/* Sticky header */
.ve-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--color-surface);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--color-border);
  padding: 0.75rem 1.5rem;
}

/* Sticky footer */
.ve-footer {
  position: sticky;
  bottom: 0;
  z-index: 100;
  background: var(--color-surface);
  border-top: 1px solid var(--color-border);
  padding: 0.75rem 1.5rem;
}
```

### Full-Viewport Sections

```css
.ve-section-full {
  min-height: 100dvh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 4rem 2rem;
}
```

---

## Card Components

### Base Card

```css
.ve-card {
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}
```

### Hero Card (Elevated)

```css
.ve-card--hero {
  padding: 2rem;
  border-radius: 16px;
  border: 1px solid var(--color-accent-muted);
  background: var(--color-accent-bg);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
}
```

### Recessed Card (Sunken)

```css
.ve-card--recessed {
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid var(--color-border);
  background: var(--color-bg);
  box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.08);
}
```

### Card Grid Responsive Breakpoints

```css
.ve-card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

@media (max-width: 640px) {
  .ve-card-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}
```

---

## SVG Connectors

### Vertical Flow Arrow Between Cards

```html
<svg width="40" height="40" viewBox="0 0 40 40" style="display:block;margin:0 auto;">
  <line x1="20" y1="0" x2="20" y2="30" stroke="var(--color-accent)" stroke-width="2"/>
  <polygon points="14,28 20,38 26,28" fill="var(--color-accent)"/>
</svg>
```

### Horizontal Connector

```html
<svg width="60" height="20" viewBox="0 0 60 20" style="display:block;margin:auto 0;">
  <line x1="0" y1="10" x2="50" y2="10" stroke="var(--color-accent)" stroke-width="2"/>
  <polygon points="48,5 58,10 48,15" fill="var(--color-accent)"/>
</svg>
```

### Curved Connector (SVG path)

```html
<svg width="120" height="60" viewBox="0 0 120 60">
  <path d="M10,10 C40,10 80,50 110,50"
        fill="none"
        stroke="var(--color-accent)"
        stroke-width="2"
        stroke-dasharray="4,4"/>
  <polygon points="106,45 114,50 106,55" fill="var(--color-accent)"/>
</svg>
```

### CSS-Only Connector (vertical dashed line)

```css
.ve-connector-vertical {
  width: 2px;
  height: 2rem;
  margin: 0 auto;
  background: repeating-linear-gradient(
    to bottom,
    var(--color-accent) 0px,
    var(--color-accent) 6px,
    transparent 6px,
    transparent 12px
  );
}
```

---

## Code Blocks

### Pre-formatted Code

```css
.ve-code {
  background: var(--color-code-bg, #1e1e2e);
  color: var(--color-code-fg, #cdd6f4);
  padding: 1.25rem 1.5rem;
  border-radius: 8px;
  font-family: 'Fira Code', 'JetBrains Mono', monospace;
  font-size: 0.875rem;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
  overflow-x: auto;
  border: 1px solid var(--color-border);
}
```

### Syntax Highlighting via CSS Classes

```css
.ve-code .keyword  { color: #cba6f7; }  /* purple */
.ve-code .string   { color: #a6e3a1; }  /* green */
.ve-code .comment  { color: #6c7086; font-style: italic; }
.ve-code .function { color: #89b4fa; }  /* blue */
.ve-code .number   { color: #fab387; }  /* peach */
.ve-code .operator { color: #89dceb; }  /* teal */
.ve-code .type     { color: #f9e2af; }  /* yellow */
```

### Line Numbers Pattern

```css
.ve-code-numbered {
  counter-reset: line;
}
.ve-code-numbered .line::before {
  counter-increment: line;
  content: counter(line);
  display: inline-block;
  width: 2.5em;
  margin-right: 1em;
  text-align: right;
  color: var(--color-muted, #585b70);
  user-select: none;
}
```

### Copy Button Pattern

```html
<div class="ve-code-wrapper" style="position:relative;">
  <button class="ve-copy-btn" onclick="navigator.clipboard.writeText(this.parentElement.querySelector('code').textContent)">
    Copy
  </button>
  <pre class="ve-code"><code>...</code></pre>
</div>
```

```css
.ve-copy-btn {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  padding: 0.25rem 0.75rem;
  font-size: 0.75rem;
  border-radius: 4px;
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  color: var(--color-muted);
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s ease;
}
.ve-code-wrapper:hover .ve-copy-btn { opacity: 1; }
.ve-copy-btn:active { background: var(--color-accent); color: #fff; }
```

---

## Prose Page Elements

### Lead Paragraph

```css
.ve-lead {
  font-size: 1.25rem;
  line-height: 1.7;
  max-width: 65ch;
  color: var(--color-text-secondary);
  margin-bottom: 2rem;
}
```

### Pull Quote

```css
.ve-pullquote {
  border-left: 4px solid var(--color-accent);
  padding: 1rem 1.5rem;
  margin: 2rem 0;
  font-size: 1.15rem;
  font-style: italic;
  color: var(--color-text-secondary);
  background: var(--color-accent-bg);
  border-radius: 0 8px 8px 0;
}
```

### Callout Boxes

```css
.ve-callout {
  padding: 1rem 1.25rem;
  border-radius: 8px;
  border-left: 4px solid;
  margin: 1.5rem 0;
  font-size: 0.9rem;
}
.ve-callout--info {
  border-color: #89b4fa;
  background: rgba(137, 180, 250, 0.1);
  color: #89b4fa;
}
.ve-callout--warning {
  border-color: #f9e2af;
  background: rgba(249, 226, 175, 0.1);
  color: #f9e2af;
}
.ve-callout--success {
  border-color: #a6e3a1;
  background: rgba(166, 227, 161, 0.1);
  color: #a6e3a1;
}
.ve-callout--error {
  border-color: #f38ba8;
  background: rgba(243, 139, 168, 0.1);
  color: #f38ba8;
}
```

### Section Dividers

```css
.ve-divider {
  border: none;
  height: 1px;
  margin: 3rem auto;
  max-width: 200px;
  background: linear-gradient(
    to right,
    transparent,
    var(--color-border),
    transparent
  );
}
```

---

## Collapsible Sections

### Details/Summary Styling

```css
details.ve-collapsible {
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 0;
  margin: 1rem 0;
  overflow: hidden;
}

details.ve-collapsible summary {
  padding: 0.75rem 1.25rem;
  cursor: pointer;
  font-weight: 600;
  background: var(--color-surface);
  list-style: none;
  display: flex;
  align-items: center;
  justify-content: space-between;
  user-select: none;
}

details.ve-collapsible summary::-webkit-details-marker { display: none; }
```

### Custom Marker / Indicator

```css
details.ve-collapsible summary::after {
  content: '+';
  font-size: 1.25rem;
  font-weight: 300;
  transition: transform 0.2s ease;
}
details.ve-collapsible[open] summary::after {
  content: '\2212'; /* minus sign */
}
```

### Animated Open/Close

```css
details.ve-collapsible .ve-collapsible-body {
  padding: 1rem 1.25rem;
  animation: ve-slideDown 0.2s ease;
}

@keyframes ve-slideDown {
  from { opacity: 0; transform: translateY(-8px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

---

## Status Indicators

### Colored Dot Badges

```css
.ve-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.8rem;
  font-weight: 500;
}
.ve-badge::before {
  content: '';
  width: 8px;
  height: 8px;
  border-radius: 50%;
}
.ve-badge--green::before  { background: #a6e3a1; }
.ve-badge--red::before    { background: #f38ba8; }
.ve-badge--amber::before  { background: #f9e2af; }
.ve-badge--muted::before  { background: #6c7086; }
```

### Progress Bars

```css
.ve-progress {
  height: 8px;
  border-radius: 4px;
  background: var(--color-border);
  overflow: hidden;
}
.ve-progress-fill {
  height: 100%;
  border-radius: 4px;
  background: linear-gradient(90deg, var(--color-accent), var(--color-accent-light));
  transition: width 0.6s ease;
}
```

Usage: `<div class="ve-progress"><div class="ve-progress-fill" style="width:72%"></div></div>`

### Trend Arrows

```css
.ve-trend { font-weight: 600; font-size: 0.85rem; }
.ve-trend--up   { color: #a6e3a1; }
.ve-trend--up::before   { content: '\2191 '; } /* up arrow */
.ve-trend--down { color: #f38ba8; }
.ve-trend--down::before { content: '\2193 '; } /* down arrow */
```

---

## Animation Patterns

### Staggered Fade-In on Load

```css
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

.ve-card {
  opacity: 0;
  animation: fadeUp 0.5s ease forwards;
}

/* Stagger children by index */
.ve-card:nth-child(1) { animation-delay: 0.05s; }
.ve-card:nth-child(2) { animation-delay: 0.10s; }
.ve-card:nth-child(3) { animation-delay: 0.15s; }
.ve-card:nth-child(4) { animation-delay: 0.20s; }
.ve-card:nth-child(5) { animation-delay: 0.25s; }
.ve-card:nth-child(6) { animation-delay: 0.30s; }
```

### Fade + Scale for KPIs

```css
@keyframes fadeScale {
  from { opacity: 0; transform: scale(0.9); }
  to   { opacity: 1; transform: scale(1); }
}

.ve-kpi {
  opacity: 0;
  animation: fadeScale 0.4s ease forwards;
}
```

### Count-Up for Numbers

```css
@keyframes countUp {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Use JS for actual number interpolation; CSS handles the entrance */
.ve-number {
  animation: countUp 0.6s ease forwards;
  font-variant-numeric: tabular-nums;
}
```

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Dark / Light Theme

### CSS Custom Properties Pattern

```css
:root {
  /* Light theme defaults */
  --color-bg: #f8f9fa;
  --color-surface: #ffffff;
  --color-elevated: #ffffff;
  --color-text: #1a1a2e;
  --color-text-secondary: #4a4a6a;
  --color-muted: #8888a0;
  --color-border: #e2e4e8;
  --color-accent: #6366f1;
  --color-accent-light: #818cf8;
  --color-accent-muted: rgba(99, 102, 241, 0.2);
  --color-accent-bg: rgba(99, 102, 241, 0.06);
  --color-code-bg: #1e1e2e;
  --color-code-fg: #cdd6f4;
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-bg: #0f0f1a;
    --color-surface: #1a1a2e;
    --color-elevated: #252540;
    --color-text: #e2e4f0;
    --color-text-secondary: #a0a0b8;
    --color-muted: #585b70;
    --color-border: #2e2e48;
    --color-accent: #818cf8;
    --color-accent-light: #a5b4fc;
    --color-accent-muted: rgba(129, 140, 248, 0.2);
    --color-accent-bg: rgba(129, 140, 248, 0.06);
    --color-code-bg: #11111b;
    --color-code-fg: #cdd6f4;
  }
}
```

### Surface Depth Levels

Use three depth levels for visual hierarchy:

| Level | Variable | Light | Dark | Usage |
|-------|----------|-------|------|-------|
| Background | `--color-bg` | `#f8f9fa` | `#0f0f1a` | Page background |
| Surface | `--color-surface` | `#ffffff` | `#1a1a2e` | Cards, panels |
| Elevated | `--color-elevated` | `#ffffff` | `#252540` | Modals, tooltips, dropdowns |

Apply depth via borders and shadows rather than background alone for subtle differentiation in light mode.

### Google Cloud Theme

Use for GCP architecture, migration plans, and cloud-themed content. Uses Google brand colors and Google Sans typography.

```css
:root {
  --gcloud-blue: #4285F4;
  --gcloud-green: #34A853;
  --gcloud-yellow: #FBBC05;
  --gcloud-red: #EA4335;
  --gcloud-grey-900: #202124;
  --gcloud-grey-700: #5F6368;
  --gcloud-grey-200: #E8EAED;
  --gcloud-grey-100: #F1F3F4;
}

.preset-gcloud {
  --color-bg: #ffffff;
  --color-surface: var(--gcloud-grey-100);
  --color-elevated: #ffffff;
  --color-text: var(--gcloud-grey-900);
  --color-text-secondary: var(--gcloud-grey-700);
  --color-muted: #9AA0A6;
  --color-border: var(--gcloud-grey-200);
  --color-accent: var(--gcloud-blue);
  --color-accent-light: #669DF6;
  --color-accent-muted: rgba(66, 133, 244, 0.15);
  --color-accent-bg: rgba(66, 133, 244, 0.06);
  --color-code-bg: var(--gcloud-grey-900);
  --color-code-fg: #E8EAED;
  --font-heading: 'Google Sans', Arial, sans-serif;
  --font-body: 'Google Sans', Arial, sans-serif;
  --font-mono: 'Google Sans Mono', 'Roboto Mono', monospace;
}
```

```html
<link href="https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Google+Sans+Mono:wght@400;500&display=swap" rel="stylesheet">
```

Four-color accent patterns:

```css
/* Hero card with four-color top border */
.preset-gcloud .ve-card--hero {
  border-top: 4px solid;
  border-image: linear-gradient(
    to right,
    var(--gcloud-blue) 25%,
    var(--gcloud-red) 25%,
    var(--gcloud-red) 50%,
    var(--gcloud-yellow) 50%,
    var(--gcloud-yellow) 75%,
    var(--gcloud-green) 75%
  ) 1;
}

/* Callout boxes with Google colors */
.preset-gcloud .ve-callout--info    { border-color: var(--gcloud-blue);   background: rgba(66, 133, 244, 0.08); color: var(--gcloud-blue); }
.preset-gcloud .ve-callout--success { border-color: var(--gcloud-green);  background: rgba(52, 168, 83, 0.08);  color: var(--gcloud-green); }
.preset-gcloud .ve-callout--warning { border-color: var(--gcloud-yellow); background: rgba(251, 188, 5, 0.08);  color: #E37400; }
.preset-gcloud .ve-callout--error   { border-color: var(--gcloud-red);    background: rgba(234, 67, 53, 0.08);  color: var(--gcloud-red); }
```
