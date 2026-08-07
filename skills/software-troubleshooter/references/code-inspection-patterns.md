# Code Inspection Patterns Guide

Reference for common bug patterns, code smells, and inspection techniques to use during troubleshooting.

## Common Bug Patterns

### State and Concurrency

| Pattern | What to Look For |
|---------|-----------------|
| **Race condition** | Two code paths read/write shared state without synchronization. Check for missing locks, atomic operations, or transaction boundaries. |
| **Stale state** | Cached or local copies of state that diverge from the source of truth. Look for values read once and used later without refresh. |
| **Double processing** | The same input processed by two independent systems (e.g., two event listeners on the same event, duplicate queue consumers). |
| **Missing cleanup** | Resources acquired but never released — open connections, subscriptions, timers, or event listeners not removed on teardown. |

### Control Flow

| Pattern | What to Look For |
|---------|-----------------|
| **Off-by-one** | Loop boundaries using `<` vs `<=`, array index starting at 0 vs 1, fence-post errors in pagination. |
| **Silent failure** | Empty `catch` blocks, swallowed errors, functions that return `null` instead of throwing on invalid input. |
| **Infinite loop / recursion** | Missing or unreachable base case. A condition that can never become false. Recursive calls that don't reduce the problem size. |
| **Wrong branch taken** | Inverted boolean logic, `&&` vs `||` confusion, negation errors. Check operator precedence. |
| **Fall-through** | Missing `break` in switch/case, missing `return` in if/else chains, unintended fall-through in pattern matching. |

### Data and Types

| Pattern | What to Look For |
|---------|-----------------|
| **Null / undefined access** | Accessing properties on values that could be null. Missing null checks after lookups, API calls, or optional chaining. |
| **Type coercion** | Implicit type conversion causing unexpected behavior (e.g., string `"0"` treated as truthy, integer overflow, float precision). |
| **Shape mismatch** | Data structure doesn't match what the consumer expects — renamed fields, nested vs flat, array vs single value. |
| **Encoding issues** | UTF-8 vs ASCII, URL encoding, HTML entity escaping, JSON serialization of special characters. |

### Configuration and Environment

| Pattern | What to Look For |
|---------|-----------------|
| **Config drift** | Different defaults between environments. Feature flags enabled in dev but disabled in prod, or vice versa. |
| **Hardcoded values** | Magic numbers, hardcoded URLs, embedded credentials, or environment-specific paths in source code. |
| **Missing env variable** | Code reads an env var that isn't set, falls back to a default that doesn't work in the current environment. |
| **Dependency conflict** | Two libraries requiring different versions of the same transitive dependency. Lock file out of sync with manifest. |

## Code Inspection Techniques

### Tracing Execution Flow

1. **Find the entry point.** Start from the user action, API endpoint, event handler, or CLI command that triggers the issue.
2. **Follow function calls depth-first.** At each call site, read the called function before continuing to the next line.
3. **Track state mutations.** Note every place a variable, field, or global state is modified. Draw a timeline of state changes.
4. **Identify branching points.** At each `if/else`, `switch`, or ternary, determine which branch is taken for the failing case.
5. **Check boundary crossings.** When data crosses a boundary (function call, API request, serialization, database query), verify the data shape is preserved.

### Comparing Expected vs Actual

1. **Read the spec or documentation.** What is the intended behavior according to docs, comments, or tests?
2. **Read the test.** If there is a test for this code path, does it match the current behavior or the expected behavior?
3. **Diff recent changes.** Use `git log -p --follow <file>` to see how the code evolved. Look for accidental reversions or incomplete refactors.

### Conflict Detection

1. **Search for duplicate handlers.** Grep for the event name, route path, or signal to find all listeners/handlers.
2. **Search for shared state.** Identify global variables, singletons, shared caches, or database rows accessed by multiple components.
3. **Check initialization order.** Verify that dependencies are initialized before they are used, especially in async or module-loading contexts.

## Git Investigation Commands

```bash
# Recent changes to a specific file
git log --oneline -20 -- path/to/file.py

# Show what changed in a file with full diffs
git log -p --follow -5 -- path/to/file.py

# Find commits that added or removed a specific string
git log -S "function_name" --oneline

# Find commits whose diff contains a regex match
git log -G "config.*enabled" --oneline

# Show who last modified each line
git blame path/to/file.py

# Compare a file between two commits or branches
git diff main..feature -- path/to/file.py

# Find when a line was deleted
git log -p -S "deleted_line_content" -- path/to/file.py
```

## Dependency Investigation

```bash
# Node.js — check for duplicate/conflicting packages
npm ls <package-name>
npm explain <package-name>

# Python — show installed version and dependencies
pip show <package-name>
pip check

# Java/Gradle — dependency tree with conflicts
./gradlew dependencies --configuration runtimeClasspath

# Java/Maven — dependency tree
mvn dependency:tree

# Go — why is a module required
go mod why <module>
go mod graph | grep <module>
```
