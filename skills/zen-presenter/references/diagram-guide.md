# Diagram Guide for Zen Presenter (Inline SVG & Google Cloud HTML)

Diagrams in Presentation Zen decks must follow **restraint (Kanso)**, **naturalness (Shizen)**, and **emptiness (Ma)** — communicating a single clear relationship per slide using inline `<svg>` inside the self-contained HTML presentation.

## Why Inline SVG in Pure HTML

Because `zen-presenter` generates pure self-contained HTML directly (without Marp), diagrams are embedded as native `<svg viewBox="0 0 800 320">` elements inside `<section class="slide">`:
- Zero external image links that can break offline.
- Crisp vector scaling at any projector resolution and in PDF exports.
- Direct use of Google Cloud palette variables (`#4285F4`, `#EA4335`, `#FBBC05`, `#34A853`, `#202124`, `#5F6368`).

## Zen Diagram Style Rules

| Principle | Rule |
| :--- | :--- |
| **Restraint** | Maximum 3–4 nodes per diagram. If a flow has more stages, split it across slides. |
| **One Idea** | Show a single mechanism, bottleneck, or before/after contrast — never a 15-box system map. |
| **Minimal Labels** | Node labels: 1–3 words maximum (`18px–22px` `Roboto` / `Google Sans`). |
| **Google Cloud Palette** | Use `#4285F4` (Google Blue) for the active/solution node, `#202124` for standard nodes, and `#EA4335` for bottleneck/failure nodes. |

## Example: 3-Node Google Cloud Inline SVG Flow

```html
<section class="slide">
  <h2>A signed GET cookie isolates each attendee behind shared Wi-Fi NAT</h2>
  <svg viewBox="0 0 860 240" width="100%" height="240" role="img" aria-label="Three-stage request flow">
    <defs>
      <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 8 5 L 0 9 z" fill="#5F6368"/>
      </marker>
    </defs>
    <!-- Node 1 -->
    <rect x="20" y="60" width="220" height="110" rx="12" fill="#F8F9FA" stroke="#DADCE0" stroke-width="2"/>
    <text x="130" y="110" text-anchor="middle" font-family="Roboto, Arial, sans-serif" font-size="20" font-weight="600" fill="#202124">300 Attendees</text>
    <text x="130" y="138" text-anchor="middle" font-family="Roboto, Arial, sans-serif" font-size="15" fill="#5F6368">1 Shared CGNAT IP</text>

    <line x1="240" y1="115" x2="310" y2="115" stroke="#5F6368" stroke-width="3" marker-end="url(#arrow)"/>

    <!-- Node 2 (Google Blue Highlight) -->
    <rect x="320" y="60" width="220" height="110" rx="12" fill="#E8F0FE" stroke="#4285F4" stroke-width="3"/>
    <text x="430" y="110" text-anchor="middle" font-family="Roboto, Arial, sans-serif" font-size="20" font-weight="600" fill="#1967D2">Signed GET Cookie</text>
    <text x="430" y="138" text-anchor="middle" font-family="Roboto, Arial, sans-serif" font-size="15" fill="#1967D2">Per-Device Session</text>

    <line x1="540" y1="115" x2="610" y2="115" stroke="#5F6368" stroke-width="3" marker-end="url(#arrow)"/>

    <!-- Node 3 (Google Green Outcome) -->
    <rect x="620" y="60" width="220" height="110" rx="12" fill="#E6F4EA" stroke="#34A853" stroke-width="2"/>
    <text x="730" y="110" text-anchor="middle" font-family="Roboto, Arial, sans-serif" font-size="20" font-weight="600" fill="#137333">Zero Lockouts</text>
    <text x="730" y="138" text-anchor="middle" font-family="Roboto, Arial, sans-serif" font-size="15" fill="#137333">Isolated Quotas</text>
  </svg>
  <aside class="notes">
    Point to the middle box: the GET page load mints an HMAC-signed device token before the user submits the form, so rate limiting happens per device rather than per venue IP.
  </aside>
</section>
```
