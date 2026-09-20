# Google Docs REST API v1 Styling & Multi-Tab Architecture Guide

This guide documents the low-level engineering mechanics implemented in [`../scripts/build_gdoc_spec.py`](../scripts/build_gdoc_spec.py) to produce native, zero-corruption multi-tab Google Docs specifications.

---

## 1. UTF-16 Code Unit Indexing (`u16_len`)

All character offsets (`startIndex`, `endIndex`) in the Google Docs v1 REST API (`documents.batchUpdate`) are measured in **16-bit UTF-16 code units**, not Unicode code points (`len(str)` in Python 3) and not UTF-8 bytes.

- Basic Multilingual Plane (BMP) characters (`U+0000` to `U+FFFF`) occupy **1 UTF-16 unit**.
- Supplementary Plane characters (such as `📖`, `🔌`, `💻`, `🚀`) are encoded as surrogate pairs and occupy **2 UTF-16 units**.
- Keycap and ZWJ sequences (such as `1️⃣` = `'1' + '\uFE0F' + '\u20E3'`) occupy **3 UTF-16 units**.

Always compute index deltas using:

```python
def u16_len(s: str) -> int:
    return len(s.encode("utf-16-le")) // 2
```

---

## 2. Two-Pass Reverse-Order Native Table Injection

Inserting a native Google Docs table (`insertTable`) shifts all subsequent document indices by a structural overhead (`3 + rows * (1 + cols * 2)` UTF-16 units) that varies with cell paragraph breaks.

To prevent index drift across complex tabs containing multiple tables, headings, callout boxes, and code blocks:

1. **Pass 1 (Linear Forward Cursor):**
   - Insert all headings, rich paragraphs, callout boxes, bullet lists, code blocks, and lightweight placeholder paragraphs (`[[TABLE_0]]`, `[[TABLE_1]]`, ...) in a single `batchUpdate` request with `tabId`.
2. **Pass 2 (Bottom-Up Table Expansion):**
   - Iterate through `tables_to_fill` in **reverse order** (bottom table first).
   - Fetch the current tab body via `GET /v1/documents/{docId}?includeTabsContent=true`.
   - Locate the exact `startIndex` and `endIndex` of `[[TABLE_k]]`, delete the marker text, and call `insertTable(rows, columns)` at `startIndex`.
   - Re-fetch the tab body to read the exact `startIndex` of each cell's first paragraph, sort all cells in **descending order of `startIndex`**, and issue a single `batchUpdate` that styles the header row (`#1E3A8A`), applies alternating zebra row shading (`#FFFFFF` / `#F8FAFC`), and populates every cell from bottom-right to top-left so earlier cell offsets never shift.

---

## 3. Continuous Shaded Callouts & Code Blocks

Google Docs automatically merges adjacent paragraphs into a single continuous visual container when they share identical `shading`, `borderLeft`, `borderTop`, `borderBottom`, `borderRight`, `indentStart`, and `indentEnd` properties:

- **Callout Banners (`add_callout`):**
  - `amber` (`#FFFBEB` background, `3.5pt #F59E0B` left border): Environment warnings, staging-to-production cutover notices, non-blocking fallback rules.
  - `blue` (`#EFF6FF` background, `3.5pt #2563EB` left border): Routing invariants, architectural constraints, environment variable practices.
  - `green` (`#F0FDF4` background, `3.5pt #16A34A` left border): UX recommendations, performance tips.
  - `red` (`#FEF2F2` background, `3.5pt #DC2626` left border): Prohibited routes, security boundaries, destructive actions.
- **Monospace Code Containers (`add_code_block`):**
  - Preceded by a `keepWithNext: true` dark slate header pill (`#334155` background, `#E2E8F0` `Roboto Mono 8.5pt Bold`).
  - Body lines rendered in `#F8FAFC` shading with a `3pt #3B82F6` left border and `Roboto Mono 9.5pt`.
  - Empty lines are replaced with a single space (`" "`) so Google Docs maintains continuous paragraph shading across blank lines inside the snippet.
