# Parallel Agent Isolation, Port Allocation & Teardown Patterns

Use these patterns when running multiple AI coding agents or parallel feature branches across concurrent Git worktrees.

---

## 1. Port & Service Offset Strategy Across Worktrees

When 2+ worktrees run dev servers or integration tests simultaneously on the same machine, deterministic port offsets prevent `EADDRINUSE` collisions:

| Worktree Slot | Offset (`+N*10`) | Frontend Port | Backend API Port | Test DB / Redis Port |
|---------------|------------------|---------------|------------------|----------------------|
| Primary (`main`) | `+0` | `5173` | `8000` | `5432` / `6379` |
| Worktree 1 (`wt-1`) | `+10` | `5183` | `8010` | `5442` / `6389` |
| Worktree 2 (`wt-2`) | `+20` | `5193` | `8020` | `5452` / `6399` |

```bash
# Example: Generate deterministic port offset from worktree name hash
WT_OFFSET=$(( ($(printf '%s' "$WORKTREE_NAME" | cksum | awk '{print $1}') % 50 + 1) * 10 ))
export PORT=$(( 8000 + WT_OFFSET ))
```

---

## 2. Environment & Credential Hygiene in Worktrees

1. **Never copy unencrypted `.env` files into tracked git directories.**
2. Verify `.worktrees/` and `.env*` are ignored before creating worktrees:
   ```bash
   git check-ignore -q .worktrees .env
   ```
3. If temporary test credentials or SQLite databases are created for a worktree run, store them in a user-isolated `0700` directory (`$HOME/.cache/worktrees/<branch>/` or `mktemp -d`) with `0600` file permissions (`umask 077`).

---

## 3. Safe Teardown & Prune Checklist

Before removing a completed worktree:

```bash
set -euo pipefail
# 1. Verify no uncommitted modifications remain
git -C "$WORKTREE_PATH" status --porcelain

# 2. Remove the worktree cleanly via git
git worktree remove "$WORKTREE_PATH"

# 3. Prune stale worktree administrative metadata
git worktree prune
```
