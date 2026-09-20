# System Design (`system-design`)

Design distributed systems, microservice topologies, APIs, and storage schemas with back-of-the-envelope capacity math and explicit architectural trade-off analysis.

---

## Overview

The `system-design` skill guides engineers through a structured 5-phase architectural workflow:

1. **Requirements & Scope Calibration**: Functional user journeys, Non-Functional SLOs (latency, availability, durability), and scale constraints.
2. **Back-of-the-Envelope Capacity Estimation**: RPS, peak bandwidth, cache working-set memory, and 5-year storage sizing.
3. **High-Level Topology & Data Flow**: Edge routing, stateless compute, data partitioning, and asynchronous event pipelines.
4. **Component Deep Dive**: API contracts (REST/gRPC/GraphQL), SQL vs NoSQL vs NewSQL selection, sharding keys, and cache invalidation.
5. **Resilience & Trade-Off Analysis**: Single points of failure (SPOFs), PACELC consistency/latency trade-offs, rate limiting, and graceful degradation.

---

## Reference Guides (`references/`)

| File | Purpose |
|------|---------|
| [`references/design-framework.md`](references/design-framework.md) | Step-by-step 5-stage system design blueprint, API contract schemas, and architectural review template. |
| [`references/capacity-and-tradeoff-cheatsheet.md`](references/capacity-and-tradeoff-cheatsheet.md) | Latency numbers every engineer should know, RPS/bandwidth/storage formulas, and PACELC/caching/queueing trade-off matrix. |

---

## Installation

### Workspace Scope

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- system-design
```

### User Scope

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- system-design --scope user
```

---

## Usage Examples

- *"Design a multi-region notification delivery service handling 50M daily active users with P99 latency under 200ms."*
- *"Review our current Postgres + Redis checkout architecture and identify bottlenecks at 10x traffic growth."*
- *"Compare Kafka vs Google Cloud Pub/Sub vs Cloud Tasks for our asynchronous order fulfillment pipeline."*