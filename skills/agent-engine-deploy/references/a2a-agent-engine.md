# A2A Agents on Agent Engine Reference

Detailed guide for deploying and operating Agent-to-Agent (A2A) protocol agents on Vertex AI Agent Engine.

## Overview

The A2A protocol enables standardized communication between agents across different services and platforms. Agent Engine provides managed hosting for A2A agents, handling discovery, routing, and execution.

## Core Components

### AgentCard

The AgentCard describes an agent's capabilities and is used for discovery:

```python
from a2a.types import AgentCard, AgentSkill, AgentCapabilities

agent_card = AgentCard(
    name="Customer Support Agent",
    description="Handles customer support queries including order status, returns, and account issues",
    url="https://your-endpoint.run.app",
    version="1.0.0",
    capabilities=AgentCapabilities(
        streaming=True,
        pushNotifications=False,
    ),
    skills=[
        AgentSkill(
            id="order-status",
            name="Order Status",
            description="Check the status of customer orders",
            examples=["What's the status of order #12345?"],
        ),
        AgentSkill(
            id="returns",
            name="Returns Processing",
            description="Process product returns and refunds",
            examples=["I want to return my recent purchase"],
        ),
    ],
)
```

### AgentExecutor

The AgentExecutor bridges ADK agents with the A2A protocol:

```python
from vertexai.agent_engines import A2aAgent, AgentExecutor
from google.adk.agents import Agent

# Define your ADK agent
support_agent = Agent(
    name="support",
    model="gemini-2.5-flash",
    instruction="""You are a customer support agent.
    Handle order inquiries, returns, and account issues.
    Use available tools to look up information.""",
    tools=[lookup_order, process_return, check_account],
)

# Create A2A wrapper with AgentExecutor
a2a_agent = A2aAgent(
    agent=support_agent,
    agent_executor=AgentExecutor(),
)
```

### Deploying A2A Agents

```python
import vertexai

client = vertexai.Client(
    project="your-project-id",
    location="us-central1",
)

agent_engine = client.agent_engines.create(
    agent_engine=a2a_agent,
    display_name="support-a2a",
    requirements=[
        "google-cloud-aiplatform[adk,agent_engines,a2a]",
    ],
)
```

## LlmAgent with A2A

Use `LlmAgent` for agents that need A2A capabilities with full LLM control:

```python
from google.adk.agents import LlmAgent
from google.genai import types

llm_agent = LlmAgent(
    name="coordinator",
    model="gemini-2.5-pro",
    description="Coordinates tasks across multiple specialized agents",
    instruction="""You are a task coordinator.
    Route requests to the appropriate specialist agent.
    Synthesize responses from multiple agents when needed.""",
    generate_content_config=types.GenerateContentConfig(
        temperature=0.3,
    ),
    tools=[...],
    sub_agents=[...],
)

a2a_agent = A2aAgent(
    agent=llm_agent,
    agent_executor=AgentExecutor(),
)
```

## Multi-Agent A2A Architecture

### Hub-and-Spoke Pattern

A coordinator agent that delegates to specialist A2A agents:

```python
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.agents import RemoteA2aAgent

# Remote specialist agents (deployed as A2A on Agent Engine)
billing_agent = RemoteA2aAgent(
    name="billing",
    description="Handles billing and payment queries",
    agent_card_url="https://billing-agent.run.app/.well-known/agent.json",
)

shipping_agent = RemoteA2aAgent(
    name="shipping",
    description="Handles shipping and delivery queries",
    agent_card_url="https://shipping-agent.run.app/.well-known/agent.json",
)

# Coordinator agent
coordinator = Agent(
    name="coordinator",
    model="gemini-2.5-flash",
    instruction="Route customer queries to the appropriate specialist.",
    sub_agents=[billing_agent, shipping_agent],
)
```

### Peer-to-Peer Pattern

Agents that communicate directly without a central coordinator:

```python
# Each agent is deployed independently as an A2A agent
# They discover each other via AgentCard URLs

agent_a = Agent(
    name="data_analyst",
    model="gemini-2.5-flash",
    instruction="Analyze data and request visualizations from the chart agent.",
    tools=[
        RemoteA2aAgent(
            name="chart_maker",
            description="Creates charts and visualizations",
            agent_card_url="https://chart-agent.run.app/.well-known/agent.json",
        ),
    ],
)
```

## Local Testing

### Testing A2A Agents Locally

Before deploying to Agent Engine, test A2A agents locally:

```python
import asyncio
from google.adk.runners import InMemoryRunner
from google.genai import types

async def test_a2a_agent():
    # Use InMemoryRunner for local testing
    runner = InMemoryRunner(
        agent=support_agent,  # The underlying ADK agent
        app_name="test",
    )

    session = await runner.session_service.create_session(
        user_id="test_user",
        app_name="test",
    )

    content = types.Content(
        role="user",
        parts=[types.Part.from_text("What's the status of order #12345?")],
    )

    events = []
    async for event in runner.run_async(
        user_id="test_user",
        session_id=session.id,
        new_message=content,
    ):
        events.append(event)
        print(f"{event.author}: {event.content}")

    return events

asyncio.run(test_a2a_agent())
```

### Testing A2A Protocol Locally

Test the full A2A protocol stack with a local server:

```python
# Start local A2A server
# adk run --a2a my_agent

# Test with A2A client
from a2a.client import A2AClient

async def test_a2a_protocol():
    client = A2AClient(url="http://localhost:8080")

    # Get agent card
    card = await client.get_agent_card()
    print(f"Agent: {card.name}")
    print(f"Skills: {[s.name for s in card.skills]}")

    # Send a message
    response = await client.send_message(
        message="Check order #12345",
    )
    print(f"Response: {response}")
```

## A2A Message Format

### Request

```json
{
  "jsonrpc": "2.0",
  "method": "message/send",
  "params": {
    "message": {
      "role": "user",
      "parts": [
        {
          "kind": "text",
          "text": "What's the status of order #12345?"
        }
      ]
    }
  },
  "id": "request-001"
}
```

### Response

```json
{
  "jsonrpc": "2.0",
  "result": {
    "message": {
      "role": "agent",
      "parts": [
        {
          "kind": "text",
          "text": "Order #12345 is currently in transit..."
        }
      ]
    },
    "status": "completed"
  },
  "id": "request-001"
}
```

## Troubleshooting A2A

| Issue | Cause | Solution |
|-------|-------|----------|
| Agent not discoverable | AgentCard not served | Verify `/.well-known/agent.json` endpoint |
| Connection refused | Wrong URL or agent down | Check agent_card_url and deployment status |
| Skill mismatch | AgentCard skills not aligned | Update AgentCard to match agent capabilities |
| Serialization error | Incompatible message format | Ensure A2A protocol version compatibility |
| Auth failure | Missing credentials | Configure service-to-service authentication |
