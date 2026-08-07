/**
 * deck_kit.js — shared helpers for Zen-style pptxgenjs decks.
 *
 * Usage:
 *   const pptxgen = require("pptxgenjs");
 *   const kit = require("./deck_kit");
 *   const pres = new pptxgen();
 *   pres.layout = "LAYOUT_WIDE";
 *   const K = kit.init(pres, kit.palettes.googleCloud);
 *   K.cover(...); K.stat(...); ...
 *
 * Every layout function returns the slide so you can add extra elements to it.
 * All coordinates assume LAYOUT_WIDE (13.3" x 7.5").
 */

const W = 13.3;
const H = 7.5;
const M = 0.8; // standard left margin

const palettes = {
  googleCloud: {
    accents: ["4285F4", "EA4335", "FBBC04", "34A853"],
    accentsOnLight: ["4285F4", "EA4335", "F9AB00", "34A853"], // amber swap: FBBC04 is unreadable as text on white
    dark: "202124",
    ink: "202124",
    muted: "5F6368",
    faint: "80868B",
    surface: "F1F3F4",
    rule: "DADCE0",
    onDark: "FFFFFF",
    onDarkMuted: "9AA0A6",
    bg: "FFFFFF",
  },
  midnight: {
    accents: ["1E2761", "7A9CC6", "CADCFC", "3E5C99"],
    accentsOnLight: ["1E2761", "3E5C99", "2A4A80", "4C6BA8"],
    dark: "10142E", ink: "1E2761", muted: "5A6180", faint: "8A90A8",
    surface: "F2F5FC", rule: "D9E0F0", onDark: "FFFFFF", onDarkMuted: "A8B2D1",
    bg: "FFFFFF",
  },
  forest: {
    accents: ["2C5F2D", "97BC62", "D9B310", "5C8001"],
    accentsOnLight: ["2C5F2D", "5C8001", "8A6D00", "6B8E23"],
    dark: "13210F", ink: "1F2D19", muted: "5B6B55", faint: "8A9584",
    surface: "F1F5EE", rule: "DCE4D6", onDark: "FFFFFF", onDarkMuted: "A9B6A2",
    bg: "FFFFFF",
  },
  charcoal: {
    accents: ["36454F", "7A93A3", "C89F5D", "5E7A87"],
    accentsOnLight: ["36454F", "5E7A87", "A67C34", "7A93A3"],
    dark: "1C242A", ink: "212121", muted: "5C666D", faint: "8B959B",
    surface: "F2F4F5", rule: "DCE1E3", onDark: "FFFFFF", onDarkMuted: "A9B3B9",
    bg: "FFFFFF",
  },
};

function init(pres, P, opts) {
  opts = opts || {};
  const F = opts.font || "Arial";
  const NONE = { type: "none" };

  // ---------- primitives ----------

  function light() {
    const s = pres.addSlide();
    s.background = { color: P.bg };
    return s;
  }

  function dark() {
    const s = pres.addSlide();
    s.background = { color: P.dark };
    return s;
  }

  /** The repeated visual motif: a row of small accent dots. */
  function motif(s, x, y, size) {
    P.accents.forEach((col, i) => {
      s.addShape(pres.ShapeType.ellipse, {
        x: x + i * (size * 1.75), y: y, w: size, h: size,
        fill: { color: col }, line: NONE,
      });
    });
  }

  /** Small uppercase kicker above the slide statement. */
  function eyebrow(s, text, color) {
    s.addText(String(text).toUpperCase(), {
      x: M, y: 0.62, w: 9, h: 0.3, fontFace: F, fontSize: 11, bold: true,
      color: color || P.muted, charSpacing: 2, margin: 0,
    });
  }

  /** The slide statement. Returns the y coordinate where content may begin. */
  function statement(s, text, o) {
    o = o || {};
    const size = o.size || 38;
    const lines = String(text).split("\n").length;
    const h = lines * (size / 60) + 0.5;
    s.addText(text, {
      x: M, y: o.y || 1.25, w: o.w || 11.5, h: h,
      fontFace: F, fontSize: size, bold: true, color: P.ink,
      lineSpacing: size * 1.22, margin: 0,
    });
    return (o.y || 1.25) + h + 0.35;
  }

  /** Muted one-liner, usually near the bottom of a content slide. */
  function footnote(s, text, y) {
    s.addText(text, {
      x: M, y: y || 6.4, w: 11.5, h: 0.4,
      fontFace: F, fontSize: 14, italic: true, color: P.muted, margin: 0,
    });
  }

  function notes(s, text) { if (text) s.addNotes(text); }

  // ---------- layouts ----------

  /** 1. COVER — dark, motif, title, subtitle, signature. */
  function cover(o) {
    const s = dark();
    motif(s, M, 1.55, 0.3);
    s.addText(o.title, {
      x: M, y: 2.35, w: 11.5, h: 1.3,
      fontFace: F, fontSize: o.size || 66, bold: true, color: P.onDark, margin: 0,
    });
    if (o.subtitle) s.addText(o.subtitle, {
      x: M, y: 3.72, w: 11.5, h: 0.6,
      fontFace: F, fontSize: 24, color: P.onDarkMuted, margin: 0,
    });
    if (o.signature) s.addText(o.signature, {
      x: M, y: 6.35, w: 11, h: 0.35,
      fontFace: F, fontSize: 12, color: P.faint, margin: 0,
    });
    notes(s, o.notes);
    return s;
  }

  /** 2. PIVOT — dark, motif, one sentence. The turn of the deck. */
  function pivot(o) {
    const s = dark();
    motif(s, M, 1.85, 0.24);
    s.addText(o.text, {
      x: M, y: 2.7, w: 11.5, h: 2.2,
      fontFace: F, fontSize: o.size || 48, bold: true, color: P.onDark,
      lineSpacing: (o.size || 48) * 1.24, margin: 0,
    });
    if (o.signature) s.addText(o.signature, {
      x: M, y: 6.35, w: 11, h: 0.35,
      fontFace: F, fontSize: 13, color: P.faint, margin: 0,
    });
    notes(s, o.notes);
    return s;
  }

  /** 3. STAT — hero number left, meaning beside it, optional doughnut right. */
  function stat(o) {
    const s = light();
    if (o.eyebrow) eyebrow(s, o.eyebrow, o.eyebrowColor || P.accentsOnLight[2]);
    const col = o.color || P.accentsOnLight[1];
    s.addText(o.value, {
      x: M, y: 1.5, w: 5.4, h: 1.9,
      fontFace: F, fontSize: o.valueSize || 128, bold: true, color: col, margin: 0,
    });
    s.addText(o.meaning, {
      x: M, y: 3.55, w: 5.6, h: 1.4,
      fontFace: F, fontSize: 24, color: P.ink, lineSpacing: 34,
      valign: "top", margin: 0,
    });
    if (o.support) s.addText(o.support, {
      x: M, y: 5.05, w: 5.6, h: 0.9,
      fontFace: F, fontSize: 15, color: P.muted, margin: 0,
    });
    if (o.donut) {
      s.addChart(pres.ChartType.doughnut, [{
        name: o.donut.name || "", labels: o.donut.labels, values: o.donut.values,
      }], {
        x: 7.1, y: 1.35, w: 5.2, h: 4.9,
        chartColors: [col, P.surface], holeSize: 62,
        showLegend: false, showValue: false, showTitle: false,
        dataBorder: { pt: 3, color: P.bg },
      });
    }
    notes(s, o.notes);
    return s;
  }

  /** 4. ESCALATION — numbers growing left to right, arrows between. */
  function escalation(o) {
    const s = light();
    if (o.eyebrow) eyebrow(s, o.eyebrow, o.eyebrowColor || P.accentsOnLight[1]);
    statement(s, o.statement, { size: o.size || 40 });
    const items = o.steps;
    const bw = 2.7, gap = 0.45;
    const sx = (W - (items.length * bw + (items.length - 1) * gap)) / 2;
    items.forEach((st, i) => {
      const x = sx + i * (bw + gap);
      const c = st.color || P.accentsOnLight[i % 4];
      s.addShape(pres.ShapeType.roundRect, {
        x: x, y: 3.6, w: bw, h: 1.95, rectRadius: 0.1,
        fill: { color: P.surface }, line: NONE,
      });
      s.addText(st.value, {
        x: x, y: 3.85, w: bw, h: 0.95,
        fontFace: F, fontSize: 44, bold: true, color: c, align: "center", margin: 0,
      });
      s.addText(st.label, {
        x: x, y: 4.82, w: bw, h: 0.4,
        fontFace: F, fontSize: 13, color: P.muted, align: "center", margin: 0,
      });
      if (i < items.length - 1) s.addText("→", {
        x: x + bw, y: 4.28, w: gap, h: 0.5,
        fontFace: F, fontSize: 18, color: P.rule, align: "center", margin: 0,
      });
    });
    if (o.footnote) footnote(s, o.footnote, 6.05);
    notes(s, o.notes);
    return s;
  }

  /** 5. CARDS — 2 to 4 tinted cards, each with an accent dot, title, body. */
  function cards(o) {
    const s = light();
    if (o.eyebrow) eyebrow(s, o.eyebrow, o.eyebrowColor || P.accentsOnLight[3]);
    const top = statement(s, o.statement, { size: o.size || 38 });
    const n = o.cards.length;
    const gap = 0.5;
    const cw = (11.7 - (n - 1) * gap) / n;
    const y = Math.max(top, 2.75);
    const ch = Math.min(3.2, 6.05 - y);
    o.cards.forEach((cd, i) => {
      const x = M + i * (cw + gap);
      const c = cd.color || P.accentsOnLight[i % 4];
      s.addShape(pres.ShapeType.roundRect, {
        x: x, y: y, w: cw, h: ch, rectRadius: 0.1,
        fill: { color: P.surface }, line: NONE,
      });
      s.addShape(pres.ShapeType.ellipse, {
        x: x + 0.4, y: y + 0.4, w: 0.42, h: 0.42,
        fill: { color: c }, line: NONE,
      });
      s.addText(cd.title, {
        x: x + 0.4, y: y + 0.98, w: cw - 0.8, h: 0.5,
        fontFace: F, fontSize: 20, bold: true, color: P.ink, margin: 0,
      });
      s.addText(cd.body, {
        x: x + 0.4, y: y + 1.5, w: cw - 0.8, h: ch - 1.75,
        fontFace: F, fontSize: 13.5, color: P.muted, lineSpacing: 19,
        valign: "top", margin: 0,
      });
    });
    notes(s, o.notes);
    return s;
  }

  /** 6. COLUMNS — 2 to 4 unboxed columns: dot, name, role label, body. */
  function columns(o) {
    const s = light();
    if (o.eyebrow) eyebrow(s, o.eyebrow, o.eyebrowColor || P.accentsOnLight[0]);
    statement(s, o.statement, { size: o.size || 36 });
    const n = o.columns.length;
    const gap = 0.5;
    const cw = (11.7 - (n - 1) * gap) / n;
    o.columns.forEach((cl, i) => {
      const x = M + i * (cw + gap);
      const c = cl.color || P.accentsOnLight[i % 4];
      s.addShape(pres.ShapeType.ellipse, {
        x: x, y: 3.35, w: 0.5, h: 0.5, fill: { color: c }, line: NONE,
      });
      s.addText(cl.title, {
        x: x, y: 4.05, w: cw, h: 0.5,
        fontFace: F, fontSize: 26, bold: true, color: P.ink, margin: 0,
      });
      if (cl.label) s.addText(cl.label, {
        x: x, y: 4.58, w: cw, h: 0.35,
        fontFace: F, fontSize: 12.5, bold: true, color: c, charSpacing: 1, margin: 0,
      });
      s.addText(cl.body, {
        x: x, y: cl.label ? 5.0 : 4.62, w: cw - 0.15, h: 1.5,
        fontFace: F, fontSize: 13.5, color: P.muted, lineSpacing: 19,
        valign: "top", margin: 0,
      });
    });
    notes(s, o.notes);
    return s;
  }

  /** 7. FLOW — numbered process steps in tinted cards with arrows. */
  function flow(o) {
    const s = light();
    if (o.eyebrow) eyebrow(s, o.eyebrow, o.eyebrowColor || P.accentsOnLight[1]);
    statement(s, o.statement, { size: o.size || 38 });
    const n = o.steps.length;
    const gap = 0.35;
    const bw = (11.7 - (n - 1) * gap) / n;
    o.steps.forEach((st, i) => {
      const x = M + i * (bw + gap);
      const c = st.color || P.accentsOnLight[i % 4];
      s.addShape(pres.ShapeType.roundRect, {
        x: x, y: 2.75, w: bw, h: 2.85, rectRadius: 0.1,
        fill: { color: P.surface }, line: NONE,
      });
      s.addText(String(i + 1).padStart(2, "0"), {
        x: x + 0.35, y: 3.05, w: bw - 0.6, h: 0.5,
        fontFace: F, fontSize: 22, bold: true, color: c, margin: 0,
      });
      s.addText(st.title, {
        x: x + 0.35, y: 3.62, w: bw - 0.6, h: 0.45,
        fontFace: F, fontSize: 19, bold: true, color: P.ink, margin: 0,
      });
      s.addText(st.body, {
        x: x + 0.35, y: 4.12, w: bw - 0.65, h: 1.55,
        fontFace: F, fontSize: 12.5, color: P.muted, lineSpacing: 18,
        valign: "top", margin: 0,
      });
      if (i < n - 1) s.addText("→", {
        x: x + bw, y: 4.1, w: gap, h: 0.4,
        fontFace: F, fontSize: 15, color: P.rule, align: "center", margin: 0,
      });
    });
    notes(s, o.notes);
    return s;
  }

  /** 8. SPLIT — statement + prose on the left, dark detail panel on the right. */
  function split(o) {
    const s = light();
    if (o.eyebrow) eyebrow(s, o.eyebrow, o.eyebrowColor || P.accentsOnLight[0]);
    s.addText(o.statement, {
      x: M, y: 1.4, w: 6.4, h: 1.8,
      fontFace: F, fontSize: o.size || 34, bold: true, color: P.ink,
      lineSpacing: 44, margin: 0,
    });
    if (o.body) s.addText(o.body, {
      x: M, y: 3.4, w: 6.2, h: 1.8,
      fontFace: F, fontSize: 15.5, color: P.muted, lineSpacing: 24,
      valign: "top", margin: 0,
    });
    if (o.kicker) s.addText(o.kicker, {
      x: M, y: 5.35, w: 6.2, h: 0.8,
      fontFace: F, fontSize: 17, italic: true, bold: true,
      color: o.kickerColor || P.accentsOnLight[0], margin: 0,
    });
    const items = o.panel || [];
    const ph = Math.max(3.0, items.length * 0.62 + 0.85);
    s.addShape(pres.ShapeType.roundRect, {
      x: 7.65, y: 1.4, w: 4.85, h: ph, rectRadius: 0.1,
      fill: { color: P.dark }, line: NONE,
    });
    items.forEach((it, i) => {
      const y = 1.82 + i * 0.62;
      s.addShape(pres.ShapeType.ellipse, {
        x: 8.05, y: y + 0.09, w: 0.16, h: 0.16,
        fill: { color: it.color || P.accents[i % 4] }, line: NONE,
      });
      s.addText(it.title, {
        x: 8.42, y: y - 0.04, w: 3.9, h: 0.3,
        fontFace: F, fontSize: 13.5, bold: true, color: P.onDark, margin: 0,
      });
      if (it.sub) s.addText(it.sub, {
        x: 8.42, y: y + 0.22, w: 3.9, h: 0.3,
        fontFace: F, fontSize: 11, color: P.onDarkMuted, margin: 0,
      });
    });
    notes(s, o.notes);
    return s;
  }

  /** 9. VERSUS — two labelled lists side by side. Old way vs new way. */
  function versus(o) {
    const s = light();
    if (o.eyebrow) eyebrow(s, o.eyebrow, o.eyebrowColor || P.accentsOnLight[2]);
    statement(s, o.statement, { size: o.size || 40, y: 1.35 });
    const cw = 5.4, gap = 0.9;
    [o.left, o.right].forEach((c, i) => {
      const x = M + i * (cw + gap);
      const col = c.color || (i === 0 ? P.accentsOnLight[1] : P.accentsOnLight[3]);
      s.addShape(pres.ShapeType.ellipse, {
        x: x, y: 3.4, w: 0.34, h: 0.34, fill: { color: col }, line: NONE,
      });
      s.addText(c.title, {
        x: x + 0.5, y: 3.38, w: cw - 0.5, h: 0.4,
        fontFace: F, fontSize: 20, bold: true, color: P.ink, margin: 0,
      });
      c.items.forEach((ln, j) => {
        s.addText(ln, {
          x: x, y: 4.08 + j * 0.46, w: cw, h: 0.4,
          fontFace: F, fontSize: 14.5, color: P.muted, margin: 0,
        });
      });
    });
    notes(s, o.notes);
    return s;
  }

  /** 10. STACK — labelled rows of chips. Good for architecture layers. */
  function stack(o) {
    const s = light();
    if (o.eyebrow) eyebrow(s, o.eyebrow, o.eyebrowColor || P.accentsOnLight[3]);
    statement(s, o.statement, { size: o.size || 34 });
    o.rows.forEach((r, i) => {
      const y = 2.55 + i * 1.02;
      const c = r.color || P.accentsOnLight[i % 4];
      s.addShape(pres.ShapeType.ellipse, {
        x: M, y: y + 0.19, w: 0.26, h: 0.26, fill: { color: c }, line: NONE,
      });
      s.addText(r.label, {
        x: M + 0.45, y: y + 0.1, w: 2.5, h: 0.45,
        fontFace: F, fontSize: 15, bold: true, color: P.ink, margin: 0,
      });
      r.items.forEach((it, j) => {
        const x = 3.95 + j * 2.9;
        s.addShape(pres.ShapeType.roundRect, {
          x: x, y: y, w: 2.6, h: 0.66, rectRadius: 0.08,
          fill: { color: P.surface }, line: NONE,
        });
        s.addText(it, {
          x: x, y: y, w: 2.6, h: 0.66,
          fontFace: F, fontSize: 13.5, color: P.ink,
          align: "center", valign: "middle", margin: 0,
        });
      });
    });
    if (o.footnote) footnote(s, o.footnote, 6.55);
    notes(s, o.notes);
    return s;
  }

  /** 11. LEDGER — comparison rows: criterion, before, after. */
  function ledger(o) {
    const s = light();
    if (o.eyebrow) eyebrow(s, o.eyebrow, o.eyebrowColor || P.accentsOnLight[0]);
    statement(s, o.statement, { size: o.size || 38 });
    const colA = o.beforeColor || P.accentsOnLight[1];
    const colB = o.afterColor || P.accentsOnLight[3];
    s.addText(o.beforeLabel, {
      x: 6.4, y: 2.6, w: 2.9, h: 0.35,
      fontFace: F, fontSize: 12, bold: true, color: colA, charSpacing: 1.5, margin: 0,
    });
    s.addText(o.afterLabel, {
      x: 9.6, y: 2.6, w: 3.2, h: 0.35,
      fontFace: F, fontSize: 12, bold: true, color: colB, charSpacing: 1.5, margin: 0,
    });
    o.rows.forEach((r, i) => {
      const y = 3.15 + i * 0.85;
      s.addShape(pres.ShapeType.rect, {
        x: M, y: y - 0.12, w: 11.7, h: 0.02,
        fill: { color: P.rule }, line: NONE,
      });
      s.addText(r.criterion, {
        x: M, y: y + 0.08, w: 5.4, h: 0.5,
        fontFace: F, fontSize: 15, color: P.ink, margin: 0,
      });
      s.addText(r.before, {
        x: 6.4, y: y + 0.08, w: 2.9, h: 0.5,
        fontFace: F, fontSize: 15, color: P.muted, margin: 0,
      });
      s.addText(r.after, {
        x: 9.6, y: y + 0.08, w: 3.2, h: 0.5,
        fontFace: F, fontSize: 15, bold: true, color: colB, margin: 0,
      });
    });
    notes(s, o.notes);
    return s;
  }

  /** 12. TIMELINE — dots along a rule, labels below. */
  function timeline(o) {
    const s = light();
    if (o.eyebrow) eyebrow(s, o.eyebrow, o.eyebrowColor || P.accentsOnLight[0]);
    statement(s, o.statement, { size: o.size || 42, y: 1.35 });
    const pts = o.points;
    const startX = 1.35, span = 10.6;
    const step = pts.length > 1 ? span / (pts.length - 1) : 0;
    s.addShape(pres.ShapeType.rect, {
      x: startX, y: 4.68, w: span, h: 0.03,
      fill: { color: P.rule }, line: NONE,
    });
    pts.forEach((pt, i) => {
      const cx = startX + i * step;
      s.addShape(pres.ShapeType.ellipse, {
        x: cx - 0.11, y: 4.58, w: 0.22, h: 0.22,
        fill: { color: P.accentsOnLight[i % 4] }, line: NONE,
      });
      s.addText(pt, {
        x: cx - 0.85, y: 4.95, w: 1.7, h: 0.5,
        fontFace: F, fontSize: 11, color: P.muted, align: "center", margin: 0,
      });
    });
    if (o.footnote) footnote(s, o.footnote, 5.95);
    notes(s, o.notes);
    return s;
  }

  return {
    P, F, W, H, M, NONE,
    light, dark, motif, eyebrow, statement, footnote,
    cover, pivot, stat, escalation, cards, columns,
    flow, split, versus, stack, ledger, timeline,
  };
}

module.exports = { init, palettes, W, H, M };
