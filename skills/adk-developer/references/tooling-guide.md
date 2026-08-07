# ADK Tooling Guide

Everything about giving agents capabilities: function tools, MCP servers, database connectors, RAG retrieval, and agent-as-tool patterns.

## How Tools Work in ADK

An agent without tools can only generate text. Tools let agents take actions: query databases, call APIs, read files, delegate to other agents. The LLM decides **when** to call a tool and **what arguments** to pass based on the tool's name, docstring, and parameter types.

## Function Tools (Python)

The simplest tool: a Python function with type hints and a docstring.

```python
def lookup_order(order_id: str, include_history: bool = False) -> dict:
    """Look up an order by its ID.

    Args:
        order_id: The order identifier (e.g., ORD-12345).
        include_history: Whether to include status change history.

    Returns:
        Order details including status, items, and shipping info.
    """
    order = db.orders.find(order_id)
    if not order:
        return {"error": f"Order {order_id} not found"}
    result = {"id": order.id, "status": order.status, "items": order.items}
    if include_history:
        result["history"] = order.status_history
    return result

agent = Agent(
    name="order_support",
    model="gemini-2.5-flash",
    instruction="Help customers check their order status.",
    tools=[lookup_order],
)
```

**Three requirements:**
1. **Type hints** on every parameter -- the LLM uses them to understand input types
2. **Docstring** with description and Args -- this becomes the tool's description for the model
3. **Return type** -- return dicts for structured data, strings for simple responses

### Explicit FunctionTool Wrapping

For cases where you need more control:

```python
from google.adk.tools import FunctionTool

calc_tool = FunctionTool(func=my_calculate_function)
agent = Agent(name="calculator", tools=[calc_tool])
```

## Tools with State Access (ToolContext)

Add a `ToolContext` parameter to read/write session state from within a tool:

```python
from google.adk.tools import ToolContext

def save_preference(category: str, value: str, tool_context: ToolContext) -> dict:
    """Save a user preference.

    Args:
        category: Preference category (e.g., 'theme', 'language').
        value: The preference value.
    """
    prefs = tool_context.state.get("user:preferences", {})
    prefs[category] = value
    tool_context.state["user:preferences"] = prefs
    return {"saved": True, "category": category, "value": value}

def get_preferences(tool_context: ToolContext) -> dict:
    """Retrieve all saved user preferences."""
    return tool_context.state.get("user:preferences", {})
```

`ToolContext` is injected automatically -- the LLM never sees it as a parameter.

## Built-in Tools

ADK ships with tools ready to use:

```python
from google.adk.tools import google_search

agent = Agent(
    name="research_assistant",
    model="gemini-2.5-flash",
    instruction="Answer questions using web search when needed.",
    tools=[google_search],
)
```

## MCP Server Integration

Connect to any MCP-compatible server for external capabilities.

### Local MCP Server (Stdio)

For MCP servers that run as local processes:

```python
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams
from mcp import StdioServerParameters

filesystem_tools = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp/workspace"],
        ),
        timeout=30,
    ),
)

agent = Agent(
    name="file_manager",
    model="gemini-2.5-flash",
    instruction="Help users manage files in the workspace.",
    tools=[filesystem_tools],
)
```

### Remote MCP Server (HTTP)

For MCP servers running as web services:

```python
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams

api_tools = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="http://localhost:3000/mcp",
    ),
)
```

## Database Access (ToolboxToolset)

Connect to databases via MCP Toolbox:

```python
from google.adk.tools.toolbox_toolset import ToolboxToolset

db_tools = ToolboxToolset(server_url="http://127.0.0.1:5000")

agent = Agent(
    name="data_analyst",
    model="gemini-2.5-flash",
    instruction="Query the database to answer user questions.",
    tools=[db_tools],
)
```

### With Bound Parameters

Pre-fill parameters that shouldn't be set by the LLM:

```python
db_tools = ToolboxToolset(
    server_url="http://127.0.0.1:5000",
    bound_params={
        "tenant_id": "acme-corp",
        "api_token": lambda: os.environ["DB_TOKEN"],
    },
)
```

## RAG Retrieval (Vertex AI)

Give agents access to document corpora:

```python
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai import rag

knowledge_base = VertexAiRagRetrieval(
    name="search_docs",
    description="Search the company knowledge base for policies and procedures",
    rag_resources=[rag.RagResource(rag_corpus=os.environ["RAG_CORPUS_ID"])],
    similarity_top_k=10,
    vector_distance_threshold=0.6,
)

agent = Agent(
    name="policy_expert",
    model="gemini-2.5-flash",
    instruction="Answer questions about company policies using the knowledge base.",
    tools=[knowledge_base],
)
```

## Agent-as-Tool (AgentTool)

Wrap one agent as a tool for another. The wrapper agent calls the inner agent on demand:

```python
from google.adk.tools.agent_tool import AgentTool

sentiment_analyzer = Agent(
    name="sentiment",
    model="gemini-2.5-flash",
    instruction="Analyze the sentiment of the provided text. Return positive, negative, or neutral with a confidence score.",
)

customer_rep = Agent(
    name="customer_rep",
    model="gemini-2.5-flash",
    instruction="""Handle customer messages.
    Before responding to complaints, use the sentiment tool to gauge severity.""",
    tools=[AgentTool(agent=sentiment_analyzer)],
)
```

**AgentTool vs sub_agents:** Use `AgentTool` when delegation is optional (agent decides when). Use `sub_agents` when routing is the primary job.

## Async and Long-Running Operations

For tools that start background jobs:

```python
def start_export(format: str, filters: dict, tool_context: ToolContext) -> dict:
    """Start a data export job.

    Args:
        format: Export format ('csv', 'json', 'parquet').
        filters: Query filters for the export.
    """
    job = export_service.start(format=format, filters=filters)
    tool_context.state["pending_exports"] = tool_context.state.get("pending_exports", [])
    tool_context.state["pending_exports"].append(job.id)
    return {"job_id": job.id, "status": "started", "estimated_rows": job.estimated_rows}

def check_export(job_id: str) -> dict:
    """Check the status of an export job.

    Args:
        job_id: The export job identifier.
    """
    job = export_service.status(job_id)
    result = {"job_id": job_id, "status": job.status}
    if job.status == "complete":
        result["download_url"] = job.download_url
    return result
```

## Tool Design Principles

| Principle | Good | Bad |
|-----------|------|-----|
| **One action per tool** | `create_user`, `delete_user` | `manage_user(action="create")` |
| **Descriptive names** | `search_knowledge_base` | `search` |
| **Typed parameters** | `def f(count: int)` | `def f(count)` |
| **Structured returns** | `return {"status": "ok", "id": 42}` | `return "Created"` |
| **Graceful errors** | `return {"error": "Not found"}` | `raise Exception(...)` |
| **Docstring explains "when"** | "Use when the user asks about..." | "Does stuff" |
| **State via ToolContext** | `tool_context.state["key"]` | Global variables |
