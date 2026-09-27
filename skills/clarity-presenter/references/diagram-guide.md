# Diagram Guide for Clarity Presenter (Inline SVG & Google Cloud HTML)

How to include diagrams as visual evidence in SCQA assertion-evidence HTML presentations. Diagrams support assertion headlines (`<h2>`) — they are the evidence, not decoration.

## Diagrams as Evidence in Dual-Perspective Decks

| Slide Type | HTML Container | Diagram Role |
| :--- | :--- | :--- |
| **Technical** (white) | `<section class="slide">` | Architecture, data flow, request sequence — proves *how* the mechanism works |
| **Business** (dark) | `<section class="slide invert">` | Process flow, incident cost reduction, rollout timeline — proves *why it matters* |

## Embedding Inline SVG in Pure HTML

Because `clarity-presenter` outputs self-contained HTML directly without Marp, embed diagrams as inline `<svg>` elements inside `<section class="slide">`:

### Technical Slide Example (White Background)

```html
<section class="slide">
  <h2>Active-active replication eliminates cold-start regional failover delays</h2>
  <svg viewBox="0 0 860 240" width="100%" height="240" role="img" aria-label="Active-active regional replication">
    <defs>
      <marker id="arrow-tech" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 8 5 L 0 9 z" fill="#4285F4"/>
      </marker>
    </defs>
    <rect x="30" y="65" width="220" height="100" rx="10" fill="#E8F0FE" stroke="#4285F4" stroke-width="2"/>
    <text x="140" y="110" text-anchor="middle" font-family="Roboto, Arial, sans-serif" font-size="18" font-weight="600" fill="#1967D2">Global Load Balancer</text>
    <text x="140" y="136" text-anchor="middle" font-family="Roboto, Arial, sans-serif" font-size="14" fill="#5F6368">Anycast Health Routing</text>

    <line x1="250" y1="95" x2="350" y2="65" stroke="#4285F4" stroke-width="2.5" marker-end="url(#arrow-tech)"/>
    <line x1="250" y1="135" x2="350" y2="165" stroke="#4285F4" stroke-width="2.5" marker-end="url(#arrow-tech)"/>

    <rect x="360" y="20" width="220" height="80" rx="10" fill="#F8F9FA" stroke="#34A853" stroke-width="2"/>
    <text x="470" y="65" text-anchor="middle" font-family="Roboto, Arial, sans-serif" font-size="17" font-weight="600" fill="#137333">us-central1 (Active)</text>

    <rect x="360" y="130" width="220" height="80" rx="10" fill="#F8F9FA" stroke="#34A853" stroke-width="2"/>
    <text x="470" y="175" text-anchor="middle" font-family="Roboto, Arial, sans-serif" font-size="17" font-weight="600" fill="#137333">southamerica-east1 (Active)</text>
  </svg>
  <p><em>Pre-warmed connection pools in both regions keep P99 failover under 50ms.</em></p>
  <aside class="notes">
    Emphasize that both regions serve live traffic continuously, avoiding cold-start connection pool exhaustion during failover.
  </aside>
</section>
```

### Business Slide Example (Dark `invert` Background)

```html
<section class="slide invert">
  <h2>Sub-50ms automatic failover reduces incident revenue exposure by 90%</h2>
  <svg viewBox="0 0 860 220" width="100%" height="220" role="img" aria-label="Incident cost comparison">
    <rect x="40" y="30" width="350" height="150" rx="12" fill="#2D2E31" stroke="#EA4335" stroke-width="2"/>
    <text x="215" y="75" text-anchor="middle" font-family="Roboto, Arial, sans-serif" font-size="18" font-weight="600" fill="#F28B82">Before: Manual Failover</text>
    <text x="215" y="115" text-anchor="middle" font-family="Roboto, Arial, sans-serif" font-size="28" font-weight="700" fill="#FFFFFF">$180K / incident</text>
    <text x="215" y="148" text-anchor="middle" font-family="Roboto, Arial, sans-serif" font-size="14" fill="#9AA0A6">4–8 min operator response window</text>

    <rect x="470" y="30" width="350" height="150" rx="12" fill="#1E3A2F" stroke="#34A853" stroke-width="2"/>
    <text x="645" y="75" text-anchor="middle" font-family="Roboto, Arial, sans-serif" font-size="18" font-weight="600" fill="#81C995">After: Active-Active Routing</text>
    <text x="645" y="115" text-anchor="middle" font-family="Roboto, Arial, sans-serif" font-size="28" font-weight="700" fill="#FFFFFF">$12K / month</text>
    <text x="645" y="148" text-anchor="middle" font-family="Roboto, Arial, sans-serif" font-size="14" fill="#E8EAED">Zero manual intervention required</text>
  </svg>
  <aside class="notes">
    Compare the single-incident loss ($180K) against the predictable monthly active-active footprint ($12K/month).
  </aside>
</section>
```

## Clarity Diagram Rules

| Principle | Rule |
| :--- | :--- |
| **Evidence, not decoration** | Every diagram must directly prove the slide's `<h2>` assertion headline. |
| **Readable at projection scale** | Maximum 6–8 nodes per slide; font size `>= 14px`. |
| **Technical vs. Business** | Technical diagrams show system topology/protocol flow; business diagrams show SLA, cost, or timeline impact. |
