# Using Git Worktrees

A Agy skill for creating isolated git worktrees with smart directory selection, safety verification, automatic dependency setup, and baseline test checks.

## What It Does

This skill automates the process of setting up a parallel workspace in the same repository using git worktrees. It handles the full lifecycle:

1. **Directory selection** — Detects existing worktree directories, checks project preferences in `GEMINI.md`, or asks the user. Follows a strict priority order.
2. **Safety verification** — Ensures project-local worktree directories are git-ignored before creating anything. Fixes `.gitignore` automatically if needed.
3. **Worktree creation** — Creates the worktree with a new or existing branch, based from the appropriate starting point.
4. **Dependency setup** — Auto-detects the project type (Node.js, Python, Rust, Go, Ruby, Dart, PHP) and runs the appropriate install command.
5. **Baseline testing** — Runs the project's test suite to confirm the worktree starts clean. Reports failures and asks before proceeding.
6. **Status report** — Provides the full path, branch info, and test results so the user knows exactly where to work.

## When Does It Activate?

The skill activates when you ask Agy to create an isolated workspace or set up a worktree:

```
Create a worktree for the user authentication feature
```

```
Set up an isolated workspace for this bugfix
```

```
I want to work on the refactor branch without leaving main
```

```
Create a parallel workspace to experiment with the new API
```

```
Set up a worktree for reviewing PR #42
```

## How It Works

```
User request → Detect worktree directory → Verify .gitignore safety
                                                    ↓
        Report ready ← Run tests ← Install deps ← Create worktree + branch
```

### Directory Priority

| Priority | Source | Action |
|----------|--------|--------|
| 1 | `.worktrees/` exists | Use it (verify ignored) |
| 2 | `worktrees/` exists | Use it (verify ignored) |
| 3 | Both exist | Use `.worktrees/` |
| 4 | `GEMINI.md` specifies preference | Use it |
| 5 | None of the above | Ask the user |

### Safety Checks

- Project-local directories (`.worktrees/`, `worktrees/`) must be in `.gitignore` before any worktree is created
- If not ignored, the skill adds it to `.gitignore` and commits the change automatically
- Global directories (`~/worktrees/`) skip this check — they are outside the project

## Installation

### Option B: One-liner

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- using-git-worktrees
```

For user-scope installation (available across all projects):

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- using-git-worktrees --scope user
```

### Option C: Manual

```bash
cp -r skills/using-git-worktrees ~/.gemini/config/skills/using-git-worktrees
```

## Usage Examples

### Create a feature branch worktree

```
Create a worktree for adding OAuth2 support, branching from main
```

### Set up a worktree for a bugfix

```
I need an isolated workspace to fix the race condition in the queue processor
```

### Check out an existing branch in a worktree

```
Create a worktree to work on the existing branch release/v2.1
```

### Review a pull request in isolation

```
Set up a worktree so I can review and test PR #87
```

### List and manage worktrees

```
Show me all active worktrees in this project
```

```
Remove the worktree for the auth feature — it's been merged
```

## Included References

| File | Description |
|------|-------------|
| **worktree-commands.md** | Complete git worktree command reference — creation, listing, removal, maintenance, common patterns, constraints, and troubleshooting |
