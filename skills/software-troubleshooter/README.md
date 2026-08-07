# Software Troubleshooter

A Gemini CLI skill for structured code inspection, troubleshooting, and root cause analysis of software issues.

## What It Does

This skill guides Gemini through a systematic code inspection workflow that produces a structured **Troubleshoot & Code Inspection Report**:

1. **Issue intake** — Gathers symptoms, environment, and observed evidence.
2. **Code inspection** — Reads source code, traces execution paths, quotes specific code blocks, and identifies conflicting logic.
3. **Historical context** — Checks git history for recent changes, reverts, or contributing factors.
4. **Impact analysis** — Assesses blast radius across UX, resources, and stability.
5. **Affected files** — Catalogs configuration, core logic, and prompt files involved.
6. **Proposed solutions** — Presents multiple fix options with trade-offs and a recommendation.
7. **Verification criteria** — Defines behavioral tests, regression checks, and edge cases.

## Installation

### Option A: Gemini CLI native

```bash
gemini skills install https://github.com/duboc/agy-skills.git --path skills/software-troubleshooter
```

### Option B: One-liner

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- software-troubleshooter
```

For user-scope installation (available across all projects):

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- software-troubleshooter --scope user
```

### Option C: Manual

```bash
cp -r skills/software-troubleshooter ~/.gemini/skills/software-troubleshooter
```

## Usage Examples

Once installed, the skill activates when you ask Gemini to troubleshoot or inspect code.

### Investigating a bug in code

```
Users are seeing duplicate notifications. I think it's in the event
handler code. Can you inspect src/handlers/notifications.py and trace
why events are being processed twice?
```

### Debugging a regression after a refactor

```
The payment flow broke after last week's refactor. Can you compare
the current code with what was there before and find the root cause?
Here's the failing test output: [paste output]
```

### Inspecting conflicting logic

```
We have two systems that both handle user session expiry — one in the
middleware and one in the auth service. Can you inspect both and tell
me if they conflict?
```

### Producing a full troubleshoot report

```
I need a formal Troubleshoot & Code Inspection Report for the
duplicate processing bug. Inspect the code, trace the logic, and
give me the full report with proposed solutions.
```

## Included References

- **report-template.md** — The structured Troubleshoot & Code Inspection Report template (8 sections).
- **code-inspection-patterns.md** — Common bug patterns, code smells, inspection techniques, and git investigation commands.

## Included Scripts

- **collect-diagnostics.sh** — Gathers project structure, git status, dependency info, and runtime versions for context.
