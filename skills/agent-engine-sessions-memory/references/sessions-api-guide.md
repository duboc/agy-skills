# Sessions API Reference

Detailed guide for managing Vertex AI Agent Engine sessions via REST API, Console, and SDK.

## REST API Endpoints

### Base URL

```
https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/reasoningEngines/{ENGINE_ID}
```

### Create Session

```bash
curl -X POST \
  "https://us-central1-aiplatform.googleapis.com/v1/projects/my-project/locations/us-central1/reasoningEngines/12345/sessions" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "user-123"
  }'
```

**Response:**

```json
{
  "name": "projects/my-project/locations/us-central1/reasoningEngines/12345/sessions/session-789",
  "userId": "user-123",
  "createTime": "2025-01-15T10:30:00Z",
  "updateTime": "2025-01-15T10:30:00Z"
}
```

### Get Session

```bash
curl -X GET \
  "https://us-central1-aiplatform.googleapis.com/v1/projects/my-project/locations/us-central1/reasoningEngines/12345/sessions/session-789" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)"
```

### List Sessions

```bash
curl -X GET \
  "https://us-central1-aiplatform.googleapis.com/v1/projects/my-project/locations/us-central1/reasoningEngines/12345/sessions?filter=userId=user-123" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)"
```

**Query parameters:**

| Parameter | Description |
|-----------|-------------|
| `filter` | Filter expression (e.g., `userId=user-123`) |
| `pageSize` | Maximum sessions per page (default: 100) |
| `pageToken` | Token for next page of results |
| `orderBy` | Sort order (e.g., `createTime desc`) |

### Delete Session

```bash
curl -X DELETE \
  "https://us-central1-aiplatform.googleapis.com/v1/projects/my-project/locations/us-central1/reasoningEngines/12345/sessions/session-789" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)"
```

### Send Message (Query)

```bash
curl -X POST \
  "https://us-central1-aiplatform.googleapis.com/v1/projects/my-project/locations/us-central1/reasoningEngines/12345:query" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "userId": "user-123",
      "sessionId": "session-789",
      "message": "Hello, how can you help me?"
    }
  }'
```

### Stream Query

```bash
curl -X POST \
  "https://us-central1-aiplatform.googleapis.com/v1/projects/my-project/locations/us-central1/reasoningEngines/12345:streamQuery" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "userId": "user-123",
      "sessionId": "session-789",
      "message": "Explain quantum computing"
    }
  }'
```

## SDK Session Management

### Python SDK

```python
import vertexai

client = vertexai.Client(
    project="your-project-id",
    location="us-central1",
)

# Get a deployed agent engine
agent_engine = client.agent_engines.get(
    name="projects/my-project/locations/us-central1/reasoningEngines/12345"
)

# Create a session
session = agent_engine.create_session(user_id="user-123")

# Query with session
response = agent_engine.query(
    user_id="user-123",
    session_id=session.name,
    message="Hello!",
)

# Stream query
import asyncio

async def stream():
    async for event in agent_engine.async_stream_query(
        user_id="user-123",
        session_id=session.name,
        message="Tell me about AI",
    ):
        print(event)

asyncio.run(stream())

# List sessions
sessions = agent_engine.list_sessions(user_id="user-123")

# Delete session
agent_engine.delete_session(session_id=session.name)
```

## Session Events

### Event Structure

Each event in a session represents an interaction:

```json
{
  "name": "projects/.../sessions/session-789/events/event-001",
  "author": "user",
  "content": {
    "role": "user",
    "parts": [
      {
        "text": "What's the weather?"
      }
    ]
  },
  "createTime": "2025-01-15T10:31:00Z",
  "actions": {}
}
```

### Event Types

| Author | Description |
|--------|-------------|
| `user` | User-sent message |
| Agent name | Agent response (matches agent's `name` field) |
| Tool name | Tool invocation and result |

### Listing Events

```bash
curl -X GET \
  "https://us-central1-aiplatform.googleapis.com/v1/projects/my-project/locations/us-central1/reasoningEngines/12345/sessions/session-789/events" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)"
```

## Session State Management

### State via API

State is automatically managed through agent interactions. To read state:

```python
session = agent_engine.get_session(session_id="session-789")
state = session.state
print(f"Current state: {state}")
```

### State Scope Prefixes

| Prefix | Scope | Example Key | Behavior |
|--------|-------|------------|----------|
| (none) | Session | `cart` | Exists for session lifetime |
| `user:` | User | `user:preferences` | Shared across sessions for same user |
| `app:` | Application | `app:config` | Shared across all users and sessions |
| `temp:` | Turn | `temp:intermediate` | Cleared after each turn |

### State in Tools

```python
from google.adk.tools import ToolContext

def get_user_profile(tool_context: ToolContext) -> dict:
    """Retrieve user profile from session state."""
    # Read from different scopes
    session_cart = tool_context.state.get("cart", [])
    user_prefs = tool_context.state.get("user:preferences", {})
    app_config = tool_context.state.get("app:config", {})

    return {
        "cart": session_cart,
        "preferences": user_prefs,
        "config": app_config,
    }

def update_user_preferences(preference: str, value: str, tool_context: ToolContext) -> dict:
    """Update user preferences (persists across sessions)."""
    prefs = tool_context.state.get("user:preferences", {})
    prefs[preference] = value
    tool_context.state["user:preferences"] = prefs
    return {"updated": preference, "value": value}
```

## Session TTL Configuration

### Setting TTL

Configure how long sessions persist before automatic cleanup:

```python
# TTL is configured at the session service level
session_service = VertexAiSessionService(
    project="your-project-id",
    location="us-central1",
)

# Sessions will automatically expire based on the configured TTL
session = await session_service.create_session(
    app_name="my-app",
    user_id="user-123",
)
```

### TTL Guidelines

| Use Case | Recommended TTL | Reasoning |
|----------|----------------|-----------|
| Customer support | 24 hours | Support conversations typically resolve within a day |
| Shopping assistant | 7 days | Users may return to complete purchases |
| Personal assistant | 30 days | Long-term context is valuable |
| One-shot queries | 1 hour | No need to persist |

## Console Management

### Viewing Sessions in Google Cloud Console

1. Navigate to **Vertex AI** > **Agent Engine**
2. Select your deployed agent
3. Click the **Sessions** tab
4. View, filter, and inspect sessions
5. Click a session to see its events and state

### Filtering Sessions

| Filter | Example | Description |
|--------|---------|-------------|
| User ID | `userId = "user-123"` | Sessions for a specific user |
| Created after | `createTime > "2025-01-01"` | Sessions created after a date |
| Updated recently | `updateTime > "2025-01-15"` | Recently active sessions |

## IAM Conditions for Sessions

### Restricting Session Access

Use IAM conditions to limit session access per user:

```yaml
# IAM policy binding with condition
bindings:
  - role: roles/aiplatform.user
    members:
      - user:alice@example.com
    condition:
      title: "Own sessions only"
      description: "User can only access their own sessions"
      expression: >
        resource.type == "aiplatform.googleapis.com/Session" &&
        resource.name.extract("sessions/{session}") != "" &&
        request.auth.claims.email == resource.userId
```

### Session Access Patterns

| Role | Session Permissions |
|------|-------------------|
| `aiplatform.user` | Create, read, delete own sessions |
| `aiplatform.admin` | Full access to all sessions |
| `aiplatform.viewer` | Read-only access to session metadata |
| Custom role | Fine-grained with IAM conditions |
