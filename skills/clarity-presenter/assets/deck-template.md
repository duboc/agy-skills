---
marp: true
theme: gcloud
---

<!-- _class: title -->

# Your Topic Here
### SCQA + Assertion-Evidence Deck

---

<!-- _class: section -->

# Situation

---

## Our platform serves 2M daily active users across 12 regions

Current architecture handles peak load reliably

---

<!-- _class: section -->

# Complication

---

## Request latency spikes 3x during regional failover events

*Current failover adds 800ms to P99 response times*

---

<!-- _class: invert -->

## Latency spikes during outages erode user trust and increase churn

*Each 1-second delay correlates with 7% drop in conversion*

---

<!-- _class: lead -->

## How can we achieve sub-200ms failover without re-architecting the entire platform?

---

<!-- _class: section -->

# Answer

---

## Active-active replication eliminates cold-start failover delays

- Pre-warmed connections in each region
- Consistent hashing routes traffic instantly
- Health checks trigger in under 50ms

---

<!-- _class: invert -->

## Active-active cuts incident revenue loss by 90% at predictable cost

*$12K/month infrastructure vs $180K/incident in lost transactions*

---

## Global load balancing distributes traffic based on real-time health scores

*Weighted routing adapts within a single health-check interval*

---

<!-- _class: invert -->

## Automatic traffic shifting keeps SLA compliance above 99.99%

*Eliminates manual intervention that currently takes 4-8 minutes*

---

<!-- _class: closing -->

# Resilience is a revenue strategy, not just an infrastructure cost

Start the active-active pilot in staging this quarter
