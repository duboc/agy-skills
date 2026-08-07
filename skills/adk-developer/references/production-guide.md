# Running ADK Agents in Production

Deployment options, safety mechanisms, configuration management, and operational patterns.

## Deployment Options

### Local Development

```bash
adk run my_agent          # Interactive CLI
adk web my_agent          # Web UI at localhost:8000
```

The web UI is for development and debugging only -- not for production use.

### Google Cloud Run

Deploy agents as containerized services:

```bash
adk deploy cloud_run \
    --project=my-gcp-project \
    --region=us-central1 \
    --service_name=order-agent \
    --app_name=my_agent \
    --agent_module=my_agent.agent
```

### Vertex AI Agent Engine

For managed agent hosting with built-in session management:

```python
from google.adk.sessions import VertexAiSessionService

session_service = VertexAiSessionService(
    project="my-gcp-project",
    location="us-central1",
)
```

### Custom API Server (FastAPI)

Embed agents in your own HTTP service:

```python
from fastapi import FastAPI
from google.adk.runners import InMemoryRunner
from google.genai import types

app = FastAPI()
runner = InMemoryRunner(agent=root_agent, app_name="production")

@app.post("/api/chat")
async def handle_message(user_id: str, session_id: str, message: str):
    content = types.Content(
        role="user",
        parts=[types.Part.from_text(text=message)],
    )
    events = []
    async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=content,
    ):
        events.append(event)

    return {
        "response": events[-1].content.parts[0].text,
        "event_count": len(events),
    }
```

---

## Safety and Guardrails

### Layered Defense Model

No single safety mechanism is sufficient. Use multiple layers:

| Layer | ADK Mechanism | Purpose |
|-------|--------------|---------|
| Input screening | `before_model_callback` | Block prompt injection and jailbreaks |
| Tool parameter checks | `before_tool_callback` | Validate arguments before execution |
| Tool output checks | `after_tool_callback` | Sanitize tool results |
| Output screening | `after_model_callback` | Catch harmful or off-policy responses |
| Behavioral constraints | Agent `instruction` | Define role boundaries and forbidden actions |

### Input Safety Gate

```python
from google.genai import types

BLOCKED_PATTERNS = ["ignore previous instructions", "system prompt", "jailbreak"]

def screen_input(callback_context, llm_request):
    """Block suspicious inputs before they reach the model."""
    if not llm_request.contents:
        return None

    last = llm_request.contents[-1]
    if last.role != "user" or not last.parts:
        return None

    text = last.parts[0].text.lower() if last.parts[0].text else ""
    for pattern in BLOCKED_PATTERNS:
        if pattern in text:
            return types.Content(
                role="model",
                parts=[types.Part.from_text(
                    "I can't process that request. Please rephrase."
                )],
            )
    return None

agent = Agent(
    name="safe_agent",
    model="gemini-2.5-flash",
    instruction="...",
    before_model_callback=screen_input,
)
```

### Tool Parameter Validation

```python
def validate_tool_inputs(tool, args, tool_context):
    """Reject tool calls with invalid parameters."""
    if tool.name == "transfer_funds":
        amount = args.get("amount", 0)
        if amount > 10000:
            return {"error": "Transfer amount exceeds single-transaction limit of $10,000."}
        if amount <= 0:
            return {"error": "Transfer amount must be positive."}
    return None  # Proceed with execution

agent = Agent(
    name="banking_agent",
    before_tool_callback=validate_tool_inputs,
    ...
)
```

### LLM-as-Judge Safety

```python
from google.adk.agents.plugins import LlmAsAJudge
from google.adk.runners import InMemoryRunner

runner = InMemoryRunner(
    agent=root_agent,
    app_name="guarded_app",
    plugins=[LlmAsAJudge()],
)
```

---

## Callback Patterns

### Session Initialization

Set up default state values at the start of every session:

```python
import uuid
from datetime import datetime, timezone

def init_session(callback_context):
    """Populate initial session state."""
    callback_context.state.setdefault("session_id", str(uuid.uuid4()))
    callback_context.state.setdefault("started_at", datetime.now(timezone.utc).isoformat())
    callback_context.state.setdefault("interaction_count", 0)
    callback_context.state["interaction_count"] += 1

agent = Agent(
    name="tracked_agent",
    before_agent_callback=init_session,
    ...
)
```

### Rate Limiting

Throttle model calls to stay within API quotas:

```python
import time

MAX_REQUESTS_PER_MINUTE = 15

def throttle(callback_context, llm_request):
    """Enforce rate limits on model calls."""
    now = time.time()
    window_start = callback_context.state.get("rate_window_start", now)
    call_count = callback_context.state.get("rate_call_count", 0) + 1

    if now - window_start > 60:
        # New window
        callback_context.state["rate_window_start"] = now
        callback_context.state["rate_call_count"] = 1
        return None

    if call_count > MAX_REQUESTS_PER_MINUTE:
        wait = 61 - (now - window_start)
        if wait > 0:
            time.sleep(wait)
        callback_context.state["rate_window_start"] = time.time()
        callback_context.state["rate_call_count"] = 1
    else:
        callback_context.state["rate_call_count"] = call_count
    return None
```

---

## Configuration Management

### Environment-Based Config

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class AgentConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="AGENT_")

    model_name: str = "gemini-2.5-flash"
    temperature: float = 0.5
    google_api_key: str = ""
    google_cloud_project: str = ""
    google_cloud_location: str = "us-central1"

config = AgentConfig()
```

### .env File Patterns

**For API key auth:**
```bash
GOOGLE_API_KEY=your-api-key
```

**For Vertex AI (GCP) auth:**
```bash
GOOGLE_CLOUD_PROJECT=my-project
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=TRUE
```

### Model Selection Per Agent

Match model capability to task complexity:

```python
from google.genai import types

# Fast model for simple routing and classification
router = Agent(
    name="router",
    model="gemini-2.5-flash",
    generate_content_config=types.GenerateContentConfig(temperature=0.1),
    ...
)

# Powerful model for complex reasoning
analyst = Agent(
    name="analyst",
    model="gemini-2.5-pro",
    generate_content_config=types.GenerateContentConfig(temperature=0.3),
    ...
)
```

---

## Session and Memory Services

| Service | Use Case | Persistence |
|---------|----------|-------------|
| `InMemorySessionService` | Dev/test | None (process lifetime) |
| `DatabaseSessionService` | Production with custom DB | Database-backed |
| `VertexAiSessionService` | GCP production | Managed by Vertex AI |
| `InMemoryMemoryService` | Dev/test for long-term memory | None |
| `VertexAiRagMemoryService` | Production semantic memory | Managed RAG corpus |

---

## Operational Checklist

Before deploying an agent to production:

- [ ] All tools handle errors gracefully (return error dicts, don't raise)
- [ ] `before_model_callback` screens for prompt injection
- [ ] `before_tool_callback` validates parameters for sensitive operations
- [ ] `LoopAgent` instances have `max_iterations` set
- [ ] API keys are in `.env` or secret manager, not in source code
- [ ] Session service is appropriate for the deployment (not `InMemory` in prod)
- [ ] Agent instructions use positive framing ("do X" not "don't do Y")
- [ ] Sub-agent descriptions clearly describe routing criteria
- [ ] Eval suite covers key tool trajectories and response quality
- [ ] Structured output (`output_schema`) is used between pipeline stages
