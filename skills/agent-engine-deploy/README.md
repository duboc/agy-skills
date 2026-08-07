# Agent Engine Deploy

A Gemini CLI skill for deploying, managing, and querying ADK agents on Vertex AI Agent Engine -- the managed runtime for production agent hosting.

## What It Does

This skill gives your coding agent deep knowledge of the Vertex AI Agent Engine deployment lifecycle, covering SDK setup, agent deployment with `AdkApp`, querying deployed agents, lifecycle management, A2A agents on Agent Engine, bidirectional streaming, and performance optimization.

## When Does It Activate?

The skill activates when you mention:

- Vertex AI Agent Engine, agent deployment, production agents
- AdkApp, agent_engines.create, async_stream_query
- Deploying ADK agents to Vertex AI
- Managing deployed agents (list, get, update, delete)
- A2A agents on Agent Engine, AgentExecutor
- Bidirectional streaming, real-time agent communication
- Cold start optimization, scaling, concurrency
- Staging buckets, deployment requirements, environment variables

## Topics Covered

| Area | What You Get |
|------|-------------|
| SDK Setup | `vertexai.Client`, authentication, required packages |
| Deployment | `AdkApp`, `client.agent_engines.create()`, requirements, env vars, staging |
| Querying | `async_stream_query`, synchronous query, streaming events |
| Management | List, get, update, delete deployed agents |
| A2A Agents | `A2aAgent`, `AgentExecutor`, AgentCard, cross-service communication |
| Bidi Streaming | Real-time bidirectional streaming patterns |
| Performance | Cold start mitigation, concurrency, min/max instances, scaling |
| Patterns | Deployment configurations, staging buckets, telemetry setup |

## Installation

### Option A: Gemini CLI native

```bash
gemini skills install https://github.com/duboc/agy-skills.git --path skills/agent-engine-deploy
```

### Option B: One-liner

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- agent-engine-deploy
```

For user-scope installation (available across all projects):

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- agent-engine-deploy --scope user
```

### Option C: Manual

```bash
cp -r skills/agent-engine-deploy ~/.gemini/skills/agent-engine-deploy
```

## Usage Examples

- "Deploy my ADK agent to Vertex AI Agent Engine"
- "How do I set up AdkApp for production deployment?"
- "Query my deployed agent with streaming"
- "List all my deployed agents on Agent Engine"
- "Deploy an A2A agent on Agent Engine"
- "Optimize cold starts for my deployed agent"
- "Update my deployed agent with new code"
- "Set up bidirectional streaming with Agent Engine"

## Included References

| File | Description |
|------|-------------|
| **deployment-patterns.md** | Detailed deployment configurations, staging buckets, requirements, env vars, telemetry setup |
| **a2a-agent-engine.md** | A2A protocol on Agent Engine: AgentCard, AgentExecutor, LlmAgent, local testing |
| **performance-scaling.md** | Cold start mitigation, container concurrency, min/max instances, bidi streaming setup |
