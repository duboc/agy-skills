# Dual-Perspective Slide Guide

A reference guide for creating paired technical and business slides that explain the same concept from two angles.

## Core Principle

Every key concept gets two slides:
1. **Technical slide** (white/default background) — explains **how** it works
2. **Business slide** (dark/blue background) — explains **why** it matters

The pair ensures mixed audiences stay engaged. Engineers get the mechanism; stakeholders get the impact.

## Translation Patterns

Use these patterns to translate technical assertions into business assertions for the same concept.

| Technical Concept | Technical Headline (How) | Business Headline (Why) |
|-------------------|--------------------------|-------------------------|
| **Latency reduction** | Edge caching reduces API response time from 450ms to 38ms | Sub-50ms responses increase checkout completion by 12% |
| **Scalability** | Horizontal autoscaling handles 10x traffic spikes in under 90 seconds | Auto-scaling ensures Black Friday traffic never crashes the storefront |
| **Encryption** | AES-256 encryption at rest protects data across all storage layers | Encryption at rest satisfies HIPAA and SOC 2 audit requirements |
| **Observability** | Distributed tracing correlates requests across 14 microservices | Tracing cuts mean-time-to-resolution from 4 hours to 20 minutes |
| **CI/CD** | Trunk-based development with canary deploys ships code 10x more frequently | Faster releases mean customer-reported bugs get fixed in days, not months |
| **Database migration** | Online schema migration applies changes without table locks or downtime | Zero-downtime migrations eliminate the 2AM maintenance windows |
| **Container orchestration** | Kubernetes bin-packing optimizes node utilization to 78% average | Container orchestration reduces compute costs by 35% at current scale |
| **API versioning** | Semantic versioning with sunset headers gives consumers 6 months to migrate | Graceful deprecation prevents partner integration breakage and support tickets |
| **Feature flags** | Runtime feature flags decouple deployment from feature activation | Feature flags enable same-day rollback without redeployment |
| **Data federation** | Federated query engine abstracts 4 warehouses behind standard SQL | Unified data access reduces analyst onboarding from 3 weeks to 3 days |
| **Load balancing** | Weighted round-robin distributes traffic based on real-time health scores | Intelligent routing keeps uptime above 99.99% during partial outages |
| **Caching strategy** | Multi-layer cache (L1 in-process, L2 Redis, L3 CDN) reduces DB load by 80% | Caching strategy defers a $200K database upgrade by 18 months |

## Translation Principles

### 1. Metrics Over Mechanisms

Technical slides explain *what the system does*. Business slides translate to *what the organization gains*.

- **Technical**: "gRPC reduces payload size by 60% compared to REST+JSON"
- **Business**: "Smaller payloads cut mobile data costs and improve emerging-market performance"

### 2. Time and Money

Business audiences care about three things: revenue, cost, and risk. Translate technical improvements into at least one of these.

| Technical Metric | Business Translation |
|-----------------|---------------------|
| Latency (ms) | User experience, conversion rate |
| Throughput (req/s) | Capacity for growth, headroom |
| Availability (%) | SLA compliance, contractual penalties |
| Error rate (%) | Customer satisfaction, support costs |
| Deploy frequency | Time to market, competitive advantage |
| MTTR (hours) | Incident cost, engineering productivity |
| Resource utilization (%) | Infrastructure cost, cloud spend |
| Test coverage (%) | Defect rate, maintenance cost |

### 3. Concrete Over Abstract

Avoid vague business claims. Use specific, measurable outcomes.

- **Vague**: "Improves efficiency"
- **Concrete**: "Reduces manual review time from 6 hours to 20 minutes per release"

- **Vague**: "Enhances security posture"
- **Concrete**: "Eliminates the #1 audit finding for 3 consecutive quarters"

### 4. Consequences, Not Features

Business slides describe outcomes, not capabilities.

- **Feature**: "Supports automatic failover"
- **Consequence**: "Automatic failover prevented $180K in lost transactions during last month's outage"

## Writing Process for Paired Headlines

Follow this sequence for each concept:

1. **Write the technical headline first** — what does the system do? Be specific.
2. **Identify the business metric** — which of time/money/risk does this affect?
3. **Quantify the impact** — use real or realistic numbers.
4. **Write the business headline** — express the outcome in stakeholder language.
5. **Check independence** — each headline should stand alone without the other.

### Example Walkthrough

**Concept**: Service mesh adoption

1. Technical: "Istio service mesh provides mTLS, traffic management, and observability across 14 services"
2. Business metric: Risk (security), Time (debugging), Money (incident cost)
3. Quantify: mTLS eliminates unencrypted internal traffic; traffic management reduced cascading failures by 90%
4. Business: "Service mesh eliminated 3 categories of security findings and cut cascading failures by 90%"
5. Independence check: Both headlines make sense read alone.

## Audience Balance Adaptation

Adjust the emphasis based on who is in the room.

| Audience Balance | Technical Slides | Business Slides | Adaptation |
|-----------------|-----------------|-----------------|------------|
| **Balanced** (default) | Equal depth | Equal depth | Standard alternation: tech → biz → tech → biz |
| **Technical-heavy** | More detail, code snippets, architecture diagrams | Lighter, focused on ROI summary | Tech slide may include evidence; biz slide is concise |
| **Business-heavy** | Lighter, focused on key mechanism | More detail, metrics, stakeholder quotes | Biz slide may include evidence; tech slide is concise |

### Technical-Heavy Example

```markdown
## Istio sidecar proxies intercept all pod-to-pod traffic for mTLS

- Envoy proxy injected automatically via admission webhook
- Certificate rotation every 24 hours via citadel
- Zero application code changes required

---

<!-- _class: invert -->

## Automated encryption eliminates internal-traffic audit findings

```

### Business-Heavy Example

```markdown
## Service mesh encrypts all internal traffic without code changes

---

<!-- _class: invert -->

## Automated encryption eliminated 3 audit findings and saves 120 engineering hours per compliance cycle

- SOC 2 internal-traffic requirement: auto-satisfied
- PCI DSS encryption mandate: covered by default
- Annual audit prep reduced from 2 weeks to 2 days
```

## Visual Distinction Rules

| Slide Type | Background | Class | Headline Format |
|-----------|------------|-------|-----------------|
| Technical | White (default) | *(none)* | `## [Technical assertion]` |
| Business | Dark grey | `invert` | `## [Business assertion]` |
| Business (alt) | Blue | `section` | `## [Business assertion]` |

**Alternation pattern**: Default → Invert → Default → Invert (or Default → Section for variety).

The visual contrast (white vs dark) makes it immediately obvious which perspective is being presented, even to someone glancing at the deck without reading.
