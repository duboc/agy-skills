# ADK Developer

An Agy skill for building single-agent and multi-agent systems with Google's Agent Development Kit (ADK) in Python, Java, Kotlin, Go, and TypeScript.

## What It Does

This skill gives your coding agent deep knowledge of ADK architecture, patterns, and best practices -- covering agent types, tools, callbacks, state management, multi-agent orchestration, testing, evaluation, and deployment across all supported languages.

## When Does It Activate?

The skill activates when you mention:

- ADK, google-adk, Google Agent Development Kit
- Building AI agents with Gemini / Vertex AI in Python, Java, Go, or TypeScript
- Multi-agent architectures or agent orchestration
- Sequential, parallel, or loop agent workflows
- Gemini Live bidirectional streaming agents
- Agent tools, callbacks, state management, model context caching
- Deploying agents to Agent Runtime, Cloud Run, or Vertex AI
- A2A protocol, remote agents, agent-to-agent communication
- Integrating MCP tools with ADK

## Topics Covered

| Area | What You Get |
|------|-------------|
| Languages | Python, Java, Kotlin, Go, TypeScript with language-specific patterns |
| Project Setup | Directory structure, `__init__.py`, `root_agent`, `pyproject.toml` |
| Agent Types | `LlmAgent`, `SequentialAgent`, `ParallelAgent`, `LoopAgent`, `LiveAgent` |
| Tools | Function tools, `ToolContext`, `AgentTool`, `google_search`, `MCPToolset`, `RemoteA2aAgent` |
| Callbacks | before/after agent, tool, and model hooks |
| State & Context | Session state, memory banks, model context caching, context compaction |
| Output | Pydantic `output_schema` + `output_key` for structured data |
| Testing | `InMemoryRunner` with pytest |
| Evaluation | 8 metrics, `adk eval` CLI, pytest, web UI, user simulation |
| Architecture | Composition strategies, routing, data flow patterns, common mistakes |
| A2A Protocol | Expose via `to_a2a()`, consume via `RemoteA2aAgent`, agent cards, Python + Go |
| Deployment | `Agent Runtime`, `adk run/web`, Cloud Run, GKE, Vertex AI Agent Engine |
| Safety | `before_model` guardrails, `LlmAsAJudge`, layered defense |
| External Docs | Links to official ADK docs (https://adk.dev) and Google sample agents |

## Installation

### Method 1: One-liner with curl (Recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- adk-developer
```

For user-scope installation (available globally across all projects):

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- adk-developer --scope user
```

### Method 2: Manual Copy

```bash
# Workspace scope
cp -r skills/adk-developer .agents/skills/adk-developer

# User scope
cp -r skills/adk-developer ~/.gemini/config/skills/adk-developer
```

## Keeping Knowledge Fresh

ADK evolves rapidly. The skill includes a script to fetch the latest official docs from `https://adk.dev`:

```bash
skills/adk-developer/scripts/update-references.sh
```

This downloads `llms.txt` and `llms-full.txt` directly from official ADK documentation. Run it periodically or set up a CI job.

## Included References

| File | Description |
|------|-------------|
| **llms.txt** | Condensed official ADK API index |
| **llms-full.txt** | Complete official ADK documentation dump |
| **architecture-guide.md** | Agent composition, routing strategies, data flow, hierarchical patterns, common mistakes |
| **callbacks-and-state-guide.md** | Lifecycle callbacks (`before_model`, `after_tool`), session state, memory banks, context caching & compaction |
| **tooling-guide.md** | Function tools, MCP servers, database connectors, RAG, agent-as-tool, design principles |
| **remote-agents.md** | A2A protocol: exposing and consuming agents across services, Go patterns, testing |
| **testing-and-evaluation.md** | InMemoryRunner, eval datasets, 8 built-in metrics, user simulation, CI/CD integration |
| **cross-language.md** | Java (builder pattern, @Schema), Go (struct config), TypeScript (Zod schemas) |
| **production-guide.md** | Deployment (Cloud Run, Vertex AI, FastAPI), safety layers, callbacks, config management |

## Included Scripts

| File | Description |
|------|-------------|
| **update-references.sh** | Fetches latest ADK documentation from official sources (`https://adk.dev`) |
