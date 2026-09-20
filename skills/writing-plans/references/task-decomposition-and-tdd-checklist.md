# Task Decomposition, Dependency DAG & TDD Granularity Checklist

Use this checklist when breaking a feature specification or architectural design into bite-sized, verifiable engineering tasks.

---

## 1. The 5-Minute Atomic Task Rule

Every task in an implementation plan must be scoped so an engineer or subagent can complete and verify it in **2 to 5 minutes**:

| Anti-Pattern Task (Too Coarse) | Atomic TDD Task Breakdown (Right Granularity) |
|--------------------------------|-----------------------------------------------|
| *"Implement authentication middleware and user routes"* | **Task 1**: Write failing unit test for `verify_session_token()` signature & expiration validation (`tests/test_auth.py`).<br>**Task 2**: Implement minimal `verify_session_token()` with `hmac.compare_digest` and pass test.<br>**Task 3**: Write failing FastAPI dependency test for `require_authenticated_user` (`401`/`403` cases).<br>**Task 4**: Wire `require_authenticated_user` onto `/api/profile` and verify full test suite passes. |

---

## 2. Dependency Ordering (Bottom-Up vs Vertical Slice)

Order tasks so the repository remains green (all existing tests pass) after **every single commit**:

1. **Domain Schemas & Pure Functions First**: Data models, Pydantic/TypeScript types, and pure validation helpers with unit tests (`0` external dependencies).
2. **Persistence & Adapter Layer Second**: Repository methods, database migrations, or external client wrappers with isolated contract tests.
3. **API / Route / Controller Layer Third**: Wire domain logic to HTTP/RPC handlers with request/response integration tests.
4. **UI / CLI / End-to-End Integration Last**: Connect frontend components or CLI flags once backend contracts are verified.

---

## 3. Pre-Handoff Plan Quality Checklist

Before finalizing any plan in `docs/plans/YYYY-MM-DD-<feature>.md`, verify:

- [ ] Every file path is exact (`src/services/rate_limiter.py`, never `"the rate limiter file"`).
- [ ] Every task includes the exact test command (`pytest tests/test_rate_limiter.py -v`) and expected failure/pass output.
- [ ] Zero shell injection patterns (`shell=True`, `eval`), zero hardcoded local paths (`/Users/<name>`), and zero non-RFC2606 emails appear in code snippets.
- [ ] Rollback and feature-flag switches are documented for any schema or traffic migration step.
