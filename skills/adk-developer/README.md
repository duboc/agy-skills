# ADK Developer

A Gemini CLI skill for building single-agent and multi-agent systems with Google's Agent Development Kit (ADK) in Python, Java, Go, and TypeScript.

## What It Does

This skill gives your coding agent deep knowledge of ADK architecture, patterns, and best practices -- covering agent types, tools, callbacks, state management, multi-agent orchestration, testing, evaluation, and deployment across all supported languages.

## When Does It Activate?

The skill activates when you mention:

- ADK, google-adk, Google Agent Development Kit
- Building AI agents with Gemini in Python, Java, Go, or TypeScript
- Multi-agent architectures or agent orchestration
- Sequential, parallel, or loop agent workflows
- Agent tools, callbacks, state management
- Deploying agents, writing agent tests
- A2A protocol, remote agents, agent-to-agent communication
- Integrating MCP tools with ADK

## Topics Covered

| Area | What You Get |
|------|-------------|
| Languages | Python, Java, Go, TypeScript with language-specific patterns |
| Project Setup | Directory structure, `__init__.py`, `root_agent`, `pyproject.toml` |
| Agent Types | `LlmAgent`, `SequentialAgent`, `ParallelAgent`, `LoopAgent`, composition |
| Tools | Function tools, `ToolContext`, `AgentTool`, `google_search`, `MCPToolset`, `RemoteA2aAgent` |
| Callbacks | before/after agent, tool, and model hooks |
| State | Session state, scopes (`app:`, `user:`, `temp:`), data flow between agents |
| Output | Pydantic `output_schema` + `output_key` for structured data |
| Testing | `InMemoryRunner` with pytest |
| Evaluation | 8 metrics, `adk eval` CLI, pytest, web UI, user simulation |
| Architecture | Composition strategies, routing, data flow patterns, common mistakes |
| A2A Protocol | Expose via `to_a2a()`, consume via `RemoteA2aAgent`, agent cards, Python + Go |
| Deployment | `adk run/web`, Cloud Run, Vertex AI, FastAPI |
| Safety | `before_model` guardrails, `LlmAsAJudge`, layered defense |
| External Docs | Links to official ADK docs and Google sample agents |

## Installation

### Option A: Gemini CLI native

```bash
gemini skills install https://github.com/duboc/agy-skills.git --path skills/adk-developer
```

### Option B: One-liner

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- adk-developer
```

For user-scope installation (available across all projects):

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- adk-developer --scope user
```

### Option C: Manual

```bash
cp -r skills/adk-developer ~/.gemini/skills/adk-developer
```

## Keeping Knowledge Fresh

ADK evolves rapidly. The skill includes a script to fetch the latest official docs:

```bash
skills/adk-developer/scripts/update-references.sh
```

This downloads `llms.txt`, `llms-full.txt`, and the Python quickstart from official ADK repositories. Run it periodically or set up a CI job.

For Gemini CLI users, the [ADK Docs Extension](https://github.com/derailed-dash/adk-docs-ext) provides live documentation queries:

```bash
gemini extensions install https://github.com/derailed-dash/adk-docs-ext
```

## Included References

| File | Description |
|------|-------------|
| **architecture-guide.md** | Agent composition, routing strategies, data flow, hierarchical patterns, common mistakes |
| **tooling-guide.md** | Function tools, MCP servers, database connectors, RAG, agent-as-tool, design principles |
| **remote-agents.md** | A2A protocol: exposing and consuming agents across services, Go patterns, testing |
| **testing-and-evaluation.md** | InMemoryRunner, eval datasets, 8 built-in metrics, user simulation, CI/CD integration |
| **cross-language.md** | Java (builder pattern, @Schema), Go (struct config), TypeScript (Zod schemas) |
| **production-guide.md** | Deployment (Cloud Run, Vertex AI, FastAPI), safety layers, callbacks, config management |

## Included Scripts

| File | Description |
|------|-------------|
| **update-references.sh** | Fetches latest ADK documentation from official sources |
