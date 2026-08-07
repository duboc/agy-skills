# Project Recap

Mental model snapshot for context-switching back to a project.

## Usage
`/visual-explainer:project-recap`

## Workflow
1. Scan the project: README, package files, directory structure, recent git history
2. Identify: tech stack, architecture, recent activity, open issues
3. Generate HTML with:
   - Project identity card (name, description, stack, status)
   - Architecture overview (Mermaid or CSS Grid)
   - Recent activity timeline (last 10-20 commits)
   - Key files map (entry points, configs, tests)
   - Current state: what's in progress, what's blocked
   - Quick links: repo, docs, CI, deployments
4. Write to ./diagrams/<project-name>-recap.html
5. Open in browser
