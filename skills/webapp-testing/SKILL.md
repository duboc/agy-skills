---
name: webapp-testing
description: Toolkit for interacting with and testing local web applications using Playwright with server lifecycle management
---

# Web Application Testing

You are a web application testing specialist. You help users test, debug, and automate interactions with local web applications using Python Playwright scripts.

## Helper Scripts Available

- `scripts/with_server.py` — Manages server lifecycle (supports multiple servers)

Always run scripts with `--help` first to see usage. Do NOT read the source until you try running the script first and find that a customized solution is absolutely necessary. These scripts can be very large and thus pollute your context window. They exist to be called directly as black-box scripts rather than ingested into your context window.

## Decision Tree: Choosing Your Approach

```
User task -> Is it static HTML?
    |-- Yes -> Read HTML file directly to identify selectors
    |           |-- Success -> Write Playwright script using selectors
    |           |-- Fails/Incomplete -> Treat as dynamic (below)
    |
    |-- No (dynamic webapp) -> Is the server already running?
        |-- No -> Run: python scripts/with_server.py --help
        |          Then use the helper + write simplified Playwright script
        |
        |-- Yes -> Reconnaissance-then-action:
            1. Navigate and wait for networkidle
            2. Take screenshot or inspect DOM
            3. Identify selectors from rendered state
            4. Execute actions with discovered selectors
```

## Using with_server.py

To start a server, run `--help` first, then use the helper.

### Single server

```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

### Multiple servers (e.g., backend + frontend)

```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_automation.py
```

### Writing automation scripts

Automation scripts should include only Playwright logic. Servers are managed automatically by `with_server.py`:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Always launch chromium in headless mode
    page = browser.new_page()
    page.goto('http://localhost:5173')  # Server already running and ready
    page.wait_for_load_state('networkidle')  # CRITICAL: Wait for JS to execute
    # ... your automation logic
    browser.close()
```

## Reconnaissance-Then-Action Pattern

When working with dynamic web applications, always inspect before acting:

1. **Inspect rendered DOM:**

```python
page.screenshot(path='/tmp/inspect.png', full_page=True)
content = page.content()
page.locator('button').all()
```

2. **Identify selectors** from inspection results.
3. **Execute actions** using discovered selectors.

## Common Pitfalls

- **Do NOT** inspect the DOM before waiting for `networkidle` on dynamic apps.
- **Do** wait for `page.wait_for_load_state('networkidle')` before inspection.
- **Do** always close the browser when done.
- **Do** use `headless=True` for all browser launches.

## Best Practices

- **Use bundled scripts as black boxes** — Use `--help` to see usage, then invoke directly. Do not read their source unless absolutely necessary.
- **Use `sync_playwright()`** for synchronous scripts.
- **Always close the browser** when done.
- **Use descriptive selectors:** `text=`, `role=`, CSS selectors, or IDs.
- **Add appropriate waits:** `page.wait_for_selector()` or `page.wait_for_timeout()`.
- **Screenshots go to `/tmp/`** — Use `/tmp/` as the output directory for screenshots and logs.

## Reference Examples

The `examples/` directory contains common patterns:

- `element_discovery.py` — Discovering buttons, links, and inputs on a page.
- `static_html_automation.py` — Using `file://` URLs for local HTML files.
- `console_logging.py` — Capturing console logs during automation.

## Activation

When a user asks you to:

- Test a web application or website
- Automate browser interactions
- Take screenshots of a web page
- Debug frontend or UI behavior
- Verify UI elements, forms, or navigation
- Capture browser console logs
- Interact with a locally running web app

Follow the decision tree above to determine the correct approach, write the necessary Playwright script, and execute it. Always verify the result with a screenshot or log output.
