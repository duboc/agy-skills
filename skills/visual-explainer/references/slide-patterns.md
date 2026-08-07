# Slide Patterns Reference

Reference for generating self-contained HTML slide decks with CSS-driven layouts, transitions, and navigation.

---

## Slide Engine CSS

### Base Slide Container

```css
* { margin: 0; padding: 0; box-sizing: border-box; }

.ve-deck {
  width: 100vw;
  height: 100dvh;
  overflow: hidden;
  position: relative;
}

.ve-slide {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 4rem 6rem;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.5s ease, transform 0.5s ease;
}

.ve-slide.active {
  opacity: 1;
  visibility: visible;
}
```

### Slide Navigation Arrows

```css
.ve-nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 200;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: var(--color-text);
  width: 48px;
  height: 48px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s ease;
}

.ve-nav-btn:hover { background: rgba(255, 255, 255, 0.2); }
.ve-nav-prev { left: 1.5rem; }
.ve-nav-next { right: 1.5rem; }
```

### Progress Bar

```css
.ve-progress-bar {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 3px;
  background: var(--color-accent);
  transition: width 0.4s ease;
  z-index: 200;
}
```

### Slide Counter

```css
.ve-slide-counter {
  position: absolute;
  bottom: 1.25rem;
  right: 1.5rem;
  z-index: 200;
  font-size: 0.8rem;
  font-family: var(--font-mono);
  color: var(--color-muted);
  font-variant-numeric: tabular-nums;
}
```

---

## 10 Slide Types

### 1. Title Slide

```css
.ve-slide--title {
  text-align: center;
  gap: 1.5rem;
}

.ve-slide--title h1 {
  font-size: clamp(2.5rem, 5vw, 4.5rem);
  font-weight: 700;
  letter-spacing: -0.03em;
  line-height: 1.1;
}

.ve-slide--title .subtitle {
  font-size: clamp(1rem, 2vw, 1.35rem);
  color: var(--color-text-secondary);
  max-width: 40ch;
}
```

### 2. Section Divider

```css
.ve-slide--divider {
  text-align: center;
  gap: 1rem;
  background: var(--color-accent);
  color: #fff;
}

.ve-slide--divider h2 {
  font-size: clamp(2rem, 4vw, 3.5rem);
  font-weight: 700;
}

.ve-slide--divider p {
  font-size: 1.1rem;
  opacity: 0.85;
  max-width: 50ch;
}
```

### 3. Content Slide

```css
.ve-slide--content {
  align-items: flex-start;
  gap: 1.5rem;
}

.ve-slide--content h2 {
  font-size: 2rem;
  font-weight: 600;
}

.ve-slide--content p {
  font-size: 1.1rem;
  line-height: 1.7;
  max-width: 65ch;
  color: var(--color-text-secondary);
}

.ve-slide--content ul {
  list-style: none;
  padding: 0;
}

.ve-slide--content ul li {
  padding: 0.4rem 0;
  padding-left: 1.5rem;
  position: relative;
  font-size: 1.05rem;
}

.ve-slide--content ul li::before {
  content: '\2022';
  position: absolute;
  left: 0;
  color: var(--color-accent);
  font-weight: bold;
}
```

### 4. Split Slide

```css
.ve-slide--split {
  flex-direction: row;
  padding: 0;
}

.ve-slide--split .split-left,
.ve-slide--split .split-right {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 4rem;
  gap: 1rem;
}

.ve-slide--split .split-left {
  border-right: 1px solid var(--color-border);
}
```

### 5. Diagram Slide

```css
.ve-slide--diagram {
  padding: 2rem 3rem;
}

.ve-slide--diagram h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  align-self: flex-start;
}

.ve-slide--diagram .mermaid {
  width: 100%;
  max-height: 70dvh;
  overflow: auto;
}
```

### 6. Dashboard Slide

```css
.ve-slide--dashboard {
  gap: 2rem;
  padding: 3rem 4rem;
}

.ve-slide--dashboard .kpi-row {
  display: flex;
  gap: 1.5rem;
  width: 100%;
}

.ve-slide--dashboard .kpi-card {
  flex: 1;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 1.25rem;
  text-align: center;
}

.ve-slide--dashboard .kpi-value {
  font-size: 2.5rem;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  color: var(--color-accent);
}

.ve-slide--dashboard .kpi-label {
  font-size: 0.85rem;
  color: var(--color-muted);
  margin-top: 0.25rem;
}
```

### 7. Table Slide

```css
.ve-slide--table {
  padding: 3rem 4rem;
  align-items: flex-start;
}

.ve-slide--table table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
}

.ve-slide--table th {
  text-align: left;
  padding: 0.75rem 1rem;
  border-bottom: 2px solid var(--color-accent);
  font-weight: 600;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-muted);
}

.ve-slide--table td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--color-border);
}

.ve-slide--table tr:last-child td {
  border-bottom: none;
}
```

### 8. Code Slide

```css
.ve-slide--code {
  padding: 3rem 5rem;
  align-items: flex-start;
  gap: 1rem;
}

.ve-slide--code h2 {
  font-size: 1.5rem;
}

.ve-slide--code pre {
  width: 100%;
  max-height: 70dvh;
  overflow: auto;
  background: var(--color-code-bg);
  color: var(--color-code-fg);
  padding: 1.5rem 2rem;
  border-radius: 12px;
  font-family: var(--font-mono);
  font-size: 0.9rem;
  line-height: 1.6;
  white-space: pre-wrap;
}
```

### 9. Quote Slide

```css
.ve-slide--quote {
  text-align: center;
  gap: 2rem;
}

.ve-slide--quote blockquote {
  font-size: clamp(1.5rem, 3vw, 2.5rem);
  font-style: italic;
  line-height: 1.4;
  max-width: 50ch;
  color: var(--color-text);
  position: relative;
}

.ve-slide--quote blockquote::before {
  content: '\201C';
  font-size: 5rem;
  color: var(--color-accent);
  position: absolute;
  top: -2.5rem;
  left: -2rem;
  opacity: 0.3;
  font-style: normal;
}

.ve-slide--quote cite {
  font-style: normal;
  font-size: 1rem;
  color: var(--color-muted);
}
```

### 10. Full-Bleed Slide

```css
.ve-slide--bleed {
  padding: 0;
  position: relative;
}

.ve-slide--bleed .bleed-bg {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  filter: brightness(0.4);
}

.ve-slide--bleed .bleed-content {
  position: relative;
  z-index: 1;
  text-align: center;
  color: #fff;
  padding: 4rem;
}

.ve-slide--bleed .bleed-content h2 {
  font-size: clamp(2rem, 4vw, 3.5rem);
  font-weight: 700;
  text-shadow: 0 2px 20px rgba(0,0,0,0.5);
}
```

---

## Transitions

### Fade Transition

```css
.ve-slide {
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.5s ease;
}

.ve-slide.active {
  opacity: 1;
  visibility: visible;
}
```

### Slide Transition (Horizontal Movement)

```css
.ve-slide {
  opacity: 0;
  visibility: hidden;
  transform: translateX(60px);
  transition: opacity 0.5s ease, transform 0.5s ease;
}

.ve-slide.active {
  opacity: 1;
  visibility: visible;
  transform: translateX(0);
}

.ve-slide.prev {
  opacity: 0;
  transform: translateX(-60px);
}
```

### CSS-Only Transition Pattern

Combine with JS class toggling: apply `.active` to the current slide, `.prev` to the one being left, and default state for future slides.

---

## Navigation Chrome

### Arrow Buttons

```html
<button class="ve-nav-btn ve-nav-prev" onclick="changeSlide(-1)" aria-label="Previous slide">&#8592;</button>
<button class="ve-nav-btn ve-nav-next" onclick="changeSlide(1)" aria-label="Next slide">&#8594;</button>
<div class="ve-progress-bar" id="progress"></div>
<div class="ve-slide-counter" id="counter"></div>
```

### Keyboard Listeners

```javascript
document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight' || e.key === ' ') {
    e.preventDefault();
    changeSlide(1);
  }
  if (e.key === 'ArrowLeft') {
    e.preventDefault();
    changeSlide(-1);
  }
});
```

### Touch/Swipe Support

```javascript
let touchStartX = 0;
let touchEndX = 0;

document.addEventListener('touchstart', (e) => {
  touchStartX = e.changedTouches[0].screenX;
}, { passive: true });

document.addEventListener('touchend', (e) => {
  touchEndX = e.changedTouches[0].screenX;
  const diff = touchStartX - touchEndX;
  if (Math.abs(diff) > 50) {
    changeSlide(diff > 0 ? 1 : -1);
  }
}, { passive: true });
```

### Complete Navigation Controller

```javascript
let currentSlide = 0;
const slides = document.querySelectorAll('.ve-slide');
const totalSlides = slides.length;

function changeSlide(direction) {
  slides[currentSlide].classList.remove('active');
  slides[currentSlide].classList.add('prev');

  currentSlide = Math.max(0, Math.min(totalSlides - 1, currentSlide + direction));

  slides.forEach(s => s.classList.remove('prev'));
  slides[currentSlide].classList.add('active');

  // Update progress bar
  const progress = ((currentSlide + 1) / totalSlides) * 100;
  document.getElementById('progress').style.width = progress + '%';

  // Update counter
  document.getElementById('counter').textContent =
    (currentSlide + 1) + ' / ' + totalSlides;
}

// Initialize first slide
slides[0].classList.add('active');
document.getElementById('counter').textContent = '1 / ' + totalSlides;
document.getElementById('progress').style.width = (100 / totalSlides) + '%';
```

---

## 4 Curated Presets

### 1. Midnight Editorial

Dark navy background, serif headlines, gold accents.

```css
.preset-midnight {
  --color-bg: #0d1117;
  --color-surface: #161b22;
  --color-elevated: #1c2333;
  --color-text: #e6edf3;
  --color-text-secondary: #8b949e;
  --color-muted: #484f58;
  --color-border: #21262d;
  --color-accent: #d4a855;
  --color-accent-light: #e8c36e;
  --color-accent-muted: rgba(212, 168, 85, 0.2);
  --color-accent-bg: rgba(212, 168, 85, 0.06);
  --color-code-bg: #0a0e14;
  --color-code-fg: #e6edf3;
  --font-heading: 'Instrument Serif', Georgia, serif;
  --font-body: 'DM Sans', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
```

```html
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

### 2. Warm Signal

Cream background, terracotta accents, DM Sans.

```css
.preset-warm {
  --color-bg: #faf6f1;
  --color-surface: #ffffff;
  --color-elevated: #ffffff;
  --color-text: #2c1810;
  --color-text-secondary: #6b4c3b;
  --color-muted: #a08878;
  --color-border: #e8ddd3;
  --color-accent: #c45d35;
  --color-accent-light: #d97a58;
  --color-accent-muted: rgba(196, 93, 53, 0.15);
  --color-accent-bg: rgba(196, 93, 53, 0.05);
  --color-code-bg: #2c1810;
  --color-code-fg: #f0e6dc;
  --font-heading: 'Bricolage Grotesque', system-ui, sans-serif;
  --font-body: 'DM Sans', system-ui, sans-serif;
  --font-mono: 'Fragment Mono', monospace;
}
```

```html
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@400;600;700&family=DM+Sans:wght@400;500;700&family=Fragment+Mono&display=swap" rel="stylesheet">
```

### 3. Terminal Mono

Dark background, green and amber monospace aesthetic.

```css
.preset-terminal {
  --color-bg: #0c0c0c;
  --color-surface: #141414;
  --color-elevated: #1c1c1c;
  --color-text: #33ff33;
  --color-text-secondary: #88cc88;
  --color-muted: #446644;
  --color-border: #1e3a1e;
  --color-accent: #ffcc00;
  --color-accent-light: #ffdd44;
  --color-accent-muted: rgba(255, 204, 0, 0.15);
  --color-accent-bg: rgba(255, 204, 0, 0.05);
  --color-code-bg: #080808;
  --color-code-fg: #33ff33;
  --font-heading: 'JetBrains Mono', monospace;
  --font-body: 'JetBrains Mono', monospace;
  --font-mono: 'JetBrains Mono', monospace;
}
```

```html
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
```

Additional terminal styling:

```css
.preset-terminal h1,
.preset-terminal h2,
.preset-terminal h3 {
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.preset-terminal .ve-slide--title h1::before {
  content: '> ';
  color: var(--color-accent);
}
```

### 4. Swiss Clean

White background, geometric precision, minimal color.

```css
.preset-swiss {
  --color-bg: #ffffff;
  --color-surface: #f5f5f5;
  --color-elevated: #ffffff;
  --color-text: #111111;
  --color-text-secondary: #555555;
  --color-muted: #999999;
  --color-border: #e0e0e0;
  --color-accent: #e63228;
  --color-accent-light: #ff4d42;
  --color-accent-muted: rgba(230, 50, 40, 0.12);
  --color-accent-bg: rgba(230, 50, 40, 0.04);
  --color-code-bg: #1a1a1a;
  --color-code-fg: #f0f0f0;
  --font-heading: 'Plus Jakarta Sans', system-ui, sans-serif;
  --font-body: 'Plus Jakarta Sans', system-ui, sans-serif;
  --font-mono: 'Azeret Mono', monospace;
}
```

```html
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;700;800&family=Azeret+Mono:wght@400;500&display=swap" rel="stylesheet">
```

Additional Swiss styling:

```css
.preset-swiss h1,
.preset-swiss h2 {
  font-weight: 800;
  letter-spacing: -0.03em;
}

.preset-swiss .ve-slide--divider {
  background: var(--color-accent);
}

.preset-swiss .ve-card {
  border-radius: 0;
  border: 2px solid var(--color-text);
}
```

### 5. Google Cloud

White background, Google Sans typography, Google brand four-color accents. Use this preset for Google Cloud-themed presentations, migration plans, and GCP architecture diagrams.

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

Additional Google Cloud styling:

```css
/* Title styling */
.preset-gcloud h1 {
  font-size: 36pt;
  font-weight: 700;
  color: var(--gcloud-grey-900);
}

.preset-gcloud h2 {
  font-size: 24pt;
  font-weight: 700;
  color: var(--gcloud-blue);
}

/* Section divider uses Google Blue */
.preset-gcloud .ve-slide--divider {
  background: var(--gcloud-blue);
  color: #ffffff;
}

/* Cards with subtle rounded corners */
.preset-gcloud .ve-card {
  border-radius: 8px;
  border: 1px solid var(--gcloud-grey-200);
  background: #ffffff;
}

/* Bullet points in Google Blue */
.preset-gcloud ul {
  list-style: none;
  padding-left: 20px;
}
.preset-gcloud li::before {
  content: "\2022";
  color: var(--gcloud-blue);
  font-weight: bold;
  display: inline-block;
  width: 1em;
  margin-left: -1em;
}

/* Four-color accent bar for hero cards */
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

/* KPI cards with Google colors */
.preset-gcloud .kpi-card:nth-child(1) .kpi-value { color: var(--gcloud-blue); }
.preset-gcloud .kpi-card:nth-child(2) .kpi-value { color: var(--gcloud-red); }
.preset-gcloud .kpi-card:nth-child(3) .kpi-value { color: var(--gcloud-yellow); }
.preset-gcloud .kpi-card:nth-child(4) .kpi-value { color: var(--gcloud-green); }

/* Footer styling */
.preset-gcloud .slide-footer {
  font-size: 10pt;
  color: var(--gcloud-grey-700);
}

/* Status badges using Google colors */
.preset-gcloud .ve-badge--green::before  { background: var(--gcloud-green); }
.preset-gcloud .ve-badge--red::before    { background: var(--gcloud-red); }
.preset-gcloud .ve-badge--amber::before  { background: var(--gcloud-yellow); }
.preset-gcloud .ve-badge--muted::before  { background: #9AA0A6; }

/* Table header accent */
.preset-gcloud th {
  border-bottom: 2px solid var(--gcloud-blue);
  color: var(--gcloud-grey-700);
}

/* Progress bar in Google Blue */
.preset-gcloud .ve-progress-fill {
  background: linear-gradient(90deg, var(--gcloud-blue), var(--gcloud-green));
}
```

Mermaid theming for Google Cloud:

```javascript
mermaid.initialize({
  startOnLoad: true,
  theme: 'base',
  themeVariables: {
    primaryColor: '#E8F0FE',
    primaryTextColor: '#202124',
    primaryBorderColor: '#4285F4',
    lineColor: '#5F6368',
    secondaryColor: '#E6F4EA',
    tertiaryColor: '#FEF7E0',
    fontFamily: '"Google Sans", Arial, sans-serif',
    fontSize: '14px'
  }
});
```
