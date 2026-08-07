# Assertion-Evidence Slide Design

A reference guide for writing assertion-evidence slides — the structure used by clarity-presenter for every content slide.

## Core Principle

Every content slide has a **sentence headline** (the assertion) supported by **visual evidence** (the body). The headline is a complete, falsifiable claim — not a topic label.

## Good vs Bad Headlines

| Bad (Topic Label) | Good (Assertion Headline) |
|--------------------|---------------------------|
| Cloud Migration Overview | Lift-and-shift migrations reduce upfront risk but increase long-term costs |
| API Security | Token-based authentication reduces attack surface by 60% compared to API keys |
| Kubernetes Scaling | Horizontal pod autoscaling maintains P99 latency under 200ms during traffic spikes |
| Cost Optimization | Right-sizing idle instances saves 30-40% on compute without performance impact |
| Data Pipeline | Stream processing eliminates the 6-hour batch delay blocking real-time decisions |
| Monitoring | Distributed tracing pinpoints latency bottlenecks that aggregate metrics miss |
| Team Structure | Platform teams reduce cognitive load so product teams ship 2x faster |
| CI/CD Pipeline | Trunk-based development with feature flags deploys 10x more frequently with fewer rollbacks |

## The Falsifiability Test

A good assertion headline can be argued against. If no reasonable person would disagree, the headline is too vague.

- **Too vague**: "Security is important" (no one disagrees)
- **Assertive**: "Encryption at rest prevents 80% of data breach liability" (debatable, specific)

## Headline Writing Rules

1. **8-15 words** — long enough to make a claim, short enough to scan
2. **Use `##` (h2)** — reserves `#` (h1) for title and section dividers
3. **One claim per headline** — if you use "and," consider splitting into two slides
4. **Include a metric when possible** — numbers make assertions concrete
5. **Active voice** — "X reduces Y" not "Y is reduced by X"
6. **No question marks** — headlines assert, they don't ask (questions belong on the SCQA Question slide only)

## Evidence Types

The body of the slide supports the headline assertion. Choose the strongest evidence type for the claim.

### Diagrams and Architecture

Use when the assertion is about system structure, data flow, or relationships.

```
## Active-active replication eliminates single-region failure risk

[Architecture diagram showing two regions with bidirectional sync]
```

### Data and Metrics

Use when the assertion makes a quantitative claim.

```
## Right-sizing reduced our compute spend by 37% in Q3

### $142K → $89K
Monthly compute cost after right-sizing audit
```

### Comparisons (Before/After)

Use when the assertion claims improvement over a previous state.

```
## Automated rollbacks cut incident recovery from hours to minutes

### Before: 4.2 hours
Mean time to recovery with manual process

### After: 3.4 minutes
Automated canary + rollback pipeline
```

### Code Snippets

Use when the assertion is about a specific technical approach.

```
## Feature flags decouple deployment from release

‍‍‍python
if feature_flags.is_enabled("new_checkout", user_id):
    return new_checkout_flow(request)
return legacy_checkout_flow(request)
‍‍‍
```

### Short Bullet Lists (max 3 items)

Use sparingly when the assertion needs 2-3 supporting points that can't be visualized.

```
## Multi-layer caching reduces database load by 80%

- L1: In-process cache (microseconds)
- L2: Redis cluster (single-digit ms)
- L3: CDN edge cache (geographically distributed)
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Topic label headline | "Database Options" tells nothing | "PostgreSQL handles our query patterns 3x faster than MongoDB" |
| Too many bullets | 5+ bullets = a document, not a slide | Split into multiple slides or use a diagram |
| Headline repeats body | Redundant information wastes space | Headline = claim; body = evidence (different content) |
| No evidence | Assertion without support isn't persuasive | Add data, diagram, or comparison |
| Two assertions | "X improves Y and Z reduces W" | One slide per assertion |

## Headline Sequence Test

Read just the headlines in order (ignore slide bodies). They should tell a coherent story:

1. Our platform serves 2M users across 12 regions
2. Latency spikes 3x during regional failover
3. Active-active replication eliminates cold-start delays
4. Active-active cuts incident revenue loss by 90%
5. Global load balancing distributes traffic by health scores
6. Automatic traffic shifting keeps SLA above 99.99%

If the sequence reads like an executive summary, the assertions are well-structured.
