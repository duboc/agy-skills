#!/usr/bin/env python3
"""
HTML -> LibreOffice -> Google Workspace Exporter (Slides, Docs, Sheets)
=======================================================================
1. Reads a self-contained Google Cloud HTML artifact (.html).
2. Uses headless LibreOffice (`soffice --headless`) in an isolated 0700 working
   directory to generate the local asset file:
   - slides -> .pptx (via Flat ODP .fodp + LibreOffice Impress conversion) & .pdf QA
   - docs   -> .docx (via LibreOffice Writer HTML-to-DOCX conversion)
   - sheets -> .xlsx (via LibreOffice Calc HTML-to-XLSX conversion)
3. Uploads the local asset file to Google Drive API v3 with target Google Workspace
   mimeType conversion:
   - slides -> application/vnd.google-apps.presentation
   - docs   -> application/vnd.google-apps.document
   - sheets -> application/vnd.google-apps.spreadsheet
"""

import argparse
import html.parser
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
import uuid
import xml.sax.saxutils as saxutils
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


WORKSPACE_MIME_TYPES: Dict[str, Tuple[str, str, str]] = {
    "slides": (
        "application/vnd.google-apps.presentation",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "https://docs.google.com/presentation/d/{file_id}/edit",
    ),
    "docs": (
        "application/vnd.google-apps.document",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "https://docs.google.com/document/d/{file_id}/edit",
    ),
    "sheets": (
        "application/vnd.google-apps.spreadsheet",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "https://docs.google.com/spreadsheets/d/{file_id}/edit",
    ),
}


class SlideHTMLParser(html.parser.HTMLParser):
    """Extracts <section class="slide ..."> blocks, headings, bullets, and speaker notes from HTML."""

    def __init__(self) -> None:
        super().__init__()
        self.slides: List[Dict[str, Any]] = []
        self._current_slide: Optional[Dict[str, Any]] = None
        self._current_tag: Optional[str] = None
        self._in_notes: bool = False
        self._buffer: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        attr_map = {k: (v or "") for k, v in attrs}
        classes = set(attr_map.get("class", "").split())

        if tag == "section" and ("slide" in classes or self._current_slide is None):
            slide_class = "default"
            for candidate in ("title", "section", "invert", "lead", "stats", "quote", "closing"):
                if candidate in classes:
                    slide_class = candidate
                    break
            self._current_slide = {
                "class": slide_class,
                "h1": [],
                "h2": [],
                "body": [],
                "notes": [],
            }
            self.slides.append(self._current_slide)
            return

        if self._current_slide is None:
            return

        if tag == "aside" or "notes" in classes:
            self._in_notes = True
            self._buffer = []
        elif tag in ("h1", "h2", "h3", "p", "li", "blockquote"):
            self._current_tag = tag
            self._buffer = []

    def handle_endtag(self, tag: str) -> None:
        if self._current_slide is None:
            return

        if tag == "section":
            self._current_slide = None
            self._current_tag = None
            self._in_notes = False
            return

        if tag == "aside" and self._in_notes:
            text = " ".join("".join(self._buffer).split())
            if text:
                self._current_slide["notes"].append(text)
            self._in_notes = False
            self._buffer = []
            return

        if tag == self._current_tag:
            text = " ".join("".join(self._buffer).split())
            if text:
                if self._in_notes:
                    self._current_slide["notes"].append(text)
                elif tag == "h1":
                    self._current_slide["h1"].append(text)
                elif tag in ("h2", "h3"):
                    self._current_slide["h2"].append(text)
                else:
                    self._current_slide["body"].append(text)
            self._current_tag = None
            self._buffer = []

    def handle_data(self, data: str) -> None:
        if self._current_slide is not None and (self._current_tag is not None or self._in_notes):
            self._buffer.append(data)


def find_soffice_binary() -> str:
    for candidate in (
        os.environ.get("SOFFICE_BIN", ""),
        shutil.which("soffice") or "",
        shutil.which("libreoffice") or "",
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
        "/usr/bin/soffice",
        "/usr/bin/libreoffice",
    ):
        if candidate and os.path.exists(candidate):
            return candidate
    raise FileNotFoundError(
        "LibreOffice binary ('soffice' or 'libreoffice') not found. "
        "Install LibreOffice (e.g., 'brew install --cask libreoffice') or set SOFFICE_BIN."
    )


def build_google_cloud_fodp(slides: List[Dict[str, Any]]) -> str:
    """Builds a 16:9 Google Cloud styled Flat OpenDocument Presentation (.fodp) for LibreOffice Impress."""
    if not slides:
        slides = [{"class": "title", "h1": ["Presentation"], "h2": [], "body": [], "notes": []}]

    pages_xml: List[str] = []
    for idx, slide in enumerate(slides, 1):
        sclass = slide.get("class", "default")
        bg_style = "GCloudBgWhite"
        title_style = "GCloudTitleDark"
        body_style = "GCloudBodyDark"
        if sclass == "section":
            bg_style = "GCloudBgBlue"
            title_style = "GCloudTitleWhite"
            body_style = "GCloudBodyWhite"
        elif sclass == "invert":
            bg_style = "GCloudBgDark"
            title_style = "GCloudTitleWhite"
            body_style = "GCloudBodyWhite"

        headline_items = slide.get("h1") or slide.get("h2") or [f"Slide {idx}"]
        headline_text = saxutils.escape(" — ".join(headline_items))
        sub_items: List[str] = []
        if slide.get("h1") and slide.get("h2"):
            sub_items.extend(slide["h2"])
        sub_items.extend(slide.get("body", []))

        body_paras = "".join(
            f'<text:p text:style-name="{body_style}">{saxutils.escape(line)}</text:p>'
            for line in sub_items
        )
        notes_paras = "".join(
            f'<text:p text:style-name="GCloudBodyDark">{saxutils.escape(note)}</text:p>'
            for note in slide.get("notes", [])
        )

        gradient_bar = ""
        if sclass in ("title", "closing"):
            gradient_bar = (
                '<draw:rect draw:style-name="GCloudBarBlue" svg:x="0cm" svg:y="15.35cm" svg:width="7cm" svg:height="0.4cm"/>'
                '<draw:rect draw:style-name="GCloudBarRed" svg:x="7cm" svg:y="15.35cm" svg:width="7cm" svg:height="0.4cm"/>'
                '<draw:rect draw:style-name="GCloudBarYellow" svg:x="14cm" svg:y="15.35cm" svg:width="7cm" svg:height="0.4cm"/>'
                '<draw:rect draw:style-name="GCloudBarGreen" svg:x="21cm" svg:y="15.35cm" svg:width="7cm" svg:height="0.4cm"/>'
            )

        page_xml = f"""
      <draw:page draw:name="Slide_{idx}" draw:master-page-name="GoogleCloud16x9">
        <draw:rect draw:style-name="{bg_style}" svg:x="0cm" svg:y="0cm" svg:width="28cm" svg:height="15.75cm"/>
        <draw:frame draw:style-name="GCloudTextFrame" svg:x="2.0cm" svg:y="2.2cm" svg:width="24.0cm" svg:height="4.5cm">
          <draw:text-box>
            <text:p text:style-name="{title_style}">{headline_text}</text:p>
          </draw:text-box>
        </draw:frame>
        <draw:frame draw:style-name="GCloudTextFrame" svg:x="2.0cm" svg:y="7.0cm" svg:width="24.0cm" svg:height="7.2cm">
          <draw:text-box>
            {body_paras}
          </draw:text-box>
        </draw:frame>
        {gradient_bar}
        <presentation:notes>
          <draw:frame draw:style-name="GCloudTextFrame" svg:x="2.0cm" svg:y="2.0cm" svg:width="17.0cm" svg:height="10.0cm">
            <draw:text-box>
              {notes_paras}
            </draw:text-box>
          </draw:frame>
        </presentation:notes>
      </draw:page>"""
        pages_xml.append(page_xml)

    all_pages = "\n".join(pages_xml)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<office:document xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
  xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
  xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
  xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
  xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
  xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
  xmlns:presentation="urn:oasis:names:tc:opendocument:xmlns:presentation:1.0"
  office:version="1.2"
  office:mimetype="application/vnd.oasis.opendocument.presentation">
  <office:automatic-styles>
    <style:page-layout style:name="PM16x9">
      <style:page-layout-properties fo:page-width="28cm" fo:page-height="15.75cm" style:print-orientation="landscape"/>
    </style:page-layout>
    <style:style style:name="GCloudBgWhite" style:family="graphic">
      <style:graphic-properties draw:stroke="none" draw:fill="solid" draw:fill-color="#ffffff"/>
    </style:style>
    <style:style style:name="GCloudBgBlue" style:family="graphic">
      <style:graphic-properties draw:stroke="none" draw:fill="solid" draw:fill-color="#4285f4"/>
    </style:style>
    <style:style style:name="GCloudBgDark" style:family="graphic">
      <style:graphic-properties draw:stroke="none" draw:fill="solid" draw:fill-color="#202124"/>
    </style:style>
    <style:style style:name="GCloudBarBlue" style:family="graphic">
      <style:graphic-properties draw:stroke="none" draw:fill="solid" draw:fill-color="#4285f4"/>
    </style:style>
    <style:style style:name="GCloudBarRed" style:family="graphic">
      <style:graphic-properties draw:stroke="none" draw:fill="solid" draw:fill-color="#ea4335"/>
    </style:style>
    <style:style style:name="GCloudBarYellow" style:family="graphic">
      <style:graphic-properties draw:stroke="none" draw:fill="solid" draw:fill-color="#fbbc05"/>
    </style:style>
    <style:style style:name="GCloudBarGreen" style:family="graphic">
      <style:graphic-properties draw:stroke="none" draw:fill="solid" draw:fill-color="#34a853"/>
    </style:style>
    <style:style style:name="GCloudTextFrame" style:family="graphic">
      <style:graphic-properties draw:stroke="none" draw:fill="none"/>
    </style:style>
    <style:style style:name="GCloudTitleDark" style:family="paragraph">
      <style:text-properties fo:font-family="Roboto, Arial, sans-serif" fo:font-size="32pt" fo:font-weight="bold" fo:color="#202124"/>
    </style:style>
    <style:style style:name="GCloudTitleWhite" style:family="paragraph">
      <style:text-properties fo:font-family="Roboto, Arial, sans-serif" fo:font-size="32pt" fo:font-weight="bold" fo:color="#ffffff"/>
    </style:style>
    <style:style style:name="GCloudBodyDark" style:family="paragraph">
      <style:paragraph-properties fo:margin-bottom="0.35cm"/>
      <style:text-properties fo:font-family="Roboto, Arial, sans-serif" fo:font-size="18pt" fo:color="#5f6368"/>
    </style:style>
    <style:style style:name="GCloudBodyWhite" style:family="paragraph">
      <style:paragraph-properties fo:margin-bottom="0.35cm"/>
      <style:text-properties fo:font-family="Roboto, Arial, sans-serif" fo:font-size="18pt" fo:color="#e8eaed"/>
    </style:style>
  </office:automatic-styles>
  <office:master-styles>
    <style:master-page style:name="GoogleCloud16x9" style:page-layout-name="PM16x9"/>
  </office:master-styles>
  <office:body>
    <office:presentation>
{all_pages}
    </office:presentation>
  </office:body>
</office:document>
"""


def convert_html_with_libreoffice(
    html_path: Path,
    platform: str,
    work_dir: Path,
    output_path: Optional[Path] = None,
) -> Path:
    """Runs headless LibreOffice to convert the HTML artifact into the local platform asset (.pptx, .docx, .xlsx)."""
    soffice_bin = find_soffice_binary()
    stem = html_path.stem

    if platform == "slides":
        parser = SlideHTMLParser()
        parser.feed(html_path.read_text(encoding="utf-8", errors="replace"))
        fodp_path = work_dir / f"{stem}.fodp"
        fodp_path.write_text(build_google_cloud_fodp(parser.slides), encoding="utf-8")
        os.chmod(fodp_path, 0o600)

        subprocess.run(
            [soffice_bin, "--headless", "--convert-to", "pptx", "--outdir", str(work_dir), str(fodp_path)],
            check=True,
            capture_output=True,
            text=True,
        )
        local_asset = work_dir / f"{stem}.pptx"
    elif platform == "docs":
        subprocess.run(
            [
                soffice_bin,
                "--headless",
                "--writer",
                "--convert-to",
                "docx:MS Word 2007 XML",
                "--outdir",
                str(work_dir),
                str(html_path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        local_asset = work_dir / f"{stem}.docx"
    elif platform == "sheets":
        subprocess.run(
            [
                soffice_bin,
                "--headless",
                "--calc",
                '--infilter=html:HTML (StarCalc)',
                "--convert-to",
                "xlsx",
                "--outdir",
                str(work_dir),
                str(html_path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        local_asset = work_dir / f"{stem}.xlsx"
    else:
        raise ValueError(f"Unsupported platform '{platform}'. Expected 'slides', 'docs', or 'sheets'.")

    if not local_asset.exists():
        raise RuntimeError(f"LibreOffice did not produce expected local asset: {local_asset}")

    final_path = output_path or html_path.with_suffix(local_asset.suffix)
    shutil.copy2(local_asset, final_path)
    return final_path


def resolve_access_token() -> str:
    """Resolves a Google OAuth access token from GCLI_ACCESS_TOKEN_PATH, ~/.cache, or gcloud auth."""
    env_token_path = os.environ.get("GCLI_ACCESS_TOKEN_PATH")
    candidates = [
        Path(env_token_path).expanduser() if env_token_path else None,
        Path.home() / ".cache" / "gdoc-spec" / "access_token",
    ]
    for token_file in candidates:
        if token_file and token_file.exists():
            if os.name != "nt":
                mode = token_file.stat().st_mode & 0o777
                if mode & 0o077:
                    os.chmod(token_file, 0o600)
            token = token_file.read_text(encoding="utf-8").strip()
            if token:
                return token

    gcloud_bin = shutil.which("gcloud")
    if gcloud_bin:
        res = subprocess.run(
            [gcloud_bin, "auth", "print-access-token"],
            check=True,
            capture_output=True,
            text=True,
        )
        token = res.stdout.strip()
        if token:
            return token

    raise RuntimeError(
        "No Google OAuth access token found. Set GCLI_ACCESS_TOKEN_PATH (0600 permissions) "
        "or authenticate with 'gcloud auth login'."
    )


def upload_to_google_workspace(
    local_asset_path: Path,
    platform: str,
    title: str,
    folder_id: Optional[str] = None,
) -> Dict[str, str]:
    """Uploads the local LibreOffice asset to Google Drive and converts it to Docs, Slides, or Sheets."""
    target_mime, source_mime, url_template = WORKSPACE_MIME_TYPES[platform]
    token = resolve_access_token()

    metadata: Dict[str, Any] = {
        "name": title,
        "mimeType": target_mime,
    }
    if folder_id:
        metadata["parents"] = [folder_id]

    boundary = f"gcloud_boundary_{uuid.uuid4().hex}"
    meta_bytes = json.dumps(metadata).encode("utf-8")
    file_bytes = local_asset_path.read_bytes()

    body = (
        f"--{boundary}\r\n"
        "Content-Type: application/json; charset=UTF-8\r\n\r\n"
    ).encode("utf-8") + meta_bytes + (
        f"\r\n--{boundary}\r\n"
        f"Content-Type: {source_mime}\r\n\r\n"
    ).encode("utf-8") + file_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")

    req = urllib.request.Request(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&fields=id,name,mimeType,webViewLink",
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/related; boundary={boundary}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        err_text = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Google Drive upload failed (HTTP {exc.code}): {err_text}") from exc

    file_id = payload["id"]
    return {
        "id": file_id,
        "name": payload.get("name", title),
        "mimeType": payload.get("mimeType", target_mime),
        "localAsset": str(local_asset_path),
        "url": payload.get("webViewLink") or url_template.format(file_id=file_id),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert Google Cloud HTML via LibreOffice and upload to Google Workspace (Slides, Docs, Sheets)."
    )
    parser.add_argument("html_file", help="Path to the input .html file")
    parser.add_argument(
        "--platform",
        choices=["slides", "docs", "sheets"],
        default="slides",
        help="Target Google Workspace platform (default: slides)",
    )
    parser.add_argument("--title", help="Document title in Google Workspace (defaults to HTML filename stem)")
    parser.add_argument("--output", help="Optional path for the local LibreOffice asset (.pptx, .docx, .xlsx)")
    parser.add_argument("--folder-id", help="Optional Google Drive parent folder ID")
    parser.add_argument(
        "--upload",
        action="store_true",
        help="Upload the LibreOffice-generated local asset to Google Drive and convert to native Google Workspace format",
    )
    args = parser.parse_args()

    html_path = Path(args.html_file).resolve()
    if not html_path.exists():
        sys.exit(f"Input HTML file not found: {html_path}")

    os.umask(0o077)
    cache_root = Path.home() / ".cache" / "gcloud-workspace-export"
    cache_root.mkdir(parents=True, exist_ok=True)
    os.chmod(cache_root, 0o700)

    with tempfile.TemporaryDirectory(dir=str(cache_root)) as tmp_dir:
        work_dir = Path(tmp_dir)
        os.chmod(work_dir, 0o700)
        out_path = Path(args.output).resolve() if args.output else None
        local_asset = convert_html_with_libreoffice(
            html_path=html_path,
            platform=args.platform,
            work_dir=work_dir,
            output_path=out_path,
        )

        result: Dict[str, Any] = {
            "platform": args.platform,
            "htmlSource": str(html_path),
            "localAsset": str(local_asset),
        }

        if args.upload:
            title = args.title or html_path.stem
            upload_info = upload_to_google_workspace(
                local_asset_path=local_asset,
                platform=args.platform,
                title=title,
                folder_id=args.folder_id,
            )
            result.update(upload_info)

        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
