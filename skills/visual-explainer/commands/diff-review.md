# Diff Review

Visual diff review with architecture comparison and code review.

## Usage
`/visual-explainer:diff-review [branch-or-commit]`

## Workflow
1. Gather diff data: `git diff` or `git diff main...HEAD`
2. Analyze changed files, additions, deletions, modifications
3. Group changes by component/module
4. Read ./templates/architecture.html and ./templates/data-table.html
5. Generate HTML with:
   - Summary dashboard (files changed, lines added/removed, risk assessment)
   - Architecture impact diagram (which components are affected)
   - File-by-file change table with status indicators
   - Key code changes with before/after comparison
   - Risk flags (breaking changes, security concerns, missing tests)
6. Write to ./diagrams/diff-review-<date>.html
7. Open in browser

## Output Sections
- Executive summary with KPI cards
- Architecture impact (Mermaid diagram highlighting changed components)
- Change inventory table (file, type, risk, reviewer notes)
- Detailed review per file group
