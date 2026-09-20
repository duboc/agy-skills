# Synthesis Rules & Output Standards

Synthesis is the process of bringing the output of all 6 lenses together into decision-grade intelligence without flattening core tensions.

## 1. Output Files Structure

Each research project produces four synthesis files inside `.research/projects/<topic>/`:
1. `executive-summary.md` — Strict max 500 words. Executive-level overview.
2. `deep-dive.md` — Long-form, exhaustive analysis organized by cross-cutting themes.
3. `key-players.md` — Mapped index of key institutions, companies, regulators, and individuals.
4. `open-questions.md` — Unresolved dynamics, missing data, and future indicators.

## 2. Confidence Calibration Format

Major claims across all synthesis and lens files must be explicitly calibrated using the following structure:

```markdown
- **CLAIM**: [Explicit assertion statement]
- **EVIDENCE**: [Supporting facts/data with source citation and Tier classification]
- **CONFIDENCE**: [High / Medium / Low] ([Estimated % likelihood])
- **DEFEASIBILITY TRIGGER**: [Specific empirical evidence or event that would invalidate this claim]
```

## 3. Preserving Dialectical Tension

- **Do Not Pick Winners**: Never resolve disagreement by discarding a lens's valid perspective.
- **Find Boundary Conditions**: Frame contradictions around conditions (e.g., "The Technical Lens holds under local deployment, whereas the Economic Lens dominates at cloud scale").
- **Exhaustive Long-Form Prose**: Disregard brevity constraints in `deep-dive.md`. Provide thorough explanation of causal mechanisms, data nuances, and systemic feedback loops.
