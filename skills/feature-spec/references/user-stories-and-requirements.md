# Writing User Stories, Acceptance Criteria & Traceability

## INVEST Criteria for Quality User Stories

Every user story must satisfy the **INVEST** principles:

- **I — Independent**: Stories can be built, tested, and shipped without hard temporal coupling.
- **N — Negotiable**: Captures the essence of user intent without dictating rigid code implementation.
- **V — Valuable**: Delivers clear, tangible value to an identified user persona or business process.
- **E — Estimable**: Written with sufficient clarity for engineering to size effort (points/days).
- **S — Small**: Sized to complete within 1-3 days of engineering effort.
- **T — Testable**: Includes unambiguous acceptance criteria enabling QA to write direct test cases.

---

## Traceability ID Naming Scheme

Assign unique, immutable traceability IDs to every story and acceptance criterion:
- **Story Identifier**: `US-01`, `US-02`, etc.
- **Acceptance Criterion Identifier**: `AC-[StoryID]-[Number]` (e.g., `AC-US01-1`, `AC-US01-2`).

This ensures direct 1-to-1 mapping across Jira/Linear tickets, Figma specs, PRD requirements, and QA automated test suites.

---

## Given/When/Then Acceptance Criteria Syntax

Structure all acceptance criteria using the 3-clause pattern:

- **Given**: Initial system state, user authentication, or pre-existing database context.
- **When**: The specific action taken by the user or triggered by an external webhook/system event.
- **Then**: The resulting state change, UI update, database mutation, or telemetry log.

### Required 4-Path Coverage Matrix
Every user story must provide Given/When/Then scenarios for all 4 paths:

1. **Happy Path (`AC-USXX-1`)**: The standard successful execution flow.
2. **Validation / Input Boundary Path (`AC-USXX-2`)**: Client/server validation, missing fields, max length overflows, invalid formats.
3. **Auth & RBAC Restriction Path (`AC-USXX-3`)**: Unauthorized user, expired token, insufficient role level (e.g. `Viewer` trying to `Edit`).
4. **System Failure & Recovery Path (`AC-USXX-4`)**: Network timeout, API 500 error, DB lock contention, offline behavior.

---

## MoSCoW Prioritization Challenge Rules

Apply these strict criteria during scope refinement:

- **Must-Have (P0)**: *"If this criterion is omitted, will the core feature fail completely or violate security/compliance rules?"* If no, downgrade to P1.
- **Should-Have (P1)**: *"Does this significantly improve efficiency or UX, but a viable workaround exists?"*
- **Could-Have (P2)**: *"Is this visual polish or micro-interaction delight that can wait for v2?"*
- **Won't-Have (Non-Goal)**: *"Is this explicitly out of scope for the current iteration?"*
