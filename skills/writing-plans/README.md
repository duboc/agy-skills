# Writing Plans

A Agy skill for generating detailed, step-by-step implementation plans before writing any code. Plans assume the implementing developer has zero codebase context and follow strict TDD discipline with frequent commits.

## What It Does

This skill produces zero-ambiguity implementation plans that break features into atomic, testable tasks:

1. **Codebase reconnaissance** — Explores project structure, existing patterns, test infrastructure, and conventions before planning.
2. **Task dependency mapping** — Identifies which tasks depend on others and presents a clear execution order.
3. **TDD step-by-step** — Every task follows the red-green-commit cycle: write failing test, verify failure, implement, verify pass, commit.
4. **Complete code in plan** — No hand-waving. Every step includes the exact code to write and the exact commands to run.
5. **Verification and rollback** — Plans end with a checklist and a revert strategy.

## When Does It Activate

The skill activates when you:

- Have a spec, requirements doc, or feature description and want a plan before coding
- Ask Agy to plan an implementation, break down a feature, or create a task list
- Want to prepare work for another developer (or a future session) to execute

## Core Principles

- **DRY** — Don't Repeat Yourself
- **YAGNI** — You Aren't Gonna Need It
- **TDD** — Test-Driven Development (red-green-commit)
- **Frequent commits** — One commit per task, conventional commit messages

## Installation

### Option B: One-liner

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- writing-plans
```

For user-scope installation (available across all projects):

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- writing-plans --scope user
```

### Option C: Manual

```bash
cp -r skills/writing-plans ~/.gemini/config/skills/writing-plans
```

## Usage Examples

### Planning a new feature

```
I need to add user authentication with JWT tokens to our Express API.
Here's the spec: [paste spec]. Create an implementation plan before
we write any code.
```

### Planning from a GitHub issue

```
Plan the implementation for issue #42. Read the issue description
and break it down into tasks I can follow step by step.
```

### Planning a refactor

```
We need to migrate our database layer from raw SQL to SQLAlchemy ORM.
Create a plan that handles the migration incrementally with tests
at every step.
```

### Planning for handoff

```
I need a detailed implementation plan for the search feature that
another developer can pick up and execute without any context about
our codebase.
```

## Plan Output

Plans are saved to `docs/plans/YYYY-MM-DD-<feature-name>.md` and include:

- **Header** — Goal, architecture, tech stack, prerequisites
- **Task dependency map** — Visual overview of task ordering
- **Atomic tasks** — Each with exact file paths, complete code, test commands, and commit instructions
- **Verification checklist** — How to confirm everything works
- **Rollback strategy** — How to revert if needed

## Included References

- **plan-template.md** — The full plan document template with all required sections.
