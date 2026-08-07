# Analysis Framework: Velocity, Friction, Frontier

This framework evaluates developer work patterns through three complementary signals. Together they paint a picture of where a developer is strong, where they lose time, and where they are expanding.

## Signal 1: Velocity

Velocity measures how efficiently a developer moves from intent to result. High velocity does not mean rushing — it means the developer has internalized the knowledge needed to work smoothly.

### Indicators of High Velocity

| Indicator | What to Look For in Sessions |
|-----------|------------------------------|
| Clear prompts | User messages that are specific, well-scoped, and include relevant context |
| Single-pass solutions | Problems solved within one session without backtracking |
| Efficient tool use | Shell commands that succeed on first attempt; file operations that target the right paths |
| Pattern reuse | Similar tasks handled with consistent, repeatable approaches |
| Low guidance dependency | User drives the direction; Gemini is used for acceleration, not navigation |

### Indicators of Low Velocity

| Indicator | What to Look For in Sessions |
|-----------|------------------------------|
| Vague prompts | Messages like "fix this" or "make it work" without context |
| Session sprawl | Single tasks spanning multiple long sessions |
| Command retries | Same shell command attempted with variations |
| Over-reliance | Asking Gemini to explain basic concepts before every task |

### How to Rate

- **High** — Developer consistently completes tasks with minimal friction in the observed technology
- **Medium** — Developer is productive but occasionally hits knowledge gaps or needs guidance
- **Low** — Developer requires significant support and iteration to make progress

## Signal 2: Friction

Friction identifies where a developer's momentum breaks down. Friction is normal — it signals the boundary between known and unknown territory. The goal is to surface it so the developer can decide where to invest.

### Categories of Friction

#### Knowledge Friction
The developer lacks understanding of a concept, API, or pattern.

**Session evidence:**
- Asking "what does X do?" or "how does Y work?" about core tools
- Trial-and-error approaches to configuration
- Misunderstanding error messages (asking about errors that have clear explanations)

#### Tooling Friction
The developer's environment or toolchain is getting in the way.

**Session evidence:**
- Repeated setup/installation issues
- Permission errors and path problems
- Build tool misconfigurations
- Dependency conflicts

#### Architectural Friction
The developer is uncertain about how to structure or connect components.

**Session evidence:**
- Questions about where code should live
- Asking about design patterns or best practices
- Starting implementations and then rewriting from scratch
- Long sessions focused on planning without producing code

#### Debugging Friction
The developer struggles to diagnose and fix issues efficiently.

**Session evidence:**
- Adding print/log statements without a hypothesis
- Asking Gemini to "find the bug" without narrowing the search space
- Multiple attempts at fixes that don't address the root cause
- Difficulty reading stack traces or error output

### Severity Assessment

| Severity | Criteria |
|----------|----------|
| **Recurring** | Same friction point appears across multiple sessions or projects |
| **Blocking** | Friction prevented task completion in the observed window |
| **Incidental** | Friction appeared once and was resolved; no pattern yet |

## Signal 3: Frontier

Frontier captures technologies and skills the developer is actively expanding into. These are growth edges — areas where the developer is investing effort to learn.

### Identifying Frontier Activity

| Type | Session Evidence |
|------|-----------------|
| **New technology** | First-time use of a language, framework, or platform |
| **New pattern** | Attempting a design pattern, architecture, or methodology for the first time |
| **New domain** | Working in an unfamiliar problem domain (e.g., moving from backend to ML) |
| **Depth expansion** | Moving from basic to advanced usage of a known technology |

### Frontier vs. Friction

Frontier and friction often overlap. The distinction:

- **Frontier** = The developer is choosing to learn something new. The struggle is expected and productive.
- **Friction** = The developer is trying to accomplish a task they should be able to do, but something is blocking them.

When they overlap, note both: "You're expanding into [topic] (frontier), and the main friction point is [specific gap]."

## Combining Signals

The three signals together reveal an actionable picture:

| Combination | Interpretation | Recommendation |
|-------------|---------------|----------------|
| High velocity + low friction | Comfort zone | Consider expanding frontier |
| High velocity + frontier activity | Active growth | Keep investing in current frontier |
| High friction + no frontier | Stuck in known territory | Identify specific knowledge gaps and address them |
| High friction + frontier activity | Learning curve | Normal — provide targeted resources for the frontier topic |

## Quantitative Heuristics

When analyzing sessions, these rough heuristics help calibrate observations:

- **Session length** > 30 minutes with < 5 user messages may indicate thrashing
- **Token usage** > 50k in a single session suggests complex exploration or difficulty
- **Tool call failures** > 3 consecutive retries on the same operation signals tooling friction
- **Repeated questions** about the same topic across sessions signals a knowledge gap worth addressing
- **Project switches** > 3 in a short window may indicate context-switching overhead
