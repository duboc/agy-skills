# PptxGenJS Native Element Schemas & Conversion Checklist

Use these schemas and diagnostic checks when converting extracted HTML slide JSON into native PowerPoint shapes, rich text runs, tables, and vector/raster media with `scripts/build_pptx.js`.

---

## 1. Extracted Slide JSON Schema

`scripts/extract.js` produces an array of slide descriptors with the following contract:

```json
[
  {
    "slideIndex": 0,
    "background": {
      "color": "0F172A",
      "image": null
    },
    "elements": [
      {
        "type": "heading",
        "tag": "h1",
        "text": "Cloud Architecture Overview",
        "x": 0.75,
        "y": 0.65,
        "w": 8.5,
        "h": 0.85,
        "style": {
          "fontSize": 32,
          "fontFace": "Arial",
          "color": "F8FAFC",
          "bold": true,
          "align": "left"
        }
      }
    ]
  }
]
```

---

## 2. Native PowerPoint Element Mapping

| HTML DOM Node | `PptxGenJS` API | Key Options |
|---------------|-----------------|-------------|
| `<h1>` – `<h6>`, `<p>` | `slide.addText(runs, opts)` | `x, y, w, h, fontSize, fontFace, color, bold, valign: "top", margin: 0` |
| `<ul>`, `<ol>` | `slide.addText(bulletItems, opts)` | Each item `{ text, options: { bullet: true, indentLevel } }` |
| `<table>` | `slide.addTable(rows, opts)` | Native cells `{ text, options: { fill, color, bold, border } }` |
| `<pre><code>` | `slide.addText(code, opts)` | `fill: { color: "1E293B" }, fontFace: "Consolas", fontSize: 10, margin: 8` |
| `<div class="card">` | `slide.addShape(pres.ShapeType.roundRect, opts)` | `rectRadius: 0.08, fill: { color, transparency }, line: { color, width }` |
| `<img>`, `<svg>` | `slide.addImage(opts)` | `path` or `data` (`base64`), `sizing: { type: "contain", w, h }` |

---

## 3. Verification & Quality Audit Checklist

Before delivering the `.pptx` artifact, verify:

- [ ] **Slide Count Parity**: Number of slides in `.pptx` matches the `<section>` count in the HTML deck.
- [ ] **Native Editability**: Every heading, paragraph, bullet list, code block, and table is selectable and editable as native text in PowerPoint/Keynote/Google Slides (never flattened into a full-slide screenshot).
- [ ] **Contrast & Background Fidelity**: Dark-mode slides retain their dark background fill (`slide.background = { color: ... }`) so white/light text remains readable.
- [ ] **Zero Overlapping Bounding Boxes**: Container card shapes (`roundRect`) are added to the slide **before** foreground text nodes so z-order layering matches the DOM stacking context.
- [ ] **Isolated Temp Directory Cleanup**: Intermediate JSON and rasterized SVG buffers are stored inside a `0700` temporary directory (`mktemp -d`) and cleaned up via `trap 'rm -rf "$TMP_DIR"' EXIT`.
