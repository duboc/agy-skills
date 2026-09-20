# Share

Deploy an HTML page to Vercel and get a live URL.

## Usage
`/visual-explainer:share <html-file-path>`

## Workflow
1. Verify the HTML file exists and is self-contained
2. Create a temporary directory with the HTML file as index.html
3. Use the user's authorized hosting destination and existing project configuration. If Vercel is selected, inspect the target project/account and deploy the prepared directory using the installed CLI. Do not infer production deployment or a new hosting account from a request for a local file.
4. Return the live URL to the user

## Prerequisites
- Vercel CLI installed or installable via npx
- Vercel account configured (run `vercel login` if needed)

## Notes
- The deployed page is public by default
- Inspect rendered content, notes and embedded data for private identifiers before public sharing; report any required redactions.
- Vercel free tier has deployment limits
