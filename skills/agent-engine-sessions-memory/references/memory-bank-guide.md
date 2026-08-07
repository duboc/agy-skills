# Memory Bank Reference

Detailed guide for configuring and operating Vertex AI Agent Engine Memory Bank.

## Memory Bank Architecture

### How Memory Bank Works

```
Session Events → Memory Generation → Memory Storage → Memory Retrieval → Agent Context
```

1. **Generation**: Extracts facts from conversations or direct input
2. **Storage**: Persists memories with metadata, scope, and topic
3. **Retrieval**: Finds relevant memories via scope matching or similarity search
4. **Injection**: Loads memories into agent context for personalized responses

## Memory Generation Algorithm

### Automatic Extraction

The memory generation algorithm analyzes conversation content to extract:

- **Explicit preferences**: "I prefer dark mode" → "User prefers dark mode"
- **Stated facts**: "I work at Acme Corp" → "User works at Acme Corp"
- **Behavioral patterns**: Repeated tool usage → "User frequently checks order status"
- **Context clues**: Conversation topics → Relevant domain interests

### Generation from Sessions

```python
from vertexai.agent_engines.memory_bank import VertexAiMemoryBankService

memory_service = VertexAiMemoryBankService(
    project="your-project-id",
    location="us-central1",
)

# Generate memories from a completed session
await memory_service.generate_memories(
    app_name="my-app",
    user_id="user-123",
    session_id="session-456",
)
```

### Generation from Direct Contents

```python
from google.genai import types

# Provide conversation-like content for extraction
await memory_service.generate_memories(
    app_name="my-app",
    user_id="user-123",
    contents=[
        types.Content(
            role="user",
            parts=[types.Part.from_text("I'm a Python developer working on ML projects")],
        ),
        types.Content(
            role="model",
            parts=[types.Part.from_text("Great! I'll keep that in mind.")],
        ),
    ],
)
```

### Generation from Pre-extracted Facts

```python
# Directly store known facts as memories
await memory_service.generate_memories(
    app_name="my-app",
    user_id="user-123",
    facts=[
        "User's name is Alice",
        "User prefers Python over JavaScript",
        "User's timezone is America/Los_Angeles",
        "User works on machine learning projects",
        "User prefers concise explanations",
    ],
)
```

## Multimodal Input

Memory Bank supports generating memories from multimodal content:

```python
from google.genai import types

# Generate memories from text and image content
await memory_service.generate_memories(
    app_name="my-app",
    user_id="user-123",
    contents=[
        types.Content(
            role="user",
            parts=[
                types.Part.from_text("Here's my project architecture"),
                types.Part.from_image(image_data),
            ],
        ),
    ],
)
```

## Memory Retrieval

### Scope-Based Retrieval

Retrieve all memories for a given scope:

```python
# Get all memories for a user
memories = await memory_service.retrieve_memories(
    app_name="my-app",
    user_id="user-123",
)

for memory in memories:
    print(f"Fact: {memory.fact}")
    print(f"Topic: {memory.topic}")
    print(f"Scope: {memory.scope}")
    print(f"Created: {memory.create_time}")
    print(f"Updated: {memory.update_time}")
    print("---")
```

### Similarity Search

Find memories relevant to a specific query using semantic similarity:

```python
# Find memories related to a specific topic
memories = await memory_service.retrieve_memories(
    app_name="my-app",
    user_id="user-123",
    query="What are the user's programming language preferences?",
)

# The results are ranked by relevance
for i, memory in enumerate(memories):
    print(f"#{i+1} (relevance: {memory.score:.3f}): {memory.fact}")
```

### Similarity Search Tuning

| Parameter | Effect | Recommendation |
|-----------|--------|----------------|
| Query specificity | More specific → fewer, more relevant results | Use specific queries for targeted retrieval |
| Result limit | Controls max memories returned | Start with 10-20, adjust based on context window |
| Score threshold | Filter low-relevance results | Set based on empirical testing (e.g., 0.7) |

## Memory Topics

### Managed Topics

The system automatically categorizes memories into managed topics:

| Topic | Examples |
|-------|---------|
| Preferences | "Prefers dark mode", "Likes Python" |
| Personal info | "Works at Acme Corp", "Lives in San Francisco" |
| Technical | "Uses VS Code", "Prefers REST over GraphQL" |
| Behavioral | "Often asks about deployment", "Prefers step-by-step guides" |

### Custom Topics

Define domain-specific topics for structured memory organization:

```python
# Store memories with custom topics
await memory_service.generate_memories(
    app_name="my-app",
    user_id="user-123",
    facts=["User prefers agile methodology"],
    topic="work-methodology",
)

await memory_service.generate_memories(
    app_name="my-app",
    user_id="user-123",
    facts=["User's favorite framework is FastAPI"],
    topic="tech-stack",
)

# Retrieve by topic
memories = await memory_service.retrieve_memories(
    app_name="my-app",
    user_id="user-123",
    topic="tech-stack",
)
```

### Topic Management

```python
# List all topics for a user
memories = await memory_service.retrieve_memories(
    app_name="my-app",
    user_id="user-123",
)

topics = set(m.topic for m in memories)
print(f"Active topics: {topics}")
```

## Memory Revisions

### How Revisions Work

When new information contradicts existing memories, the system creates revisions:

```
Original: "User prefers JavaScript"
New fact:  "User now prefers TypeScript"
Result:    Memory updated to "User prefers TypeScript", old version preserved as revision
```

### Viewing Revisions

```python
# Memory objects include revision history
memory = memories[0]
if hasattr(memory, "revisions"):
    for revision in memory.revisions:
        print(f"Previous: {revision.fact}")
        print(f"Changed: {revision.update_time}")
```

## Memory TTL

### Configuring Memory Expiration

Set TTL to automatically expire memories after a specified duration:

```python
# Configure memory TTL at the service level
memory_service = VertexAiMemoryBankService(
    project="your-project-id",
    location="us-central1",
    # TTL configuration
)
```

### TTL Guidelines

| Memory Type | Recommended TTL | Reasoning |
|-------------|----------------|-----------|
| User preferences | Long (90+ days) | Preferences change slowly |
| Session context | Medium (7-30 days) | Relevant for recent interactions |
| Temporary facts | Short (1-7 days) | Time-sensitive information |
| No TTL | Permanent | Critical user information |

## Memory Metadata

### Attaching Metadata

Memories can include metadata for filtering and organization:

```python
# Metadata is attached during generation
await memory_service.generate_memories(
    app_name="my-app",
    user_id="user-123",
    facts=["User prefers detailed error messages"],
    topic="development-preferences",
    # Additional metadata may be attached by the system
)
```

### System-Generated Metadata

| Field | Description |
|-------|-------------|
| `create_time` | When the memory was created |
| `update_time` | Last modification time |
| `source_session_id` | Session the memory was extracted from |
| `confidence` | System's confidence in the extracted fact |
| `scope` | User, session, or app scope |

## Purging Memories

### Deleting Specific Memories

```python
# Delete individual memories
await memory_service.delete_memory(
    app_name="my-app",
    user_id="user-123",
    memory_id="memory-789",
)
```

### Purging All Memories for a User

```python
# Remove all memories for a specific user (GDPR compliance)
await memory_service.purge_memories(
    app_name="my-app",
    user_id="user-123",
)
```

### Purge Considerations

| Scenario | Action | Notes |
|----------|--------|-------|
| User requests deletion | `purge_memories` | GDPR/privacy compliance |
| Outdated memories | Delete specific memories | Keep relevant ones |
| App decommission | Purge all app memories | Clean up all data |
| Testing cleanup | Purge test user memories | Reset test state |

## ADK Integration Patterns

### PreloadMemoryTool

Automatically load relevant memories at conversation start:

```python
from vertexai.agent_engines.memory_bank import PreloadMemoryTool

root_agent = Agent(
    name="personalized_assistant",
    model="gemini-2.5-flash",
    instruction="""You are a personalized assistant.
    Review the loaded memories to understand user preferences.
    Use this context to provide tailored responses.
    If you learn new preferences, acknowledge them.""",
    tools=[
        PreloadMemoryTool(memory_bank_service=memory_service),
        # ... other tools
    ],
)
```

### Memory-Aware Agent Pattern

```python
from google.adk.tools import ToolContext

def save_preference(category: str, preference: str, tool_context: ToolContext) -> dict:
    """Save a user preference for future sessions."""
    # Store in session state for immediate use
    prefs = tool_context.state.get("user:preferences", {})
    prefs[category] = preference
    tool_context.state["user:preferences"] = prefs

    return {
        "status": "saved",
        "message": f"I'll remember that you prefer {preference} for {category}.",
    }

root_agent = Agent(
    name="memory_agent",
    model="gemini-2.5-flash",
    instruction="""You are a helpful assistant that remembers user preferences.
    When users express preferences, use save_preference to store them.
    Reference loaded memories to personalize your responses.""",
    tools=[
        PreloadMemoryTool(memory_bank_service=memory_service),
        save_preference,
    ],
)
```

### Post-Session Memory Generation

```python
from google.adk.agents import Agent
from google.adk.tools import ToolContext

# After a session ends, generate memories
async def on_session_end(session_id: str, user_id: str):
    await memory_service.generate_memories(
        app_name="my-app",
        user_id=user_id,
        session_id=session_id,
    )
```
