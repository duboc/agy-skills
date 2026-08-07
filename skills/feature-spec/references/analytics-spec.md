# Analytics Telemetry & Data Governance Specification

Define telemetry schemas directly in product specifications so data instrumentation is built into engineering tickets.

---

## Event Naming Convention
Follow standard `object_action` (noun + past-tense verb) snake_case convention:
- Good: `onboarding_step_completed`, `sso_config_updated`, `payment_method_added`
- Bad: `clickButton`, `userFinishedOnboarding`, `sso_stuff`

---

## Analytics Telemetry Schema Template

Every PRD must include a Telemetry Schema Table with explicit PII Data Governance classification:

| Event Name | Trigger Condition | Required Properties | PII / Data Class | Business Purpose |
|---|---|---|---|---|
| `invite_modal_opened` | User clicks "Invite Member" CTA | `source_location`, `user_role` | Non-PII | Funnel top step |
| `invite_sent` | Server returns 200 after submission | `recipient_role`, `invite_type` (`email`/`link`) | Non-PII (No raw emails!) | Conversion tracking |
| `invite_failed` | Server returns 4xx/5xx error | `error_code`, `error_type` | Non-PII | Error & friction analysis |

---

## Data Governance & PII Protection Rules

> 🛑 **CRITICAL DATA GOVERNANCE RULE**:
> Telemetry events MUST NEVER log raw PII (e.g. unhashed email addresses, user full names, passwords, authorization tokens, or precise physical addresses) in analytics platforms (PostHog, Mixpanel, Segment).

1. **Hashed User Identifiers**: Use anonymized SHA-256 hashed IDs (`user_id_hash`, `org_id_hash`).
2. **Categorical Enums**: Capture categorical types instead of raw inputs (e.g. `invite_type: "email"` instead of `email: "user@example.com"`).
3. **Automatic Context**: Baseline properties automatically captured by SDK (`platform`, `app_version`, `timestamp`, `locale`).
