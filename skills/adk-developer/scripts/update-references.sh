#!/usr/bin/env bash
set -euo pipefail
umask 077

# update-references.sh
# Fetches the latest ADK documentation from official sources using an isolated
# temporary staging directory (0700) with deterministic cleanup and PII hygiene.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REFERENCES_DIR="${SCRIPT_DIR}/../references"
TMP_DIR="$(mktemp -d)"
chmod 700 "$TMP_DIR"
trap 'rm -rf "$TMP_DIR"' EXIT

mkdir -p "$REFERENCES_DIR"

echo "Updating ADK reference documentation..."

# ADK Python SDK - condensed API reference
echo "  Fetching llms.txt (condensed API reference)..."
curl -fsSL "https://adk.dev/llms.txt" -o "${TMP_DIR}/llms.txt"

# ADK Documentation - full text dump
echo "  Fetching llms-full.txt (full documentation)..."
curl -fsSL "https://adk.dev/llms-full.txt" -o "${TMP_DIR}/llms-full.txt"

# Sanitize upstream docs for RFC-2606 email & path hygiene before installing
python3 - "$TMP_DIR" "$REFERENCES_DIR" <<'PYEOF'
import re
import shutil
import sys
from pathlib import Path

tmp_dir = Path(sys.argv[1])
ref_dir = Path(sys.argv[2])

for fname in ("llms.txt", "llms-full.txt"):
    src = tmp_dir / fname
    text = src.read_text(encoding="utf-8", errors="replace")
    text = re.sub(
        r"\b[A-Za-z0-9._%+-]+@(?!example\.(?:com|org|net)\b|[A-Za-z0-9.-]*\.gserviceaccount\.com\b)[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "agent-feedback@example.com",
        text,
    )
    text = re.sub(r"/Users/(?!<|shared|Shared|example)[A-Za-z0-9._-]+", "$HOME/workspace", text)
    text = re.sub(r"(?<![a-zA-Z0-9_.-])go/(index|example|cloud-run|a2a_basic)\b", r"golang/\1", text)
    text = text.replace('working_dir="$HOME/.cache/my_agent_workspace"', 'working_dir=os.path.expanduser("~/.cache/adk/my_agent_workspace")')
    text = text.replace('"@modelcontextprotocol/server-filesystem", "/tmp"', '"@modelcontextprotocol/server-filesystem", os.path.expanduser("~/.cache/adk-mcp")')
    dst = ref_dir / fname
    dst.write_text(text, encoding="utf-8")
PYEOF

echo "References updated in ${REFERENCES_DIR}/"
ls -lh "${REFERENCES_DIR}/llms.txt" "${REFERENCES_DIR}/llms-full.txt"
