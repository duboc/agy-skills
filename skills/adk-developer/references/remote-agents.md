# Remote Agents and the A2A Protocol

How to build distributed agent systems where agents communicate across services, teams, and languages using the Agent-to-Agent (A2A) protocol.

## Local vs Remote: When to Go Distributed

Keep agents in the same process when they share state and belong to the same team. Distribute them when:

- **Separate deployments** -- agents run on different servers or in different containers
- **Team boundaries** -- different teams own different agents
- **Language mixing** -- a Python agent needs to call a Go agent
- **Independent scaling** -- agents have very different resource requirements
- **Formal contracts** -- you need versioned APIs between components

If none of these apply, local `sub_agents` are simpler and faster.

## How A2A Works

A2A is an HTTP-based protocol where agents publish **agent cards** (JSON descriptions of their capabilities) and communicate via structured messages.

```
Your App                                     Remote Service
┌──────────────┐    HTTP/A2A    ┌──────────────────┐
│ Root Agent   │                │  A2A Server      │
│   └─ Remote  │────────────>  │   └─ Math Agent  │
│      A2aAgent│  <────────────│      (your code) │
└──────────────┘               └──────────────────┘
```

The consuming side uses `RemoteA2aAgent` as a drop-in replacement for local sub-agents. The exposing side wraps any ADK agent with `to_a2a()`.

## Setting Up: Install A2A Support

A2A dependencies are not included in base `google-adk`. Install the extra:

```bash
pip install google-adk[a2a]
```

---

## Exposing an Agent (Server Side)

### Quick Start with `to_a2a()`

The fastest way to make any agent accessible over A2A:

```python
# services/inventory/agent.py
from google.adk.agents import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a

def check_stock(product_id: str, warehouse: str = "main") -> dict:
    """Check inventory levels for a product.

    Args:
        product_id: The product SKU.
        warehouse: Which warehouse to check.
    """
    # ... database lookup ...
    return {"product_id": product_id, "warehouse": warehouse, "quantity": 42, "available": True}

root_agent = Agent(
    name="inventory_service",
    model="gemini-2.5-flash",
    instruction="You manage inventory queries. Use check_stock to look up product availability.",
    tools=[check_stock],
)

# One line to expose as A2A
app = to_a2a(root_agent, port=8002)
```

Run it:

```bash
uvicorn services.inventory.agent:app --host 0.0.0.0 --port 8002
```

Verify the agent card is published:

```bash
curl -s http://localhost:8002/.well-known/agent-card.json | python -m json.tool
```

### What `to_a2a()` Generates

It auto-creates an agent card from your agent's metadata:
- `name` and `description` come from the agent
- Each tool becomes a `skill` entry in the card
- Default version is `"0.0.1"`

### Custom Agent Cards

Override the auto-generated card when you need specific metadata:

```python
from a2a.types import AgentCard

custom_card = AgentCard(
    name="inventory_service",
    url="https://inventory.internal.company.com",
    description="Production inventory management service",
    version="2.1.0",
    capabilities={},
    skills=[],
    defaultInputModes=["text/plain"],
    defaultOutputModes=["text/plain"],
    supportsAuthenticatedExtendedCard=False,
)

app = to_a2a(root_agent, port=8002, agent_card=custom_card)
```

### CLI-Based Exposure

Alternative to `to_a2a()` for quick local testing:

```bash
adk api_server --a2a --port 8002 path/to/agent_folder
```

Requires a manual `agent-card.json` file in the agent folder.

---

## Consuming a Remote Agent (Client Side)

### Connecting to an A2A Service

```python
# app/agent.py
from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

inventory = RemoteA2aAgent(
    name="inventory_service",
    description="Checks product stock levels across warehouses",
    agent_card="http://localhost:8002/.well-known/agent-card.json",
)

order_agent = Agent(
    name="order_processor",
    model="gemini-2.5-flash",
    instruction="""Process customer orders.
    Before confirming any order, check stock availability with inventory_service.
    If the product is out of stock, suggest alternatives.""",
    sub_agents=[inventory],
)
```

`RemoteA2aAgent` behaves like any other sub-agent -- the root agent's LLM decides when to delegate based on the `description` field.

### Mixing Local and Remote Agents

```python
# Local specialist
pricing_agent = Agent(
    name="pricing",
    model="gemini-2.5-flash",
    description="Calculates prices, discounts, and promotions",
    instruction="...",
    tools=[calculate_price, apply_discount],
)

# Remote service
shipping = RemoteA2aAgent(
    name="shipping_service",
    description="Estimates shipping costs and delivery times",
    agent_card="http://shipping:8003/.well-known/agent-card.json",
)

root_agent = Agent(
    name="checkout",
    model="gemini-2.5-flash",
    instruction="Handle the checkout process...",
    sub_agents=[pricing_agent, shipping],
)
```

---

## Go Implementation

### Exposing (Go)

```go
package main

import (
    "context"
    "strconv"

    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/launcher/a2a"
    "google.golang.org/adk/launcher/web"
    "google.golang.org/adk/model/gemini"
    "google.golang.org/genai"
)

func main() {
    ctx := context.Background()
    port := 8002

    model, _ := gemini.NewModel(ctx, "gemini-2.0-flash", &genai.ClientConfig{})
    agent, _ := llmagent.New(llmagent.Config{
        Name:        "inventory_service",
        Model:       model,
        Instruction: "Handle inventory queries.",
        Tools:       []tool.Tool{stockCheckTool},
    })

    launcher := web.NewLauncher(a2a.NewLauncher())
    launcher.Launch(ctx, agent,
        "a2a", "--a2a_agent_url", "http://localhost:"+strconv.Itoa(port),
        "--port", strconv.Itoa(port),
    )
}
```

### Consuming (Go)

```go
import "google.golang.org/adk/agent/remoteagent"

remote, _ := remoteagent.NewA2A(remoteagent.A2AConfig{
    Name:            "inventory_service",
    Description:     "Checks product stock levels",
    AgentCardSource: "http://localhost:8002",
})

root, _ := llmagent.New(llmagent.Config{
    Name:      "order_processor",
    Model:     model,
    SubAgents: []agent.Agent{remote},
})
```

---

## Passing Metadata Across Services

Propagate tracing IDs, user context, or feature flags through A2A calls:

```python
from google.adk.agents.run_config import RunConfig

config = RunConfig(
    custom_metadata={
        "correlation_id": "req-abc-123",
        "user_tier": "enterprise",
        "feature_flags": {"new_pricing": True},
    }
)

# On the remote side, metadata arrives in:
# event.custom_metadata["a2a_metadata"]["correlation_id"]
```

---

## Testing A2A Systems

Test the consuming side with `InMemoryRunner` while the remote service runs separately:

```python
import pytest
from google.adk.runners import InMemoryRunner
from google.genai import types
from app.agent import root_agent

@pytest.mark.asyncio
async def test_order_checks_inventory():
    """Verify that order processing delegates to inventory service."""
    runner = InMemoryRunner(agent=root_agent, app_name="test")
    session = await runner.session_service.create_session(
        user_id="test_user", app_name="test",
    )

    msg = types.Content(
        role="user",
        parts=[types.Part.from_text("Is product SKU-789 in stock?")],
    )

    responses = []
    async for event in runner.run_async(
        user_id="test_user", session_id=session.id, new_message=msg,
    ):
        responses.append(event)

    final = responses[-1].content.parts[0].text.lower()
    assert "stock" in final or "available" in final

# IMPORTANT: The remote A2A server must be running before tests execute.
```

**Async warning:** Run all A2A tests within a single `asyncio.run()` invocation. Separate `asyncio.run()` calls close the event loop, breaking httpx connections.

---

## Port Allocation

| Service | Suggested Port | Notes |
|---------|---------------|-------|
| Main agent (`adk web`) | 8000 | Default for dev UI |
| First remote agent | 8001 | |
| Additional remote agents | 8002+ | One port per service |

---

## Troubleshooting

| Problem | Likely Cause | Solution |
|---------|-------------|----------|
| `Connection refused` | Remote agent isn't running | Start the service, verify port |
| Agent card 404 | Wrong URL or agent not exposing A2A | Check `/.well-known/agent-card.json` endpoint |
| `ImportError` on A2A modules | Missing dependencies | `pip install google-adk[a2a]` |
| `Event loop is closed` in tests | Multiple `asyncio.run()` calls | Run all tests in one async session |
| Root agent never delegates | Bad description on RemoteA2aAgent | Description must clearly match the query type |
| `UserWarning` about experimental | ADK's A2A integration is experimental | Suppress with `warnings.filterwarnings("ignore", category=UserWarning)` |
