# Deployment Patterns Reference

Detailed deployment configurations and patterns for Vertex AI Agent Engine.

## Deployment Configuration Options

### Full Configuration Example

```python
import vertexai
from google.adk.agents import Agent
from vertexai.agent_engines import AdkApp

client = vertexai.Client(
    project="your-project-id",
    location="us-central1",
)

root_agent = Agent(
    name="production_agent",
    model="gemini-2.5-flash",
    instruction="Production-ready agent instructions...",
    tools=[...],
)

adk_app = AdkApp(agent=root_agent)

agent_engine = client.agent_engines.create(
    agent_engine=adk_app,
    display_name="production-agent-v1",
    requirements=[
        "google-cloud-aiplatform[adk,agent_engines]",
        "requests>=2.31.0",
        "google-cloud-storage>=2.14.0",
    ],
    env_vars={
        "LOG_LEVEL": "INFO",
        "ENABLE_TRACING": "true",
        "CUSTOM_CONFIG": "production",
    },
    gcs_dir_name="gs://my-bucket/agent-staging/",
    extra_packages=["./my_lib-0.1.0.tar.gz"],
)
```

## Requirements Specification

### Python Package Requirements

The `requirements` parameter accepts a list of pip-compatible requirement strings:

```python
requirements=[
    "google-cloud-aiplatform[adk,agent_engines]",   # Core requirement
    "requests>=2.31.0",                              # Version pinning
    "beautifulsoup4==4.12.3",                        # Exact version
    "google-cloud-storage",                          # Latest compatible
    "pydantic>=2.0,<3.0",                            # Version range
]
```

**Best practices:**
- Always include `google-cloud-aiplatform[adk,agent_engines]` as the first requirement
- Pin versions for reproducible deployments
- Add `[a2a]` extra if using A2A agents: `google-cloud-aiplatform[adk,agent_engines,a2a]`
- Minimize dependencies to reduce cold start time
- Test requirements locally before deploying

### Extra Packages

For custom local packages not available on PyPI:

```python
extra_packages=[
    "./my_custom_tools-0.1.0.tar.gz",
    "./shared_utils-1.0.0.whl",
]
```

Build packages with:

```bash
cd my_custom_tools
python -m build
# Produces dist/my_custom_tools-0.1.0.tar.gz
```

## Staging Buckets

### GCS Directory for Staging

The `gcs_dir_name` parameter specifies a Cloud Storage location for staging deployment artifacts:

```python
agent_engine = client.agent_engines.create(
    agent_engine=adk_app,
    display_name="staged-agent",
    gcs_dir_name="gs://my-bucket/staging/agent-v1/",
    requirements=[...],
)
```

**What gets staged:**
- Agent code and configuration
- Extra packages
- Serialized agent state
- Deployment metadata

**Bucket setup:**

```bash
# Create a staging bucket
gsutil mb -l us-central1 gs://my-agent-staging/

# Set lifecycle rules for cleanup
gsutil lifecycle set lifecycle.json gs://my-agent-staging/
```

## Environment Variables

### Setting Environment Variables

```python
env_vars={
    # Logging and tracing
    "LOG_LEVEL": "INFO",
    "ENABLE_TRACING": "true",

    # Application config
    "APP_ENV": "production",
    "MAX_RETRIES": "3",

    # Feature flags
    "ENABLE_MEMORY": "true",
    "ENABLE_STREAMING": "true",
}
```

**Important notes:**
- All values must be strings
- Sensitive values (API keys, secrets) should use Secret Manager, not env vars
- Environment variables are set at deployment time and require redeployment to change

### Accessing Environment Variables in Agent Code

```python
import os

def my_tool(query: str) -> dict:
    """Tool that uses environment configuration."""
    log_level = os.environ.get("LOG_LEVEL", "WARNING")
    max_retries = int(os.environ.get("MAX_RETRIES", "3"))
    # ...
```

## Telemetry Setup

### OpenTelemetry Configuration

Agent Engine supports OpenTelemetry for custom telemetry:

```python
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider

# Agent Engine auto-configures exporters when ENABLE_TRACING=true
# You can add custom instrumentation:

tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

# Custom counter
query_counter = meter.create_counter(
    name="agent.queries.processed",
    description="Number of queries processed",
)

def my_tool(query: str) -> dict:
    """Tool with custom telemetry."""
    with tracer.start_as_current_span("process-query") as span:
        span.set_attribute("query.type", classify_query(query))
        query_counter.add(1, {"query.type": classify_query(query)})
        return process(query)
```

## Deployment Lifecycle

### Versioning Strategy

```python
# Deploy new version alongside existing
v2_engine = client.agent_engines.create(
    agent_engine=updated_app,
    display_name="my-agent-v2",
    requirements=[...],
)

# Validate new version
# ... run tests against v2_engine ...

# Delete old version after validation
client.agent_engines.delete(name=v1_engine.api_resource.name)
```

### Update vs. Redeploy

**Update** (in-place):
```python
client.agent_engines.update(
    agent_engine=updated_app,
    update_mask=["agent_engine"],
)
```

**Redeploy** (new instance):
```python
new_engine = client.agent_engines.create(
    agent_engine=updated_app,
    display_name="my-agent-v2",
)
```

| Approach | When to Use |
|----------|------------|
| Update | Minor changes, same config, quick iteration |
| Redeploy | Major changes, different requirements, blue-green deployment |

## Multi-Region Deployment

Deploy agents to multiple regions for availability and latency:

```python
regions = ["us-central1", "europe-west1", "asia-northeast1"]

engines = {}
for region in regions:
    regional_client = vertexai.Client(
        project="your-project-id",
        location=region,
    )
    engines[region] = regional_client.agent_engines.create(
        agent_engine=adk_app,
        display_name=f"my-agent-{region}",
        requirements=[...],
    )
```

## Troubleshooting Deployments

| Issue | Cause | Solution |
|-------|-------|----------|
| Import errors | Missing requirements | Add package to `requirements` list |
| Permission denied | Missing IAM roles | Grant `roles/aiplatform.user` or `roles/aiplatform.admin` |
| Staging failure | Bucket permissions | Grant `roles/storage.objectAdmin` on staging bucket |
| Cold start timeout | Heavy imports | Lazy-load large libraries, reduce dependencies |
| Serialization error | Non-serializable agent | Ensure all agent components are pickle-compatible |
