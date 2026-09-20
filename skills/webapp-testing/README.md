# Web Application Testing

A Agy skill for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.

## What It Does

This skill provides a structured toolkit for browser-based testing and automation:

1. **Server lifecycle management** — Automatically starts and stops development servers using the `with_server.py` helper, supporting single or multiple servers (e.g., backend + frontend).
2. **Static HTML testing** — Reads HTML files directly and automates interactions via `file://` URLs.
3. **Dynamic app testing** — Uses a reconnaissance-then-action pattern: navigate, wait for load, inspect DOM, then act.
4. **Element discovery** — Finds buttons, links, inputs, and other interactive elements on a page.
5. **Console log capture** — Records browser console output during automation for debugging.
6. **Screenshot capture** — Takes full-page screenshots for visual verification.

## When Does It Activate

The skill activates when you ask Agy to:

- Test or interact with a web application
- Take screenshots of a web page
- Debug frontend or UI behavior
- Verify forms, navigation, or UI elements
- Capture browser console logs
- Automate browser interactions with a locally running app

## Installation

### Option B: One-liner

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- webapp-testing
```

For user-scope installation (available across all projects):

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- webapp-testing --scope user
```

### Option C: Manual

```bash
cp -r skills/webapp-testing ~/.gemini/config/skills/webapp-testing
```

## Prerequisites

This skill requires Python and Playwright to be installed:

```bash
pip install playwright
playwright install chromium
```

## Usage Examples

### Testing a running development server

```
My React app is running on port 3000. Can you take a screenshot
and check if the login form renders correctly?
```

### Starting a server and running tests

```
I have a Next.js app in the frontend/ directory. Start the dev
server and verify that the dashboard page loads with all the
expected charts.
```

### Testing a static HTML file

```
I have an HTML file at src/index.html. Can you open it in the
browser and verify the form validation works?
```

### Debugging console errors

```
My app at localhost:5173 is behaving strangely. Can you capture
the browser console logs and check for errors?
```

### Discovering interactive elements

```
I need to automate some interactions with the app running on
port 8080. Can you first discover what buttons and forms are
available on the page?
```

## Included Examples

- **element_discovery.py** — Discovering buttons, links, and inputs on a page.
- **static_html_automation.py** — Using `file://` URLs for local HTML files.
- **console_logging.py** — Capturing console logs during automation.

## Included Scripts

- **with_server.py** — Manages server lifecycle: starts one or more servers, waits for them to be ready, runs a command, then cleans up.

## Included References

- **playwright-selectors-and-assertions.md** — Role/label/test-id locator priority, auto-waiting assertions, and flake-free interaction patterns.
- **visual-and-console-diagnostics.md** — Console error/pageerror capture, failed network request interception, and isolated `0700` screenshot artifacts.
