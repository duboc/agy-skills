# Playwright Resilient Locators, Web-First Assertions & Hydration Guide

Use these patterns to write deterministic, non-flaky Playwright Python scripts against React, Next.js, Vue, and Vite web applications.

---

## 1. Locator Priority Hierarchy (Resilience Order)

Always prefer user-facing accessible locators over fragile CSS class or XPath selectors:

| Priority | Locator API | Example | Why |
|----------|-------------|---------|-----|
| **1 (Best)** | `page.get_by_role()` | `page.get_by_role("button", name="Submit Order")` | Verifies both semantic HTML role and accessible name |
| **2** | `page.get_by_label()` | `page.get_by_label("Email address")` | Verifies `<label for="...">` or `aria-label` binding on form inputs |
| **3** | `page.get_by_placeholder()` | `page.get_by_placeholder("Search projects...")` | Fallback for unlabeled search inputs |
| **4** | `page.get_by_text()` | `page.get_by_text("Payment confirmed", exact=True)` | Verifies visible copy rendered to users |
| **5** | `page.get_by_test_id()` | `page.get_by_test_id("checkout-summary-card")` | Stable contract for dynamic containers lacking unique text |
| **Avoid** | `.locator(".css-1x9a2b")` | Styled-components / Tailwind utility chains | Breaks on minor styling refactors |

---

## 2. Synchronization & SPA Hydration Rules

1. **Never use fixed `time.sleep()` for DOM readiness.**
2. **Wait for Initial Network & Hydration**:
   ```python
   page.goto("http://localhost:5173", wait_until="domcontentloaded")
   page.wait_for_load_state("networkidle")
   ```
3. **Use Web-First Auto-Retrying Assertions (`expect`)**:
   ```python
   from playwright.sync_api import expect

   submit_btn = page.get_by_role("button", name="Create Account")
   expect(submit_btn).to_be_visible()
   expect(submit_btn).to_be_enabled()
   submit_btn.click()

   expect(page.get_by_role("alert")).to_contain_text("Account created")
   ```

---

## 3. Multi-Server Orchestration with `scripts/with_server.py`

When testing a full-stack application with a separate backend API and frontend dev server, pass explicit command arguments (never `shell=True`) to `with_server.py`:

```bash
python3 scripts/with_server.py \
  --server "uvicorn app.main:app --port 8000" --port 8000 \
  --server "npm run dev -- --port 5173" --port 5173 \
  -- python3 tests/e2e_verify.py
```
