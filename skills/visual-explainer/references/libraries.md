# CDN Libraries Reference

Library reference for self-contained HTML pages. All libraries are loaded via CDN so pages remain single-file and portable.

---

## Mermaid.js

### CDN URL

```html
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
```

### ELK Layout (for complex graphs)

```html
<script type="module">
  import elkLayouts from 'https://cdn.jsdelivr.net/npm/@mermaid-js/layout-elk@0.1.4/dist/mermaid-layout-elk.esm.min.mjs';
  mermaid.registerLayoutLoaders(elkLayouts);
</script>
```

### Initialization Pattern

```html
<script>
  mermaid.initialize({
    startOnLoad: true,
    theme: 'base',
    themeVariables: {
      primaryColor: '#6366f1',
      primaryTextColor: '#e2e4f0',
      primaryBorderColor: '#4f46e5',
      lineColor: '#585b70',
      secondaryColor: '#252540',
      tertiaryColor: '#1a1a2e',
      fontFamily: '"DM Sans", sans-serif',
      fontSize: '14px'
    },
    flowchart: {
      curve: 'basis',
      padding: 20,
      htmlLabels: true
    }
  });
</script>
```

### Custom CSS Overrides

```css
/* Node rectangles */
.mermaid .node rect {
  rx: 8;
  ry: 8;
  stroke-width: 1.5px;
}

/* Edge labels */
.mermaid .edgeLabel {
  background: var(--color-surface);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.8rem;
}

/* Edge paths */
.mermaid .flowchart-link {
  stroke: var(--color-muted);
  stroke-width: 1.5px;
}

/* Cluster backgrounds */
.mermaid .cluster rect {
  fill: var(--color-accent-bg);
  stroke: var(--color-accent-muted);
  rx: 12;
}
```

### Layout Direction Guidance

- **TD (top-down)**: Best for hierarchies, data flows, org charts. Default choice.
- **LR (left-right)**: Best for pipelines, timelines, sequence-like flows. Feels more like reading.

---

## Chart.js

### CDN URL

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
```

### Basic Bar Chart

```html
<canvas id="barChart" width="400" height="250"></canvas>
<script>
  new Chart(document.getElementById('barChart'), {
    type: 'bar',
    data: {
      labels: ['Q1', 'Q2', 'Q3', 'Q4'],
      datasets: [{
        label: 'Revenue',
        data: [120, 190, 170, 240],
        backgroundColor: 'rgba(99, 102, 241, 0.6)',
        borderColor: '#6366f1',
        borderWidth: 1,
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.06)' } },
        x: { grid: { display: false } }
      }
    }
  });
</script>
```

### Basic Line Chart

```html
<canvas id="lineChart" width="400" height="250"></canvas>
<script>
  new Chart(document.getElementById('lineChart'), {
    type: 'line',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      datasets: [{
        label: 'Users',
        data: [400, 450, 500, 620, 780, 950],
        borderColor: '#6366f1',
        backgroundColor: 'rgba(99, 102, 241, 0.1)',
        fill: true,
        tension: 0.4,
        pointRadius: 4,
        pointBackgroundColor: '#6366f1'
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } }
    }
  });
</script>
```

### Basic Pie / Doughnut Chart

```html
<canvas id="pieChart" width="300" height="300"></canvas>
<script>
  new Chart(document.getElementById('pieChart'), {
    type: 'doughnut',
    data: {
      labels: ['Frontend', 'Backend', 'Infra', 'Data'],
      datasets: [{
        data: [35, 30, 20, 15],
        backgroundColor: ['#6366f1', '#a78bfa', '#818cf8', '#c4b5fd'],
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      cutout: '55%',
      plugins: {
        legend: { position: 'bottom', labels: { padding: 16, usePointStyle: true } }
      }
    }
  });
</script>
```

### Custom Color Theming

Match Chart.js colors to the page palette by using CSS custom property values read via JS:

```javascript
const style = getComputedStyle(document.documentElement);
const accent = style.getPropertyValue('--color-accent').trim();
const muted = style.getPropertyValue('--color-muted').trim();
const border = style.getPropertyValue('--color-border').trim();
```

---

## anime.js

### CDN URL

```html
<script src="https://cdn.jsdelivr.net/npm/animejs@3/lib/anime.min.js"></script>
```

### Staggered Entrance Animation

```javascript
anime({
  targets: '.ve-card',
  opacity: [0, 1],
  translateY: [30, 0],
  duration: 600,
  easing: 'easeOutCubic',
  delay: anime.stagger(80)
});
```

### Timeline Animation for Sequenced Reveals

```javascript
const tl = anime.timeline({ easing: 'easeOutExpo' });

tl.add({
  targets: '.ve-header',
  opacity: [0, 1],
  translateY: [-20, 0],
  duration: 500
})
.add({
  targets: '.ve-kpi',
  opacity: [0, 1],
  scale: [0.9, 1],
  duration: 400,
  delay: anime.stagger(60)
}, '-=200')
.add({
  targets: '.ve-card',
  opacity: [0, 1],
  translateY: [20, 0],
  duration: 500,
  delay: anime.stagger(80)
}, '-=300');
```

---

## Google Fonts

### Link Pattern

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=FONT_NAME:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### Recommended Font Pairings

| Heading | Body/Code | CDN URL | Best For |
|---------|-----------|---------|----------|
| DM Sans | Fira Code | `family=DM+Sans:wght@400;500;700&family=Fira+Code:wght@400;500` | General purpose, clean |
| Instrument Serif | JetBrains Mono | `family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500` | Editorial, storytelling |
| IBM Plex Sans | IBM Plex Mono | `family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500` | Enterprise, technical |
| Bricolage Grotesque | Fragment Mono | `family=Bricolage+Grotesque:wght@400;600;700&family=Fragment+Mono` | Bold, modern |
| Plus Jakarta Sans | Azeret Mono | `family=Plus+Jakarta+Sans:wght@400;500;700&family=Azeret+Mono:wght@400;500` | Startup, product |
| Google Sans | Google Sans Mono | `family=Google+Sans:wght@400;500;700&family=Google+Sans+Mono:wght@400;500` | Google Cloud, GCP themes |

### Full CDN Link Example

```html
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
```

---

## Typography by Content Voice

### Technical Documentation

```css
body {
  font-family: 'DM Sans', 'IBM Plex Sans', system-ui, sans-serif;
  font-size: 0.95rem;
  line-height: 1.65;
}
code, pre {
  font-family: 'Fira Code', 'JetBrains Mono', monospace;
  font-size: 0.85em;
}
```

### Editorial / Narrative

```css
h1, h2, h3 {
  font-family: 'Instrument Serif', 'Georgia', serif;
  font-weight: 400;
  letter-spacing: -0.01em;
}
body {
  font-family: 'DM Sans', sans-serif;
  font-size: 1.05rem;
  line-height: 1.75;
}
```

### Data-Dense / Dashboard

```css
body {
  font-family: 'IBM Plex Sans', system-ui, sans-serif;
  font-size: 0.85rem;
  line-height: 1.45;
}
.ve-kpi-value {
  font-family: 'IBM Plex Mono', monospace;
  font-variant-numeric: tabular-nums;
  font-weight: 600;
  font-size: 2rem;
  letter-spacing: -0.02em;
}
```
