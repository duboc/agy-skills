# DriveFS Mechanics, Dataless Cloud Stubs & Recursive Vault Rescue

This guide covers the filesystem mechanics of Google Drive for Desktop (`DriveFS` / macOS FileProvider) required to scan, rescue, and move files without triggering multi-GB cloud downloads or breaking Google Workspace URLs.

---

## 1. Google Workspace Pointers (`.gdoc`, `.gsheet`, `.gslides`)

On macOS and Windows Google Drive for Desktop mounts, native Google Workspace documents are stored locally as ~176-byte JSON pointer files:

```json
{"doc_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms", "email": "user@example.com", "resource_key": ""}
```

### Key Rules for Pointer Files
1. **Never pass `.gdoc`/`.gsheet`/`.gslides` to binary parsers** (`python-docx`, `openpyxl`, `python-pptx`). Instead, parse the JSON to extract `doc_id`.
2. **Same-Mount `os.rename(src, dst)` Preserves Everything:**
   - Moving a `.gdoc`, `.gsheet`, or `.gslides` file inside the same `My Drive` mount using Python's `os.rename(src, dst)` triggers an atomic server-side parent update in Google Drive.
   - It preserves the exact `doc_id`, `webViewLink` URL, revision history, `modifiedTime`, and sharing permissions while keeping the local DriveFS cache synchronized.
   - Avoid mixing remote Drive REST API `files().update(addParents=..., removeParents=...)` with local `shutil.move` during a single batch run, as doing so causes DriveFS cache desynchronization.

---

## 2. Detecting Cloud-Evicted ("Dataless") Stubs (`st_blocks == 0`)

Google Drive for Desktop streams files on demand. Files that exist in the cloud but have been evicted from local disk storage are marked with `SF_DATALESS` (`0x40000000` on macOS) and report `0` allocated 512-byte blocks (`st_blocks == 0`) even though `st_size > 0`:

```python
import os
from pathlib import Path

SF_DATALESS = 0x40000000  # macOS FileProvider / DriveFS dataless flag
CLOUD_POINTER_EXTS = {".gdoc", ".gsheet", ".gslides"}

def is_dataless(path: Path) -> bool:
    """Return True if path is a cloud-evicted stub whose bytes are not materialized locally."""
    st = os.lstat(path)
    if getattr(st, "st_flags", 0) & SF_DATALESS:
        return True
    return (
        st.st_blocks == 0
        and st.st_size > 0
        and path.suffix.lower() not in CLOUD_POINTER_EXTS
    )
```

### Why You Must Never Run `zipfile` or `tarfile` on Dataless Trees
- Calling `zipfile.ZipFile.write()`, `tarfile`, `shutil.make_archive()`, or `path.read_bytes()` on a dataless file forces the kernel to block while `DriveFS` downloads the full file over the network.
- Retired Obsidian or markdown vaults in Google Drive frequently contain hundreds of evicted `.md` and `.png` files (`st_blocks == 0`). Attempting to zip them blocks indefinitely or hits Drive rate limits.
- **Required Pattern:** Move retired vault folders intact into `99_Archive/Vaults/<vault_name>/` using `os.rename(src, dst)` (a `<0.1s` metadata-only server-side move). If the user later wants a `.zip` archive, instruct them to right-click `99_Archive/Vaults/` in Finder and select **"Make available offline"** before compressing.

---

## 3. Active Vault Protection vs. Recursive Retired Vault Rescue

Before scanning a Drive root, inspect top-level and second-level directories for workspace markers (`.obsidian/`, `.foam/`, `.logseq/`, `.git/`) and Google system directories (`Colab Notebooks`, `Google AI Studio`, `Google Meet`, `Gemini Gems`, `appsheet`).

Confirm with the user which directories belong to:
- **`PROTECTED_DIRS` (Active Vaults & System Folders):** Strictly off-limits. Prune at the top of `os.walk` so zero files inside are ever listed, read, or moved.
- **`RETIRED_VAULTS` (Inactive Vaults to Archive):** Must be recursively scanned to rescue live cloud pointers and client deliverables *before* archiving the markdown vault.

```python
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Set

RESCUE_EXTS = {".gdoc", ".gsheet", ".gslides", ".pptx", ".docx", ".xlsx", ".pdf", ".drawio"}

def build_drive_inventory(
    drive_root: Path,
    protected_dirs: Set[str],
    retired_vaults: Set[str],
) -> List[Dict[str, Any]]:
    """Scan drive_root while enforcing PROTECTED_DIRS and rescuing deliverables from RETIRED_VAULTS."""
    inventory: List[Dict[str, Any]] = []

    for cur_root, dirs, files in os.walk(drive_root, topdown=True):
        rel_dir = Path(cur_root).relative_to(drive_root)
        parts = rel_dir.parts

        # 1. Hard guardrail: never descend into PROTECTED_DIRS
        if not parts:
            dirs[:] = [
                d for d in dirs
                if d not in protected_dirs and not d.startswith(".")
            ]
        else:
            if parts[0] in protected_dirs:
                dirs[:] = []
                continue
            dirs[:] = [d for d in dirs if not d.startswith(".")]

        rel_dir_posix = "" if str(rel_dir) == "." else rel_dir.as_posix()
        in_retired_vault = any(
            rel_dir_posix == rv or rel_dir_posix.startswith(rv + "/")
            for rv in retired_vaults
        )

        visible_files = sorted(f for f in files if f != ".DS_Store" and not f.startswith("~$"))

        for fname in visible_files:
            fpath = Path(cur_root) / fname
            ext = fpath.suffix.lower()

            # 2. Inside a retired vault: recursively rescue ONLY cloud pointers and binary deliverables
            if in_retired_vault and ext not in RESCUE_EXTS:
                continue

            st = os.lstat(fpath)
            mtime_iso = datetime.fromtimestamp(st.st_mtime, tz=timezone.utc).strftime("%Y-%m-%d")
            doc_id = None
            if ext in CLOUD_POINTER_EXTS:
                try:
                    doc_id = json.loads(fpath.read_text(encoding="utf-8")).get("doc_id")
                except Exception:
                    doc_id = None

            siblings = [s for s in visible_files if s != fname][:8]
            inventory.append({
                "filename": fname,
                "rel_path": f"{rel_dir_posix}/{fname}" if rel_dir_posix else fname,
                "parent_rel_dir": rel_dir_posix or "(root)",
                "ext": ext,
                "doc_id": doc_id,
                "size_bytes": st.st_size,
                "is_dataless": is_dataless(fpath),
                "modified_date": mtime_iso,
                "folder_cluster_hint": ", ".join(siblings),
                "vault_source": next(
                    (rv for rv in retired_vaults if rel_dir_posix == rv or rel_dir_posix.startswith(rv + "/")),
                    None,
                ),
            })

    return inventory
```

---

## 4. Checking Folder Sharing Permissions Before Unpacking

When a legacy container folder (e.g., `shared-deliverables/`, `general-share/`, `clients/`) holds files that will be unpacked into a new taxonomy (`01_Clients/`, `02_Events/`, etc.), moving a file out of a shared parent folder changes the permissions it inherits from that parent.

Always verify folder-level permissions before flattening a legacy folder:
- **Via Google Drive MCP (`gdrive permissions`):** Check whether the folder has non-owner permissions (`anyoneWithLink`, domain-wide, or external collaborator emails).
- **Via Google Drive API v3:** Call `permissions().list(fileId=folder_id, fields="permissions(id,type,role,emailAddress,domain)")`.
- If a folder has active external or team-wide sharing, either keep that folder intact or flag its children for explicit user confirmation before moving them.
