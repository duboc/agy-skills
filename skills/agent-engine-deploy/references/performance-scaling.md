# Performance & Scaling Reference

Detailed guide for optimizing performance and configuring scaling for agents on Vertex AI Agent Engine.

## Cold Start Mitigation

### Understanding Cold Starts

Cold starts occur when Agent Engine provisions a new container to handle a request. They impact:
- First request latency after deployment
- Requests during scale-up events
- Requests after periods of inactivity

### Strategies to Reduce Cold Start Time

**1. Minimize Import Time**

```python
# BAD: Heavy imports at module level
import pandas as pd
import numpy as np
from transformers import pipeline

# GOOD: Lazy imports inside functions
def analyze_data(data: str) -> dict:
    """Analyze data using pandas."""
    import pandas as pd
    df = pd.read_json(data)
    return {"summary": df.describe().to_dict()}
```

**2. Reduce Package Count**

```python
# BAD: Kitchen-sink requirements
requirements=[
    "google-cloud-aiplatform[adk,agent_engines]",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "matplotlib",
    "seaborn",
]

# GOOD: Only what you need
requirements=[
    "google-cloud-aiplatform[adk,agent_engines]",
    "requests",
]
```

**3. Set Minimum Instances**

Keep containers warm to eliminate cold starts for latency-sensitive workloads:

```python
# Configure minimum instances at deployment
agent_engine = client.agent_engines.create(
    agent_engine=adk_app,
    display_name="low-latency-agent",
    requirements=[...],
    # Min instances keep containers warm
)
```

**4. Optimize Agent Initialization**

```python
# BAD: Heavy initialization in agent setup
def create_agent():
    # Loading large models at import time
    embedding_model = load_embedding_model()  # Slow!
    vector_store = initialize_vector_store()   # Slow!
    return Agent(name="agent", tools=[...])

# GOOD: Defer heavy initialization to first use
_embedding_model = None

def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = load_embedding_model()
    return _embedding_model

def search_tool(query: str) -> dict:
    """Search with lazy-loaded embeddings."""
    model = get_embedding_model()
    return model.search(query)
```

## Container Concurrency

### Understanding Concurrency

Each Agent Engine container can handle multiple concurrent requests. Concurrency settings affect:
- Request throughput per instance
- Memory usage per instance
- Request isolation

### Concurrency Guidelines

| Scenario | Recommended Concurrency | Reasoning |
|----------|------------------------|-----------|
| Stateless, fast tools | Higher (10-50) | Tools complete quickly, low memory per request |
| Stateful, heavy tools | Lower (1-5) | High memory per request, state isolation needed |
| Streaming responses | Medium (5-20) | Long-lived connections, moderate memory |
| Large model calls | Lower (1-10) | Each request uses significant memory for context |

### Memory Considerations

```python
# Estimate memory per concurrent request:
# - Base agent: ~50-100 MB
# - Per request context: ~10-50 MB (depends on conversation length)
# - Tool execution: varies by tool
#
# Container memory / per-request memory = max safe concurrency
#
# Example: 2 GB container, 100 MB per request → ~20 concurrent requests
```

## Scaling Configuration

### Auto-Scaling Behavior

Agent Engine auto-scales based on:
- **Request rate**: More requests → more instances
- **Request latency**: High latency triggers scale-up
- **CPU utilization**: High CPU → more instances

### Min/Max Instance Configuration

```python
# Scaling is managed by Agent Engine
# Configure through deployment settings:

agent_engine = client.agent_engines.create(
    agent_engine=adk_app,
    display_name="scaled-agent",
    requirements=[...],
)
```

### Scaling Guidelines

| Workload | Min Instances | Max Instances | Notes |
|----------|--------------|---------------|-------|
| Dev/Test | 0 | 2 | Allow scale to zero |
| Low traffic | 1 | 5 | One warm instance |
| Production | 2 | 20 | Redundancy + headroom |
| High traffic | 5 | 100 | Pre-warmed capacity |
| Burst traffic | 2 | 50 | Balance cost vs. latency |

## Bidirectional Streaming Setup

### Enabling Bidi Streaming

Bidirectional streaming enables real-time communication between clients and agents:

```python
import asyncio

async def bidi_stream(agent_engine, user_id, session_id):
    """Full bidirectional streaming example."""
    async for event in agent_engine.async_stream_query(
        user_id=user_id,
        session_id=session_id,
        message="Analyze this data step by step",
    ):
        # Handle different event types
        if hasattr(event, "content") and event.content:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    print(part.text, end="", flush=True)
        elif hasattr(event, "actions"):
            print(f"\n[Action: {event.actions}]")

asyncio.run(bidi_stream(agent_engine, "user-123", None))
```

### Streaming Event Types

| Event Type | Description | When It Occurs |
|-----------|-------------|----------------|
| Content | Text response from agent | During response generation |
| Tool call | Agent invoking a tool | Before tool execution |
| Tool result | Result from tool execution | After tool completes |
| State update | Session state change | When state is modified |
| End | Stream completion | When agent finishes |

### Client-Side Streaming Patterns

```python
async def streaming_with_timeout(agent_engine, user_id, session_id, message, timeout=60):
    """Streaming with timeout and error handling."""
    try:
        async for event in asyncio.wait_for(
            collect_events(agent_engine, user_id, session_id, message),
            timeout=timeout,
        ):
            yield event
    except asyncio.TimeoutError:
        print("Stream timed out")
    except Exception as e:
        print(f"Stream error: {e}")

async def collect_events(agent_engine, user_id, session_id, message):
    async for event in agent_engine.async_stream_query(
        user_id=user_id,
        session_id=session_id,
        message=message,
    ):
        yield event
```

## Performance Monitoring

### Key Metrics to Track

| Metric | Target | Action if Exceeded |
|--------|--------|--------------------|
| Cold start time | < 5s | Reduce imports, set min instances |
| Request latency (p50) | < 2s | Optimize tools, check model selection |
| Request latency (p99) | < 10s | Investigate outliers, check concurrency |
| Error rate | < 1% | Review logs, check tool reliability |
| Instance count | Stable | Adjust min/max, check traffic patterns |

### Profiling Agent Performance

```python
import time
import logging

logger = logging.getLogger(__name__)

def profiled_tool(query: str) -> dict:
    """Tool with performance profiling."""
    start = time.monotonic()

    # Tool logic
    result = process_query(query)

    duration = time.monotonic() - start
    logger.info(f"Tool execution: {duration:.3f}s", extra={
        "json_fields": {
            "tool": "profiled_tool",
            "duration_ms": int(duration * 1000),
            "query_length": len(query),
        }
    })
    return result
```

## Cost Optimization

| Strategy | Impact | Trade-off |
|----------|--------|-----------|
| Scale to zero | Eliminates idle costs | Cold starts on first request |
| Lower min instances | Reduces baseline cost | Possible cold starts during low traffic |
| Right-size max instances | Caps costs during spikes | May throttle during extreme bursts |
| Use Flash model | Lower per-token cost | Slightly less capable for complex tasks |
| Optimize tool calls | Fewer LLM round-trips | May need tool redesign |
| Reduce token usage | Lower per-request cost | Shorter context may reduce quality |
