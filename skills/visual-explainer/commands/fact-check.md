# Fact Check

Verify accuracy of a document against actual code.

## Usage
`/visual-explainer:fact-check <document-path>`

## Workflow
1. Read the document (README, wiki page, design doc, etc.)
2. Extract all technical claims (API endpoints, file paths, function names, config values, architecture statements)
3. Verify each claim against the actual codebase
4. Generate HTML with:
   - Verification summary (claims checked, accurate, inaccurate, unverifiable)
   - Claim audit table with status indicators (✓ verified, ✗ incorrect, ? unverifiable)
   - Details per claim: what the doc says vs what the code shows
   - Recommended corrections
5. Write to ./diagrams/fact-check-<doc-name>.html
6. Open in browser
