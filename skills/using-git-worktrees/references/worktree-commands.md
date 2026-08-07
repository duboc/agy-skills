# Git Worktree Command Reference

Quick reference for all git worktree operations.

---

## Creating Worktrees

### New branch from current HEAD

```bash
git worktree add <path> -b <new-branch>
```

Creates a new worktree at `<path>` and checks out a new branch `<new-branch>` based on the current HEAD.

### New branch from a specific base

```bash
git worktree add <path> -b <new-branch> <base-ref>
```

Creates a new worktree with `<new-branch>` based on `<base-ref>` (branch, tag, or commit).

### Existing branch

```bash
git worktree add <path> <existing-branch>
```

Creates a new worktree at `<path>` and checks out `<existing-branch>`.

### Detached HEAD

```bash
git worktree add --detach <path> <commit>
```

Creates a worktree in detached HEAD state at a specific commit.

---

## Listing Worktrees

### Basic list

```bash
git worktree list
```

Output format:
```
/path/to/main       abc1234 [main]
/path/to/worktree1  def5678 [feature/auth]
/path/to/worktree2  ghi9012 [fix/login-bug]
```

### Verbose list

```bash
git worktree list --porcelain
```

Machine-readable output with additional details (HEAD commit, branch, prunable status).

---

## Removing Worktrees

### Clean removal

```bash
git worktree remove <path>
```

Removes the worktree directory and its administrative files. Fails if the worktree has uncommitted changes or untracked files.

### Force removal

```bash
git worktree remove --force <path>
```

Removes the worktree even if it has uncommitted changes. Use when you want to discard all work in the worktree.

### Manual removal + prune

```bash
rm -rf <worktree-path>
git worktree prune
```

Alternative: delete the directory manually and then clean up the administrative files. Useful if the worktree directory was already deleted.

---

## Maintenance

### Prune stale entries

```bash
git worktree prune
```

Removes administrative data for worktrees whose directories no longer exist on disk.

### Dry-run prune

```bash
git worktree prune --dry-run
```

Shows what would be pruned without actually doing it.

### Lock a worktree

```bash
git worktree lock <path>
```

Prevents a worktree from being pruned. Useful for worktrees on removable drives or network mounts.

### Unlock a worktree

```bash
git worktree unlock <path>
```

---

## Moving Worktrees

```bash
git worktree move <old-path> <new-path>
```

Moves a worktree to a new location. Updates the administrative files automatically.

---

## Common Patterns

### Create worktree for a feature branch

```bash
git worktree add .worktrees/auth -b feature/auth main
cd .worktrees/auth
npm install
npm test
```

### Create worktree to review a PR

```bash
git fetch origin pull/123/head:pr-123
git worktree add .worktrees/pr-123 pr-123
cd .worktrees/pr-123
```

### Create worktree for a hotfix

```bash
git worktree add .worktrees/hotfix -b hotfix/critical-fix production
cd .worktrees/hotfix
```

### List and clean up all worktrees

```bash
git worktree list
git worktree remove .worktrees/auth
git worktree remove .worktrees/pr-123
git worktree prune
```

### Check if a branch is already checked out

```bash
git worktree list | grep "feature/auth"
```

If the branch appears in the list, it is already checked out in another worktree. Git will refuse to create a new worktree with the same branch.

---

## Constraints

- **One branch per worktree**: A branch cannot be checked out in multiple worktrees simultaneously.
- **Shared objects**: All worktrees share the same `.git/objects` database. Commits made in any worktree are visible from all others.
- **Independent working directories**: Each worktree has its own working directory, index, and HEAD. Changes in one worktree do not affect another.
- **Garbage collection**: `git gc` in any worktree affects all of them (shared object database).
- **Submodules**: Each worktree needs its own submodule checkout. Run `git submodule update --init` in the new worktree if the project uses submodules.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "fatal: '<branch>' is already checked out" | Branch is in use in another worktree. Use `git worktree list` to find where. |
| Worktree has stale lock | Run `git worktree unlock <path>` then `git worktree prune` |
| Worktree directory was deleted manually | Run `git worktree prune` to clean up administrative files |
| Can't remove worktree — dirty state | Use `git worktree remove --force <path>` or commit/stash changes first |
| New worktree missing node_modules | Run `npm install` in the worktree — dependencies are not shared |
| Git hooks not running in worktree | Hooks are shared from the main `.git` directory. Check `.git/hooks/` in the main repo. |
