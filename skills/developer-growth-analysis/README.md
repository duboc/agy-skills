# Developer Growth Analysis

A Gemini CLI skill that analyzes your recent session history to surface development patterns, friction points, and growth opportunities, then curates learning resources tailored to your actual work.

## What It Does

This skill reads your local Gemini CLI session data and produces a **Developer Momentum Report** using three analytical signals:

1. **Velocity** — Where you work efficiently, showing established skills and productive workflows.
2. **Friction** — Where momentum breaks down due to knowledge gaps, tooling issues, or architectural uncertainty.
3. **Frontier** — Technologies and patterns you are actively expanding into, representing your growth edges.

The report includes prioritized growth opportunities with curated resources and a concrete challenge for your next session.

## When Does It Activate?

The skill activates when you ask Gemini to review your work patterns or growth:

```
Analyze my developer growth
```

```
Review my recent coding patterns
```

```
Generate a momentum report from my last 72 hours
```

```
What have I been working on this week?
```

```
Where should I focus my learning?
```

## How It Works

1. Runs a helper script to collect session data from `~/.gemini/tmp/*/chats/session-*.json`.
2. Maps project hashes to names via `~/.gemini/projects.json`.
3. Analyzes user messages, tool calls, model responses, and token usage.
4. Classifies each session by task type (feature work, debugging, DevOps, learning, etc.).
5. Evaluates Velocity, Friction, and Frontier signals using evidence from sessions.
6. Searches for high-quality resources addressing identified gaps.
7. Generates a structured report and optionally saves it as a markdown file.

## Installation

### Option A: Gemini CLI native

```bash
gemini skills install https://github.com/duboc/agy-skills.git --path skills/developer-growth-analysis
```

### Option B: One-liner

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- developer-growth-analysis
```

For user-scope installation (available across all projects):

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- developer-growth-analysis --scope user
```

### Option C: Manual

```bash
cp -r skills/developer-growth-analysis ~/.gemini/skills/developer-growth-analysis
```

## Usage Examples

### Basic analysis (last 48 hours)

```
Analyze my developer growth
```

### Custom time window

```
Generate a momentum report from my last 7 days
```

### Focus on friction

```
What patterns in my recent work are slowing me down?
```

### Get learning resources

```
Based on my recent sessions, what should I study next?
```

### Project-specific review

```
Review my work on the search2agent project from the past week
```

## Included References

| File | Description |
|------|-------------|
| `references/analysis-framework.md` | Detailed criteria for evaluating Velocity, Friction, and Frontier signals with indicator tables and severity ratings |
| `references/report-template.md` | Structured template for the Developer Momentum Report with all sections and formatting |

## Included Scripts

| File | Description |
|------|-------------|
| `scripts/collect-sessions.sh` | Aggregates Gemini CLI session data across all projects within a time window. Requires `python3`. |
