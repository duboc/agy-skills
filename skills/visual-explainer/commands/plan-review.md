# Plan Review

Compare a plan against the codebase with risk assessment.

## Usage
`/visual-explainer:plan-review <plan-file>`

## Workflow
1. Read the plan file (markdown, doc, etc.)
2. Analyze the codebase to understand current state
3. Compare plan requirements against existing implementation
4. Identify gaps, risks, and alignment issues
5. Generate HTML with:
   - Plan overview (goals, scope, timeline)
   - Requirement audit table (plan item vs current state vs gap)
   - Risk assessment with severity indicators
   - Dependency analysis (what the plan depends on)
   - Recommended adjustments
6. Write to ./diagrams/plan-review-<date>.html
7. Open in browser
