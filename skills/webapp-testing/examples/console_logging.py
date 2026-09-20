#!/usr/bin/env python3
"""
Example: Capturing console logs during browser automation.

Usage:
    python examples/console_logging.py

Assumes a server is already running on localhost:5173.
Use with_server.py to manage the server lifecycle if needed.
"""
import os
from pathlib import Path
import tempfile
from playwright.sync_api import sync_playwright

url = 'http://localhost:5173'  # Replace with your URL

console_logs = []

with tempfile.TemporaryDirectory(prefix="agy-webapp-") as tmp_dir:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})

        # Set up console log capture
        def handle_console_message(msg):
            console_logs.append(f"[{msg.type}] {msg.text}")
            print(f"Console: [{msg.type}] {msg.text}")

        page.on("console", handle_console_message)

        # Navigate to page
        page.goto(url)
        page.wait_for_load_state('networkidle')

        # Interact with the page (triggers console logs)
        page.click('text=Dashboard')
        page.wait_for_timeout(1000)

        browser.close()

    # Save console logs inside isolated 0700 directory with 0600 permissions
    log_path = Path(tmp_dir) / "console.log"
    log_path.write_text("\n".join(console_logs), encoding="utf-8")
    os.chmod(log_path, 0o600)

    print(f"\nCaptured {len(console_logs)} console messages")
    print(f"Logs saved to isolated temp file: {log_path}")
