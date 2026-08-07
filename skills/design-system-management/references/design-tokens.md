# Design Tokens

Design tokens are the atomic values that define a product's visual language. They represent small, repeatable design decisions.

## Token Categories

1. **Global Tokens (Base Tokens):** The primitive values.
   - e.g., `blue-500: #3b82f6`, `spacing-4: 16px`.
2. **Semantic Tokens (Alias Tokens):** Values tied to a specific meaning or intent.
   - e.g., `color-primary: {blue-500}`, `spacing-layout: {spacing-4}`.
3. **Component Tokens:** Values specific to a single component, mapping back to semantic or global tokens.
   - e.g., `button-background-color: {color-primary}`.

## Token Types to Define

- **Colors:** Brand colors, semantic colors (success, warning, error, info), neutral colors (backgrounds, text, borders).
- **Typography:** Font families, type scale (sizes), font weights, line heights.
- **Spacing:** A mathematical scale (usually 4px or 8px based) for padding, margins, and layout.
- **Borders:** Border radii (rounding), border widths.
- **Shadows/Elevation:** Different levels of depth and drop shadows.
- **Motion:** Standard animation durations and easing curves.