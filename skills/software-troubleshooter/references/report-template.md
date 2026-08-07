# Troubleshoot & Code Inspection Report

**Issue:** [Short, Descriptive Title of the Bug or Issue]
**Status:** [Draft | Under Investigation | Proposed Fix | Resolved]
**Date:** [YYYY-MM-DD]
**Author:** [Name]
**Topic:** [One-sentence summary of the behavior and context]

---

## 1. Issue Description

### Symptoms

Describe the observable behavior from the user's or system's perspective.

- **Symptom A:** [e.g., Duplicate speech output]
- **Symptom B:** [e.g., Infinite loop on mobile devices]

**Environment:** [e.g., Specific to Mobile/Web, Production/Staging, Specific OS]

### Observed Evidence

Paste relevant logs, stack traces, or JSON payloads here. Annotate important lines.

```
// Example Log Snippet
{
  "event": "Error event",
  "timestamp": "...",
  "details": "Paste log evidence here"
}
```

**Observation:** [Explain what the log shows, e.g., "Note the timestamp difference of only 0.5s"]

---

## 2. Root Cause Analysis

### Primary Root Cause

State the fundamental technical reason for the issue in one distinct statement.

**Summary:** [e.g., Two conflicting systems are processing the same input simultaneously.]

### Technical Deep Dive

Explain the logic flow. Quote specific code blocks that are causing the problem.

**1. System/Component A Behavior:**

In `path/to/file.py`:

```python
# Paste relevant code causing the issue
def problematic_function():
    # This setting enables the conflict
    config = Config(enabled=True)
```

**Analysis:** The code above sets X to True, which implies...

**2. System/Component B Behavior:**

In `path/to/other_file.py`:

```python
# Paste the other side of the conflict
```

**Analysis:** Meanwhile, this component receives the same signal and...

**3. The Conflict/Bug:**

Explain how A and B interact to cause the failure.

### Historical Context

How did we get here? Was this introduced by a recent refactor or a revert of a previous fix?

[e.g., Feature X was disabled in commit Y but accidentally re-enabled during migration Z.]

### Secondary Contributing Factors

List other variables that exacerbate the issue (e.g., configuration defaults, hardware limitations).

- **Factor A:** [e.g., Default thresholds are too low for noisy environments.]
- **Factor B:** [e.g., Missing cooldown timers.]
- **Factor C:** [e.g., User prompt lacks specific guardrails.]

---

## 3. Impact Analysis

| Area | Impact | Severity | Details |
|------|--------|----------|---------|
| UX | [e.g., Confusing feedback] | [Critical/High/Med/Low] | [Description of user pain] |
| Resources | [e.g., High Token Usage] | [Low] | [Cost implication] |
| Stability | [e.g., Infinite Loop] | [Critical] | [System health implication] |

---

## 4. Affected Files

### Configuration & Runtime

- `src/path/to/config.py`: [Description of what needs changing]
- `.env`: [Environment variables to update]

### Core Logic

- `src/path/to/logic.py`: [Specific function or class logic to fix]

### Prompts / Instructions

- `src/path/to/prompts.py`: [System instructions that need tuning]

---

## 5. Reference Material

Include links to API documentation, internal wikis, or specs that validate the expected behavior.

- **Documentation:** [Link or Quote]
  > "By default, parameter X is set to True..."
- **Internal Spec:** [Link]

---

## 6. Proposed Solutions

### Option A: [Title, e.g., Use Native API Features] (Recommended)

**Rationale:** [Why is this the best approach? e.g., "Leverages built-in model intelligence."]

**Changes Required:**

1. Modify `file.py` to enable X.
2. Remove custom logic in `gateway.py`.
3. Update configuration Y.

**Trade-offs:**

- (+) [Pro]
- (-) [Con]

### Option B: [Title, e.g., Custom Implementation]

**Rationale:** [Why choose this? e.g., "Preserves current architecture, lower risk."]

**Changes Required:**

1. Explicitly disable external feature X.
2. Tighten thresholds in `local_config.py`.

**Trade-offs:**

- (+) [Pro]
- (-) [Con]

---

## 7. Related Issue History

List previous bugs or tickets that are semantically related to this issue.

| Date | Issue / Topic | Relevance |
|------|--------------|-----------|
| YYYY-MM-DD | [Issue Title] | [How is it related?] |

---

## 8. Verification Criteria

Checklist to confirm the fix works.

- [ ] **Log Validation:** [Specific log event] appears only once per turn.
- [ ] **Behavioral Test:** System does not trigger on [Condition X].
- [ ] **Regression Test:** Feature Y still works as expected.
- [ ] **Edge Case:** Tested in [High Noise / Low Bandwidth / etc.] environment.
