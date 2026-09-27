# Domain Research, Requirements Spine & Narrative Arcs

Use this workflow whenever a presentation must persuade, pitch a solution, win an executive decision, or synthesize domain research into a Presentation Zen narrative.

## 1. Layered Domain Research (4 Layers)

A summary answers *"what is true about this space."* A persuasive deck needs **the specific number or concrete mechanism that makes the audience recognize their own reality.**

Search in four narrowing layers:

1. **Layer 1 — Domain Vocabulary**: Establish practitioner terminology and system boundaries.
2. **Layer 2 — Specific Friction**: Search the concrete bottleneck (e.g., `"CGNAT Wi-Fi rate limit lockout"` rather than `"API rate limiting"`).
3. **Layer 3 — Quantification**: Locate benchmark studies, incident metrics, latency numbers, or cost breakdowns. Every hero metric must be **specific**, **recognizable**, and **sourced or explicitly labeled as an order-of-magnitude estimate**.
4. **Layer 4 — What Changed Now**: Identify the architectural, platform, or economic shift that makes the problem solvable today.

### Recency & Contested Facts
- Verify current platform limits, quotas, pricing tiers, and SDK versions against primary documentation.
- When sources disagree, note the range in `<aside class="notes">` so the presenter can pre-empt objections in the room.

---

## 2. Requirements Spine (`Challenge -> Evidence -> Resolution`)

Before writing slide HTML, map research findings into a **Requirements Spine** table. The spine can also be exported as an HTML `<table>` and converted via LibreOffice Calc (`--platform sheets`) to Google Sheets:

| ID | Challenge Element | Quantitative / Qualitative Evidence | What Resolves It | Slide-Worthy? |
| :--- | :--- | :--- | :--- | :--- |
| `R1` | Venue Wi-Fi NAT shares 1 IP across 300 attendees | Flat `5 req/10m` IP limit locks out 98% of legitimate users | 4D limiter with `GET`-minted signed device cookie | **Yes (Slide 3–4)** |
| `R2` | Unhandled exception logs print full request URLs | `?key=AIza...` leaked in child logger stack traces | `setLogRecordFactory` global log redaction | **Yes (Slide 6)** |
| `R3` | Minor CSS spacing jitter on legacy browsers | Low severity, no functional impact | Standardize flexbox gap tokens | No (Speaker notes) |

- **Filter ruthlessly**: Promote only 30–40% of the spine to slides; keep supporting details in `<aside class="notes">`.
- **Keep the argument honest**: If a challenge row has no resolution, surface it explicitly as a known scope boundary rather than hiding it.

---

## 3. Three-Act Narrative Spine & Arc Catalog

Every persuasive Zen deck follows a three-act proportion:
- **Act I — Tension (~40% of slides)**: Establish the problem in the audience's terms and land the defining metric.
- **Act II — Pivot (1 dark/blue slide)**: A single `<section class="slide invert lead">` or `<section class="slide section lead">` containing one question or reversal statement and nothing else.
- **Act III — Resolution (~55% of slides)**: Show the mechanism that resolves the tension, quantify the delta, and return to the opening metric on the closing slide.

### Six Proven Narrative Arcs

| Arc | When to Use | Sequence |
| :--- | :--- | :--- |
| **1. Problem / Solution** | Audience feels the pain but hasn't sized it | Context → Multiplication of pain → Hero number → Cost → **Pivot** → What changed → Mechanism → Delta → Close |
| **2. Before / After / Bridge** | Migrations, architecture modernization, transformations | Current state → Concrete desired state → **Pivot: what stands between** → Bridge architecture → First step |
| **3. Contrarian Reversal** | Audience holds a conventional belief blocking progress | Conventional wisdom X → Why X made sense → What changed → **Pivot: X is now the expensive choice** → Replacement |
| **4. Escalating Stakes** | Security, technical debt, reliability, compliance | Small symptom → Scale multiplication → Unmitigated blast radius → **Pivot** → Intervention point → ROI |
| **5. Origin Story** | Post-mortems, field lessons, architecture retrospectives | Specific incident moment → Root cause → Why it happens broadly → **Pivot** → What we built → General principle |
| **6. Steelman Comparison** | Architecture trade-offs and executive decision readouts | Decision at hand → Shared evaluation criteria → Option A → Option B → **Pivot: what criteria reward** → Recommendation |

---

## 4. Interactive Narrative Gate & Speaker Notes

Before generating the full HTML deck for a persuasive pitch, present the **one-line-per-slide claim outline** for user sign-off:

```text
1. [title]   Edge Resilience at Live Events — Zero Lockouts Under Venue CGNAT
2. [default] Three hundred attendees share a single public IPv4 address on venue Wi-Fi.
3. [stats]   98% — Legitimate check-ins blocked after the 5th user by flat IP rate limits.
4. [invert]  What if rate limiting identified the device before the POST ever fired?
5. [default] A signed GET session cookie isolates each attendee behind shared NAT.
6. [closing] 98% blocked becomes 100% isolated — deploy the 4D edge limiter before game day.
```

### Speaker Notes (`<aside class="notes">`)
Because Zen slides are intentionally sparse, every `<section class="slide">` must include an `<aside class="notes">` block containing:
- **The point** of the slide in one sentence.
- **Delivery pacing** (where to pause, which number to emphasize).
- **Evidence & caveats** (source citation, denominator, and how to answer likely challenges).
