# Share

Deploy an HTML page to Vercel and get a live URL.

## Usage
`/visual-explainer:share <html-file-path>`

## Workflow
1. Verify the HTML file exists and is self-contained
2. Create a temporary directory with the HTML file as index.html
3. Deploy to Vercel using `npx vercel --yes`
4. Return the live URL to the user

## Prerequisites
- Vercel CLI installed or installable via npx
- Vercel account configured (run `vercel login` if needed)

## Notes
- The deployed page is public by default
- Consider whether content is sensitive before sharing
- Vercel free tier has deployment limits
