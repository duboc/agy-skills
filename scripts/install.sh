#!/usr/bin/env bash
set -euo pipefail

REPO="duboc/agy-skills"
BRANCH="main"
TARBALL_URL="https://api.github.com/repos/${REPO}/tarball/${BRANCH}"

usage() {
  cat <<EOF
Usage: $(basename "$0") <skill-name> [--scope user|workspace]

Install an Agy skill from the agy-skills repository.

Arguments:
  skill-name          Name of the skill to install (e.g., software-troubleshooter)

Options:
  --scope user        Install to ~/.gemini/config/skills/<name>/ (user scope)
  --scope workspace   Install to .agents/skills/<name>/ in current directory (default)
  -h, --help          Show this help message

Examples:
  $(basename "$0") software-troubleshooter
  $(basename "$0") software-troubleshooter --scope user

Available skills:
  software-troubleshooter   Structured code inspection and troubleshooting
  adk-developer             Build agents with Google's ADK (Python, Java, Go, TS)
  agent-engine-deploy       Deploy ADK agents on Vertex AI Agent Engine
  agent-engine-sessions-memory  Manage sessions and memory for Agent Engine agents
  agent-engine-ops          Monitor, trace, secure, and evaluate Agent Engine agents
  ai-studio-architect       Convert AI Studio prototypes to production on GCP
  clarity-presenter         MARP decks with SCQA narrative + assertion-evidence design
  developer-growth-analysis Analyze Agy session history for growth patterns
  google-ads-funnel         Funnel-as-Code workflows for Google Ads
  spring-boot-upgrader      Migrate Spring Boot apps to 4.0 with phased upgrade plans
  using-git-worktrees       Create isolated git worktrees with safety checks
  webapp-testing            Test local web apps with Playwright
  writing-plans             Generate TDD implementation plans
  zen-presenter             MARP decks following Presentation Zen principles
  visual-explainer          Generate visual HTML pages for diagrams and data
  html-to-pptx              Convert MARP HTML slides to editable PowerPoint
  zen-pitch                 Research domain & compile persuasive Presentation Zen pitch deck
  technical-drawing         Create precise, dimensioned technical drawings in SVG
  cloud-architecture-diagram  Draw a deployed system as a Google Cloud reference architecture
  app-security-audit        Google Cloud, GenAI/Gemini, BFF proxy, CGNAT & 8h+ kiosk security audit
EOF
}

# --- Parse arguments ---
SKILL_NAME=""
SCOPE="workspace"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --scope)
      if [[ -z "${2:-}" ]]; then
        echo "Error: --scope requires a value (user or workspace)" >&2
        exit 1
      fi
      SCOPE="$2"
      shift 2
      ;;
    -*)
      echo "Error: Unknown option '$1'" >&2
      usage
      exit 1
      ;;
    *)
      if [[ -z "$SKILL_NAME" ]]; then
        SKILL_NAME="$1"
      else
        echo "Error: Unexpected argument '$1'" >&2
        usage
        exit 1
      fi
      shift
      ;;
  esac
done

if [[ -z "$SKILL_NAME" ]]; then
  echo "Error: skill name is required" >&2
  echo ""
  usage
  exit 1
fi

if [[ "$SCOPE" != "user" && "$SCOPE" != "workspace" ]]; then
  echo "Error: --scope must be 'user' or 'workspace'" >&2
  exit 1
fi

# --- Determine install directory ---
if [[ "$SCOPE" == "user" ]]; then
  INSTALL_DIR="${HOME}/.gemini/config/skills/${SKILL_NAME}"
else
  INSTALL_DIR=".agents/skills/${SKILL_NAME}"
fi

echo "Installing skill '${SKILL_NAME}' to ${INSTALL_DIR} ..."

# --- Download and extract ---
TMPDIR_PATH=$(mktemp -d)
trap 'rm -rf "$TMPDIR_PATH"' EXIT

echo "Downloading from GitHub ..."
HTTP_CODE=$(curl -fsSL -w "%{http_code}" -o "${TMPDIR_PATH}/repo.tar.gz" "$TARBALL_URL")

if [[ "$HTTP_CODE" -lt 200 || "$HTTP_CODE" -ge 300 ]]; then
  echo "Error: Failed to download tarball (HTTP ${HTTP_CODE})" >&2
  exit 1
fi

# Extract only the skill directory.
# GitHub tarballs have a top-level directory like "duboc-agy-skills-<sha>/".
# We use --strip-components=1 and filter to skills/<name>/ to get just the skill files.
EXTRACT_DIR="${TMPDIR_PATH}/extracted"
mkdir -p "$EXTRACT_DIR"

tar -xzf "${TMPDIR_PATH}/repo.tar.gz" -C "$EXTRACT_DIR" --strip-components=1 2>/dev/null

SKILL_SOURCE="${EXTRACT_DIR}/skills/${SKILL_NAME}"

if [[ ! -d "$SKILL_SOURCE" ]]; then
  echo "Error: Skill '${SKILL_NAME}' not found in the repository." >&2
  echo ""
  echo "Available skills:"
  if [[ -d "${EXTRACT_DIR}/skills" ]]; then
    for dir in "${EXTRACT_DIR}/skills"/*/; do
      if [[ -d "$dir" ]]; then
        basename "$dir"
      fi
    done | sed 's/^/  /'
  else
    echo "  (none found)"
  fi
  exit 1
fi

# --- Install ---
mkdir -p "$INSTALL_DIR"
cp -r "$SKILL_SOURCE"/* "$INSTALL_DIR"/

# Make scripts executable
if [[ -d "${INSTALL_DIR}/scripts" ]]; then
  chmod +x "${INSTALL_DIR}/scripts"/*.sh 2>/dev/null || true
  chmod +x "${INSTALL_DIR}/scripts"/*.js 2>/dev/null || true
  chmod +x "${INSTALL_DIR}/scripts"/*.py 2>/dev/null || true
fi

echo ""
echo "Skill '${SKILL_NAME}' installed successfully to ${INSTALL_DIR}"
echo ""
echo "The skill will be available the next time you start Agy."
