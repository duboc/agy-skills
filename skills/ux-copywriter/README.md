# UX Copywriter (`ux-copywriter`)

Write clear, accessible (`WCAG 2.2`), and conversion-focused product microcopy for CTAs, error messages, empty states, onboarding flows, and confirmation dialogs.

---

## Overview

The `ux-copywriter` skill applies content design principles to eliminate user friction across digital interfaces:

- **Clarity Over Cleverness**: Actionable, plain-language labels that tell users exactly what happens next.
- **Contextual Tone Calibration**: Adapts warmth, urgency, and brevity based on the user's emotional state (celebratory on success, calm and constructive on error).
- **Screen-Reader & Localization Readiness**: Meaningful standalone labels (never `"Click here"`), `aria-label` guidance, and `+30%` text-expansion resilience for translations.

---

## Reference Guides (`references/`)

| File | Purpose |
|------|---------|
| [`references/copy-patterns.md`](references/copy-patterns.md) | Structural templates and Before/After examples for CTAs, inline validation errors (What happened + Why + How to fix), empty states, and destructive modals. |
| [`references/voice-and-tone.md`](references/voice-and-tone.md) | Voice vs Tone matrix across user emotional states (anxious, frustrated, focused, relieved) with vocabulary guardrails. |

---

## Installation

### Workspace Scope

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- ux-copywriter
```

### User Scope

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- ux-copywriter --scope user
```

---

## Usage Examples

- *"Write 3 microcopy options (direct, reassuring, action-oriented) for a payment declined error banner with clear recovery steps."*
- *"Audit the labels and confirmation modal copy in our account deletion flow to prevent accidental data loss."*
- *"Draft the empty-state heading, body copy, and primary CTA for a newly created analytics dashboard."*