# SCQA Framework Guide

A reference guide for structuring presentations using the SCQA (Situation-Complication-Question-Answer) narrative framework, adapted for technical and business audiences.

## What Is SCQA?

SCQA is a storytelling framework developed at McKinsey for structuring persuasive communication. It ensures every presentation answers a clear question that the audience cares about.

| Component | Purpose | Typical Length |
|-----------|---------|---------------|
| **Situation** | Establish shared context the audience already agrees with | 1-2 slides |
| **Complication** | Introduce the tension, problem, or change that disrupts the status quo | 1-3 slides |
| **Question** | Crystallize the central question the audience now needs answered | 1 slide |
| **Answer** | Present the solution with evidence — this is the bulk of the deck | 3-8 slides |

## Component Details

### Situation (S)

**Purpose**: Ground the audience in a reality they recognize. No surprises here — this is common knowledge.

**Tips**:
- State facts, not opinions
- Use present tense
- Keep it brief — the audience already knows this
- Include a concrete metric if possible (users, revenue, scale)

**Examples**:
- "Our API gateway processes 50K requests per second across 3 regions"
- "The data science team runs 200+ experiments per quarter on shared infrastructure"
- "Our mobile app has 4M monthly active users with 98% on the latest version"

### Complication (C)

**Purpose**: Create tension. Something has changed, is broken, or is about to become a problem. This is where the audience starts to lean in.

**Tips**:
- Show the gap between current state and desired state
- Use specific numbers to quantify the pain
- Can be a recent event, a trend, or an emerging risk
- Technical slides show the "how" of the problem; business slides show the "so what"

**Examples**:
- "P99 latency exceeds our SLA during peak traffic, triggering contractual penalties"
- "Experiment queue times have grown from 2 hours to 3 days as the team scaled"
- "Session drop-off increased 23% after the last infrastructure migration"

### Question (Q)

**Purpose**: Frame the exact question the rest of the presentation will answer. This slide is the hinge — everything before it builds tension, everything after releases it.

**Tips**:
- One question only
- Phrased as "How can we..." or "What is the best way to..."
- Should feel inevitable given the Situation and Complication
- Use `<!-- _class: lead -->` for centered, prominent display

**Examples**:
- "How can we maintain sub-100ms latency at 3x current traffic?"
- "What infrastructure changes will restore experiment velocity without increasing cost?"
- "How do we reduce session drop-off while completing the migration?"

### Answer (A)

**Purpose**: Present the solution with evidence. This is where assertion-evidence slides shine — each slide makes one claim and backs it up.

**Tips**:
- Lead with the strongest argument
- Alternate technical (white) and business (dark/blue) slides for each concept
- Each assertion-evidence pair covers one concept from two angles
- End with a clear call to action

## Content Mapping Table

Use this table to plan your deck before writing slides:

| SCQA Section | Slide Count | Slide Class | Content Type |
|-------------|-------------|-------------|--------------|
| Title | 1 | `title` | Topic + subtitle |
| Situation | 1-2 | *(default)* | Factual context, shared reality |
| Complication | 1-3 | *(default)* + `invert` | Problem from technical + business view |
| Question | 1 | `lead` | Central question |
| Answer | 3-8 | *(default)* + `invert`/`section` alternating | Assertion-evidence pairs |
| Closing | 1 | `closing` | Call to action |

## Complete Examples

### Example 1: Cloud Migration

| Section | Headline |
|---------|----------|
| **S** | Our monolith serves 10M transactions daily on legacy infrastructure |
| **C** (tech) | Deployment frequency dropped to once per month due to coupling risk |
| **C** (biz) | Slow releases cost us 3 competitive feature launches last quarter |
| **Q** | How can we increase deployment frequency without destabilizing production? |
| **A** (tech) | Strangler fig pattern isolates services without rewriting the monolith |
| **A** (biz) | Incremental migration reduces risk while restoring weekly release cadence |
| **A** (tech) | API gateway routing enables gradual traffic shifting per service |
| **A** (biz) | Each migrated service unlocks independent scaling and team autonomy |
| **Closing** | Start with the authentication service — highest value, lowest coupling |

### Example 2: API Security

| Section | Headline |
|---------|----------|
| **S** | Our public API serves 500 partner integrations with key-based auth |
| **C** (tech) | Leaked API keys caused 3 unauthorized access incidents in 6 months |
| **C** (biz) | Each incident required 72-hour response and partner notification under SOC 2 |
| **Q** | How do we eliminate key-based vulnerabilities without breaking partner integrations? |
| **A** (tech) | OAuth 2.0 with short-lived tokens limits blast radius of credential exposure |
| **A** (biz) | Automated token rotation eliminates the compliance burden of manual key management |
| **A** (tech) | Scoped permissions enforce least-privilege at the API endpoint level |
| **A** (biz) | Granular access control satisfies enterprise customer security reviews |
| **Closing** | Pilot OAuth migration with top 10 partners this quarter |

### Example 3: Data Platform

| Section | Headline |
|---------|----------|
| **S** | Analytics team queries 20TB of data daily across 4 data warehouses |
| **C** (tech) | Cross-warehouse joins take 45 minutes and fail 30% of the time |
| **C** (biz) | Analysts spend 60% of their time on data wrangling instead of insights |
| **Q** | How can we unify data access without migrating all sources to one warehouse? |
| **A** (tech) | A federated query layer abstracts warehouse differences behind standard SQL |
| **A** (biz) | Unified access reduces analyst onboarding time from weeks to days |
| **A** (tech) | Materialized views pre-compute frequent joins, cutting query time by 90% |
| **A** (biz) | Faster queries mean daily insights instead of weekly reports |
| **Closing** | Deploy the federation layer on the two highest-traffic warehouses first |

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Skipping the Situation | Audience can't calibrate the severity of the Complication | Always ground them in shared facts first |
| Complication without specifics | "Things are bad" doesn't create urgency | Use numbers: "latency increased 3x" not "latency increased" |
| Question that's too broad | "How do we fix everything?" isn't answerable | Narrow the scope to one specific, achievable outcome |
| Answer without evidence | Claims without data aren't persuasive | Every assertion needs a metric, diagram, or comparison |
| No call to action | Audience agrees but doesn't know the next step | Closing slide names the specific first action |
| All technical, no business | Half the audience tunes out | Pair every technical concept with a business consequence |
| All business, no technical | Engineers can't evaluate feasibility | Pair every business claim with the technical mechanism |
