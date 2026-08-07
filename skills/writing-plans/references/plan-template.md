# [Feature Name] Implementation Plan

**Goal:** [One sentence — what does this build and why]

**Architecture:** [2-3 sentences about the technical approach, key design decisions, and how it fits into the existing codebase]

**Tech Stack:** [Languages, frameworks, libraries involved]

**Prerequisites:** [Tools to install, environment setup, branches to create]

**Estimated Tasks:** [N tasks, M total steps]

---

## Task Dependency Map

```
Task 1: [Name] (no dependencies)
Task 2: [Name] (depends on: Task 1)
Task 3: [Name] (depends on: Task 2)
```

---

### Task 1: [Descriptive Component Name]

**Depends on:** None

**Files:**
- Create: `exact/path/to/new_file.py`
- Modify: `exact/path/to/existing.py` (lines 45-60, the `process_data` function)
- Test: `tests/exact/path/to/test_file.py`

**References:** [Docs, API refs, or existing code to study before starting]

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

### Task 2: [Next Component Name]

**Depends on:** Task 1

**Files:**
- Create: `...`
- Modify: `...`
- Test: `...`

_(Repeat step structure)_

---

## Verification Checklist

- [ ] All tests pass: `pytest` (or project-specific test command)
- [ ] Linter passes: `<linting command>`
- [ ] No untracked files left behind
- [ ] Each task has its own commit
- [ ] Feature works end-to-end: [describe manual verification steps]

## Rollback

If the feature needs to be reverted, revert these commits in reverse order:

- Task N: `feat(component): ...`
- ...
- Task 1: `feat(component): ...`
