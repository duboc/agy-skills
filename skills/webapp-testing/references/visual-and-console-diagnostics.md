# Visual Regression, Console Error & Network Diagnostics Guide

Use this diagnostic template to capture uncaught JavaScript exceptions, console errors, failed HTTP requests (`>= 400`), and responsive screenshots inside a user-isolated temporary directory (`0700`).

---

## 1. Full Telemetry & Screenshot Harness (`Python`)

```python
import os
import tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright

def run_diagnostic_probe(target_url: str) -> None:
    console_errors: list[str] = []
    page_exceptions: list[str] = []
    failed_requests: list[str] = []

    with tempfile.TemporaryDirectory(prefix="webapp_audit_") as tmp_dir:
        os.chmod(tmp_dir, 0o700)
        artifact_dir = Path(tmp_dir)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width": 1440, "height": 900})
            page = context.new_page()

            page.on(
                "console",
                lambda msg: console_errors.append(f"[{msg.type}] {msg.text}")
                if msg.type in {"error", "warning"}
                else None,
            )
            page.on("pageerror", lambda exc: page_exceptions.append(str(exc)))
            page.on(
                "response",
                lambda res: failed_requests.append(f"{res.status} {res.url}")
                if res.status >= 400
                else None,
            )

            page.goto(target_url, wait_until="networkidle")
            screenshot_path = artifact_dir / "desktop_1440x900.png"
            page.screenshot(path=str(screenshot_path), full_page=True)
            os.chmod(screenshot_path, 0o600)
            browser.close()

        assert not page_exceptions, f"Uncaught page errors: {page_exceptions}"
        assert not failed_requests, f"Failed HTTP responses: {failed_requests}"
```

---

## 2. Responsive Viewport Verification Matrix

| Device Profile | Viewport (`width × height`) | Primary Checks |
|----------------|-----------------------------|----------------|
| Desktop Widescreen | `1440 × 900` | Multi-column grid alignment, sticky nav, table overflow |
| Tablet Landscape / Kiosk | `1024 × 768` | Touch target size (`>= 44×44 px`), modal viewport clipping |
| Mobile Portrait | `390 × 844` | Zero horizontal scrollbar (`document.documentElement.scrollWidth <= window.innerWidth`), drawer navigation |
