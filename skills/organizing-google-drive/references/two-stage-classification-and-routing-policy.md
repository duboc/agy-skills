# Two-Stage Hybrid Classification, Deterministic Policy & Reversible Execution

This reference provides the 6-signal classification schema, deterministic policy routing engine, unit test invariants, and 4-phase reversible execution script templates.

---

## 1. Two-Stage Hybrid Classification Schema

### Why Two Stages?
In a typical Google Drive with 1,000+ files, ~80% are `.gdoc`/`.gsheet`/`.gslides` pointers. Fetching cloud content for every pointer via REST API or MCP is slow and wastes quota. Instead:
- **Stage 1 (Local Pass — 0 Cloud API Calls):** Classify all files using local previews (for materialized `.pptx`, `.docx`, `.xlsx`, `.pdf`, `.ipynb`, and images) and the **6 context signals** below. Even when a `.gdoc` pointer has no local text, `parent_rel_dir` + `folder_cluster_hint` (sibling filenames in the same directory) resolves ~85% of cloud files with high confidence.
- **Stage 2 (Targeted Cloud Snippet Sampling — ~15% of Files):** Only fetch the first 200–400 chars from the cloud (via parallel Workspace MCP subagents `gdocs`/`gsheets`/`gslides` or Drive API `files().export`) for cloud pointers where:
  1. `confidence < 0.78`, OR
  2. `needs_content_fetch == True`, OR
  3. `filename` matches a generic untitled pattern (`^(untitled|copy of|documento sem|apresenta|planilha|document|presentation|spreadsheet)`).

### Classifier Prompt & Structured Output Contract

Pass these 6 signals per item (in batches of 8–12 items per prompt, saving checkpoints to an isolated `0700` cache directory with `0600` permissions after every batch):

```text
Item [i]:
- filename: <filename>
- parent_rel_dir: <relative directory path>
- folder_cluster_hint: <up to 8 sibling filenames in the same folder>
- modified_date: <YYYY-MM-DD>
- file_type: <ext> (doc_id=<doc_id or local>)
- content_preview: <500-char local preview or Stage 2 cloud snippet or [CLOUD_POINTER_NO_LOCAL_TEXT]>
```

Require the model to return a JSON array matching this schema:

```json
[
  {
    "idx": 0,
    "domain": "client | event | template_or_asset | internal | personal | empty_or_junk",
    "entity_name": "Canonical Client or Event Name or null",
    "asset_type": "deck | demo_or_dataset | template_or_arch | impact_review | private_sensitive | general_doc",
    "is_private_or_sensitive": false,
    "confidence": 0.92,
    "needs_content_fetch": false,
    "rationale": "Concise one-sentence explanation citing filename, sibling cluster, or content snippet."
  }
]
```

---

## 2. Deterministic Policy & Routing Engine (`compute_target_path`)

Never let the LLM output raw destination folder paths directly. Always pass the model's semantic prediction through a deterministic, unit-tested Python function that enforces organizational invariants:

```python
from typing import Any, Dict, Set

KNOWN_EVENTS: Set[str] = {
    "Next",
    "Executive Forum",
    "Cloud Summit",
    "Retail Day",
    "GenAI Day",
}

def compute_target_path(
    item: Dict[str, Any],
    pred: Dict[str, Any],
    archive_cutoff_year: int = 2025,
) -> str:
    """Map item metadata + model semantic tags to a deterministic target path."""
    rel = item["rel_path"].lower()
    fname = item["filename"]
    year = int(item["modified_date"][:4])
    domain = pred.get("domain", "internal")
    entity = (pred.get("entity_name") or "").strip()
    asset = pred.get("asset_type", "general_doc")

    # Invariant 1: Private/Sensitive & Impact Review protection across ALL modification years
    if "/private/" in f"/{rel}" or "private-" in rel or pred.get("is_private_or_sensitive"):
        return f"04_Internal/Private/{fname}"
    if "impact review" in rel or asset == "impact_review":
        return f"04_Internal/Impact Reviews/{fname}"

    # Invariant 2: Client/Customer continuity across ALL modification years
    if domain == "client" and entity:
        return f"01_Clients/{entity}/{fname}"

    # Empty or untitled scratch files
    if domain == "empty_or_junk":
        return f"99_Archive/_Empty and Untitled/{fname}"

    # Personal files
    if domain == "personal":
        return f"05_Personal/{fname}"

    # Events (canonical recurring events vs. 1-off events)
    if domain == "event":
        bucket = entity if entity in KNOWN_EVENTS else "Other Events"
        return f"02_Events/{bucket}/{fname}"

    # Reusable talks, assets, demos, and templates
    if domain == "template_or_asset":
        subfolder = {
            "deck": "Decks",
            "demo_or_dataset": "Demos_and_Datasets",
            "template_or_arch": "Templates_and_Architectures",
        }.get(asset, "Templates_and_Architectures")
        return f"03_Talks_Assets_Templates/{subfolder}/{fname}"

    # Invariant 3: Scoped age-based archiving ONLY for general internal files
    if year < archive_cutoff_year:
        return f"99_Archive/{year}/{fname}"
    return f"04_Internal/{fname}"
```

### Mandatory `pytest` Guardrail Tests

Before running batch classification or moving any files, verify these invariants with `pytest`:
1. `test_protected_dirs_never_scanned`: Asserts `0` items in the inventory have `rel_path` starting with any directory in `PROTECTED_DIRS`.
2. `test_private_files_never_archived_by_age`: Asserts a file modified in `2022` inside `Private/` or with `is_private_or_sensitive=True` routes to `04_Internal/Private/`, never `99_Archive/2022/`.
3. `test_client_files_never_archived_by_age`: Asserts a file modified in `2023` with `domain="client", entity_name="Acme"` routes to `01_Clients/Acme/`, never `99_Archive/2023/`.
4. `test_old_general_internal_files_archived_by_year`: Asserts a general internal doc modified in `2023` without a client or private flag routes to `99_Archive/2023/`.

---

## 3. Human Review Staging & 4-Phase Reversible Execution

### Step 1: Stage Plan to Google Sheet or CSV
Generate the complete plan table with columns:
`action` (`MOVE`, `REVIEW` when `confidence < 0.75`, `KEEP`, `ARCHIVE_VAULT`), `current_rel_path`, `target_rel_path`, `domain`, `entity_name`, `asset_type`, `confidence`, `rationale`, `modified_date`, `doc_id`.
Wait for explicit human approval before executing any moves.

### Step 2: Execute in 4 Ordered Phases & Write `execution_manifest.json`

```python
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Set

def non_colliding_destination(dst: Path, src: Path) -> Path:
    """Resolve destination filename collisions without overwriting existing files."""
    if not dst.exists() or os.path.samefile(src, dst):
        return dst
    stem, suffix = dst.stem, dst.suffix
    counter = 1
    while True:
        candidate = dst.parent / f"{stem} ({counter}){suffix}"
        if not candidate.exists():
            return candidate
        counter += 1

def move_atomic(src: Path, dst: Path, phase: str, manifest: List[Dict[str, str]]) -> None:
    """Move a file or directory within DriveFS via os.rename and record reversible audit entry."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    final_dst = non_colliding_destination(dst, src)
    os.rename(src, final_dst)
    manifest.append({
        "phase": phase,
        "src": str(src),
        "dst": str(final_dst),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })

def rollback_manifest(manifest_path: Path) -> None:
    """Reverse all moves recorded in execution_manifest.json in LIFO order."""
    entries = json.loads(manifest_path.read_text(encoding="utf-8"))
    for entry in reversed(entries):
        src = Path(entry["src"])
        dst = Path(entry["dst"])
        if dst.exists() and not src.exists():
            src.parent.mkdir(parents=True, exist_ok=True)
            os.rename(dst, src)
```

Execute phases in strict order:
1. **`Phase_A_Vault_Rescue`**: Move rescued `.gdoc`/`.gsheet`/`.gslides`/`.pptx`/`.pdf`/`.xlsx` deliverables out of `RETIRED_VAULTS` into their target taxonomy folders.
2. **`Phase_B_Archive_Vaults`**: Move the remaining `RETIRED_VAULTS` directories intact into `99_Archive/Vaults/<vault_name>/` via `os.rename()`.
3. **`Phase_C_Regular_Moves`**: Move all remaining approved files into `01_Clients/`, `02_Events/`, `03_Talks_Assets_Templates/`, `04_Internal/`, `05_Personal/`, and `99_Archive/`.
4. **`Phase_D_Park_Legacy_Folders`**: Move emptied legacy root folders into `99_Archive/_Empty and Untitled/Legacy_Folders/`—never delete legacy folders with `shutil.rmtree` or `os.rmdir`.
