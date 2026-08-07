# Generate Visual Plan

Generate a visual implementation plan for a feature or task.

## Usage
`/visual-explainer:generate-visual-plan <feature-description>`

## Workflow
1. Analyze the feature/task to identify components, phases, and dependencies
2. Read ./templates/architecture.html for layout patterns
3. Structure as: Overview → Phases → File Changes → Dependencies → Risks
4. Use CSS Grid cards for phases with flow arrows showing sequence
5. Include file structure with descriptions (not full code)
6. Key code snippets in collapsible sections
7. Generate self-contained HTML with Blueprint aesthetic
8. Write to ./diagrams/<plan-slug>.html
9. Open in browser

## Output Structure
- Hero section: plan title, summary, scope
- Phase cards: numbered, with status indicators
- File map: tree structure with change descriptions
- Dependency diagram: Mermaid flowchart of component relationships
- Risk assessment: table with severity indicators
- Timeline: estimated phases with milestones
