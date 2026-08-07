#!/usr/bin/env bash
set -euo pipefail

# update-references.sh
# Fetches the latest ADK documentation from official sources.
# Run periodically to keep the skill's knowledge current.
# Works on macOS and Linux.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REFERENCES_DIR="${SCRIPT_DIR}/../references"

mkdir -p "$REFERENCES_DIR"

echo "Updating ADK reference documentation..."

# ADK Python SDK - condensed API reference
echo "  Fetching llms.txt (condensed API reference)..."
curl -sL "https://google.github.io/adk-docs/llms.txt" \
    -o "${REFERENCES_DIR}/llms.txt"

# ADK Documentation - full text dump
echo "  Fetching llms-full.txt (full documentation)..."
curl -sL "https://google.github.io/adk-docs/llms-full.txt" \
    -o "${REFERENCES_DIR}/llms-full.txt"

# ADK Python getting started guide
echo "  Fetching Python quickstart..."
curl -sL "https://raw.githubusercontent.com/google/adk-docs/main/docs/get-started/python.md" \
    -o "${REFERENCES_DIR}/getting-started-python.md"

# Fix relative image/link paths to absolute GitHub URLs
if [[ "$(uname)" == "Darwin" ]]; then
    sed -i '' 's|](/adk-docs/|](https://google.github.io/adk-docs/|g' \
        "${REFERENCES_DIR}/getting-started-python.md" 2>/dev/null || true
else
    sed -i 's|](/adk-docs/|](https://google.github.io/adk-docs/|g' \
        "${REFERENCES_DIR}/getting-started-python.md" 2>/dev/null || true
fi

echo ""
echo "References updated in ${REFERENCES_DIR}/"
echo ""
echo "Files:"
ls -lh "${REFERENCES_DIR}/llms.txt" "${REFERENCES_DIR}/llms-full.txt" "${REFERENCES_DIR}/getting-started-python.md" 2>/dev/null
echo ""
echo "These files provide the latest ADK API details and documentation."
echo "The skill's curated guides (architecture-guide.md, etc.) are maintained manually."
