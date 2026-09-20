#!/usr/bin/env python3
"""
Google Docs Engineering Spec Builder (gdoc-engineering-spec)
============================================================
Generic, declarative multi-tab Google Docs generator for engineering specifications,
API integration guides, RFCs/Design Docs, PRDs, and operational runbooks.

Features:
- Automatic creation of Pageless Google Docs via `gdocs_oauth` or REST API
- Native Multi-Tab creation & renaming (`create-tab`, `rename-tab`)
- Exact UTF-16 index math (`len(s.encode('utf-16-le')) // 2`) for emoji-safe styling
- Two-pass reverse-order native Table injection (header styling, zebra striping, code columns)
- Semantic Callout Boxes (`amber`, `blue`, `green`, `red`)
- Monospace Code Blocks (`Roboto Mono`, header label pill, comment coloring, empty-line preservation)
- Inline semantic badges (`badge_blue`, `badge_green`, `badge_amber`, `badge_red`, `code`, `bold`, `italic`, `link`)

Usage:
  python3 build_gdoc_spec.py path/to/spec.json [--doc-id EXISTING_DOC_ID]
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional, Tuple

def _resolve_default_token_path() -> str:
    env_path = os.environ.get("GCLI_ACCESS_TOKEN_PATH")
    if env_path:
        return os.path.expanduser(env_path)
    cache_token = os.path.expanduser("~/.cache/gdoc-spec/access_token")
    legacy_token = os.path.expanduser("~/cowork_workspace/.cowork/access_token")
    if os.path.exists(legacy_token) and not os.path.exists(cache_token):
        return legacy_token
    return cache_token


DEFAULT_TOKEN_PATH = _resolve_default_token_path()
DEFAULT_GDOCS_BIN = os.environ.get(
    "GDOCS_OAUTH_BIN",
    "/Applications/Cowork Agent.app/Contents/Resources/gdocs_oauth",
)


def get_token(token_path: str = DEFAULT_TOKEN_PATH) -> str:
    if not os.path.exists(token_path):
        raise FileNotFoundError(
            f"OAuth access token not found at {token_path}. "
            "Ensure GCLI_ACCESS_TOKEN_PATH points to a valid token file with 0600 permissions."
        )
    if os.name != "nt":
        mode = os.stat(token_path).st_mode & 0o777
        if mode & 0o077:
            os.chmod(token_path, 0o600)
    with open(token_path, "r", encoding="utf-8") as f:
        return f.read().strip()


def api_request(method: str, url: str, body: Optional[Dict[str, Any]] = None, token_path: str = DEFAULT_TOKEN_PATH) -> Dict[str, Any]:
    token = get_token(token_path)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        raise RuntimeError(f"Google Docs API HTTP {e.code} on {url}: {err_body}") from e


def get_doc(doc_id: str, token_path: str = DEFAULT_TOKEN_PATH) -> Dict[str, Any]:
    url = f"https://docs.googleapis.com/v1/documents/{doc_id}?includeTabsContent=true"
    return api_request("GET", url, token_path=token_path)


def batch_update(doc_id: str, requests_list: List[Dict[str, Any]], token_path: str = DEFAULT_TOKEN_PATH) -> Dict[str, Any]:
    if not requests_list:
        return {}
    url = f"https://docs.googleapis.com/v1/documents/{doc_id}:batchUpdate"
    return api_request("POST", url, {"requests": requests_list}, token_path=token_path)


def run_gdocs_cli(args: List[str], token_path: str = DEFAULT_TOKEN_PATH, gdocs_bin: str = DEFAULT_GDOCS_BIN) -> str:
    env = os.environ.copy()
    env["GCLI_ACCESS_TOKEN_PATH"] = token_path
    cmd = [gdocs_bin] + args
    res = subprocess.run(cmd, env=env, capture_output=True, text=True, check=True)
    return res.stdout.strip()


def rgb(hex_str: str) -> Dict[str, Any]:
    h = hex_str.lstrip("#")
    return {
        "color": {
            "rgbColor": {
                "red": int(h[0:2], 16) / 255.0,
                "green": int(h[2:4], 16) / 255.0,
                "blue": int(h[4:6], 16) / 255.0,
            }
        }
    }


def u16_len(s: str) -> int:
    """Google Docs API uses UTF-16 code units for all character indices."""
    return len(s.encode("utf-16-le")) // 2


class TabBuilder:
    def __init__(self, doc_id: str, tab_id: str, token_path: str = DEFAULT_TOKEN_PATH):
        self.doc_id = doc_id
        self.tab_id = tab_id
        self.token_path = token_path
        self.cursor = 1
        self.requests: List[Dict[str, Any]] = []
        self.tables_to_fill: List[Dict[str, Any]] = []

    def _insert_raw(self, text: str) -> Tuple[int, int]:
        start = self.cursor
        length = u16_len(text)
        self.requests.append({
            "insertText": {
                "location": {"index": start, "tabId": self.tab_id},
                "text": text,
            }
        })
        self.cursor += length
        return start, self.cursor

    def _style_paragraph(self, start: int, end: int, style: Dict[str, Any], fields: str):
        self.requests.append({
            "updateParagraphStyle": {
                "range": {"startIndex": start, "endIndex": end, "tabId": self.tab_id},
                "paragraphStyle": style,
                "fields": fields,
            }
        })

    def _style_text(self, start: int, end: int, style: Dict[str, Any], fields: str):
        if start >= end:
            return
        self.requests.append({
            "updateTextStyle": {
                "range": {"startIndex": start, "endIndex": end, "tabId": self.tab_id},
                "textStyle": style,
                "fields": fields,
            }
        })

    def add_title(self, title_text: str, subtitle_text: str = "", metadata_badges: Optional[List[Dict[str, str]]] = None):
        s1, e1 = self._insert_raw(title_text + "\n")
        self._style_paragraph(
            s1, e1,
            {
                "namedStyleType": "TITLE",
                "spaceAbove": {"magnitude": 4, "unit": "PT"},
                "spaceBelow": {"magnitude": 4, "unit": "PT"},
            },
            "namedStyleType,spaceAbove,spaceBelow",
        )
        self._style_text(
            s1, e1 - 1,
            {
                "bold": True,
                "fontSize": {"magnitude": 22, "unit": "PT"},
                "foregroundColor": rgb("#0F172A"),
                "weightedFontFamily": {"fontFamily": "Google Sans", "weight": 700},
            },
            "bold,fontSize,foregroundColor,weightedFontFamily",
        )

        if subtitle_text:
            s2, e2 = self._insert_raw(subtitle_text + "\n")
            self._style_paragraph(
                s2, e2,
                {
                    "namedStyleType": "SUBTITLE",
                    "spaceAbove": {"magnitude": 0, "unit": "PT"},
                    "spaceBelow": {"magnitude": 8 if metadata_badges else 14, "unit": "PT"},
                    "borderBottom": {
                        "color": rgb("#CBD5E1"),
                        "width": {"magnitude": 1, "unit": "PT"},
                        "padding": {"magnitude": 8, "unit": "PT"},
                        "dashStyle": "SOLID",
                    },
                },
                "namedStyleType,spaceAbove,spaceBelow,borderBottom",
            )
            self._style_text(
                s2, e2 - 1,
                {
                    "italic": False,
                    "fontSize": {"magnitude": 11.5, "unit": "PT"},
                    "foregroundColor": rgb("#475569"),
                    "weightedFontFamily": {"fontFamily": "Arial", "weight": 400},
                },
                "italic,fontSize,foregroundColor,weightedFontFamily",
            )

        if metadata_badges:
            segments = []
            for idx, b in enumerate(metadata_badges):
                if idx > 0:
                    segments.append(("   •   ", "normal"))
                label = b.get("label", "")
                value = b.get("value", "")
                kind = b.get("style", "badge_blue")
                if label:
                    segments.append((f"{label}: ", "bold"))
                segments.append((f" {value} ", kind))
            self.add_rich_paragraph(segments, space_above=4, space_below=12)

    def add_heading(self, level: int, text: str):
        s, e = self._insert_raw(text + "\n")
        sizes = {1: 16.5, 2: 13.5, 3: 11.5}
        colors = {1: "#1E3A8A", 2: "#0F172A", 3: "#334155"}
        space_above = {1: 18, 2: 14, 3: 10}
        space_below = {1: 6, 2: 4, 3: 3}
        p_style: Dict[str, Any] = {
            "namedStyleType": f"HEADING_{level}",
            "spaceAbove": {"magnitude": space_above.get(level, 12), "unit": "PT"},
            "spaceBelow": {"magnitude": space_below.get(level, 4), "unit": "PT"},
        }
        p_fields = "namedStyleType,spaceAbove,spaceBelow"
        if level == 1:
            p_style["borderBottom"] = {
                "color": rgb("#DBEAFE"),
                "width": {"magnitude": 1.5, "unit": "PT"},
                "padding": {"magnitude": 4, "unit": "PT"},
                "dashStyle": "SOLID",
            }
            p_fields += ",borderBottom"
        self._style_paragraph(s, e, p_style, p_fields)
        self._style_text(
            s, e - 1,
            {
                "bold": True,
                "fontSize": {"magnitude": sizes.get(level, 12), "unit": "PT"},
                "foregroundColor": rgb(colors.get(level, "#0F172A")),
                "weightedFontFamily": {"fontFamily": "Google Sans", "weight": 700},
            },
            "bold,fontSize,foregroundColor,weightedFontFamily",
        )

    def add_rich_paragraph(self, segments: List[Any], space_above: float = 4, space_below: float = 6, bullet: bool = False):
        """
        segments can be:
          - list of [text, style_kind] or {"text": ..., "style": ..., "url": ...}
        Supported style_kind values:
          - "normal"
          - "bold"
          - "italic"
          - "code" (inline monospace pill)
          - "badge_blue" / "badge_post" (blue pill with white text)
          - "badge_green" / "badge_200" (green pill)
          - "badge_amber" / "badge_warn" (amber pill)
          - "badge_red" (red pill)
          - "link" (requires url)
        """
        span_queue = []
        full_text = ""
        for seg in segments:
            if isinstance(seg, dict):
                seg_text = seg.get("text", "")
                kind = seg.get("style", "normal")
                url = seg.get("url")
            elif isinstance(seg, (list, tuple)):
                seg_text = seg[0]
                kind = seg[1] if len(seg) > 1 else "normal"
                url = seg[2] if len(seg) > 2 else None
            else:
                seg_text = str(seg)
                kind = "normal"
                url = None

            seg_s = self.cursor + u16_len(full_text)
            full_text += seg_text
            seg_e = self.cursor + u16_len(full_text)
            span_queue.append((seg_s, seg_e, kind, url))

        s, e = self._insert_raw(full_text + "\n")
        self._style_paragraph(
            s, e,
            {
                "namedStyleType": "NORMAL_TEXT",
                "lineSpacing": 125.0,
                "spaceAbove": {"magnitude": space_above, "unit": "PT"},
                "spaceBelow": {"magnitude": space_below, "unit": "PT"},
            },
            "namedStyleType,lineSpacing,spaceAbove,spaceBelow",
        )
        self._style_text(
            s, e - 1,
            {
                "bold": False,
                "italic": False,
                "fontSize": {"magnitude": 10.5, "unit": "PT"},
                "foregroundColor": rgb("#1E293B"),
                "backgroundColor": rgb("#FFFFFF"),
                "weightedFontFamily": {"fontFamily": "Arial", "weight": 400},
            },
            "bold,italic,fontSize,foregroundColor,backgroundColor,weightedFontFamily",
        )

        if bullet:
            self.requests.append({
                "createParagraphBullets": {
                    "range": {"startIndex": s, "endIndex": e, "tabId": self.tab_id},
                    "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
                }
            })

        badge_palettes = {
            "badge_blue": ("#FFFFFF", "#2563EB"),
            "badge_post": ("#FFFFFF", "#2563EB"),
            "badge_green": ("#166534", "#DCFCE7"),
            "badge_200": ("#166534", "#DCFCE7"),
            "badge_amber": ("#92400E", "#FEF3C7"),
            "badge_warn": ("#92400E", "#FEF3C7"),
            "badge_red": ("#991B1B", "#FEE2E2"),
        }

        for seg_s, seg_e, kind, url in span_queue:
            if kind == "bold":
                self._style_text(seg_s, seg_e, {"bold": True, "foregroundColor": rgb("#0F172A")}, "bold,foregroundColor")
            elif kind == "italic":
                self._style_text(seg_s, seg_e, {"italic": True, "foregroundColor": rgb("#475569")}, "italic,foregroundColor")
            elif kind == "code":
                self._style_text(
                    seg_s, seg_e,
                    {
                        "bold": True,
                        "fontSize": {"magnitude": 9.5, "unit": "PT"},
                        "foregroundColor": rgb("#0F172A"),
                        "backgroundColor": rgb("#F1F5F9"),
                        "weightedFontFamily": {"fontFamily": "Roboto Mono", "weight": 500},
                    },
                    "bold,fontSize,foregroundColor,backgroundColor,weightedFontFamily",
                )
            elif kind in badge_palettes:
                fg_hex, bg_hex = badge_palettes[kind]
                self._style_text(
                    seg_s, seg_e,
                    {
                        "bold": True,
                        "fontSize": {"magnitude": 9.0, "unit": "PT"},
                        "foregroundColor": rgb(fg_hex),
                        "backgroundColor": rgb(bg_hex),
                        "weightedFontFamily": {"fontFamily": "Roboto Mono", "weight": 700},
                    },
                    "bold,fontSize,foregroundColor,backgroundColor,weightedFontFamily",
                )
            elif kind == "link" and url:
                self._style_text(
                    seg_s, seg_e,
                    {
                        "bold": True,
                        "underline": True,
                        "foregroundColor": rgb("#2563EB"),
                        "link": {"url": url},
                    },
                    "bold,underline,foregroundColor,link",
                )

    def add_callout(self, title: str, lines: List[str], theme: str = "amber"):
        palettes = {
            "amber": ("#FFFBEB", "#F59E0B", "#92400E", "#78350F"),
            "blue": ("#EFF6FF", "#2563EB", "#1E40AF", "#1E3A8A"),
            "green": ("#F0FDF4", "#16A34A", "#166534", "#14532D"),
            "red": ("#FEF2F2", "#DC2626", "#991B1B", "#7F1D1D"),
        }
        bg_hex, border_hex, title_hex, body_hex = palettes.get(theme, palettes["amber"])

        all_lines = [(title, True)] + [(ln, False) for ln in lines]
        line_ranges = []
        for txt, is_title in all_lines:
            s, e = self._insert_raw(txt + "\n")
            line_ranges.append((s, e, is_title))

        thin_border = {
            "color": rgb(border_hex),
            "width": {"magnitude": 0.5, "unit": "PT"},
            "padding": {"magnitude": 8, "unit": "PT"},
            "dashStyle": "SOLID",
        }
        left_border = {
            "color": rgb(border_hex),
            "width": {"magnitude": 3.5, "unit": "PT"},
            "padding": {"magnitude": 10, "unit": "PT"},
            "dashStyle": "SOLID",
        }

        for idx, (s, e, is_title) in enumerate(line_ranges):
            self._style_paragraph(
                s, e,
                {
                    "namedStyleType": "NORMAL_TEXT",
                    "shading": {"backgroundColor": rgb(bg_hex)},
                    "borderLeft": left_border,
                    "borderTop": thin_border,
                    "borderBottom": thin_border,
                    "borderRight": thin_border,
                    "indentStart": {"magnitude": 10, "unit": "PT"},
                    "indentEnd": {"magnitude": 10, "unit": "PT"},
                    "spaceAbove": {"magnitude": 6 if idx == 0 else 2, "unit": "PT"},
                    "spaceBelow": {"magnitude": 8 if idx == len(line_ranges) - 1 else 2, "unit": "PT"},
                    "lineSpacing": 120.0,
                },
                "namedStyleType,shading,borderLeft,borderTop,borderBottom,borderRight,indentStart,indentEnd,spaceAbove,spaceBelow,lineSpacing",
            )
            self._style_text(
                s, e - 1,
                {
                    "bold": is_title,
                    "fontSize": {"magnitude": 10.5 if is_title else 10.0, "unit": "PT"},
                    "foregroundColor": rgb(title_hex if is_title else body_hex),
                    "backgroundColor": rgb(bg_hex),
                    "weightedFontFamily": {"fontFamily": "Arial", "weight": 700 if is_title else 400},
                },
                "bold,fontSize,foregroundColor,backgroundColor,weightedFontFamily",
            )

    def add_code_block(self, label: str, code_text: str):
        hs, he = self._insert_raw(f"  {label}  \n")
        self._style_paragraph(
            hs, he,
            {
                "namedStyleType": "NORMAL_TEXT",
                "spaceAbove": {"magnitude": 8, "unit": "PT"},
                "spaceBelow": {"magnitude": 0, "unit": "PT"},
                "keepWithNext": True,
            },
            "namedStyleType,spaceAbove,spaceBelow,keepWithNext",
        )
        self._style_text(
            hs, he - 1,
            {
                "bold": True,
                "fontSize": {"magnitude": 8.5, "unit": "PT"},
                "foregroundColor": rgb("#E2E8F0"),
                "backgroundColor": rgb("#334155"),
                "weightedFontFamily": {"fontFamily": "Roboto Mono", "weight": 700},
            },
            "bold,fontSize,foregroundColor,backgroundColor,weightedFontFamily",
        )

        code_lines = code_text.strip("\n").split("\n")
        line_ranges = []
        for ln in code_lines:
            safe_ln = ln if ln.strip() != "" else " "
            s, e = self._insert_raw(safe_ln + "\n")
            line_ranges.append((s, e, safe_ln))

        border_box = {
            "color": rgb("#CBD5E1"),
            "width": {"magnitude": 0.75, "unit": "PT"},
            "padding": {"magnitude": 8, "unit": "PT"},
            "dashStyle": "SOLID",
        }
        left_accent = {
            "color": rgb("#3B82F6"),
            "width": {"magnitude": 3.0, "unit": "PT"},
            "padding": {"magnitude": 10, "unit": "PT"},
            "dashStyle": "SOLID",
        }

        for idx, (s, e, safe_ln) in enumerate(line_ranges):
            self._style_paragraph(
                s, e,
                {
                    "namedStyleType": "NORMAL_TEXT",
                    "shading": {"backgroundColor": rgb("#F8FAFC")},
                    "borderLeft": left_accent,
                    "borderTop": border_box,
                    "borderBottom": border_box,
                    "borderRight": border_box,
                    "indentStart": {"magnitude": 8, "unit": "PT"},
                    "indentEnd": {"magnitude": 8, "unit": "PT"},
                    "spaceAbove": {"magnitude": 4 if idx == 0 else 0, "unit": "PT"},
                    "spaceBelow": {"magnitude": 8 if idx == len(line_ranges) - 1 else 0, "unit": "PT"},
                    "lineSpacing": 115.0,
                },
                "namedStyleType,shading,borderLeft,borderTop,borderBottom,borderRight,indentStart,indentEnd,spaceAbove,spaceBelow,lineSpacing",
            )
            is_comment = safe_ln.lstrip().startswith("//") or safe_ln.lstrip().startswith("#")
            fg_hex = "#64748B" if is_comment else "#0F172A"
            self._style_text(
                s, e - 1,
                {
                    "bold": False,
                    "italic": is_comment,
                    "fontSize": {"magnitude": 9.5, "unit": "PT"},
                    "foregroundColor": rgb(fg_hex),
                    "backgroundColor": rgb("#F8FAFC"),
                    "weightedFontFamily": {"fontFamily": "Roboto Mono", "weight": 400},
                },
                "bold,italic,fontSize,foregroundColor,backgroundColor,weightedFontFamily",
            )

    def add_table_placeholder(self, headers: List[str], rows: List[List[str]], header_bg: str = "#1E3A8A"):
        marker = f"[[TABLE_{len(self.tables_to_fill)}]]"
        s, e = self._insert_raw(marker + "\n")
        self._style_paragraph(
            s, e,
            {
                "namedStyleType": "NORMAL_TEXT",
                "spaceAbove": {"magnitude": 6, "unit": "PT"},
                "spaceBelow": {"magnitude": 8, "unit": "PT"},
            },
            "namedStyleType,spaceAbove,spaceBelow",
        )
        self.tables_to_fill.append({
            "marker": marker,
            "headers": headers,
            "rows": rows,
            "header_bg": header_bg,
        })


def _find_tab_body(doc_json: Dict[str, Any], tab_id: str) -> Dict[str, Any]:
    for t in doc_json.get("tabs", []):
        if t.get("tabProperties", {}).get("tabId") == tab_id:
            return t.get("documentTab", {}).get("body", {})
        for child in t.get("childTabs", []):
            if child.get("tabProperties", {}).get("tabId") == tab_id:
                return child.get("documentTab", {}).get("body", {})
    return {}


def _find_marker_range(body: Dict[str, Any], marker_text: str) -> Tuple[Optional[int], Optional[int]]:
    for el in body.get("content", []):
        if "paragraph" in el:
            full_p = "".join(
                run.get("textRun", {}).get("content", "")
                for run in el["paragraph"].get("elements", [])
            )
            if marker_text in full_p:
                return el["startIndex"], el["endIndex"]
    return None, None


def _find_table_at_or_after(body: Dict[str, Any], min_index: int) -> Optional[Dict[str, Any]]:
    for el in body.get("content", []):
        if "table" in el and el.get("startIndex", 0) >= min_index - 2:
            return el
    return None


def populate_tables_for_tab(builder: TabBuilder):
    for tbl_spec in reversed(builder.tables_to_fill):
        doc_json = get_doc(builder.doc_id, builder.token_path)
        body = _find_tab_body(doc_json, builder.tab_id)
        m_start, m_end = _find_marker_range(body, tbl_spec["marker"])
        if m_start is None or m_end is None:
            continue

        total_rows = 1 + len(tbl_spec["rows"])
        total_cols = len(tbl_spec["headers"])

        reqs = [
            {
                "deleteContentRange": {
                    "range": {
                        "startIndex": m_start,
                        "endIndex": m_end - 1,
                        "tabId": builder.tab_id,
                    }
                }
            },
            {
                "insertTable": {
                    "location": {"index": m_start, "tabId": builder.tab_id},
                    "rows": total_rows,
                    "columns": total_cols,
                }
            },
        ]
        batch_update(builder.doc_id, reqs, builder.token_path)

        doc_json = get_doc(builder.doc_id, builder.token_path)
        body = _find_tab_body(doc_json, builder.tab_id)
        tbl_el = _find_table_at_or_after(body, m_start)
        if not tbl_el:
            continue

        table_start = tbl_el["startIndex"]
        all_rows_data = [tbl_spec["headers"]] + tbl_spec["rows"]

        cell_ops = []
        for r_idx, row_obj in enumerate(tbl_el["table"].get("tableRows", [])):
            for c_idx, cell_obj in enumerate(row_obj.get("tableCells", [])):
                cell_content = cell_obj.get("content", [])
                if not cell_content:
                    continue
                first_p = cell_content[0]
                cell_start = first_p["startIndex"]
                text_val = str(all_rows_data[r_idx][c_idx]) if c_idx < len(all_rows_data[r_idx]) else ""
                cell_ops.append((cell_start, r_idx, c_idx, text_val))

        cell_ops.sort(key=lambda x: x[0], reverse=True)

        fill_reqs = []
        border_spec = {
            "color": rgb("#CBD5E1"),
            "width": {"magnitude": 0.75, "unit": "PT"},
            "dashStyle": "SOLID",
        }
        fill_reqs.append({
            "updateTableCellStyle": {
                "tableRange": {
                    "tableCellLocation": {
                        "tableStartLocation": {"index": table_start, "tabId": builder.tab_id},
                        "rowIndex": 0,
                        "columnIndex": 0,
                    },
                    "rowSpan": 1,
                    "columnSpan": total_cols,
                },
                "tableCellStyle": {
                    "backgroundColor": rgb(tbl_spec.get("header_bg", "#1E3A8A")),
                    "paddingTop": {"magnitude": 6, "unit": "PT"},
                    "paddingBottom": {"magnitude": 6, "unit": "PT"},
                    "paddingLeft": {"magnitude": 8, "unit": "PT"},
                    "paddingRight": {"magnitude": 8, "unit": "PT"},
                    "borderTop": border_spec,
                    "borderBottom": border_spec,
                    "borderLeft": border_spec,
                    "borderRight": border_spec,
                },
                "fields": "backgroundColor,paddingTop,paddingBottom,paddingLeft,paddingRight,borderTop,borderBottom,borderLeft,borderRight",
            }
        })

        for r_idx in range(1, total_rows):
            row_bg = "#F8FAFC" if r_idx % 2 == 0 else "#FFFFFF"
            fill_reqs.append({
                "updateTableCellStyle": {
                    "tableRange": {
                        "tableCellLocation": {
                            "tableStartLocation": {"index": table_start, "tabId": builder.tab_id},
                            "rowIndex": r_idx,
                            "columnIndex": 0,
                        },
                        "rowSpan": 1,
                        "columnSpan": total_cols,
                    },
                    "tableCellStyle": {
                        "backgroundColor": rgb(row_bg),
                        "paddingTop": {"magnitude": 5, "unit": "PT"},
                        "paddingBottom": {"magnitude": 5, "unit": "PT"},
                        "paddingLeft": {"magnitude": 8, "unit": "PT"},
                        "paddingRight": {"magnitude": 8, "unit": "PT"},
                        "borderTop": border_spec,
                        "borderBottom": border_spec,
                        "borderLeft": border_spec,
                        "borderRight": border_spec,
                    },
                    "fields": "backgroundColor,paddingTop,paddingBottom,paddingLeft,paddingRight,borderTop,borderBottom,borderLeft,borderRight",
                }
            })

        for cell_start, r_idx, c_idx, text_val in cell_ops:
            if not text_val:
                continue
            t_len = u16_len(text_val)
            fill_reqs.append({
                "insertText": {
                    "location": {"index": cell_start, "tabId": builder.tab_id},
                    "text": text_val,
                }
            })
            is_header = (r_idx == 0)
            is_code_col = (not is_header and c_idx == 0 and any(ch in text_val for ch in ["-", "_", "/", "CT-", "P0", "P1"]))
            fill_reqs.append({
                "updateTextStyle": {
                    "range": {
                        "startIndex": cell_start,
                        "endIndex": cell_start + t_len,
                        "tabId": builder.tab_id,
                    },
                    "textStyle": {
                        "bold": is_header or (c_idx == 0),
                        "fontSize": {"magnitude": 9.5, "unit": "PT"},
                        "foregroundColor": rgb("#FFFFFF" if is_header else "#0F172A"),
                        "weightedFontFamily": {
                            "fontFamily": "Roboto Mono" if is_code_col else "Arial",
                            "weight": 700 if (is_header or c_idx == 0) else 400,
                        },
                    },
                    "fields": "bold,fontSize,foregroundColor,weightedFontFamily",
                }
            })

        batch_update(builder.doc_id, fill_reqs, builder.token_path)


def render_blocks_into_tab(builder: TabBuilder, blocks: List[Dict[str, Any]]):
    for block in blocks:
        btype = block.get("type", "paragraph")
        if btype == "title":
            builder.add_title(
                title_text=block.get("title", ""),
                subtitle_text=block.get("subtitle", ""),
                metadata_badges=block.get("metadata", []),
            )
        elif btype == "heading":
            builder.add_heading(
                level=int(block.get("level", 1)),
                text=block.get("text", ""),
            )
        elif btype == "callout":
            builder.add_callout(
                title=block.get("title", ""),
                lines=block.get("lines", []),
                theme=block.get("theme", "amber"),
            )
        elif btype == "code_block":
            builder.add_code_block(
                label=block.get("label", "Code"),
                code_text=block.get("code", ""),
            )
        elif btype == "table":
            builder.add_table_placeholder(
                headers=block.get("headers", []),
                rows=block.get("rows", []),
                header_bg=block.get("header_bg", "#1E3A8A"),
            )
        elif btype == "bullets":
            for item in block.get("items", []):
                if isinstance(item, list):
                    builder.add_rich_paragraph(item, bullet=True)
                else:
                    builder.add_rich_paragraph([[str(item), "normal"]], bullet=True)
        elif btype == "paragraph":
            segments = block.get("segments")
            if segments:
                builder.add_rich_paragraph(
                    segments,
                    space_above=block.get("space_above", 4),
                    space_below=block.get("space_below", 6),
                    bullet=block.get("bullet", False),
                )
            else:
                builder.add_rich_paragraph(
                    [[block.get("text", ""), "normal"]],
                    space_above=block.get("space_above", 4),
                    space_below=block.get("space_below", 6),
                    bullet=block.get("bullet", False),
                )

    batch_update(builder.doc_id, builder.requests, builder.token_path)
    populate_tables_for_tab(builder)


def build_spec_document(spec_data: Dict[str, Any], existing_doc_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Create or populate a multi-tab Google Doc from a declarative spec dictionary.
    Returns metadata with documentId, documentUrl, and tabs list.
    """
    doc_title = spec_data.get("title", "Engineering Specification")
    tabs_spec = spec_data.get("tabs", [])
    if not tabs_spec:
        raise ValueError("spec_data must contain a non-empty 'tabs' list.")

    if existing_doc_id:
        doc_id = existing_doc_id
    else:
        out = run_gdocs_cli(["create", "--title", doc_title, "--json"])
        created = json.loads(out)
        doc_id = created["documentId"]

    # Always make engineering specs pageless so wide tables & code blocks never wrap badly
    run_gdocs_cli(["pageless", doc_id])

    created_tabs = []
    for idx, tab_def in enumerate(tabs_spec):
        tab_title = tab_def.get("title", f"Tab {idx + 1}")
        if idx == 0:
            tab_id = "t.0"
            run_gdocs_cli(["rename-tab", doc_id, tab_id, tab_title])
        else:
            res_out = run_gdocs_cli(["create-tab", doc_id, "--title", tab_title, "--json"])
            res_json = json.loads(res_out)
            # Extract newest tabId from list-tabs
            tabs_list_out = run_gdocs_cli(["list-tabs", doc_id, "--json"])
            tabs_list = json.loads(tabs_list_out)
            tab_id = tabs_list[-1]["tabProperties"]["tabId"]

        print(f"[{idx + 1}/{len(tabs_spec)}] Populating tab '{tab_title}' ({tab_id})...")
        builder = TabBuilder(doc_id=doc_id, tab_id=tab_id)
        render_blocks_into_tab(builder, tab_def.get("blocks", []))
        created_tabs.append({
            "tabId": tab_id,
            "title": tab_title,
            "url": f"https://docs.google.com/document/d/{doc_id}/edit?tab={tab_id}",
        })

    return {
        "documentId": doc_id,
        "title": doc_title,
        "url": f"https://docs.google.com/document/d/{doc_id}/edit",
        "tabs": created_tabs,
    }


def main():
    parser = argparse.ArgumentParser(description="Build a multi-tab Google Doc Engineering Specification from JSON.")
    parser.add_argument("spec_json", help="Path to the declarative JSON specification file.")
    parser.add_argument("--doc-id", help="Optional existing Google Doc ID to populate.", default=None)
    args = parser.parse_args()

    with open(args.spec_json, "r", encoding="utf-8") as f:
        spec_data = json.load(f)

    result = build_spec_document(spec_data, existing_doc_id=args.doc_id)
    print("\n✅ Google Doc Spec Generated Successfully!")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
