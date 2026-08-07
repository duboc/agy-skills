# Generate Web Diagram

Generate an HTML diagram for any topic. This is the general-purpose diagram command.

## Usage
`/visual-explainer:generate-web-diagram <topic>`

## Workflow
1. Analyze the topic to determine the best diagram type (architecture, flowchart, sequence, ER, state machine, mind map, data flow, C4)
2. Choose an aesthetic direction that matches the content
3. Select the appropriate rendering approach (Mermaid vs CSS Grid vs hybrid)
4. Read the relevant template from ./templates/
5. Generate a self-contained HTML file
6. Write to ./diagrams/<topic-slug>.html
7. Open in browser

## Input
- Topic description or technical concept to visualize
- Optional: specific diagram type preference
- Optional: aesthetic preference

## Output
- Self-contained HTML file with the diagram
- File path printed to chat
- Browser opened automatically
