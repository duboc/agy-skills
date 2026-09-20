#!/usr/bin/env python3
"""
Example: Automating interaction with static HTML files using file:// URLs.

Usage:
    python examples/static_html_automation.py

No server needed — opens HTML files directly in the browser.
"""
import os
from pathlib import Path
import tempfile
from playwright.sync_api import sync_playwright

html_file_path = os.path.abspath('path/to/your/file.html')
file_url = f'file://{html_file_path}'

with tempfile.TemporaryDirectory(prefix="agy-webapp-") as tmp_dir, sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})

    # Navigate to local HTML file
    page.goto(file_url)

    # Take screenshot in isolated 0700 temp directory
    before_path = Path(tmp_dir) / "static_page.png"
    after_path = Path(tmp_dir) / "after_submit.png"
    page.screenshot(path=str(before_path), full_page=True)

    # Interact with elements
    page.click('text=Click Me')
    page.fill('#name', 'John Doe')
    page.fill('#email', 'john@example.com')

    # Submit form
    page.click('button[type="submit"]')
    page.wait_for_timeout(500)

    # Take final screenshot
    page.screenshot(path=str(after_path), full_page=True)

    browser.close()

    print("Static HTML automation completed!")
    print(f"Screenshots saved to {before_path} and {after_path}")
