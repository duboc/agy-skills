# HTML/Marp to PowerPoint Coordinate & Typography Mapping Guide

This reference details the geometric and typographic conversion math used when extracting DOM bounding boxes (`getBoundingClientRect()`) from a 16:9 HTML/Marp viewport (`1280×720` px) and rendering native PowerPoint objects via `PptxGenJS` (`10×5.625` inches).

---

## 1. Coordinate Conversion Formulas (`px` → `inches`)

Standard 16:9 widescreen PowerPoint layout (`LAYOUT_16x9`) measures `10.0` inches wide by `5.625` inches high.

| Dimension | HTML Viewport (`px`) | PowerPoint (`in`) | Conversion Formula |
|-----------|----------------------|-------------------|--------------------|
| Slide Width | `1280 px` | `10.0 in` | `x_in = (rect.left / slideRect.width) * 10.0` |
| Slide Height | `720 px` | `5.625 in` | `y_in = (rect.top / slideRect.height) * 5.625` |
| Element Width | `rect.width` | `w_in` | `w_in = (rect.width / slideRect.width) * 10.0` |
| Element Height | `rect.height` | `h_in` | `h_in = (rect.height / slideRect.height) * 5.625` |

### Anti-Truncation Width & Margin Buffer

Browser text rendering uses sub-pixel kerning that differs slightly from PowerPoint's GDI/DirectWrite layout engine. To prevent single-line headings or badges from wrapping prematurely in PowerPoint:

1. **Horizontal Width Buffer**: Add a `+4%` width allowance (`w_in = Math.min(10 - x_in, raw_w_in * 1.04)`) on headings (`h1`, `h2`, `h3`) and pill badges.
2. **Zero Internal Text Box Margin**: Set `margin: 0` (or `[2, 4, 2, 4]` points for padded cards) on `slide.addText()` calls so PowerPoint's default `0.1 in` internal margin does not shrink the usable text width.

---

## 2. CSS Font Size (`px`) to PowerPoint Point (`pt`) Scaling

When rendered at `1280×720` (`96 DPI`), CSS pixel sizes must scale proportionally to the `10 in` (`720 pt`) slide width:

```javascript
// 1 inch = 72 points; 10 inches = 720 points across 1280 CSS pixels
// Scale factor = 720 / 1280 = 0.5625
const fontSizePt = Math.round(cssFontSizePx * 0.5625 * 10) / 10;
```

| HTML / Marp Element | Typical CSS Size (`1280px`) | Converted PowerPoint Size (`pt`) | Recommended Weight |
|---------------------|-----------------------------|----------------------------------|--------------------|
| Hero Title (`h1`) | `56 px – 64 px` | `31.5 pt – 36 pt` | Bold (`true`) |
| Slide Title (`h2`) | `40 px – 48 px` | `22.5 pt – 27 pt` | Bold (`true`) |
| Section Header (`h3`)| `28 px – 32 px` | `16 pt – 18 pt` | Semi-Bold / Bold |
| Body Copy (`p`, `li`)| `22 px – 26 px` | `12.5 pt – 14.5 pt` | Regular (`false`) |
| Code Block (`pre`) | `16 px – 20 px` | `9 pt – 11.5 pt` | Monospace (`Consolas` / `Courier New`) |
| Caption / Footer | `14 px – 16 px` | `8 pt – 9 pt` | Regular (`#64748B`) |

---

## 3. Font Family Normalization Matrix

PowerPoint only renders fonts installed on the target OS or embedded in the deck. Map web fonts to cross-platform system-safe equivalents when generating `.pptx`:

| CSS Computed `font-family` | Cross-Platform PowerPoint Font | Fallback |
|----------------------------|--------------------------------|----------|
| `Inter`, `Roboto`, `system-ui`, `-apple-system` | `Arial` or `Calibri` | `Helvetica` |
| `Outfit`, `Plus Jakarta Sans`, `Montserrat` | `Trebuchet MS` or `Arial` | `Calibri` |
| `Georgia`, `Merriweather`, `Playfair Display` | `Georgia` | `Times New Roman` |
| `JetBrains Mono`, `Fira Code`, `monospace` | `Consolas` | `Courier New` |

---

## 4. Color & Alpha Conversion Rules

`PptxGenJS` requires 6-character uppercase hexadecimal RGB strings **without** a leading `#` (`"1E293B"`, not `"#1e293b"` or `"rgb(30, 41, 59)"`).

```javascript
function rgbToHex(rgbStr) {
  const match = rgbStr.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)/);
  if (!match) return { hex: "000000", transparency: 0 };
  const [, r, g, b, a] = match;
  const hex = [r, g, b]
    .map((v) => parseInt(v, 10).toString(16).padStart(2, "0"))
    .join("")
    .toUpperCase();
  const alpha = a !== undefined ? parseFloat(a) : 1.0;
  return { hex, transparency: Math.round((1 - alpha) * 100) };
}
```
