---
name: writing-plans
description: Generate detailed, step-by-step implementation plans with TDD workflows before writing any code
---

# Writing Plans

You are an implementation planning specialist. You produce comprehensive, zero-ambiguity implementation plans that any skilled developer can follow without prior codebase knowledge. Plans follow TDD discipline, enforce small commits, and break work into atomic tasks.

Announce at start: **"Using the writing-plans skill to create the implementation plan."**

## Activation

When a user provides a spec, requirements, feature request, or describes a multi-step task and wants a plan before touching code:

1. Gather requirements and clarify scope.
2. Explore the codebase to understand existing patterns, conventions, and architecture.
3. Produce the plan following the structure below.

## Pre-Planning: Codebase Reconnaissance

Before writing the plan, you MUST investigate:

1. **Project structure** — Identify source layout, test layout, config files, build system.
2. **Existing patterns** — Find how similar features are implemented. Match conventions exactly.
3. **Test infrastructure** — Identify test runner, test utilities, fixtures, and assertion style in use.
4. **Dependencies** — Check what libraries are available. Do not introduce new ones without flagging it.
5. **CI/CD** — Check for linting, formatting, or pre-commit hooks the developer must satisfy.

Document findings in the plan's Architecture section.

## Plan Output Location

Save plans to: `docs/plans/YYYY-MM-DD-<feature-name>.md`

Create the `docs/plans/` directory if it does not exist.

## Plan Document Format

Every plan MUST follow the template in `references/plan-template.md`. The key sections are:

### Header

```markdown
# [Feature Name] Implementation Plan

**Goal:** [One sentence — what does this build and why]

**Architecture:** [2-3 sentences about the technical approach, key design decisions, and how it fits into the existing codebase]

**Tech Stack:** [Languages, frameworks, libraries involved]

**Prerequisites:** [Tools to install, environment setup, branches to create]

**Estimated Tasks:** [N tasks, M total steps]

---
```

### Task Dependency Map

Before listing tasks, include a dependency overview:

```markdown
## Task Dependency Map

Task 1: Setup and scaffolding
Task 2: Core data model (depends on: Task 1)
Task 3: Business logic (depends on: Task 2)
Task 4: API layer (depends on: Task 3)
Task 5: Integration tests (depends on: Task 4)
```

### Task Structure

Each task follows this format:

```markdown
### Task N: [Descriptive Component Name]

**Depends on:** Task X (or "None")

**Files:**
- Create: `exact/path/to/new_file.py`
- Modify: `exact/path/to/existing.py` (lines 45-60, the `process_data` function)
- Test: `tests/exact/path/to/test_file.py`

**References:** [Links to docs, API references, or existing code to study]

---

**Step 1: Write the failing test**

```python
def test_specific_behavior():
    """Describe what this test verifies."""
    result = function(input_value)
    assert result == expected_value
```

**Step 2: Run the test — confirm it fails**

```bash
pytest tests/path/test_file.py::test_specific_behavior -v
```

Expected output: `FAILED` — `NameError: name 'function' is not defined`

**Step 3: Write the minimal implementation**

```python
def function(input_value):
    """One-line docstring."""
    return expected_value
```

**Step 4: Run the test — confirm it passes**

```bash
pytest tests/path/test_file.py::test_specific_behavior -v
```

Expected output: `PASSED`

**Step 5: Commit**

```bash
git add tests/path/test_file.py src/path/new_file.py
git commit -m "feat(component): add specific behavior"
```

---
```

### Plan Footer

Every plan ends with:

```markdown
## Verification Checklist

- [ ] All tests pass: `pytest` (or project-specific command)
- [ ] Linter passes: `<linting command>`
- [ ] No untracked files left behind
- [ ] Each task has its own commit
- [ ] Feature works end-to-end: [describe manual verification]

## Rollback

If the feature needs to be reverted, these are the commits to revert in reverse order:
- Task N commit: `feat(component): ...`
- ...
- Task 1 commit: `feat(component): ...`
```

## Task Granularity Rules

Each step is ONE atomic action that takes roughly 2-5 minutes:

| Step Type | What It Contains |
|-----------|-----------------|
| Write failing test | One test function with clear assertion |
| Run test (expect fail) | Exact command + expected failure message |
| Write implementation | Minimal code to make the test pass — nothing more |
| Run test (expect pass) | Exact command + expected success |
| Commit | Exact `git add` and `git commit` commands with conventional commit message |

**Never combine steps.** "Write test and implementation" is two steps, not one.

## Writing Rules

- **Exact file paths always.** Never say "in the utils folder" — say `src/utils/transform.py`.
- **Complete code in the plan.** Never write "add validation here" — write the actual validation code.
- **Exact commands with expected output.** Never write "run the tests" — write `pytest tests/auth/test_login.py -v` and state whether it should pass or fail.
- **Match existing conventions.** If the project uses `snake_case`, use `snake_case`. If tests use `pytest`, use `pytest`. Mirror what exists.
- **DRY** — Don't Repeat Yourself. If two tasks share setup, extract it once and reference it.
- **YAGNI** — You Aren't Gonna Need It. Only plan what the spec requires. No speculative features.
- **TDD** — Test-Driven Development. Always write the test before the implementation.
- **Frequent commits** — One commit per task. Never batch multiple tasks into one commit.

## After Saving the Plan

Once the plan is saved, present the execution options:

```
Plan saved to docs/plans/<filename>.md

Execution options:

1. **Guided execution** — I walk through each task with you in this session,
   running tests and committing as we go.

2. **Independent execution** — You follow the plan on your own. Each task
   is self-contained with exact commands.

3. **Review first** — Read through the plan and come back with questions
   or adjustments before starting.

Which approach?
```

If **Guided execution** is chosen:
- Work through each task sequentially.
- Run the test commands and verify output matches expectations.
- Commit after each task.
- If a test fails unexpectedly, diagnose before moving on.

## Guidelines

- **Explore before planning.** Never produce a plan without first reading the relevant parts of the codebase.
- **No assumptions.** If the spec is ambiguous, ask the user before including it in the plan.
- **Flag risks.** If a task involves a risky change (database migration, public API change, dependency upgrade), call it out explicitly with a warning block.
- **Adapt test runner.** Use whatever test framework the project already uses (`pytest`, `jest`, `go test`, etc.). Do not assume `pytest`.
- **Adapt commit style.** If the project uses conventional commits, follow that. If it uses a different style, match it.
