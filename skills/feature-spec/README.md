# Feature Spec Skill

An expert Product Manager, Technical Program Manager, and Product Architect skill for the Gemini CLI and AI coding agents.

This skill equips the agent to write engineering-ready Product Requirements Documents (PRDs), traceable user stories with Given/When/Then acceptance criteria (`AC-US01-1`), WCAG 2.1 AA accessibility specs, structured API contract tables, database schema migration rules, PII data governance telemetry schemas, feature flag rollout schedules, and MoSCoW scope management.

---

## Key Features

- **6-Stage PRD Generation Pipeline**: From discovery and problem framing to engineering-ready stories, technical API tables, telemetry data governance schemas, and canary rollout plans.
- **INVEST & Traceable Acceptance Criteria**: Formats user requirements into testable scenarios (`AC-US01-1`, `AC-US01-2`) covering Happy Path, Validation Error, Auth/RBAC Restriction, and System Failure modes.
- **Structured Engineering Contracts**: Includes API contract tables (Methods, Paths, Auth Scope, Payload, Error Mapping), DB schema migration strategies, and operational SLAs (p95/p99 latency budgets).
- **Accessibility (WCAG 2.1 AA) & UI Specs**: Screen state checklists (Loading, Empty, Error, Disabled) and WCAG accessibility standards built into product templates.
- **PII Telemetry & Data Governance**: Mandatory PII data classification for telemetry events (`object_action`) with strict unhashed PII logging prohibitions.
- **AI / LLM Capability Standards**: Specialized reference module ([`references/ai-and-llm-specs.md`](file:///Users/duboc/.gemini/config/skills/feature-spec/references/ai-and-llm-specs.md)) covering model fallback architecture, confidence score thresholds, and token cost caps.
- **MoSCoW & Scope Equalizer**: Prevents scope creep by enforcing non-goals and v1 MVP trade-off boundaries.

---

## Skill Structure

```
feature-spec/
├── SKILL.md                          # Main skill system prompt and workflow pipeline
├── README.md                         # Skill overview documentation
├── references/
│   ├── prd-template.md              # Complete 12-section PRD template layout
│   ├── user-stories-and-requirements.md # INVEST stories, Given/When/Then, and MoSCoW rules
│   ├── metrics-and-scope.md         # Leading/lagging metrics, counter-metrics, and scope equalizer
│   ├── technical-and-edge-cases.md  # API tables, DB schemas, SLAs, and edge case checklist
│   ├── analytics-spec.md            # Telemetry schemas (`object_action`) and PII governance
│   └── ai-and-llm-specs.md          # Non-determinism, fallback models, and token budget rules
└── examples/
    └── sample-prd.md                # Reference sample enterprise PRD deliverable
```

---

## Usage Examples

Trigger this skill in conversation by asking:
- *"Write a PRD for an enterprise SAML SSO feature."*
- *"Generate user stories and Given/When/Then acceptance criteria for a file upload component."*
- *"Create an analytics tracking spec and PII data governance plan for our new checkout flow."*
- *"Audit this feature specification and help us prune scope for a v1 MVP."*
- *"Write technical edge cases and API contract specifications for our notification service."*
