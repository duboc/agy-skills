# Testing and Evaluating ADK Agents

How to verify agent behavior: unit testing with `InMemoryRunner`, building eval datasets, choosing metrics, and integrating into CI/CD.

## Unit Testing with InMemoryRunner

`InMemoryRunner` creates a fully functional agent runtime in memory -- no server, no API calls to manage.

```python
import pytest
from google.adk.runners import InMemoryRunner
from google.genai import types
from my_agent.agent import root_agent

@pytest.mark.asyncio
async def test_agent_uses_tool():
    runner = InMemoryRunner(agent=root_agent, app_name="test_app")
    session = await runner.session_service.create_session(
        user_id="tester", app_name="test_app",
    )

    user_msg = types.Content(
        role="user",
        parts=[types.Part.from_text("What's the weather in Tokyo?")],
    )

    events = []
    async for event in runner.run_async(
        user_id="tester", session_id=session.id, new_message=user_msg,
    ):
        events.append(event)

    last_response = events[-1].content.parts[0].text
    assert "tokyo" in last_response.lower()
```

### Testing State Changes

Verify that tools and agents correctly modify session state:

```python
@pytest.mark.asyncio
async def test_cart_state():
    runner = InMemoryRunner(agent=shopping_agent, app_name="test_app")
    session = await runner.session_service.create_session(
        user_id="tester", app_name="test_app",
    )

    msg = types.Content(
        role="user",
        parts=[types.Part.from_text("Add 2 notebooks to my cart")],
    )

    async for event in runner.run_async(
        user_id="tester", session_id=session.id, new_message=msg,
    ):
        pass

    # Retrieve updated session to check state
    updated = await runner.session_service.get_session(
        user_id="tester", app_name="test_app", session_id=session.id,
    )
    cart = updated.state.get("cart", [])
    assert len(cart) > 0
    assert any(item["item"] == "notebook" for item in cart)
```

---

## Evaluation Framework

### Why Evaluate (Not Just Test)

Unit tests check deterministic behavior. Evaluation handles the non-deterministic nature of LLMs:

- Did the agent pick the **right tool** with the **right arguments**?
- Is the response **semantically correct** even if worded differently?
- Is the output **grounded** in real data (not hallucinated)?
- Is the response **safe** and policy-compliant?

### Eval Data Format

ADK uses JSON files with `.test.json` (unit) or `.evalset.json` (integration) extensions.

**Minimal eval case:**

```json
{
  "eval_set_id": "order_agent_tests",
  "name": "Order agent tool use",
  "eval_cases": [
    {
      "eval_id": "lookup_existing_order",
      "conversation": [
        {
          "invocation_id": "turn-1",
          "user_content": {
            "parts": [{"text": "What's the status of order ORD-555?"}],
            "role": "user"
          },
          "final_response": {
            "parts": [{"text": "Order ORD-555 is currently being shipped."}],
            "role": "model"
          },
          "intermediate_data": {
            "tool_uses": [
              {
                "name": "lookup_order",
                "args": {"order_id": "ORD-555"}
              }
            ],
            "intermediate_responses": []
          }
        }
      ],
      "session_input": {
        "app_name": "order_agent",
        "user_id": "eval_user",
        "state": {}
      }
    }
  ]
}
```

**Multi-turn eval** -- add multiple objects to the `conversation` array, each with its own `invocation_id`.

### Anatomy of an Eval Case

| Field | Purpose |
|-------|---------|
| `eval_id` | Unique name for this test case |
| `conversation[].user_content` | What the user says (input) |
| `conversation[].final_response` | What the agent should say (reference answer) |
| `conversation[].intermediate_data.tool_uses` | Which tools should be called and with what args |
| `session_input.state` | Pre-populated state for the session |

---

## The 8 Built-In Metrics

### Deterministic Metrics (Fast, No LLM Needed)

| Metric | What It Measures | When to Use |
|--------|-----------------|-------------|
| `tool_trajectory_avg_score` | Did the agent call the right tools in the right order? | Every eval -- most bugs show up here |
| `response_match_score` | ROUGE-1 word overlap with reference response | Quick CI/CD regression checks |

**Tool trajectory match modes:**

| Mode | Strictness |
|------|-----------|
| `EXACT` | Same tools, same args, same order, no extras |
| `IN_ORDER` | Expected tools appear in sequence, extras allowed |
| `ANY_ORDER` | All expected tools called, any order, extras allowed |

### LLM-Judged Metrics (Deeper, Requires LLM Call)

| Metric | What It Measures | When to Use |
|--------|-----------------|-------------|
| `final_response_match_v2` | Semantic similarity to reference (tolerates rephrasing) | When exact wording doesn't matter |
| `rubric_based_final_response_quality_v1` | Quality against custom rubrics (no reference needed) | Subjective quality: tone, completeness, clarity |
| `rubric_based_tool_use_quality_v1` | Tool reasoning quality against rubrics | Validating multi-step reasoning |
| `hallucinations_v1` | Are claims grounded in context? | Preventing fabrication |
| `safety_v1` | Is the response safe and policy-compliant? | Compliance-sensitive domains |
| `per_turn_user_simulator_quality_v1` | User simulation fidelity | Dynamic conversation testing |

### Metric Config Examples

**Tool trajectory (strict):**
```json
{"tool_trajectory_avg_score": {"threshold": 1.0, "match_type": "EXACT"}}
```

**Semantic matching with LLM judge:**
```json
{
  "final_response_match_v2": {
    "threshold": 0.8,
    "judge_model_options": {"judge_model": "gemini-2.5-flash", "num_samples": 5}
  }
}
```

**Custom quality rubrics (no reference answer needed):**
```json
{
  "rubric_based_final_response_quality_v1": {
    "threshold": 0.8,
    "judge_model_options": {"judge_model": "gemini-2.5-flash"},
    "rubrics": [
      {"rubric_id": "actionable", "rubric_content": {"text_property": "The response includes a clear next step for the user."}},
      {"rubric_id": "grounded", "rubric_content": {"text_property": "All claims reference data from tool outputs."}}
    ]
  }
}
```

**Hallucination detection:**
```json
{
  "hallucinations_v1": {
    "threshold": 0.8,
    "judge_model_options": {"judge_model": "gemini-2.5-flash"},
    "evaluate_intermediate_nl_responses": true
  }
}
```

---

## Running Evaluations

### CLI

```bash
# Run all cases in a file
adk eval my_agent tests/eval/orders.test.json

# With custom config and verbose output
adk eval my_agent tests/eval/orders.test.json \
  --config_file_path tests/eval/config.json \
  --print_detailed_results

# Run specific cases only
adk eval my_agent tests/eval/orders.test.json:lookup_existing_order,cancel_order
```

### Pytest Integration

```python
from google.adk.evaluation.agent_evaluator import AgentEvaluator

@pytest.mark.asyncio
async def test_order_evals():
    await AgentEvaluator.evaluate(
        agent_module="my_agent",
        eval_dataset_file_path_or_dir="tests/eval/orders.test.json",
    )

@pytest.mark.asyncio
async def test_all_evals():
    await AgentEvaluator.evaluate(
        agent_module="my_agent",
        eval_dataset_file_path_or_dir="tests/eval/",  # Runs all .test.json files
    )
```

### Web UI

```bash
adk web my_agent
```

Use the **Eval** tab to create eval cases from real conversations, edit them, and run evaluations interactively. The **Trace** tab helps debug tool calls and model interactions.

---

## Simulated Conversations

For multi-turn agents where scripting every user message is impractical, let an LLM simulate the user:

```json
{
  "scenarios": [
    {
      "starting_prompt": "I need to return a product.",
      "conversation_plan": "Provide order number ORD-999. Confirm the return when prompted. Ask about refund timeline."
    }
  ]
}
```

```bash
adk eval_set create my_agent return_flow_tests
adk eval_set add_eval_case my_agent return_flow_tests \
  --scenarios_file scenarios.json \
  --session_input_file session.json
```

User simulation supports: `hallucinations_v1`, `safety_v1`, rubric-based metrics, and `per_turn_user_simulator_quality_v1`. It does **not** support reference-based metrics (trajectory, ROUGE, semantic match).

---

## Evaluation Config File

Combine metrics in `test_config.json`:

```json
{
  "criteria": {
    "tool_trajectory_avg_score": {"threshold": 1.0, "match_type": "IN_ORDER"},
    "response_match_score": 0.8,
    "hallucinations_v1": {"threshold": 0.8, "evaluate_intermediate_nl_responses": true}
  }
}
```

---

## Metric Selection Guide

| Goal | Use These Metrics |
|------|------------------|
| CI/CD gate (fast) | `tool_trajectory_avg_score` + `response_match_score` |
| Semantic correctness | `final_response_match_v2` |
| Subjective quality | `rubric_based_final_response_quality_v1` with custom rubrics |
| Reasoning validation | `rubric_based_tool_use_quality_v1` |
| Factual accuracy | `hallucinations_v1` |
| Compliance | `safety_v1` (requires Google Cloud project) |
| Dynamic conversations | User simulation + `hallucinations_v1` + `safety_v1` |

---

## TypeScript Evaluation

TypeScript uses the same JSON eval format and config. Run with:

```bash
npx adk eval my_agent tests/eval/cases.test.json --config_file_path tests/eval/config.json
```

Java and Go evaluation support is planned but not yet available.
