---
name: agent-engine-ops
description: "Monitor, trace, secure, and evaluate agents on Vertex AI Agent Engine. Use when setting up Cloud Trace for agents, configuring Cloud Monitoring dashboards, implementing agent logging, managing agent identity and IAM, configuring service accounts and roles, setting up API keys and OAuth, enabling CMEK encryption, configuring Private Service Connect, evaluating agents with GenAI evaluation, or when the user mentions agent observability, agent security, agent tracing, agent metrics, or agent evaluation on Vertex AI."
---

# Vertex AI Agent Engine Operations Guide

## Overview

Operating agents in production requires observability, security, and evaluation. This guide covers the full operations stack for Vertex AI Agent Engine: tracing with Cloud Trace, monitoring with Cloud Monitoring, structured logging, agent identity and IAM, encryption, network security, and agent evaluation.

## Documentation & Resources

- **Tracing**: https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/monitor/trace
- **Monitoring**: https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/monitor/monitor
- **Agent Identity**: https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/security/agent-identity
- **Evaluation**: https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/evaluate

## Quick Reference

| Task | Approach |
|------|----------|
| Enable tracing | Set `ENABLE_TRACING=true` env var at deployment |
| View traces | Cloud Trace in Google Cloud Console |
| Monitor metrics | Cloud Monitoring with built-in Agent Engine metrics |
| Agent logs | Python `logging` module + Cloud Logging |
| Agent identity | Provision via IAM, assign roles |
| Service accounts | Configure per-agent service accounts |
| API key management | Secret Manager for third-party keys |
| OAuth integration | Configure OAuth for external service access |
| CMEK encryption | Customer-managed encryption keys |
| Private networking | Private Service Connect (PSC) |
| Evaluate agents | GenAI evaluation service |

---

## Tracing with Cloud Trace

### Enabling Tracing

Enable tracing at deployment to get distributed traces across agent interactions:

```python
from google.adk.agents import Agent
from vertexai.agent_engines import AdkApp

root_agent = Agent(
    name="my_agent",
    model="gemini-2.5-flash",
    instruction="...",
    tools=[...],
)

adk_app = AdkApp(agent=root_agent)

# Enable tracing via environment variable
agent_engine = client.agent_engines.create(
    agent_engine=adk_app,
    display_name="traced-agent",
    requirements=["google-cloud-aiplatform[adk,agent_engines]"],
    env_vars={
        "ENABLE_TRACING": "true",
    },
)
```

### Viewing Traces

1. Open **Cloud Trace** in the Google Cloud Console
2. Filter by service name or trace ID
3. Examine spans for:
   - Agent execution time
   - Tool call duration
   - Model inference latency
   - Sub-agent delegation

### Trace Spans

Agent Engine automatically creates spans for:

| Span | Description |
|------|-------------|
| Agent execution | Full agent turn from input to output |
| Model call | LLM inference request and response |
| Tool execution | Individual tool function calls |
| Sub-agent call | Delegation to sub-agents |
| Session operations | Session read/write operations |

### Custom Spans

Add custom spans for application-specific tracing:

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def my_tool(query: str) -> dict:
    """Process a query with custom tracing."""
    with tracer.start_as_current_span("custom-processing") as span:
        span.set_attribute("query.length", len(query))
        result = process_query(query)
        span.set_attribute("result.count", len(result))
        return result
```

---

## Monitoring with Cloud Monitoring

### Built-in Metrics

Agent Engine exposes metrics to Cloud Monitoring automatically:

| Metric | Description |
|--------|-------------|
| Request count | Number of agent queries |
| Request latency | End-to-end response time |
| Error rate | Failed queries as percentage |
| Token usage | Input/output token consumption |
| Active instances | Number of running replicas |

### Viewing Metrics

1. Open **Cloud Monitoring** in Google Cloud Console
2. Navigate to **Metrics Explorer**
3. Search for `aiplatform.googleapis.com/reasoning_engine/` metrics
4. Create charts and dashboards

### Creating Dashboards

```python
# Use Cloud Monitoring API to create dashboards programmatically
# Or use the Console UI to build dashboards with:
# - Request rate over time
# - Latency percentiles (p50, p95, p99)
# - Error rate trends
# - Token usage patterns
# - Instance scaling events
```

### Setting Up Alerts

Configure alerts for critical thresholds:

- **High error rate**: Alert when error rate exceeds 5% over 5 minutes
- **High latency**: Alert when p95 latency exceeds acceptable threshold
- **Token budget**: Alert when daily token usage approaches limits

For PromQL queries, Cloud Monitoring API usage, custom metrics, log-based metrics, and detailed alerting configuration, see [references/monitoring-alerting.md](references/monitoring-alerting.md).

---

## Logging

### Standard Logging

Agent Engine captures stdout/stderr from your agent code:

```python
import logging

logger = logging.getLogger(__name__)

def my_tool(query: str) -> dict:
    """A tool with structured logging."""
    logger.info(f"Processing query: {query}")
    try:
        result = process(query)
        logger.info(f"Query processed successfully, {len(result)} results")
        return result
    except Exception as e:
        logger.error(f"Query processing failed: {e}", exc_info=True)
        raise
```

### Cloud Logging Client

For structured logging with labels and severity:

```python
from google.cloud import logging as cloud_logging

client = cloud_logging.Client()
client.setup_logging()

# Now standard Python logging goes to Cloud Logging
logger = logging.getLogger(__name__)
logger.info("Agent started", extra={
    "json_fields": {
        "agent_name": "my_agent",
        "version": "1.0.0",
    }
})
```

### Log Severity Levels

| Level | Use Case |
|-------|----------|
| DEBUG | Detailed diagnostic information |
| INFO | Normal operations, request processing |
| WARNING | Unexpected but handled situations |
| ERROR | Failed operations, exceptions |
| CRITICAL | System-level failures |

---

## Agent Identity

### Overview

Agent identity allows each deployed agent to have its own identity for accessing Google Cloud resources and external services. This replaces the default Vertex AI service agent identity with a purpose-specific principal.

### Provisioning Agent Identity

```python
# Agent identity is configured at deployment time
# The agent receives a unique service account

agent_engine = client.agent_engines.create(
    agent_engine=adk_app,
    display_name="identity-agent",
    requirements=["google-cloud-aiplatform[adk,agent_engines]"],
)

# The agent's service account can be granted specific IAM roles
```

### IAM Roles for Agent Engine

| Role | Description |
|------|-------------|
| `roles/aiplatform.user` | Query agents, manage sessions |
| `roles/aiplatform.admin` | Full agent management (create, update, delete) |
| `roles/aiplatform.viewer` | Read-only access to agent metadata |

### Service Account Configuration

Each agent can use a dedicated service account for fine-grained access control:

```python
# Grant the agent's service account access to specific resources
# Example: Allow agent to read from Cloud Storage
# gcloud projects add-iam-policy-binding PROJECT_ID \
#     --member="serviceAccount:AGENT_SA@PROJECT_ID.iam.gserviceaccount.com" \
#     --role="roles/storage.objectViewer"
```

---

## API Keys and OAuth

### API Key Management with Secret Manager

Store third-party API keys securely using Secret Manager:

```python
from google.cloud import secretmanager

def get_api_key(secret_id: str) -> str:
    """Retrieve API key from Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/your-project/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

def my_tool(query: str, tool_context: ToolContext) -> dict:
    """Tool that uses a third-party API."""
    api_key = get_api_key("third-party-api-key")
    # Use api_key to call external service
    return {"result": "..."}
```

### OAuth for External Services

Configure OAuth for agents that need to access external services on behalf of users:

```python
# OAuth integration pattern:
# 1. Configure OAuth consent screen in Google Cloud Console
# 2. Store client credentials in Secret Manager
# 3. Implement token exchange in agent tools
# 4. Use refresh tokens for long-lived access
```

---

## CMEK Encryption

Customer-Managed Encryption Keys (CMEK) provide additional control over data encryption:

```python
# Configure CMEK at deployment time
agent_engine = client.agent_engines.create(
    agent_engine=adk_app,
    display_name="cmek-agent",
    requirements=["google-cloud-aiplatform[adk,agent_engines]"],
    # CMEK configuration through Vertex AI platform settings
)
```

**CMEK covers:**
- Agent code and configuration at rest
- Session data
- Memory Bank data
- Logs and traces

---

## Private Service Connect (PSC)

For agents that must not traverse the public internet:

- **PSC Interface**: Creates a private endpoint within your VPC
- **DNS Peering**: Resolves Agent Engine endpoints to private IPs
- **Network Isolation**: Agent traffic stays within Google's network

```bash
# Configure PSC for Agent Engine
# 1. Create a PSC endpoint in your VPC
# 2. Configure DNS peering for aiplatform.googleapis.com
# 3. Deploy agents that connect through the PSC endpoint
```

For detailed security setup, IAM allow/deny policies, Principal Access Boundary, OAuth integration patterns, API key management, CMEK configuration, and PSC setup, see [references/security-identity.md](references/security-identity.md).

---

## Evaluating Agents

### GenAI Evaluation Service

Vertex AI provides a managed evaluation service for measuring agent quality:

```python
from vertexai.evaluation import EvalTask

# Define evaluation criteria
eval_task = EvalTask(
    dataset="gs://your-bucket/eval-dataset.jsonl",
    metrics=[
        "tool_call_accuracy",
        "response_quality",
        "safety",
    ],
)

# Run evaluation
results = eval_task.evaluate(
    agent_engine=agent_engine,
)
print(f"Tool accuracy: {results.metrics['tool_call_accuracy']}")
print(f"Response quality: {results.metrics['response_quality']}")
```

### Evaluation Metrics

| Metric | What It Measures |
|--------|-----------------|
| Tool call accuracy | Whether the agent calls the right tools with correct parameters |
| Response quality | Relevance and helpfulness of agent responses |
| Safety | Absence of harmful or inappropriate content |
| Groundedness | Whether responses are grounded in provided context |
| Instruction following | How well the agent follows its instructions |

### Evaluation Dataset Format

```json
{
  "input": "What's the weather in Tokyo?",
  "expected_tool_calls": [
    {"tool": "get_weather", "args": {"city": "Tokyo"}}
  ],
  "expected_output_keywords": ["temperature", "Tokyo"]
}
```

### Continuous Evaluation

Set up periodic evaluation to track agent quality over time:

1. Create evaluation datasets covering key scenarios
2. Run evaluations after each deployment
3. Set quality thresholds for deployment gates
4. Track metrics trends in dashboards

---

## Decision Guide

**Observability:**

```
Need request tracing?          -> Enable Cloud Trace (ENABLE_TRACING=true)
Need performance metrics?      -> Cloud Monitoring built-in metrics
Need custom metrics?           -> Log-based metrics or user-defined metrics
Need structured logs?          -> Python logging + Cloud Logging client
Need alerts?                   -> Cloud Monitoring alerting policies
```

**Security:**

```
Need per-agent identity?       -> Provision agent identity via IAM
Need third-party API keys?     -> Secret Manager
Need OAuth for users?          -> OAuth integration pattern
Need encryption control?       -> CMEK
Need private networking?       -> Private Service Connect (PSC)
Need access control?           -> IAM roles + conditions
```

**Evaluation:**

```
Measure tool accuracy?         -> GenAI evaluation with tool_call_accuracy
Measure response quality?      -> GenAI evaluation with response_quality
Continuous quality tracking?   -> Periodic evaluation + dashboards
Deployment gates?              -> Quality thresholds in CI/CD
```
