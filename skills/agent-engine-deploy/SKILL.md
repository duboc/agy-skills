---
name: agent-engine-deploy
description: "Deploy, manage, and query ADK agents on Vertex AI Agent Engine. Use when deploying agents to production, creating AdkApp instances, querying deployed agents, managing agent lifecycle (list, get, update, delete), working with A2A agents on Agent Engine, configuring bidirectional streaming, optimizing cold starts and scaling, or when the user mentions Agent Engine, Vertex AI agent deployment, agent_engines.create, AdkApp, async_stream_query, or production agent hosting."
---

# Vertex AI Agent Engine Deployment Guide

## Overview

Vertex AI Agent Engine is a managed runtime for deploying, hosting, and operating ADK agents in production. It handles infrastructure, scaling, authentication, and lifecycle management so you can focus on agent logic.

This guide covers the full deployment lifecycle: SDK setup, deploying agents, querying them, managing deployed instances, A2A agents on Agent Engine, bidirectional streaming, and performance optimization.

## Documentation & Resources

- **Agent Engine Overview**: https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview
- **Deploy ADK Agents**: https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/deploy/adk
- **A2A on Agent Engine**: https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/deploy/a2a

## Quick Reference

| Task | Approach |
|------|----------|
| Initialize SDK | `vertexai.Client(project=..., location=...)` |
| Deploy ADK agent | `client.agent_engines.create(agent_engine=..., display_name=...)` |
| Query agent | `agent_engine.async_stream_query(...)` |
| List agents | `client.agent_engines.list()` |
| Update agent | `client.agent_engines.update(agent_engine=..., update_mask=...)` |
| Delete agent | `client.agent_engines.delete(name=...)` |
| A2A agent | `A2aAgent` + `AgentExecutor` |
| Bidi streaming | `agent_engine.async_stream_query()` with streaming config |
| Reduce cold starts | Set min instances, optimize imports |

---

## SDK Setup

### Authentication and Client Initialization

```python
import vertexai

# Initialize the Vertex AI client
client = vertexai.Client(
    project="your-project-id",
    location="us-central1",
)
```

**Prerequisites:**
- Google Cloud project with Vertex AI API enabled
- Authentication via `gcloud auth application-default login` or service account
- Required roles: `roles/aiplatform.user` or `roles/aiplatform.admin`

### Required Packages

```bash
pip install google-cloud-aiplatform[adk,agent_engines]
```

For A2A support:

```bash
pip install google-cloud-aiplatform[adk,agent_engines,a2a]
```

---

## Deploying ADK Agents

### Basic Deployment with AdkApp

Wrap your ADK agent in `AdkApp` and deploy via the client:

```python
from google.adk.agents import Agent
from vertexai.agent_engines import AdkApp

# Define your agent
root_agent = Agent(
    name="support_agent",
    model="gemini-2.5-flash",
    description="Customer support assistant",
    instruction="You are a helpful customer support agent...",
    tools=[...],
)

# Wrap in AdkApp
adk_app = AdkApp(agent=root_agent)

# Deploy to Agent Engine
agent_engine = client.agent_engines.create(
    agent_engine=adk_app,
    display_name="support-agent-prod",
)
```

### Deployment with Requirements and Environment Variables

```python
agent_engine = client.agent_engines.create(
    agent_engine=adk_app,
    display_name="support-agent-prod",
    requirements=[
        "google-cloud-aiplatform[adk,agent_engines]",
        "requests>=2.31.0",
        "beautifulsoup4",
    ],
    env_vars={
        "LOG_LEVEL": "INFO",
        "ENABLE_TRACING": "true",
    },
)
```

### Deployment with Staging Bucket

For agents with local dependencies or extra files:

```python
agent_engine = client.agent_engines.create(
    agent_engine=adk_app,
    display_name="support-agent-prod",
    requirements=["google-cloud-aiplatform[adk,agent_engines]"],
    gcs_dir_name="gs://your-bucket/agent-staging/",
    extra_packages=["./my_custom_lib-0.1.0.tar.gz"],
)
```

### Deployment with Cloud Storage Artifacts

```python
agent_engine = client.agent_engines.create(
    agent_engine=adk_app,
    display_name="support-agent-prod",
    requirements=["google-cloud-aiplatform[adk,agent_engines]"],
    gcs_dir_name="gs://my-bucket/staging/",
)
```

For detailed deployment configurations, staging patterns, telemetry setup, and advanced options, see [references/deployment-patterns.md](references/deployment-patterns.md).

---

## Querying Deployed Agents

### Streaming Query

```python
import asyncio

async def query_agent(agent_engine, user_id, session_id, message):
    async for event in agent_engine.async_stream_query(
        user_id=user_id,
        session_id=session_id,
        message=message,
    ):
        print(event)

asyncio.run(query_agent(
    agent_engine=agent_engine,
    user_id="user-123",
    session_id=None,  # Creates a new session if None
    message="Help me reset my password",
))
```

### Synchronous Query

```python
response = agent_engine.query(
    user_id="user-123",
    session_id="session-456",
    message="What's the status of my order?",
)
print(response)
```

### Getting the Resource Name

After deployment, the agent engine resource name is used for management operations:

```python
# The resource name follows this pattern:
# projects/{project}/locations/{location}/reasoningEngines/{engine_id}
resource_name = agent_engine.api_resource.name
print(f"Deployed agent: {resource_name}")
```

---

## Managing Deployed Agents

### List All Deployed Agents

```python
agent_engines = client.agent_engines.list()
for engine in agent_engines:
    print(f"Name: {engine.name}")
    print(f"Display Name: {engine.display_name}")
    print(f"Create Time: {engine.create_time}")
    print("---")
```

### Get a Specific Agent

```python
agent_engine = client.agent_engines.get(
    name="projects/my-project/locations/us-central1/reasoningEngines/12345"
)
print(agent_engine.display_name)
```

### Update a Deployed Agent

```python
# Update the agent code/config
updated_app = AdkApp(agent=updated_root_agent)

client.agent_engines.update(
    agent_engine=updated_app,
    update_mask=["agent_engine"],
    display_name="support-agent-prod-v2",
)
```

### Delete a Deployed Agent

```python
client.agent_engines.delete(
    name="projects/my-project/locations/us-central1/reasoningEngines/12345"
)
```

---

## A2A Agents on Agent Engine

The Agent-to-Agent (A2A) protocol allows agents deployed on Agent Engine to communicate with other agents across services and platforms.

### Deploying an A2A Agent

```python
from vertexai.agent_engines import A2aAgent, AgentExecutor

# Define your ADK agent
support_agent = Agent(
    name="support",
    model="gemini-2.5-flash",
    instruction="Handle customer support queries.",
    tools=[...],
)

# Create an A2A-compatible wrapper
a2a_agent = A2aAgent(
    agent=support_agent,
    agent_executor=AgentExecutor(),
)

# Deploy to Agent Engine
agent_engine = client.agent_engines.create(
    agent_engine=a2a_agent,
    display_name="support-a2a-agent",
    requirements=["google-cloud-aiplatform[adk,agent_engines,a2a]"],
)
```

### Agent Card

A2A agents expose an AgentCard describing their capabilities:

```python
# The AgentCard is auto-generated from the agent's metadata
# You can customize it:
from a2a.types import AgentCard, AgentSkill

custom_card = AgentCard(
    name="Support Agent",
    description="Handles customer support queries",
    url="https://your-endpoint.run.app",
    skills=[
        AgentSkill(
            id="password-reset",
            name="Password Reset",
            description="Help users reset their passwords",
        ),
    ],
    version="1.0.0",
)
```

For A2A protocol details, AgentExecutor patterns, LlmAgent integration, and local testing, see [references/a2a-agent-engine.md](references/a2a-agent-engine.md).

---

## Bidirectional Streaming

Agent Engine supports bidirectional streaming for real-time, interactive agent communication:

```python
async def bidi_stream_example(agent_engine, user_id, session_id):
    async for event in agent_engine.async_stream_query(
        user_id=user_id,
        session_id=session_id,
        message="Analyze this dataset and provide insights",
    ):
        if hasattr(event, "content"):
            for part in event.content.parts:
                if hasattr(part, "text"):
                    print(part.text, end="", flush=True)
        elif hasattr(event, "actions"):
            print(f"\nAgent action: {event.actions}")
```

---

## Performance Optimization

### Cold Start Mitigation

- **Set minimum instances** to keep containers warm
- **Optimize imports** -- lazy-load heavy libraries
- **Reduce package size** -- only include necessary dependencies
- **Use lightweight base models** when possible

### Concurrency and Scaling

```python
# Configure scaling during deployment
agent_engine = client.agent_engines.create(
    agent_engine=adk_app,
    display_name="high-traffic-agent",
    requirements=["google-cloud-aiplatform[adk,agent_engines]"],
)
```

**Scaling guidelines:**
- Agent Engine auto-scales based on traffic
- Set `min_replica_count` to avoid cold starts for latency-sensitive workloads
- Set `max_replica_count` to control costs
- Each replica handles concurrent requests based on container concurrency settings

For cold start strategies, container concurrency tuning, min/max instance configuration, and bidirectional streaming setup, see [references/performance-scaling.md](references/performance-scaling.md).

---

## Decision Guide

**Deployment approach:**

```
Simple single agent?           -> AdkApp + client.agent_engines.create()
Agent with custom packages?    -> Add requirements + extra_packages
Agent needs cross-service?     -> A2aAgent with AgentExecutor
Need real-time streaming?      -> async_stream_query with bidi streaming
High-traffic, low-latency?     -> Configure min instances + concurrency
Need staging/testing?          -> Use gcs_dir_name for staging artifacts
```

**Management operations:**

```
See all deployed agents?       -> client.agent_engines.list()
Check agent details?           -> client.agent_engines.get(name=...)
Push updated agent code?       -> client.agent_engines.update(...)
Remove an agent?               -> client.agent_engines.delete(name=...)
```
