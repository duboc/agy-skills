# Layout cookbook

Twelve layouts, all in `scripts/deck_kit.js`, all QA-tested at 13.3" × 7.5" (`LAYOUT_WIDE`).

Compose from these instead of inventing layouts. Every one of them survived a render-and-inspect pass, which means the padding, contrast, and margins are already right — the failures that eat time on a fresh deck are exactly those.

## Contents

- [Setup](#setup)
- [Choosing a layout](#choosing-a-layout)
- [The layouts](#the-layouts)
- [Composition rules](#composition-rules)
- [Palette anatomy](#palette-anatomy)
- [Extending the kit](#extending-the-kit)

---

## Setup

```javascript
const pptxgen = require("pptxgenjs");
const kit = require("./deck_kit");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";        // must come before any addSlide

const K = kit.init(pres, kit.palettes.googleCloud);

K.cover({ title: "...", subtitle: "...", signature: "...", notes: "..." });
// ... more slides ...

pres.writeFile({ fileName: "/home/claude/deck/out.pptx" }).then(() => console.log("ok"));
```

Available palettes: `googleCloud`, `midnight`, `forest`, `charcoal`. To use brand colors, pass a palette object with the same keys — see [Palette anatomy](#palette-anatomy).

Every layout function accepts `notes` and returns the slide, so you can add one-off elements:

```javascript
const s = K.stat({ value: "80%", meaning: "...", notes: "..." });
s.addText("source: internal analysis", { x: 0.8, y: 6.8, w: 6, h: 0.3,
  fontFace: "Arial", fontSize: 10, color: K.P.faint, margin: 0 });
```

---

## Choosing a layout

| The slide needs to... | Use |
|---|---|
| Open the deck | `cover` |
| Turn the deck from tension to resolution | `pivot` |
| Land one number hard | `stat` |
| Show a problem compounding | `escalation` |
| Name three or four distinct costs, risks, or benefits | `cards` |
| Introduce three named things (products, models, roles) | `columns` |
| Walk an ordered process | `flow` |
| Pair one claim with a detailed list | `split` |
| Contrast old way with new way | `versus` |
| Show a technology stack or layered architecture | `stack` |
| Quantify before-and-after across criteria | `ledger` |
| Show events across time | `timeline` |
| Close the deck | `pivot` (with the closing statement) |

---

## The layouts

### `cover(o)` — dark
`{ title, subtitle?, signature?, size?, notes? }`
Motif above the title. Keep the title to three or four words; the subtitle carries the promise.

### `pivot(o)` — dark
`{ text, signature?, size?, notes? }`
One sentence, nothing else. Use for the mid-deck turn and again for the close. Write a note telling the presenter to pause.

### `stat(o)` — light
`{ value, meaning, support?, color?, valueSize?, donut?, eyebrow?, notes? }`
Hero number at 128pt on the left. Optional `donut: { labels: [...], values: [...] }` renders a native doughnut on the right — good when the number is a proportion.
The single highest-impact slide in a tension act. Only one number.

### `escalation(o)` — light
`{ statement, steps: [{ value, label, color? }], footnote?, eyebrow?, notes? }`
Three to five tinted boxes with arrows between. Values should grow: `1 → 3 → 18 → 400+`. Shows a problem multiplying better than any sentence.

### `cards(o)` — light
`{ statement, cards: [{ title, body, color? }], eyebrow?, notes? }`
Two to four tinted cards, each with an accent dot. Card height auto-fits the statement above it. Keep bodies to two or three lines — cards are for naming things, not explaining them.

### `columns(o)` — light
`{ statement, columns: [{ title, label?, body, color? }], eyebrow?, notes? }`
Like `cards` but unboxed and airier. `label` renders as a small colored role line under the name ("Understands", "Generates video"). Best for introducing named products or actors.

### `flow(o)` — light
`{ statement, steps: [{ title, body, color? }], eyebrow?, notes? }`
Auto-numbers `01`, `02`, `03`. Three to five steps. Use only when order genuinely matters — a `flow` on an unordered set reads as a false sequence.

### `split(o)` — light
`{ statement, body?, kicker?, kickerColor?, panel: [{ title, sub?, color? }], eyebrow?, notes? }`
Statement and prose left, dark panel right. The panel holds up to seven items and auto-sizes. `kicker` is the italic bolded line that lands the point. The densest layout in the kit — use it once, maybe twice, per deck.

### `versus(o)` — light
`{ statement, left: { title, items, color? }, right: { title, items, color? }, eyebrow?, notes? }`
Two lists, up to five items each. Items are short phrases, not sentences. Red for the old way, green for the new is the obvious mapping and it reads instantly.

### `stack(o)` — light
`{ statement, rows: [{ label, items, color? }], footnote?, eyebrow?, notes? }`
Up to four rows, three chips each. The default for architecture and technology stacks. `footnote` is a good place for the one design decision worth calling out.

### `ledger(o)` — light
`{ statement, beforeLabel, afterLabel, rows: [{ criterion, before, after }], eyebrow?, notes? }`
Up to four rows. Put the row that matters most to the decision-maker last — it is the one they read as the conclusion.

### `timeline(o)` — light
`{ statement, points: [string], footnote?, eyebrow?, notes? }`
Five to eight points. Labels are short; anything over about 14 characters starts crowding its neighbors.

---

## Composition rules

**Vary layouts.** A deck that alternates `cards` and `columns` for eight slides is a deck nobody remembers. Aim to use no layout more than twice, `split` and `stat` no more than once or twice.

**Reserve dark for three slides.** Cover, pivot, close. Dark used for content destroys the pivot's contrast, which is the entire reason the pivot works.

**The eyebrow is a section marker, not a title.** Two or three words, uppercase, colored. It orients the audience without spending the slide statement on navigation. Every content slide should have one; they also serve as your own check that each slide has a distinct job.

**Rotate accent colors across slides** so consecutive slides do not share an eyebrow color. The kit indexes accents automatically inside a slide, but slide-to-slide rotation is yours to manage.

**Statement lengths cluster.** If most statements are two lines, a one-line statement reads as an emphasis beat. Use that deliberately for the slides that matter most.

---

## Palette anatomy

```javascript
{
  accents: ["4285F4", "EA4335", "FBBC04", "34A853"],       // on dark backgrounds
  accentsOnLight: ["4285F4", "EA4335", "F9AB00", "34A853"], // on white — darken light hues
  dark: "202124",        // dark slide background
  ink: "202124",         // primary text on light
  muted: "5F6368",       // secondary text on light
  faint: "80868B",       // signatures, footers
  surface: "F1F3F4",     // card and chip fill
  rule: "DADCE0",        // hairlines, arrows
  onDark: "FFFFFF",      // primary text on dark
  onDarkMuted: "9AA0A6", // secondary text on dark
  bg: "FFFFFF",          // light slide background
}
```

**Why two accent arrays.** A brand yellow like `FBBC04` reads fine as a filled shape but is nearly unreadable as text on white. `accentsOnLight` swaps in a darker variant (`F9AB00`) used wherever an accent becomes type. When building a custom palette, check every accent against white and darken the light ones — this single issue accounts for most contrast failures in QA.

**Building from a brand.** Take the brand's primary as `accents[0]`, pick two or three supporting hues, derive `surface` as a very light neutral tint of the primary, and keep `ink` near-black rather than using the brand color for body text. Brand colors as body text look amateur and fail contrast.

---

## Extending the kit

Write one-off layouts directly in the build script rather than editing `deck_kit.js` — the kit should stay stable across decks. Only promote a layout into the kit after using it in two different decks.

When writing custom slides, the `pptxgenjs` footguns that matter most (full list in `/mnt/skills/public/pptx/SKILL.md`):

- Hex colors never carry `#` and never carry alpha — `"FF0000"`, not `"#FF0000"`.
- Use `line: { type: "none" }` to remove outlines. `line: { width: 0 }` still renders a hairline in LibreOffice, which is what your QA sees.
- Never share an options object between two `add*` calls — pptxgenjs mutates it in place.
- `rectRadius` works on `roundRect` only.
- Gradient fills are unsupported; use a background image if you need one.
- Text boxes carry internal padding — set `margin: 0` whenever text must align to a shape at the same x.
- Speaker notes go through `addNotes()`, never a text box.
