# Design System Management (`design-system-management`)

Architect, govern, and document scalable multi-brand design systems, semantic design tokens (`W3C DTCG`), composable component APIs, and accessible UI patterns.

---

## Overview

The `design-system-management` skill provides a systematic framework for building and maintaining production UI libraries:

- **Three-Tier Token Architecture**: Global primitives (`color.blue.500`), semantic aliases (`color.bg.surface.elevated`), and component-scoped tokens (`button.primary.bg.hover`).
- **Composable Component APIs**: Strict variant/size/state matrices, slot/compound-component composition, keyboard navigation (`WAI-ARIA`), and focus management.
- **Pattern Governance & Versioning**: Deprecation lifecycles, codemod migration guides, and "Do / Don't" usage specifications.

---

## Reference Guides (`references/`)

| File | Purpose |
|------|---------|
| [`references/design-tokens.md`](references/design-tokens.md) | Three-tier token taxonomy (Primitive → Semantic → Component), 4px/8px spatial scales, dark-mode aliasing, and JSON token schemas. |
| [`references/component-anatomy.md`](references/component-anatomy.md) | Component blueprint covering container anatomy, interactive states (`default`, `hover`, `focus-visible`, `disabled`, `loading`), and ARIA contracts. |
| [`references/ui-patterns.md`](references/ui-patterns.md) | Documentation template for multi-component UX patterns (forms, modals, data tables, empty states) with accessibility rules. |

---

## Installation

### Workspace Scope

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- design-system-management
```

### User Scope

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- design-system-management --scope user
```

---

## Usage Examples

- *"Create a semantic color and spacing token schema in W3C JSON format supporting both light and dark themes."*
- *"Design the TypeScript prop API and ARIA accessibility spec for a composable `<Combobox />` component."*
- *"Write the design system pattern documentation for destructive confirmation dialogs vs undo toasts."*