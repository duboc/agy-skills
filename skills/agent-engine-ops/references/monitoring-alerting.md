# Monitoring & Alerting Reference

Detailed guide for monitoring, alerting, and custom metrics for Vertex AI Agent Engine.

## Metrics Explorer

### Accessing Metrics Explorer

1. Open **Google Cloud Console** > **Monitoring** > **Metrics Explorer**
2. Select resource type: **Vertex AI Reasoning Engine**
3. Browse available metrics under `aiplatform.googleapis.com/reasoning_engine/`

### Built-in Metrics

| Metric | Description | Unit |
|--------|-------------|------|
| `request_count` | Number of agent queries | count |
| `request_latencies` | End-to-end response time | ms |
| `error_count` | Number of failed queries | count |
| `token_count` | Input/output tokens used | count |
| `active_instances` | Running container replicas | count |
| `instance_uptime` | Container uptime | seconds |

### Filtering Metrics

```
resource.type = "aiplatform.googleapis.com/ReasoningEngine"
resource.labels.reasoning_engine_id = "12345"
metric.type = "aiplatform.googleapis.com/reasoning_engine/request_count"
```

## PromQL Queries

### Request Rate

```promql
# Requests per second over 5 minutes
rate(aiplatform_googleapis_com:reasoning_engine_request_count[5m])
```

### Error Rate

```promql
# Error rate as percentage
rate(aiplatform_googleapis_com:reasoning_engine_error_count[5m])
/
rate(aiplatform_googleapis_com:reasoning_engine_request_count[5m])
* 100
```

### Latency Percentiles

```promql
# P95 latency
histogram_quantile(0.95,
  rate(aiplatform_googleapis_com:reasoning_engine_request_latencies_bucket[5m])
)
```

### Token Usage

```promql
# Total tokens per minute
rate(aiplatform_googleapis_com:reasoning_engine_token_count[1m]) * 60
```

## Cloud Monitoring API

### Listing Time Series

```python
from google.cloud import monitoring_v3

client = monitoring_v3.MetricServiceClient()
project_name = f"projects/your-project-id"

# Query request count
results = client.list_time_series(
    request={
        "name": project_name,
        "filter": 'metric.type = "aiplatform.googleapis.com/reasoning_engine/request_count"',
        "interval": {
            "end_time": {"seconds": int(time.time())},
            "start_time": {"seconds": int(time.time()) - 3600},
        },
    }
)

for result in results:
    for point in result.points:
        print(f"Time: {point.interval.end_time}, Count: {point.value.int64_value}")
```

### Creating a Metric Descriptor (Custom Metric)

```python
from google.cloud import monitoring_v3
from google.api import metric_pb2, label_pb2

client = monitoring_v3.MetricServiceClient()

descriptor = metric_pb2.MetricDescriptor(
    type="custom.googleapis.com/agent/tool_execution_time",
    metric_kind=metric_pb2.MetricDescriptor.MetricKind.GAUGE,
    value_type=metric_pb2.MetricDescriptor.ValueType.DOUBLE,
    description="Tool execution time in milliseconds",
    labels=[
        label_pb2.LabelDescriptor(
            key="tool_name",
            value_type=label_pb2.LabelDescriptor.ValueType.STRING,
            description="Name of the tool",
        ),
    ],
)

client.create_metric_descriptor(
    name=f"projects/your-project-id",
    metric_descriptor=descriptor,
)
```

### Writing Custom Metric Data

```python
from google.cloud import monitoring_v3
import time

client = monitoring_v3.MetricServiceClient()

series = monitoring_v3.TimeSeries()
series.metric.type = "custom.googleapis.com/agent/tool_execution_time"
series.metric.labels["tool_name"] = "search_tool"

series.resource.type = "global"
series.resource.labels["project_id"] = "your-project-id"

now = time.time()
point = monitoring_v3.Point(
    interval=monitoring_v3.TimeInterval(
        end_time={"seconds": int(now)},
    ),
    value=monitoring_v3.TypedValue(double_value=150.5),
)
series.points = [point]

client.create_time_series(
    name=f"projects/your-project-id",
    time_series=[series],
)
```

## Log-Based Metrics

### Creating Log-Based Metrics

Extract metrics from agent logs automatically:

```bash
# Create a log-based metric via gcloud
gcloud logging metrics create agent-errors \
    --description="Count of agent error logs" \
    --log-filter='resource.type="aiplatform.googleapis.com/ReasoningEngine" severity>=ERROR'
```

### Common Log-Based Metric Patterns

| Metric | Log Filter | Use Case |
|--------|-----------|----------|
| Error count | `severity>=ERROR` | Track error frequency |
| Tool failures | `jsonPayload.tool_status="error"` | Monitor tool reliability |
| Slow queries | `jsonPayload.duration_ms>5000` | Identify slow requests |
| Specific errors | `textPayload=~"TimeoutError"` | Track specific error types |

### Python Integration

```python
import logging

logger = logging.getLogger(__name__)

def my_tool(query: str) -> dict:
    """Tool with metrics-friendly logging."""
    start = time.monotonic()
    try:
        result = process(query)
        duration_ms = (time.monotonic() - start) * 1000
        logger.info("tool_execution", extra={
            "json_fields": {
                "tool_name": "my_tool",
                "duration_ms": duration_ms,
                "tool_status": "success",
                "result_count": len(result),
            }
        })
        return result
    except Exception as e:
        duration_ms = (time.monotonic() - start) * 1000
        logger.error("tool_execution", extra={
            "json_fields": {
                "tool_name": "my_tool",
                "duration_ms": duration_ms,
                "tool_status": "error",
                "error_type": type(e).__name__,
            }
        })
        raise
```

## User-Defined Metrics

### Custom Metrics in Agent Code

```python
from opentelemetry import metrics

meter = metrics.get_meter("agent-metrics")

# Counter for tool invocations
tool_invocations = meter.create_counter(
    name="agent.tool.invocations",
    description="Number of tool invocations",
    unit="1",
)

# Histogram for response times
response_time = meter.create_histogram(
    name="agent.response.time",
    description="Agent response time",
    unit="ms",
)

# Up/Down counter for active sessions
active_sessions = meter.create_up_down_counter(
    name="agent.sessions.active",
    description="Number of active sessions",
    unit="1",
)

def my_tool(query: str) -> dict:
    """Tool with custom metrics."""
    tool_invocations.add(1, {"tool": "my_tool", "query_type": "search"})
    start = time.monotonic()
    result = process(query)
    response_time.record(
        (time.monotonic() - start) * 1000,
        {"tool": "my_tool"},
    )
    return result
```

## Alerts

### Creating Alert Policies

```python
from google.cloud import monitoring_v3

client = monitoring_v3.AlertPolicyServiceClient()

# High error rate alert
policy = monitoring_v3.AlertPolicy(
    display_name="Agent High Error Rate",
    conditions=[
        monitoring_v3.AlertPolicy.Condition(
            display_name="Error rate > 5%",
            condition_threshold=monitoring_v3.AlertPolicy.Condition.MetricThreshold(
                filter='metric.type = "aiplatform.googleapis.com/reasoning_engine/error_count"',
                comparison=monitoring_v3.ComparisonType.COMPARISON_GT,
                threshold_value=0.05,
                duration={"seconds": 300},
                aggregations=[
                    monitoring_v3.Aggregation(
                        alignment_period={"seconds": 60},
                        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_RATE,
                    ),
                ],
            ),
        ),
    ],
    notification_channels=["projects/your-project/notificationChannels/12345"],
    alert_strategy=monitoring_v3.AlertPolicy.AlertStrategy(
        auto_close={"seconds": 1800},
    ),
)

client.create_alert_policy(
    name="projects/your-project-id",
    alert_policy=policy,
)
```

### Common Alert Configurations

| Alert | Condition | Threshold | Duration |
|-------|-----------|-----------|----------|
| High error rate | Error rate | > 5% | 5 minutes |
| High latency | P95 latency | > 10s | 5 minutes |
| No traffic | Request count | = 0 | 15 minutes |
| Token budget | Daily tokens | > 90% budget | 1 hour |
| Instance scaling | Instance count | > max * 0.8 | 10 minutes |

### Alert via gcloud

```bash
# Create notification channel (email)
gcloud alpha monitoring channels create \
    --display-name="Agent Alerts" \
    --type=email \
    --channel-labels=email_address=team@example.com

# Create alert policy
gcloud alpha monitoring policies create \
    --display-name="Agent High Error Rate" \
    --condition-display-name="Error rate > 5%" \
    --condition-filter='metric.type = "aiplatform.googleapis.com/reasoning_engine/error_count"' \
    --condition-threshold-value=0.05 \
    --condition-threshold-duration=300s \
    --notification-channels=CHANNEL_ID
```

## Dashboards

### Creating Dashboards via Console

1. Go to **Monitoring** > **Dashboards** > **Create Dashboard**
2. Add widgets for key metrics:
   - **Request rate** (line chart)
   - **Error rate** (line chart with threshold line)
   - **Latency percentiles** (heatmap or line chart)
   - **Token usage** (stacked area chart)
   - **Instance count** (line chart)

### Dashboard via API

```python
from google.cloud import monitoring_dashboard_v1

client = monitoring_dashboard_v1.DashboardsServiceClient()

dashboard = monitoring_dashboard_v1.Dashboard(
    display_name="Agent Engine Overview",
    grid_layout=monitoring_dashboard_v1.GridLayout(
        columns=2,
        widgets=[
            monitoring_dashboard_v1.Widget(
                title="Request Rate",
                xy_chart=monitoring_dashboard_v1.XyChart(
                    data_sets=[
                        monitoring_dashboard_v1.XyChart.DataSet(
                            time_series_query=monitoring_dashboard_v1.TimeSeriesQuery(
                                time_series_filter=monitoring_dashboard_v1.TimeSeriesFilter(
                                    filter='metric.type = "aiplatform.googleapis.com/reasoning_engine/request_count"',
                                ),
                            ),
                        ),
                    ],
                ),
            ),
        ],
    ),
)

client.create_dashboard(
    parent="projects/your-project-id",
    dashboard=dashboard,
)
```

### Recommended Dashboard Layout

| Row | Left Widget | Right Widget |
|-----|------------|-------------|
| 1 | Request rate (line) | Error rate (line + threshold) |
| 2 | Latency p50/p95/p99 (line) | Token usage (stacked area) |
| 3 | Active instances (line) | Tool execution times (heatmap) |
| 4 | Top errors (table) | Session count (line) |
