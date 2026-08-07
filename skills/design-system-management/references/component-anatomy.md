# Component Anatomy

A reusable UI component is more than just its visual appearance. A complete component definition must account for all its variations, states, and behaviors.

## Key Dimensions

### 1. Variants
The distinct visual styles or functional types of the component.
- e.g., Button variants: `Primary`, `Secondary`, `Ghost/Tertiary`, `Destructive`.

### 2. States
How the component appears in different interactive phases.
- e.g., `Default`, `Hover`, `Active/Pressed`, `Disabled`, `Loading`, `Error/Invalid`.

### 3. Sizes
The physical dimensions of the component to fit different contexts.
- e.g., `Small (sm)`, `Medium (md)`, `Large (lg)`.

### 4. Behavior
How the component acts and reacts to user input.
- **Interactions:** What happens on click, hover, or drag?
- **Animations:** Are there transitions between states?

### 5. Accessibility (A11y)
Ensuring the component is usable by everyone.
- **ARIA Attributes:** Necessary roles and states (e.g., `aria-expanded`, `aria-hidden`).
- **Keyboard Navigation:** Tab order, focus rings, and specific key interactions (e.g., `Enter` vs `Space` to activate).
- **Contrast:** Ensuring text and essential graphics meet WCAG contrast requirements.