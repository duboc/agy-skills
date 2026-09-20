#!/usr/bin/env node
// ============================================================
// MARP Slide JSON → Editable PowerPoint Builder
//
// Usage: node build_pptx.js <input.json> [output.pptx]
//
// Reads the JSON extracted by extract.js and produces a fully
// editable PowerPoint file with native text boxes, lists,
// tables, and images — not screenshots.
// ============================================================
const pptxgen = require('pptxgenjs');
const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

// --- Configuration ---
const SLIDE_WIDTH = 10;   // inches (16:9 standard)
const SLIDE_HEIGHT = 5.625; // inches (16:9 standard)

// Google Identity Colors
const COLORS = {
  blue: '4285F4',
  red: 'EA4335',
  yellow: 'FBBC05',
  green: '34A853',
  grey900: '202124',
  grey700: '5F6368',
  grey200: 'E8EAED',
  grey100: 'F1F3F4',
  white: 'FFFFFF',
  lightBlue: '5C92F6'
};

// --- Helpers ---

/**
 * Convert CSS color string to hex (without #)
 */
function cssColorToHex(cssColor) {
  if (!cssColor || cssColor === 'transparent' || cssColor === 'rgba(0, 0, 0, 0)') {
    return null;
  }

  if (cssColor.startsWith('#')) {
    const hex = cssColor.replace('#', '');
    if (hex.length === 3) {
      return (hex[0]+hex[0]+hex[1]+hex[1]+hex[2]+hex[2]).toUpperCase();
    }
    return hex.substring(0, 6).toUpperCase();
  }

  const rgbMatch = cssColor.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
  if (rgbMatch) {
    const r = parseInt(rgbMatch[1]).toString(16).padStart(2, '0');
    const g = parseInt(rgbMatch[2]).toString(16).padStart(2, '0');
    const b = parseInt(rgbMatch[3]).toString(16).padStart(2, '0');
    return (r + g + b).toUpperCase();
  }

  const hslMatch = cssColor.match(/hsla?\((\d+),\s*(\d+)%?,\s*(\d+)%?/);
  if (hslMatch) {
    let h = parseInt(hslMatch[1]) / 360;
    let s = parseInt(hslMatch[2]) / 100;
    let l = parseInt(hslMatch[3]) / 100;
    let r, g, b;
    if (s === 0) {
      r = g = b = l;
    } else {
      const hue2rgb = (p, q, t) => {
        if (t < 0) t += 1;
        if (t > 1) t -= 1;
        if (t < 1/6) return p + (q - p) * 6 * t;
        if (t < 1/2) return q;
        if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
        return p;
      };
      const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
      const p = 2 * l - q;
      r = hue2rgb(p, q, h + 1/3);
      g = hue2rgb(p, q, h);
      b = hue2rgb(p, q, h - 1/3);
    }
    const toHex = v => Math.round(v * 255).toString(16).padStart(2, '0');
    return (toHex(r) + toHex(g) + toHex(b)).toUpperCase();
  }

  const named = {
    'white': 'FFFFFF', 'black': '000000', 'red': 'FF0000',
    'blue': '0000FF', 'green': '008000', 'yellow': 'FFFF00',
    'gray': '808080', 'grey': '808080',
    'darkgray': 'A9A9A9', 'darkgrey': 'A9A9A9',
    'lightgray': 'D3D3D3', 'lightgrey': 'D3D3D3',
    'orange': 'FFA500', 'purple': '800080', 'navy': '000080',
    'teal': '008080', 'cyan': '00FFFF', 'aqua': '00FFFF',
    'magenta': 'FF00FF', 'fuchsia': 'FF00FF', 'pink': 'FFC0CB',
    'maroon': '800000', 'olive': '808000', 'silver': 'C0C0C0',
    'coral': 'FF7F50', 'salmon': 'FA8072', 'gold': 'FFD700',
    'tomato': 'FF6347', 'chocolate': 'D2691E',
    'darkblue': '00008B', 'darkgreen': '006400', 'darkred': '8B0000',
    'whitesmoke': 'F5F5F5', 'slategray': '708090', 'slategrey': '708090',
    'dimgray': '696969', 'dimgrey': '696969',
    'steelblue': '4682B4', 'royalblue': '4169E1',
    'cornflowerblue': '6495ED', 'rebeccapurple': '663399',
    'indigo': '4B0082', 'crimson': 'DC143C'
  };
  return named[cssColor.toLowerCase()] || COLORS.grey900;
}

/**
 * Check if a background color is dark
 */
function isDarkBackground(bgColor) {
  const hex = cssColorToHex(bgColor);
  if (!hex) return false;
  const r = parseInt(hex.substring(0, 2), 16);
  const g = parseInt(hex.substring(2, 4), 16);
  const b = parseInt(hex.substring(4, 6), 16);
  const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
  return luminance < 0.5;
}

/**
 * Convert pixel position/size to inches relative to slide
 */
function pxToInches(px, totalPx, totalInches) {
  return (px / totalPx) * totalInches;
}

/**
 * Convert CSS font size (px) to PowerPoint points
 */
function pxToPt(px) {
  // CSS px to pt: 1px ≈ 0.75pt, but MARP renders at higher DPI
  // Typical MARP slide is 1280x720 rendering at ~96dpi
  return Math.round(px * 0.75);
}

/**
 * Map CSS font-weight to bold boolean
 */
function isBold(fontWeight) {
  if (!fontWeight) return false;
  const w = parseInt(fontWeight);
  return w >= 600 || fontWeight === 'bold';
}

/**
 * Pick a clean font family from CSS font stack
 */
function cleanFont(fontFamily) {
  if (!fontFamily) return 'Arial';
  // Extract first font, strip quotes
  const first = fontFamily.split(',')[0].trim().replace(/['"]/g, '');
  const fontMap = {
    'Inter': 'Arial',
    'Google Sans': 'Arial',
    'Google Sans Text': 'Arial',
    'Roboto': 'Arial',
    'Helvetica': 'Arial',
    'Helvetica Neue': 'Arial',
    'sans-serif': 'Arial',
    'monospace': 'Courier New',
    'Courier': 'Courier New',
    'Courier New': 'Courier New',
    'Source Code Pro': 'Courier New',
    'Fira Code': 'Courier New',
    'JetBrains Mono': 'Courier New',
    'Consolas': 'Courier New',
    'Menlo': 'Courier New',
    'Lato': 'Calibri',
    'Open Sans': 'Calibri',
    'Noto Sans': 'Calibri',
    'Segoe UI': 'Calibri',
    'Source Sans Pro': 'Calibri',
    'Nunito': 'Calibri',
    'Poppins': 'Calibri',
    'Georgia': 'Georgia',
    'Times New Roman': 'Times New Roman',
    'serif': 'Times New Roman',
    'Merriweather': 'Georgia',
    'Playfair Display': 'Georgia',
    'Noto Serif': 'Georgia'
  };
  return fontMap[first] || first;
}

/**
 * Download an image URL to a local buffer (for embedding in PPTX)
 */
const MAX_IMAGE_SIZE = 10 * 1024 * 1024; // 10MB
const MAX_REDIRECTS = 5;

function downloadImage(url, depth = 0) {
  return new Promise((resolve, reject) => {
    if (url.startsWith('data:')) {
      const matches = url.match(/^data:([^;]+);base64,(.+)$/);
      if (matches) {
        resolve(Buffer.from(matches[2], 'base64'));
      } else {
        reject(new Error('Invalid data URI'));
      }
      return;
    }

    if (url.startsWith('file://')) {
      const filePath = url.replace('file://', '');
      fs.readFile(filePath, (err, data) => {
        if (err) reject(err);
        else resolve(data);
      });
      return;
    }

    if (depth > MAX_REDIRECTS) {
      reject(new Error(`Too many redirects (>${MAX_REDIRECTS})`));
      return;
    }

    const client = url.startsWith('https') ? https : http;
    const req = client.get(url, { timeout: 10000 }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        res.resume();
        downloadImage(res.headers.location, depth + 1).then(resolve).catch(reject);
        return;
      }

      if (res.statusCode >= 400) {
        res.resume();
        reject(new Error(`HTTP ${res.statusCode} for ${url}`));
        return;
      }

      const contentType = res.headers['content-type'] || '';
      if (contentType && !contentType.startsWith('image/') && !contentType.startsWith('application/octet-stream')) {
        res.resume();
        reject(new Error(`Unexpected content-type: ${contentType}`));
        return;
      }

      const contentLength = parseInt(res.headers['content-length'] || '0');
      if (contentLength > MAX_IMAGE_SIZE) {
        res.resume();
        reject(new Error(`Image too large: ${contentLength} bytes (max ${MAX_IMAGE_SIZE})`));
        return;
      }

      let totalSize = 0;
      const chunks = [];
      const bodyTimeout = setTimeout(() => {
        res.destroy();
        reject(new Error('Response body timeout (30s)'));
      }, 30000);

      res.on('data', chunk => {
        totalSize += chunk.length;
        if (totalSize > MAX_IMAGE_SIZE) {
          res.destroy();
          clearTimeout(bodyTimeout);
          reject(new Error(`Image too large during download (max ${MAX_IMAGE_SIZE} bytes)`));
          return;
        }
        chunks.push(chunk);
      });
      res.on('end', () => {
        clearTimeout(bodyTimeout);
        resolve(Buffer.concat(chunks));
      });
      res.on('error', (err) => {
        clearTimeout(bodyTimeout);
        reject(err);
      });
    });
    req.on('error', reject);
  });
}

/**
 * Build rich text array from element data (handles accent/bold spans)
 */
function buildTextRuns(element, defaultColor) {
  const color = cssColorToHex(element.color) || defaultColor;
  const fontSize = pxToPt(element.fontSize);
  const fontFace = cleanFont(element.fontFamily);
  const baseBold = isBold(element.fontWeight);
  const baseItalic = element.isItalic || element.fontStyle === 'italic';
  const runs = [];

  const makeRun = (text, opts = {}) => ({
    text,
    options: {
      fontSize,
      fontFace,
      color: opts.color || color,
      bold: opts.bold !== undefined ? opts.bold : baseBold,
      italic: opts.italic !== undefined ? opts.italic : baseItalic
    }
  });

  if (element.accents && element.accents.length > 0 && element.text) {
    let remaining = element.text;
    for (const accent of element.accents) {
      const idx = remaining.indexOf(accent.text);
      if (idx === -1) continue;
      if (idx > 0) {
        runs.push(makeRun(remaining.substring(0, idx)));
      }
      runs.push(makeRun(accent.text, {
        color: cssColorToHex(accent.color) || COLORS.blue,
        bold: accent.tag === 'strong' ? true : baseBold,
        italic: accent.tag === 'em' ? true : baseItalic
      }));
      remaining = remaining.substring(idx + accent.text.length);
    }
    if (remaining) {
      runs.push(makeRun(remaining));
    }
  } else if (element.hasAccent && element.accentText && element.text) {
    const parts = element.text.split(element.accentText);
    if (parts[0]) runs.push(makeRun(parts[0]));
    runs.push(makeRun(element.accentText, {
      color: cssColorToHex(element.accentColor) || COLORS.blue,
      bold: true
    }));
    if (parts[1]) runs.push(makeRun(parts[1]));
  } else {
    runs.push(makeRun(element.text || ''));
  }

  return runs;
}

// --- Main Builder ---

async function buildPresentation(inputPath, outputPath) {
  const raw = fs.readFileSync(inputPath, 'utf-8');
  const data = JSON.parse(raw);

  if (data.error) {
    console.error('Error in extracted data:', data.error);
    process.exit(1);
  }

  const { meta, slides } = data;
  const srcWidth = meta.slideWidth;
  const srcHeight = meta.slideHeight;

  const pres = new pptxgen();
  pres.layout = 'LAYOUT_16x9';
  pres.title = meta.title;
  pres.author = 'Generated by html-to-pptx skill';

  // Define slide master for Google identity
  pres.defineSlideMaster({
    title: 'GOOGLE_IDENTITY',
    background: { color: COLORS.white }
  });

  for (const slideData of slides) {
    const slide = pres.addSlide();

    // --- Set slide background ---
    const bgHex = cssColorToHex(slideData.background.color);
    if ((bgHex && bgHex !== 'FFFFFF' && bgHex !== '000000') ||
        (bgHex === '000000' && slideData.class.includes('invert'))) {
      slide.background = { color: bgHex };
    }

    // Handle background images (from CSS background-image)
    if (slideData.background.image) {
      const urlMatch = slideData.background.image.match(/url\(["']?([^"')]+)["']?\)/);
      if (urlMatch) {
        try {
          const imgBuffer = await downloadImage(urlMatch[1]);
          const base64 = imgBuffer.toString('base64');
          const ext = urlMatch[1].match(/\.(png|jpg|jpeg|gif|webp)/i);
          const mime = ext ? ext[1].toLowerCase().replace('jpg', 'jpeg') : 'png';
          slide.background = { data: `image/${mime};base64,${base64}` };
        } catch (err) {
          console.warn(`Warning: Could not download background image for slide ${slideData.index + 1}: ${err.message}`);
        }
      }
    }

    const darkBg = isDarkBackground(slideData.background.color);
    const defaultTextColor = darkBg ? COLORS.white : COLORS.grey900;

    // --- Add Google gradient bar for title/closing slides ---
    if (slideData.class.includes('title') || slideData.class.includes('closing')) {
      // 4-color gradient bar at the bottom
      const barHeight = 0.06;
      const barY = SLIDE_HEIGHT - barHeight;
      const segWidth = SLIDE_WIDTH / 4;
      const barColors = [COLORS.blue, COLORS.red, COLORS.yellow, COLORS.green];
      barColors.forEach((color, i) => {
        slide.addShape(pres.ShapeType.rect, {
          x: i * segWidth,
          y: barY,
          w: segWidth + 0.01, // slight overlap to avoid gaps
          h: barHeight,
          fill: { color: color }
        });
      });
    }

    // --- Process each element ---
    for (const el of slideData.elements) {
      const x = pxToInches(el.x, srcWidth, SLIDE_WIDTH);
      const y = pxToInches(el.y, srcHeight, SLIDE_HEIGHT);
      const w = pxToInches(el.width, srcWidth, SLIDE_WIDTH);
      const h = pxToInches(el.height, srcHeight, SLIDE_HEIGHT);

      // Clamp to slide bounds with padding
      const safeX = Math.max(0.2, Math.min(x, SLIDE_WIDTH - 0.5));
      const safeW = Math.min(w, SLIDE_WIDTH - safeX - 0.2);

      const align = el.textAlign === 'center' ? 'center'
                   : el.textAlign === 'right' ? 'right'
                   : 'left';

      switch (el.type) {
        case 'heading': {
          const runs = buildTextRuns(el, defaultTextColor);
          slide.addText(runs, {
            x: safeX,
            y: y,
            w: safeW,
            h: h,
            align: align,
            valign: 'top',
            wrap: true,
            shrinkText: true
          });
          break;
        }

        case 'text': {
          const runs = buildTextRuns(el, defaultTextColor);
          slide.addText(runs, {
            x: safeX,
            y: y,
            w: safeW,
            h: h,
            align: align,
            valign: 'top',
            wrap: true,
            shrinkText: true
          });
          break;
        }

        case 'unordered-list':
        case 'ordered-list': {
          function flattenItems(items, isUnordered) {
            const flat = [];
            for (const item of items) {
              const itemColor = cssColorToHex(item.color) || defaultTextColor;
              const depth = item.depth || 0;
              flat.push({
                text: item.text,
                options: {
                  fontSize: pxToPt(item.fontSize || el.fontSize),
                  fontFace: cleanFont(el.fontFamily),
                  color: itemColor,
                  bullet: isUnordered
                    ? { type: 'bullet', code: depth > 0 ? '25CB' : '25CF', color: cssColorToHex(el.bulletColor) || COLORS.blue }
                    : { type: 'number', color: itemColor },
                  indentLevel: Math.min(depth, 4),
                  bold: item.hasAccent || false
                }
              });
              if (item.subItems && item.subItems.length > 0) {
                flat.push(...flattenItems(item.subItems, isUnordered));
              }
            }
            return flat;
          }
          const listRows = flattenItems(el.items, el.type === 'unordered-list');
          slide.addText(listRows, {
            x: safeX,
            y: y,
            w: safeW,
            h: h,
            valign: 'top',
            wrap: true,
            shrinkText: true
          });
          break;
        }

        case 'blockquote': {
          // Add a left border accent bar
          const borderHex = cssColorToHex(el.borderColor) || COLORS.blue;
          slide.addShape(pres.ShapeType.rect, {
            x: safeX,
            y: y,
            w: 0.05,
            h: h,
            fill: { color: borderHex }
          });
          slide.addText([{
            text: el.text,
            options: {
              fontSize: pxToPt(el.fontSize),
              fontFace: cleanFont(el.fontFamily),
              color: cssColorToHex(el.color) || defaultTextColor,
              italic: true
            }
          }], {
            x: safeX + 0.15,
            y: y,
            w: safeW - 0.15,
            h: h,
            valign: 'middle',
            wrap: true,
            shrinkText: true
          });
          break;
        }

        case 'code': {
          // Dark code block background
          slide.addShape(pres.ShapeType.rect, {
            x: safeX,
            y: y,
            w: safeW,
            h: h,
            fill: { color: COLORS.grey900 },
            rectRadius: 0.08
          });
          slide.addText([{
            text: el.text,
            options: {
              fontSize: Math.min(pxToPt(el.fontSize), 12),
              fontFace: 'Courier New',
              color: COLORS.grey200
            }
          }], {
            x: safeX + 0.15,
            y: y + 0.1,
            w: safeW - 0.3,
            h: h - 0.2,
            valign: 'top',
            wrap: true,
            shrinkText: true
          });
          break;
        }

        case 'image': {
          if (el.src) {
            try {
              const imgBuffer = await downloadImage(el.src);
              const base64 = imgBuffer.toString('base64');
              const ext = el.src.match(/\.(png|jpg|jpeg|gif|webp|svg)/i);
              const mime = ext ? ext[1].toLowerCase().replace('jpg', 'jpeg') : 'png';
              slide.addImage({
                data: `image/${mime};base64,${base64}`,
                x: safeX,
                y: y,
                w: Math.min(safeW, SLIDE_WIDTH - safeX - 0.2),
                h: h
              });
            } catch (err) {
              console.warn(`Warning: Could not embed image on slide ${slideData.index + 1}: ${err.message}`);
              // Add placeholder
              slide.addText([{ text: `[Image: ${el.alt || el.src}]`, options: { fontSize: 10, color: COLORS.grey700, italic: true } }], {
                x: safeX, y: y, w: safeW, h: h, align: 'center', valign: 'middle'
              });
            }
          }
          break;
        }

        case 'table': {
          if (el.rows && el.rows.length > 0) {
            let totalCols = 0;
            for (const cell of el.rows[0]) {
              totalCols += (cell.colspan || 1);
            }
            const tableFontSize = Math.max(10, Math.min(14, pxToPt(el.fontSize)));
            const tableRows = el.rows.map(row =>
              row.map(cell => {
                const cellOpts = {
                  fontSize: tableFontSize,
                  fontFace: 'Arial',
                  color: cssColorToHex(cell.color) || defaultTextColor,
                  bold: cell.isHeader || isBold(cell.fontWeight),
                  fill: cell.isHeader
                    ? { color: COLORS.grey100 }
                    : (cssColorToHex(cell.backgroundColor) ? { color: cssColorToHex(cell.backgroundColor) } : undefined)
                };
                if (cell.colspan && cell.colspan > 1) cellOpts.colspan = cell.colspan;
                if (cell.rowspan && cell.rowspan > 1) cellOpts.rowspan = cell.rowspan;
                return { text: cell.text, options: cellOpts };
              })
            );
            slide.addTable(tableRows, {
              x: safeX,
              y: y,
              w: safeW,
              border: { pt: 0.5, color: COLORS.grey200 },
              colW: Array(totalCols).fill(safeW / totalCols),
              autoPage: false
            });
          }
          break;
        }

        case 'svg': {
          // SVGs are flagged as complex — placeholder for screenshot fallback
          slide.addText([{
            text: `[Complex SVG element — use screenshot fallback]`,
            options: { fontSize: 10, color: COLORS.grey700, italic: true }
          }], {
            x: safeX, y: y, w: safeW, h: h,
            align: 'center', valign: 'middle',
            border: { pt: 1, color: COLORS.grey200, type: 'dash' }
          });
          break;
        }
      }
    }
  }

  await pres.writeFile({ fileName: outputPath });
  console.log(`PowerPoint created: ${outputPath}`);
  console.log(`  Slides: ${slides.length}`);
  console.log(`  Source dimensions: ${srcWidth}x${srcHeight}px`);
}

// --- CLI Entry Point ---
const args = process.argv.slice(2);
if (args.length < 1) {
  console.error('Usage: node build_pptx.js <input.json> [output.pptx]');
  process.exit(1);
}

const inputFile = args[0];
const outputFile = args[1] || inputFile.replace(/\.json$/, '.pptx');

if (!fs.existsSync(inputFile)) {
  console.error(`Error: Input file not found: ${inputFile}`);
  process.exit(1);
}

buildPresentation(inputFile, outputFile).catch(err => {
  console.error('Error building presentation:', err);
  process.exit(1);
});
