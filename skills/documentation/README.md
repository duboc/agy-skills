# Technical Documentation (`documentation`)

Write and maintain developer-grade technical documentation, READMEs, OpenAPI/REST reference guides, operational runbooks, and Architecture Decision Records (ADRs) aligned with the **Diátaxis Framework** and the **Google Developer Documentation Style Guide**.

---

## Overview

The `documentation` skill structures engineering documentation into distinct, purpose-built quadrants so readers find immediate answers without cognitive overload:

- **Tutorials (`Quickstart`)**: Deterministic `< 5 minute` path to first working result.
- **How-To Guides (`Task Recipes`)**: Step-by-step procedures solving concrete engineering tasks.
- **Reference (`API / CLI Specs`)**: Exact parameter tables, status codes, and payload schemas.
- **Explanation (`Architecture & ADRs`)**: Context, system boundaries, and explicit trade-off matrices.

---

## Reference Guides (`references/`)

| File | Purpose |
|------|---------|
| [`references/document-types.md`](references/document-types.md) | Structural templates for Project READMEs, REST/gRPC API docs, SRE Runbooks, Architecture Overviews, and Developer Onboarding guides. |
| [`references/diataxis-and-google-style-guide.md`](references/diataxis-and-google-style-guide.md) | The Diátaxis 4-quadrant decision matrix, Google Developer style rules (second-person, active voice, task-oriented headings), and RFC-2606 code sample hygiene. |

---

## Installation

### Workspace Scope

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- documentation
```

### User Scope

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- documentation --scope user
```

---

## Usage Examples

- *"Write a production-ready `README.md` for this FastAPI service with a 5-minute Quickstart, environment variables table, and architecture diagram."*
- *"Create an SRE incident runbook for high P99 latency on our Redis cluster, including diagnostic checks, mitigation commands, and rollback criteria."*
- *"Document our `/v1/orders` REST API endpoints with request/response JSON examples, authentication headers, and error codes."*

---

## Security & Quality Standards

- **Command Safety**: All CLI snippets use safe argument flags (`set -euo pipefail`) and never invoke `eval()` or `shell=True`.
- **PII & Secret Hygiene**: Uses RFC 2606 domains (`example.com`, `dev@example.com`) and placeholder tokens (`<YOUR_API_KEY>`).