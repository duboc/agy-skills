# Agent Engine Sessions & Memory

A Agy skill for managing sessions and long-term memory for agents on Vertex AI Agent Engine.

## What It Does

This skill gives your coding agent deep knowledge of Vertex AI Agent Engine's session management and Memory Bank services -- covering session lifecycle, state management, events, TTL configuration, memory generation and retrieval, memory topics, and ADK integration with `VertexAiSessionService`, `VertexAiMemoryBankService`, and `PreloadMemoryTool`.

## When Does It Activate?

The skill activates when you mention:

- Agent Engine sessions, session management, conversation state
- VertexAiSessionService, session events, session TTL
- Memory Bank, long-term memory, agent memory
- VertexAiMemoryBankService, PreloadMemoryTool
- Generating memories from sessions or content
- Retrieving memories, similarity search, memory scopes
- Memory topics, memory revisions
- Session state persistence, cross-session data

## Topics Covered

| Area | What You Get |
|------|-------------|
| Sessions | Core concepts, lifecycle, creation, management, deletion |
| ADK Integration | `VertexAiSessionService`, `Runner` configuration |
| Session State | Key-value store, scope prefixes (`user:`, `app:`, `temp:`) |
| Session Events | Interaction tracking, event structure, history |
| Session TTL | Auto-expiration configuration |
| Memory Bank | Overview, setup, `VertexAiMemoryBankService` |
| Memory Generation | From sessions, direct contents, pre-extracted facts |
| Memory Retrieval | Scope-based, similarity search, query-based |
| Memory Topics | Managed and custom topic categorization |
| PreloadMemoryTool | Automatic memory injection in conversations |
| API Access | REST API endpoints, console management |

## Installation

### Option A: Agy native

```bash
agy skills install https://github.com/duboc/agy-skills.git --path skills/agent-engine-sessions-memory
```

### Option B: One-liner

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- agent-engine-sessions-memory
```

For user-scope installation (available across all projects):

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- agent-engine-sessions-memory --scope user
```

### Option C: Manual

```bash
cp -r skills/agent-engine-sessions-memory ~/.gemini/config/skills/agent-engine-sessions-memory
```

## Usage Examples

- "Set up session management for my ADK agent on Agent Engine"
- "How do I use VertexAiSessionService with my runner?"
- "Enable Memory Bank for my agent"
- "Generate memories from completed sessions"
- "Retrieve relevant memories for a user"
- "Add PreloadMemoryTool to my agent"
- "Configure session TTL for auto-cleanup"
- "How do memory topics work in Agent Engine?"

## Included References

| File | Description |
|------|-------------|
| **sessions-api-guide.md** | Detailed session management via REST API, console, SDK; events, state, IAM conditions |
| **memory-bank-guide.md** | Memory Bank configuration, similarity search, generation algorithm, multimodal input, revisions, TTL, purging |
