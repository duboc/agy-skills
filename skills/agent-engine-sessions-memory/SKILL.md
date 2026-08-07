---
name: agent-engine-sessions-memory
description: "Manage sessions and memory for agents on Vertex AI Agent Engine. Use when working with agent sessions, session state, session events, VertexAiSessionService, session TTL, Memory Bank, generating memories, retrieving memories, memory topics, VertexAiMemoryBankService, PreloadMemoryTool, or when the user mentions agent memory, session management, conversation history, long-term memory, memory scopes, or agent context persistence on Vertex AI."
---

# Vertex AI Agent Engine Sessions & Memory Guide

## Overview

Vertex AI Agent Engine provides managed services for session management and long-term memory. **Sessions** track conversation state, events, and context within interactions. **Memory Bank** enables agents to remember information across sessions, providing long-term memory that persists beyond individual conversations.

## Documentation & Resources

- **Sessions Overview**: https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/sessions/overview
- **Memory Bank Overview**: https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/memory-bank/overview
- **ADK Integration**: https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/sessions/manage-adk

## Quick Reference

| Task | Approach |
|------|----------|
| Create session (ADK) | `VertexAiSessionService` in runner config |
| Create session (API) | `POST /sessions` on Agent Engine resource |
| Get session | `client.agent_engines.sessions.get(...)` |
| List sessions | `client.agent_engines.sessions.list(...)` |
| Delete session | `client.agent_engines.sessions.delete(...)` |
| Set session TTL | Configure TTL on session creation |
| Enable Memory Bank | `VertexAiMemoryBankService` in runner config |
| Generate memories | From sessions, direct contents, or pre-extracted facts |
| Retrieve memories | Scope-based retrieval or similarity search |
| Use in agent | `PreloadMemoryTool` for automatic memory injection |

---

## Sessions

### Core Concepts

- **Session**: A conversation context between a user and an agent, containing events, state, and metadata
- **Event**: An individual interaction within a session (user message, agent response, tool call)
- **State**: Key-value data attached to a session, shared across agents and tools
- **Memory**: Long-term facts extracted from sessions, persisted across sessions

### Session Lifecycle

```
Create Session -> Send Messages (Events) -> Read/Update State -> Close/Expire (TTL)
```

### Using Sessions with ADK (VertexAiSessionService)

The recommended approach for ADK agents on Agent Engine:

```python
from google.adk.agents import Agent
from google.adk.runners import Runner
from vertexai.agent_engines.sessions import VertexAiSessionService

# Define your agent
root_agent = Agent(
    name="assistant",
    model="gemini-2.5-flash",
    instruction="You are a helpful assistant.",
    tools=[...],
)

# Configure runner with Vertex AI session service
session_service = VertexAiSessionService(
    project="your-project-id",
    location="us-central1",
)

runner = Runner(
    agent=root_agent,
    app_name="my-app",
    session_service=session_service,
)
```

### Creating and Managing Sessions

```python
# Create a new session
session = await session_service.create_session(
    app_name="my-app",
    user_id="user-123",
)
print(f"Session ID: {session.id}")

# Get an existing session
session = await session_service.get_session(
    app_name="my-app",
    user_id="user-123",
    session_id="session-456",
)

# List sessions for a user
sessions = await session_service.list_sessions(
    app_name="my-app",
    user_id="user-123",
)

# Delete a session
await session_service.delete_session(
    app_name="my-app",
    user_id="user-123",
    session_id="session-456",
)
```

### Session State

State is a key-value store attached to each session. It's shared across agents and tools within the session.

```python
# In a tool function, access state via ToolContext
from google.adk.tools import ToolContext

def update_preferences(preference: str, value: str, tool_context: ToolContext) -> dict:
    """Update user preferences in session state."""
    prefs = tool_context.state.get("preferences", {})
    prefs[preference] = value
    tool_context.state["preferences"] = prefs
    return {"status": "updated", "preference": preference, "value": value}
```

**State scope prefixes:**

| Prefix | Scope | Persistence |
|--------|-------|-------------|
| (none) | Current session | Session lifetime |
| `user:` | Tied to user ID | Cross-session for that user |
| `app:` | Shared across all users | Application-wide |
| `temp:` | Current turn only | Not persisted |

### Session Events

Events represent individual interactions within a session:

```python
# Events are automatically created when querying the agent
# Each event contains:
# - author: "user" or agent name
# - content: The message content (Parts)
# - timestamp: When the event occurred
# - actions: Any actions taken (tool calls, state changes)

# Access events from a session
session = await session_service.get_session(
    app_name="my-app",
    user_id="user-123",
    session_id="session-456",
)
for event in session.events:
    print(f"{event.author}: {event.content}")
```

### Session TTL

Configure session expiration to automatically clean up inactive sessions:

```python
# Set TTL when creating a session
session = await session_service.create_session(
    app_name="my-app",
    user_id="user-123",
    # TTL configuration depends on the service configuration
)
```

For detailed session API usage, REST endpoints, console management, IAM conditions, and advanced state patterns, see [references/sessions-api-guide.md](references/sessions-api-guide.md).

---

## Memory Bank

### Overview

Memory Bank is a managed service that extracts, stores, and retrieves long-term memories from agent interactions. It enables agents to remember user preferences, past decisions, and context across separate sessions.

### Core Concepts

- **Memory**: A fact or piece of information extracted from conversations
- **Scope**: The context for memory retrieval (user-level, session-level, or custom)
- **Topic**: A category for organizing memories (managed or custom)
- **Generation**: The process of extracting memories from sessions or content
- **Retrieval**: Looking up relevant memories for a given context

### Enabling Memory Bank with ADK

```python
from google.adk.agents import Agent
from google.adk.runners import Runner
from vertexai.agent_engines.sessions import VertexAiSessionService
from vertexai.agent_engines.memory_bank import VertexAiMemoryBankService

# Define your agent
root_agent = Agent(
    name="assistant",
    model="gemini-2.5-flash",
    instruction="You are a helpful assistant that remembers user preferences.",
    tools=[...],
)

# Configure with both session and memory services
session_service = VertexAiSessionService(
    project="your-project-id",
    location="us-central1",
)

memory_service = VertexAiMemoryBankService(
    project="your-project-id",
    location="us-central1",
)

runner = Runner(
    agent=root_agent,
    app_name="my-app",
    session_service=session_service,
    memory_bank_service=memory_service,
)
```

### Generating Memories

Memories can be generated from three sources:

**1. From Sessions (Automatic)**

After a conversation ends, extract memories from session events:

```python
# Generate memories from a completed session
await memory_service.generate_memories(
    app_name="my-app",
    user_id="user-123",
    session_id="session-456",
)
```

**2. From Direct Contents**

Provide raw content for memory extraction:

```python
from google.genai import types

await memory_service.generate_memories(
    app_name="my-app",
    user_id="user-123",
    contents=[
        types.Content(
            role="user",
            parts=[types.Part.from_text("I prefer dark mode and Python.")],
        ),
    ],
)
```

**3. From Pre-extracted Facts**

Directly store known facts as memories:

```python
await memory_service.generate_memories(
    app_name="my-app",
    user_id="user-123",
    facts=["User prefers Python over Java", "User timezone is PST"],
)
```

### Retrieving Memories

**Scope-based Retrieval**

Retrieve all memories for a given scope:

```python
memories = await memory_service.retrieve_memories(
    app_name="my-app",
    user_id="user-123",
)
for memory in memories:
    print(f"Memory: {memory.fact}")
    print(f"Topic: {memory.topic}")
    print(f"Created: {memory.create_time}")
```

**Similarity Search**

Find memories relevant to a specific query:

```python
memories = await memory_service.retrieve_memories(
    app_name="my-app",
    user_id="user-123",
    query="What programming languages does the user prefer?",
)
```

### Memory Topics

Topics organize memories into categories for structured retrieval.

**Managed Topics** are automatically assigned by the memory generation algorithm based on content analysis.

**Custom Topics** can be defined for domain-specific categorization:

```python
# When generating memories, you can specify custom topics
await memory_service.generate_memories(
    app_name="my-app",
    user_id="user-123",
    facts=["User prefers agile methodology"],
    topic="work-preferences",
)
```

### PreloadMemoryTool (ADK Integration)

The `PreloadMemoryTool` automatically loads relevant memories at the start of each conversation:

```python
from vertexai.agent_engines.memory_bank import PreloadMemoryTool

root_agent = Agent(
    name="assistant",
    model="gemini-2.5-flash",
    instruction="""You are a helpful assistant.
    Use the loaded memories to personalize your responses.
    Remember user preferences and past interactions.""",
    tools=[
        PreloadMemoryTool(memory_bank_service=memory_service),
        # ... other tools
    ],
)
```

When a session starts, `PreloadMemoryTool` automatically:
1. Retrieves relevant memories for the user
2. Injects them into the agent's context
3. The agent can reference these memories in its responses

### Memory Scopes

| Scope | Description | Use Case |
|-------|-------------|----------|
| User | Memories tied to a specific user | Preferences, history, personalization |
| Session | Memories from a specific session | Conversation context |
| App | Memories shared across all users | Global knowledge, policies |

For Memory Bank configuration, similarity search tuning, generation algorithm details, multimodal input, memory revisions, TTL, metadata, and purging, see [references/memory-bank-guide.md](references/memory-bank-guide.md).

---

## Decision Guide

**Session management:**

```
ADK agent on Agent Engine?     -> VertexAiSessionService in Runner
Need REST API access?          -> Direct API calls to /sessions endpoint
Track conversation state?      -> Session state with scope prefixes
Auto-cleanup old sessions?     -> Configure session TTL
Cross-session data?            -> Use user: or app: state prefixes
```

**Memory management:**

```
Remember across sessions?      -> Enable VertexAiMemoryBankService
Auto-extract from chats?       -> generate_memories from sessions
Import known facts?            -> generate_memories with facts=[]
Search relevant memories?      -> retrieve_memories with query=
Auto-load in new sessions?     -> PreloadMemoryTool
Organize by category?          -> Use memory topics (managed or custom)
```
