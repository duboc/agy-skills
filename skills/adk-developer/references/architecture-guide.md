# Architecting ADK Agent Systems

How to structure single and multi-agent systems for reliability, maintainability, and performance.

## The Single-Responsibility Principle for Agents

Every agent should do **one thing well**. When an agent accumulates more than 5-7 tools or handles unrelated concerns, break it apart. This isn't just clean design -- LLMs perform measurably worse with bloated tool lists and sprawling instructions.

**Decomposition checklist:**
1. Can you describe this agent's job in one sentence?
2. Are all its tools related to that single job?
3. Does it need the full conversation history, or just a focused input?

If any answer is "no," you need multiple agents.

## Choosing Your Architecture

```
                                    Is the workflow known at design time?
                                           /              \
                                         YES               NO
                                          |                 |
                            Are steps dependent?     Use a planning agent
                              /          \            that writes steps to
                            YES           NO          state, then executes
                             |             |
                    SequentialAgent   ParallelAgent
                             |
                    Need iteration?
                      /        \
                    YES         NO
                     |           |
                 LoopAgent    Done
```

### Architecture Decision Matrix

| Your Situation | Recommended Shape | Why |
|----------------|-------------------|-----|
| Steps A, B, C must run in order | `SequentialAgent([A, B, C])` | Each step depends on the previous |
| Tasks X, Y, Z are independent | `ParallelAgent([X, Y, Z])` | No data dependencies, run concurrently |
| Draft-review cycles until quality passes | `LoopAgent([drafter, reviewer])` | Iterative refinement with exit condition |
| Input type determines handler | Root `Agent` with `sub_agents` | LLM routes based on agent descriptions |
| Agent X needs help from agent Y sometimes | `AgentTool(Y)` on agent X | On-demand delegation, not permanent routing |
| Agents live in separate services | `RemoteA2aAgent` | Cross-network via A2A protocol |

## Data Flow Between Agents

The state dictionary is the backbone of inter-agent communication.

**Golden rules:**
1. **Writers declare `output_key`.** Every agent that produces data names its output slot.
2. **Readers reference state keys in instructions.** Downstream agents read from `state["key"]`.
3. **Never use free-text handoffs.** Structured data (JSON/Pydantic via `output_schema`) prevents misinterpretation.
4. **Parallel agents must write to different keys.** Two agents writing to the same `output_key` is a race condition.

```python
from pydantic import BaseModel

class ResearchFindings(BaseModel):
    topic: str
    sources: list[str]
    key_points: list[str]

# Stage 1: produces structured data
researcher = Agent(
    name="researcher",
    model="gemini-2.5-flash",
    instruction="Research the user's topic thoroughly.",
    output_schema=ResearchFindings,
    output_key="research",
)

# Stage 2: consumes structured data
editor = Agent(
    name="editor",
    model="gemini-2.5-flash",
    instruction="""Write a polished article.
    Base it on the research findings in state['research'].
    Cite all sources from the research.""",
    output_key="article",
)

pipeline = SequentialAgent(
    name="publish_pipeline",
    sub_agents=[researcher, editor],
)
```

## Routing and Delegation Strategies

### LLM-Based Routing (Auto-Flow)

The parent agent's LLM decides which sub-agent handles a request. The `description` field on each sub-agent is the primary routing signal.

```python
support_bot = Agent(
    name="support_router",
    model="gemini-2.5-flash",
    instruction="""Route customer requests to the right specialist.
    Do not answer questions yourself -- always delegate.
    If the request is unclear, ask for clarification.""",
    sub_agents=[
        Agent(name="returns_handler",
              description="Processes product returns and refund requests",
              ...),
        Agent(name="account_specialist",
              description="Handles account settings, password resets, and profile updates",
              ...),
        Agent(name="product_advisor",
              description="Answers questions about product features, compatibility, and recommendations",
              ...),
    ],
)
```

**Write descriptions like job postings** -- they should make it unambiguous when to delegate to each agent.

### Tool-Based Delegation (AgentTool)

When agent A occasionally needs agent B's capabilities but B shouldn't permanently receive traffic:

```python
from google.adk.tools.agent_tool import AgentTool

legal_reviewer = Agent(
    name="legal_review",
    model="gemini-2.5-pro",
    instruction="Review text for legal compliance issues.",
)

content_writer = Agent(
    name="content_writer",
    model="gemini-2.5-flash",
    instruction="""Write marketing content.
    If the content involves legal claims, warranties, or disclaimers,
    use the legal_review tool to check it before finalizing.""",
    tools=[AgentTool(agent=legal_reviewer)],
)
```

## Iteration with LoopAgent

Two termination strategies:

### Strategy 1: Fixed Budget

Set `max_iterations` when you know the maximum cycles needed:

```python
polish_loop = LoopAgent(
    name="editing_loop",
    sub_agents=[draft_improver, grammar_checker],
    max_iterations=4,
)
```

### Strategy 2: Quality Gate

A checker agent signals completion by calling `escalate`:

```python
def evaluate_readability(score: int, tool_context: ToolContext) -> str:
    """Assess if the text meets readability standards.

    Args:
        score: Readability score from 1-10.
    """
    if score >= 8:
        tool_context.actions.escalate = True
        return "Readability target achieved."
    return f"Score {score}/10 -- needs more simplification."

quality_gate = Agent(
    name="readability_checker",
    model="gemini-2.5-flash",
    instruction="Read the draft in state['current_draft'] and evaluate its readability.",
    tools=[evaluate_readability],
)

editing_loop = LoopAgent(
    name="iterative_editor",
    sub_agents=[simplifier_agent, quality_gate],
    max_iterations=5,  # Always set a safety bound
)
```

**Always set `max_iterations`** even with a quality gate. Unbounded loops are a production risk.

## Hierarchical Composition

Nest freely: a `SequentialAgent` can contain a `ParallelAgent` which contains `LlmAgent`s.

```python
# Gather data from multiple sources simultaneously
research_phase = ParallelAgent(
    name="gather_sources",
    sub_agents=[
        Agent(name="web_researcher", output_key="web_findings", ...),
        Agent(name="db_analyst", output_key="db_findings", ...),
        Agent(name="doc_searcher", output_key="doc_findings", ...),
    ],
)

# Then synthesize, review, and publish sequentially
full_workflow = SequentialAgent(
    name="report_generator",
    sub_agents=[
        research_phase,
        Agent(name="synthesizer", instruction="Merge all findings from state...", output_key="draft"),
        LoopAgent(name="review_cycle", sub_agents=[reviewer, reviser], max_iterations=2),
        Agent(name="publisher", tools=[publish_report]),
    ],
)
```

## Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Single agent with 15+ tools | Frequent wrong tool selection | Split into specialist agents |
| Free-text between pipeline stages | Downstream agent misinterprets data | Use `output_schema` with Pydantic models |
| Same agent generates and evaluates | Consistently rates own output highly | Separate producer and critic agents |
| `LoopAgent` without `max_iterations` | Infinite execution, cost overrun | Always set iteration cap |
| No fallback for ambiguous routing | Silent misrouting, wrong agent handles request | Add a "general/unclear" handler sub-agent |
| `ParallelAgent` sub-agents share `output_key` | Data overwritten, nondeterministic results | Each parallel agent writes unique key |
| All instructions in one massive prompt | Model ignores parts, context drift | Decompose into `SequentialAgent` pipeline |
| Expensive model for simple tasks | High cost, slow responses | Route by complexity (Flash for simple, Pro for complex) |
