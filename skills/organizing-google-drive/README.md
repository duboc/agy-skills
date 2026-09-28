# Organizing Google Drive (`organizing-google-drive`)

Reusable skill for auditing, batch-classifying, and safely reorganizing Google Drive and macOS Google Drive for Desktop (`DriveFS`) mounts containing mixed Google Workspace pointers (`.gdoc`, `.gsheet`, `.gslides`), local Office/PDF/image binaries, and active or retired Obsidian/markdown vaults.

## Key Capabilities

- **DriveFS-Safe Virtual Filesystem Mechanics:** Detects ~176-byte `.gdoc`/`.gsheet`/`.gslides` JSON pointers (`doc_id`) and cloud-evicted `SF_DATALESS` stubs (`os.lstat(path).st_blocks == 0`) so scripts never hang downloading multi-GB archives or break `webViewLink` URLs.
- **Active Vault Guardrails & Recursive Vault Rescue:** Protects active Obsidian/markdown vaults (`PROTECTED_DIRS`) with `pytest` invariants while recursively rescuing live cloud pointers and client deliverables out of retired vaults before moving them to `99_Archive/Vaults/`.
- **Two-Stage Hybrid AI Classification:** Classifies ~85% of Drive files in Stage 1 with zero cloud API calls using local previews + 6 path/sibling context signals (`folder_cluster_hint`), and selectively samples the remaining ~15% (`confidence < 0.78` or generic `Untitled*` names) in Stage 2 via parallel Workspace MCP subagents.
- **Deterministic Policy & Reversible 4-Phase Execution:** Separates semantic model predictions from a unit-tested `compute_target_path()` routing function (protecting `Private` and `Client` files across all modification years), stages the plan to a Google Sheet or CSV for human sign-off, and logs every `os.rename()` move to `execution_manifest.json`.

## Reference Guides

- [`references/drivefs-mechanics-and-vault-rescue.md`](references/drivefs-mechanics-and-vault-rescue.md): Deep-dive into `.gdoc` pointer parsing, `st_blocks == 0` dataless stub detection, shared-folder permission checks, and recursive vault deliverable rescue.
- [`references/two-stage-classification-and-routing-policy.md`](references/two-stage-classification-and-routing-policy.md): Complete 6-signal classifier schema, deterministic `compute_target_path()` routing policy, unit tests, and 4-phase reversible execution script templates.
