# Agent Engine Ops

A Gemini CLI skill for monitoring, tracing, securing, and evaluating agents on Vertex AI Agent Engine.

## What It Does

This skill gives your coding agent deep knowledge of Vertex AI Agent Engine operations -- covering distributed tracing with Cloud Trace, monitoring with Cloud Monitoring, structured logging, agent identity and IAM, API key and OAuth management, CMEK encryption, Private Service Connect, and agent evaluation with the GenAI evaluation service.

## When Does It Activate?

The skill activates when you mention:

- Agent Engine tracing, Cloud Trace for agents
- Agent monitoring, Cloud Monitoring dashboards, agent metrics
- Agent logging, structured logs, Cloud Logging
- Agent identity, IAM for agents, service accounts
- API keys for agents, Secret Manager, OAuth integration
- CMEK encryption for Agent Engine
- Private Service Connect (PSC) for agents
- Evaluating agents, GenAI evaluation, agent quality metrics
- Agent observability, agent security, agent operations

## Topics Covered

| Area | What You Get |
|------|-------------|
| Tracing | Cloud Trace setup, spans, custom tracing, viewing traces |
| Monitoring | Built-in metrics, Metrics Explorer, dashboards, alerts |
| Logging | Python logging, Cloud Logging client, structured logs, severity levels |
| Agent Identity | Service accounts, IAM roles, per-agent identity provisioning |
| API Keys | Secret Manager integration, secure key retrieval |
| OAuth | External service authentication, token management |
| CMEK | Customer-managed encryption keys for data at rest |
| PSC | Private Service Connect for network isolation |
| Evaluation | GenAI evaluation service, metrics, datasets, continuous evaluation |

## Installation

### Option A: Gemini CLI native

```bash
gemini skills install https://github.com/duboc/agy-skills.git --path skills/agent-engine-ops
```

### Option B: One-liner

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- agent-engine-ops
```

For user-scope installation (available across all projects):

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- agent-engine-ops --scope user
```

### Option C: Manual

```bash
cp -r skills/agent-engine-ops ~/.gemini/skills/agent-engine-ops
```

## Usage Examples

- "Enable tracing for my deployed agent on Agent Engine"
- "Set up Cloud Monitoring dashboard for my agents"
- "Add structured logging to my agent tools"
- "Configure agent identity and IAM roles"
- "Store API keys securely with Secret Manager"
- "Set up CMEK encryption for my Agent Engine deployment"
- "Evaluate my agent's tool call accuracy"
- "Create alerts for high error rates on my agent"

## Included References

| File | Description |
|------|-------------|
| **monitoring-alerting.md** | Metrics Explorer, PromQL queries, Cloud Monitoring API, custom metrics, log-based metrics, alerts, dashboards |
| **security-identity.md** | Agent identity setup, IAM allow/deny policies, Principal Access Boundary, OAuth integration, API key management, CMEK, PSC |
