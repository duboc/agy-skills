# Standard PRD Structure Template

Use this comprehensive template to generate engineering-ready Product Requirements Documents.

---

# 📄 Product Requirements Document: [Feature Name]

| Metadata | Details |
|---|---|
| **Author / Role** | [PM Name / Role] |
| **Status** | [Draft / Under Review / Approved / In Development] |
| **Target Release** | [e.g., Q3 2026 / Sprint 16] |
| **Feature Flag Key** | `[e.g., ff_sso_enforcement_v1]` |
| **Primary Stakeholders** | Eng Lead, Design Lead, QA Lead, Security, Data Eng |

---

## 1. Problem Statement & Evidence
- **The Core Pain**: Describe the problem in 2-3 concise sentences.
- **Affected User Segment**: Who experiences this pain and how frequently?
- **Evidence & Data**: Customer quotes, support ticket volume, dropoff analytics, or user research findings.
- **Cost of Inaction**: What happens if we do not solve this now (e.g. churn risk, lost revenue, compliance penalty)?

---

## 2. Goals & Success Metrics
- **Business & User Goals**: 3-5 measurable outcomes (e.g., "Reduce onboarding dropoff from 35% to 15%").
- **Success Metrics Table**:
  | Metric Type | Metric Name | Baseline | Target | Measurement Source |
  |---|---|---|---|---|
  | Leading | 7-day Activation Rate | 20% | 45% | Mixpanel / PostHog |
  | Lagging | 30-day Account Retention | 60% | 72% | Datadog / Analytics |
  | Counter-Metric | Support Ticket Volume | < 50/wk | < 50/wk | Zendesk |

---

## 3. Non-Goals (Scope Boundaries)
- **Explicit Non-Goals**: 3-5 capabilities explicitly excluded from this version.
  - *Non-Goal 1*: [Capability] — *Rationale*: [Why excluded for v1].
  - *Non-Goal 2*: [Capability] — *Rationale*: [Why excluded for v1].

---

## 4. Personas & Jobs-to-be-Done (JTBD)
- **Persona 1**: `[Persona Name]` — *When I am [situation], I want to [motivation], so that I can [expected outcome].*

---

## 5. UI/UX & Accessibility Specifications
- **Figma Design Link**: `[Link to Figma Specs / Prototypes]`
- **Design System Components**: `[List reused or new components, e.g., Modal, Select, StatusBadge]`
- **Screen States Matrix**:
  - `[ ] Default State`  `[ ] Hover/Active`  `[ ] Loading/Skeleton`  `[ ] Empty State`  `[ ] Error Toast`  `[ ] Disabled`
- **Accessibility (WCAG 2.1 AA Checklist)**:
  - `[ ] Keyboard Nav`: All interactive elements reachable via `Tab` / `Shift+Tab` with visible focus rings.
  - `[ ] Screen Readers`: Form fields have associated `<label>` or `aria-label`; dynamic updates use `aria-live`.
  - `[ ] Color Contrast`: Minimum 4.5:1 ratio for body text, 3:1 for UI controls and graphical icons.

---

## 6. User Stories & Traceable Acceptance Criteria

### Story US-01: [Story Title]
- **As a** `[user persona]`, **I want** `[capability]`, **so that** `[value/benefit]`.
- **Priority**: `P0 (Must-Have)` | **Est. Effort**: `[Points/Days]`
- **Acceptance Criteria**:
  - **AC-US01-1 (Happy Path)**:
    - **Given** `[precondition]`
    - **When** `[user action]`
    - **Then** `[system response / state change]`
  - **AC-US01-2 (Validation / Input Error)**:
    - **Given** `[invalid input or boundary breach]`
    - **When** `[user action]`
    - **Then** `[inline validation message displayed without network submission]`
  - **AC-US01-3 (Auth / RBAC Restriction)**:
    - **Given** `[user lacking required role/permissions]`
    - **When** `[user attempts action]`
    - **Then** `[system returns 403 Forbidden with clear permission message]`

---

## 7. MoSCoW Requirements Breakdown

| Requirement ID | Category | Description | Priority |
|---|---|---|---|
| REQ-01 | UI/UX | Form auto-saves draft state every 5 seconds | P0 |
| REQ-02 | Backend | Validate token signature using RSA-256 | P0 |
| REQ-03 | Analytics | Log `checkout_completed` event with order total | P1 |
| REQ-04 | Polish | Micro-animation on success checkmark | P2 |

---

## 8. Technical Architecture & API Specifications

### API Endpoint Contracts
| Method | Endpoint Path | Auth Scope | Req Payload / Query | Success (2xx) | Error Codes |
|---|---|---|---|---|---|
| POST | `/api/v1/feature/action` | `admin:write` | `{ "setting": "enabled" }` | `200 OK` | `400 Bad Req`, `403 Forbidden` |

### Database Schema & Backward Compatibility
- **Migration Needed**: `[Yes/No]` (Migration script reference or dual-write strategy).
- **Client App Compatibility**: Supports API client versions `>= v2.4`.

### Operational SLAs & Performance Budgets
- **API Latency Target**: `< 200ms (p95)`, `< 500ms (p99)`.
- **Availability Target**: `99.9% Uptime`.

---

## 9. Telemetry & Data Governance Specification

| Event Name | Trigger Condition | Required Properties | PII / Data Class | Business Purpose |
|---|---|---|---|---|
| `feature_started` | User clicks initial CTA | `source_page`, `user_role` | Non-PII | Funnel top step |
| `feature_completed` | Operation succeeds | `duration_ms`, `item_count` | Non-PII | Activation tracking |

> ⚠️ **Data Governance Rule**: Telemetry properties MUST NOT log raw PII (emails, passwords, unhashed tokens). Use anonymized hashed identifiers (`user_id_hash`).

---

## 10. Feature Flag & Rollout Strategy
- **Feature Flag Key**: `ff_[feature_name]_v1`
- **Rollout Schedule**:
  - Phase 1: Internal Dogfooding (Team only)
  - Phase 2: 5% Beta Canary Release
  - Phase 3: 25% → 50% → 100% General Availability
- **Rollback Criteria**: API latency `p95 > 500ms`, error rate `> 1.0%`, or critical security vulnerability.

---

## 11. Dependencies & QA Environment Setup
- **Cross-Team Dependencies**: `[e.g., Security team approval, Billing API v2 release]`
- **QA Test Needs**: `[e.g., Staging feature flag override, mock IdP credentials, synthetic seed dataset]`

---

## 12. Open Questions & Blockers

| # | Question | Assigned To | Status / Resolution | Blocking? |
|---|---|---|---|---|
| Q1 | Should SSO configuration require 2FA re-prompt? | Security Team | Pending | Yes |
| Q2 | What is the audit log retention period? | Compliance | Resolved (90 Days) | No |
