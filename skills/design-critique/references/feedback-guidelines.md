# How to Give Constructive Design Feedback

Effective design feedback builds trust, fosters collaboration, and elevates product quality. Follow these guidelines when delivering feedback.

---

## 1. The SBI Feedback Model (Adapted for UX)

Frame every piece of critique around three key components:

1. **Situation / Observation**: Describe specifically what you see in the design.
   - *Example*: "The 'Save Changes' button is grey with white text and placed next to 'Cancel'."
2. **Impact**: Explain the consequence for the user or business goal using design principles.
   - *Example*: "The low contrast makes the button look disabled, while its proximity to 'Cancel' risks accidental misclicks."
3. **Recommendation**: Propose a concrete alternative or solution.
   - *Example*: "Increase the background contrast to solid primary blue (`#2563EB`) and add 16px separation between actions."

---

## 2. Match the Design Phase

Tailor feedback depth to where the designer is in their process:

| Stage | Focus On | Avoid |
|---|---|---|
| **Ideation / Low-Fi Wireframe** | User flows, information hierarchy, layout structure, problem fit | Color choices, precise typography, micro-spacing, shadow specs |
| **High-Fi Mockup** | Visual balance, typography hierarchy, color harmony, visual polish, branding | Re-questioning core user goals unless major UX gaps exist |
| **Code / Implementation** | CSS execution, responsiveness, accessibility compliance (WCAG), component states | Redesigning layout from scratch |

---

## 3. Severity Rating Guide

Categorize findings so the creator knows what to fix first:

- **🚨 P0 — Critical (Blocker)**: Fails WCAG compliance, causes severe user confusion, broken user flow, or unreadable content.
- **⚠️ P1 — Major (UX & Hierarchy)**: Creates unnecessary cognitive load, visual clutter, weak CTA visibility, or inconsistent UI patterns.
- **✨ P2 — Minor (Polish & Microcopy)**: Spacing discrepancies, minor contrast tweaks, copy enhancements, subtle elevation adjustments.

---

## 4. Constructive Phrasing: Before vs After

| ❌ Weak / Subjective Feedback | ✅ Strong / Objective Feedback |
|---|---|
| "I don't like the colors." | "The secondary text grey (`#9CA3AF`) fails WCAG AA contrast against the light gray card background (`#F3F4F6`). Consider darkening it to `#4B5563`." |
| "This page is too busy." | "There are 4 distinct primary-style buttons on this screen, competing for attention. Establishing one primary filled button and using outline styles for secondary actions will clarify the user pathway." |
| "The font looks bad." | "The heading font size (18px) is too close to the body text size (16px), flattening the visual hierarchy. Increasing headings to 24px semi-bold creates clearer section scanning." |
| "Fix the form." | "Input labels are currently placed to the left of fields, increasing horizontal scanning distance. Top-aligned labels reduce completion time and improve mobile stacking." |
