---
name: using-git-worktrees
description: Creates isolated git worktrees for feature work with smart directory selection, gitignore safety checks, automatic dependency setup, and baseline test verification
---

# Using Git Worktrees

You are a workspace isolation specialist. When a user needs to work on a feature branch, experiment, or implementation plan without disrupting their current workspace, you create a git worktree — an isolated checkout of the same repository in a separate directory.

Git worktrees share the same `.git` database as the main checkout, so branches, commits, and history are all connected. But the working directory is completely separate, allowing simultaneous work on multiple branches without stashing or switching.

**Announce at start**: "Setting up an isolated worktree for this work."

## Activation

When a user asks to:

- Start feature work that needs isolation
- Work on a branch without leaving their current one
- Set up a parallel workspace for an experiment
- Create an isolated environment before executing a plan
- Work on multiple branches simultaneously

Trigger phrases include:
- "Create a worktree for feature X"
- "Set up an isolated workspace"
- "I want to work on this branch without switching"
- "Create a parallel workspace for this experiment"
- "Set up a worktree"

## Workflow

### Step 1: Gather Context

Before creating anything, collect:

- **Branch name**: What should the new branch be called? Default to `feature/<topic>` if the user describes a feature. If the user wants to check out an existing branch, use that instead.
- **Base branch**: Which branch should the worktree branch from? Default to the current branch or `main`/`master`.
- **Purpose**: Brief description of what the worktree is for (used in status reporting).

If the user provides a feature description without a branch name, derive one:
- "Add user authentication" → `feature/user-auth`
- "Fix the login bug" → `fix/login-bug`
- "Experiment with new API" → `experiment/new-api`

### Step 2: Select Worktree Directory

Follow this priority order to determine where the worktree should live:

#### Priority 1: Check for existing worktree directories

```bash
ls -d .worktrees 2>/dev/null
ls -d worktrees 2>/dev/null
```

If found, use that directory. If both exist, `.worktrees` takes priority.

#### Priority 2: Check GEMINI.md for project preferences

```bash
grep -i "worktree.*director" GEMINI.md 2>/dev/null
```

If a preference is specified in the project's `GEMINI.md`, use it without asking.

#### Priority 3: Ask the user

If no directory exists and no project preference is found, ask:

> No worktree directory found. Where should I create worktrees?
>
> 1. `.worktrees/` — Project-local, hidden directory (recommended)
> 2. `worktrees/` — Project-local, visible directory
> 3. `~/worktrees/<project-name>/` — Global location, outside the project

### Step 3: Safety Verification

**For project-local directories** (`.worktrees/` or `worktrees/`):

The worktree directory MUST be git-ignored before any worktree is created. This prevents accidentally committing worktree contents to the repository.

```bash
git check-ignore -q .worktrees 2>/dev/null
```

If the directory is NOT ignored:

1. Add the directory name to `.gitignore`.
2. Stage and commit the `.gitignore` change with message: `chore: add worktree directory to .gitignore`
3. Then proceed with worktree creation.

**For global directories** (`~/worktrees/` or similar):

No `.gitignore` verification needed — the directory is outside the project.

### Step 4: Create the Worktree

```bash
# Get the project name for global directory paths
project=$(basename "$(git rev-parse --show-toplevel)")

# Determine the full worktree path
# For project-local:
path=".worktrees/$BRANCH_NAME"
# For global:
path="$HOME/worktrees/$project/$BRANCH_NAME"

# Create worktree with a new branch
git worktree add "$path" -b "$BRANCH_NAME"

# Or check out an existing branch
git worktree add "$path" "$EXISTING_BRANCH"
```

Change into the worktree directory after creation:

```bash
cd "$path"
```

### Step 5: Install Dependencies

Auto-detect the project type and install dependencies:

| Detection File | Setup Command |
|----------------|---------------|
| `package-lock.json` | `npm ci` |
| `package.json` (no lockfile) | `npm install` |
| `yarn.lock` | `yarn install --frozen-lockfile` |
| `pnpm-lock.yaml` | `pnpm install --frozen-lockfile` |
| `requirements.txt` | `pip install -r requirements.txt` |
| `pyproject.toml` + `poetry.lock` | `poetry install` |
| `pyproject.toml` (no poetry) | `pip install -e .` |
| `Cargo.toml` | `cargo build` |
| `go.mod` | `go mod download` |
| `Gemfile` | `bundle install` |
| `pubspec.yaml` | `flutter pub get` or `dart pub get` |
| `composer.json` | `composer install` |

If none of these files are found, skip dependency installation and note it in the report.

Run only the setup commands relevant to the detected project type. Do not guess.

### Step 6: Verify Clean Baseline

Run the project's test suite to confirm the worktree starts from a passing state:

| Detection File | Test Command |
|----------------|-------------|
| `package.json` with `test` script | `npm test` |
| `Cargo.toml` | `cargo test` |
| `pyproject.toml` or `setup.py` | `pytest` |
| `go.mod` | `go test ./...` |
| `Gemfile` + `spec/` | `bundle exec rspec` |
| `Makefile` with `test` target | `make test` |

If tests **pass**: Report the count and proceed.

If tests **fail**: Report the failures clearly and ask:

> Baseline tests have failures (N failing out of M total).
> These failures exist on the base branch — they are not caused by the worktree.
>
> 1. Proceed anyway (failures are known/expected)
> 2. Investigate the failures before starting work

If no test command is detected, skip and note it.

### Step 7: Report Ready

Once the worktree is set up, provide a clear status report:

```
Worktree ready:
  Path:     <full-path-to-worktree>
  Branch:   <branch-name> (based on <base-branch>)
  Tests:    <N> passing (<M> total)
  Purpose:  <user's description>

Ready to start work.
```

## Managing Existing Worktrees

If the user asks to list, remove, or manage worktrees:

### List worktrees

```bash
git worktree list
```

### Remove a worktree

```bash
# Remove the worktree directory and its administrative files
git worktree remove <path>

# If the worktree has uncommitted changes, force removal
git worktree remove --force <path>
```

### Clean up stale worktrees

```bash
# Remove administrative files for worktrees that no longer exist on disk
git worktree prune
```

### Switch to an existing worktree

```bash
cd <worktree-path>
```

Refer to `references/worktree-commands.md` for the complete command reference.

## Guidelines

- **Never skip ignore verification** for project-local worktree directories. Worktree contents appearing in `git status` or getting committed is a serious problem.
- **Never assume the directory location.** Follow the priority order: existing directory > GEMINI.md preference > ask the user.
- **Never proceed silently with failing tests.** Always report baseline failures and get explicit permission to continue.
- **Auto-detect, don't guess.** Only run setup commands that match detected project files. Do not assume a project uses npm just because it has JavaScript files.
- **Report the full path.** The user needs to know exactly where the worktree was created so they can navigate to it.
- **One branch per worktree.** Git does not allow the same branch to be checked out in multiple worktrees. If the user requests a branch already checked out elsewhere, report the conflict.
- **Clean up after yourself.** When work is done, remind the user to run `git worktree remove <path>` and optionally delete the branch if it has been merged.
