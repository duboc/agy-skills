# Design Critique Skill

An expert Design Reviewer and UX Auditor skill for the Gemini CLI and AI coding agents.

This skill equips the agent to systematically evaluate UI/UX designs, wireframes, mockups, screenshots, and front-end code (HTML, Tailwind CSS, React, Vue) for usability, visual hierarchy, consistency, accessibility (WCAG), and design principles.

---

## Features

- **Structured Review Framework**: Evaluates designs across 5 core pillars: First Impression, Usability, Visual Hierarchy, Consistency, and Accessibility.
- **Severity-Based Prioritization**: Groups findings into P0 (Critical Blockers), P1 (Major Improvements), and P2 (Polish & Quick Wins).
- **Specialized Critique Modes**: Supports dedicated audits for Accessibility (WCAG 2.2), Conversion / CTA Optimization, Mobile Responsiveness, and Design System Code Alignment.
- **Actionable Solutions**: Delivers concrete code snippets (Tailwind/CSS), copy revisions, and visual layout suggestions.
- **UX Principles & Heuristics**: Grounds feedback in established principles like Fitts's Law, Hick's Law, Gestalt Principles, and NN/g Usability Heuristics.

---

## Skill Structure

```
design-critique/
├── SKILL.md                          # Main skill system prompt and workflow definition
├── README.md                         # Skill overview and documentation
├── references/
│   ├── critique-framework.md        # The 5-pillar design evaluation framework
│   ├── feedback-guidelines.md       # SBI model, severity ratings, and constructive phrasing
│   ├── heuristics-and-laws.md       # UX laws, Gestalt principles, and NN/g heuristics
│   └── component-checklists.md      # Quick checklists for buttons, forms, nav, modals, tables
└── examples/
    └── sample-critique.md           # Reference sample output of a complete critique
```

---

## Usage Examples

Trigger this skill in conversation by asking:
- *"Critique this dashboard screenshot."*
- *"Give me feedback on this checkout page layout."*
- *"Review this React component for accessibility and visual hierarchy issues."*
- *"Audit this landing page for conversion optimization and CTA clarity."*
- *"Perform a WCAG accessibility review of our form designs."*
