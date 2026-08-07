# Comprehensive Design Critique Framework

Use this framework to systematically evaluate UI/UX designs, wireframes, and code components.

---

## 1. First Impression & Initial Perception (The 2-Second Rule)
- **Focal Point Alignment**: Does the viewer's eye land on the single most important element (e.g., Primary CTA, Value Proposition header)?
- **Visual Anchor**: Is there a dominant visual anchor, or are multiple elements competing for attention?
- **Immediate Purpose**: Can a user state the main intent of the screen within 2 seconds of looking at it?
- **Emotional Resonance & Tone**: Does the visual style (colors, typography, imagery) align with the product's identity (e.g., trustworthy, energetic, clean, playful)?

---

## 2. Usability & UX Architecture
- **Goal Completion Pathway**: Is the primary user goal clear, frictionless, and requiring minimal steps?
- **Cognitive Load & Hick's Law**: Are choices kept manageable to prevent decision fatigue?
- **Affordance & Signifiers**: Do interactive elements look clickable/tappable? Are secondary actions visually distinct from primary actions?
- **Navigation & Mental Models**: Does the navigation pattern follow industry standards and user expectations (Jakob's Law)?
- **Error Prevention & Recovery**: Are input fields clear, with inline validation, helpful helper text, and forgiving formats?
- **Feedback & State Communication**: Is the system state obvious at all times (e.g., loading spinners, active tab indicators, empty states, success messages)?

---

## 3. Visual Hierarchy & Spatial Systems
- **Reading Gravity**: Does the layout support natural eye movement (F-pattern for text-dense content, Z-pattern for landing pages/promotional screens)?
- **Typography Scale & Rhythm**:
  - Is there a distinct font size, weight, and line-height scale between Display, Title, Heading, Body, and Captions?
  - Is body line height comfortable (1.4–1.6x font size)?
  - Is line length optimized for readability (45–75 characters per line)?
- **Spatial Grid (4pt / 8pt System)**:
  - Are padding and margin values consistent multiples of 4px or 8px (e.g., 4, 8, 12, 16, 24, 32, 48, 64px)?
  - Is whitespace used intentionally to group related items (Law of Proximity) and separate distinct sections?
- **Color Hierarchy & Contrast**:
  - Does the design follow the **60-30-10 rule** (60% dominant background, 30% secondary structure/text, 10% accent/CTA)?
  - Are functional colors used consistently (Green = Success, Red = Error/Destructive, Yellow/Orange = Warning, Blue/Primary = Interactive)?

---

## 4. Consistency & Design System Alignment
- **Token Uniformity**:
  - Border radii (e.g., rounded-md vs rounded-full) used consistently across inputs, buttons, and cards.
  - Shadow levels (elevation depth) reflecting consistent z-index hierarchy.
  - Color palette consistency (avoiding slight variations of gray or primary shades).
- **Component States**: Are all necessary interactive states defined?
  - `Default` / `Hover` / `Active` / `Focus-Visible` / `Disabled` / `Loading`.
- **Pattern Predictability**: Do similar actions produce predictable visual and structural results across screens?

---

## 5. Accessibility (WCAG 2.2 Standards)
- **Color Contrast Ratios**:
  - Normal text (under 18pt / 24px): **Minimum 4.5:1** contrast against background.
  - Large text (18pt+ bold or 24px+ regular): **Minimum 3:1** contrast.
  - Graphical objects and UI controls (button borders, form inputs): **Minimum 3:1** contrast.
- **Touch Target Sizes**:
  - Mobile interactive targets should be at least **44x44pt** (iOS) or **48x48dp** (Android) with adequate spacing between targets.
- **Color Independence**:
  - Information is never conveyed *solely* through color (e.g., error fields also feature icons or explicit helper text).
- **Focus Rings & Keyboard Nav**:
  - Clear, high-contrast outline focus rings visible during tab navigation (`:focus-visible`).
- **Semantic Structure**:
  - Headings follow logical nesting (`H1` → `H2` → `H3`).
  - Screen reader attributes (`aria-label`, `aria-expanded`, `role`) present where appropriate.
