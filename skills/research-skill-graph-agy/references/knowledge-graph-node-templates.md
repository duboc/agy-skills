# Knowledge Graph Node Templates & WikiLink Schema

Use these Markdown templates when constructing an interconnected local research graph (`index.md` Map of Content + atomic concept notes).

---

## 1. Map of Content (`00-index-moc.md`) Template

```markdown
---
title: "<Research Topic> — Map of Content (MOC)"
type: moc
status: complete
confidence: high
updated: YYYY-MM-DD
tags:
  - research
  - moc
---

# <Research Topic>: Executive Synthesis & Knowledge Graph

## 1. Core Thesis & Decision Summary
<3-5 sentence synthesis answering the primary research question with quantified trade-offs.>

## 2. Knowledge Graph Navigation (Atomic Nodes)
- **Foundations & Architecture**: [01-architecture-and-primitives](./01-architecture-and-primitives.md)
- **Empirical Benchmarks & Cost**: [02-benchmarks-and-unit-economics](./02-benchmarks-and-unit-economics.md)
- **Failure Modes & Security Risks**: [03-risks-and-edge-cases](./03-risks-and-edge-cases.md)
- **Decision Matrix & Recommendations**: [04-decision-matrix](./04-decision-matrix.md)

## 3. Key Quantitative Findings
| Dimension | Option A | Option B | Primary Source |
|-----------|----------|----------|----------------|
| P99 Latency | `18 ms` | `42 ms` | [02-benchmarks-and-unit-economics](./02-benchmarks-and-unit-economics.md) |
| Monthly TCO (10M req) | `$420` | `$190` | [02-benchmarks-and-unit-economics](./02-benchmarks-and-unit-economics.md) |
```

---

## 2. Atomic Concept Note (`01-<slug>.md`) Template

```markdown
---
title: "<Atomic Concept Title>"
type: concept-node
status: verified
confidence: 0.88
sources_count: 3
tags:
  - <domain-tag>
---

# <Atomic Concept Title>

> **Claim Summary**: <One-sentence falsifiable assertion backed by the evidence below.>

## Empirical Evidence & Citations
1. **Primary Benchmark**: <Metric / Finding> — *Source: `<Author/Org, Year>` (`https://example.com/spec`)*
2. **Independent Corroboration**: <Metric / Finding> — *Source: `<Author/Org, Year>` (`https://example.org/benchmark`)*

## Contradictions & Boundary Conditions
- **Where this holds**: <Workload / scale parameters>
- **Where this breaks**: <Edge case / failure threshold>

## Graph Connections
- **Upstream Context**: [00-index-moc](./00-index-moc.md)
- **Related Trade-offs**: [02-benchmarks-and-unit-economics](./02-benchmarks-and-unit-economics.md)
- **Mitigations**: [03-risks-and-edge-cases](./03-risks-and-edge-cases.md)
```
