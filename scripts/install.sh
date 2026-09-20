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

Available skills (28):
  adk-developer                 Build agents with Google's ADK (Python, Java, Go, TS)
  agent-engine-deploy           Deploy ADK agents on Vertex AI Agent Engine
  agent-engine-ops              Monitor, trace, secure, and evaluate Agent Engine agents
  agent-engine-sessions-memory  Manage sessions and memory for Agent Engine agents
  ai-studio-architect           Convert AI Studio prototypes to production on GCP
  app-security-audit            Google Cloud, GenAI/Gemini, BFF proxy, CGNAT & 8h+ kiosk security audit
  clarity-presenter             Marp decks with SCQA narrative + assertion-evidence design
  cloud-architecture-diagram    Draw a deployed system as a Google Cloud reference architecture
  design-critique               Evaluate UI/UX designs and frontend code for usability & WCAG accessibility
  design-system-management      Architect design tokens, component APIs, and design system governance
  developer-growth-analysis     Analyze Agy session history for engineering growth patterns
  documentation                 Write READMEs, API references, ADRs, and runbooks per Google Developer style
  feature-spec                  Write engineering-ready PRDs, INVEST stories, Given/When/Then criteria & MoSCoW scope
  gdoc-engineering-spec         Build Pageless, multi-tab Google Docs engineering specs, RFCs & runbooks
  google-ads-funnel             Funnel-as-Code workflows for Google Ads account audits and diagnostics
  html-to-pptx                  Convert Marp HTML slides to editable native PowerPoint (.pptx)
  research-skill-graph-agy      Investigate questions through 6 analytical lenses in a local .research/ graph
  software-troubleshooter       Structured code inspection and root-cause troubleshooting
  spring-boot-upgrader          Migrate Spring Boot apps to 4.0 with phased upgrade plans
  system-design                 Design distributed systems and APIs with explicit trade-off analysis
  technical-drawing             Create precise, dimensioned orthographic technical drawings in SVG
  using-git-worktrees           Create isolated Git worktrees with safety checks and baseline tests
  ux-copywriter                 Write clear, accessible UI microcopy and recovery-oriented error messages
  visual-explainer              Generate self-contained interactive HTML explainers for systems and diffs
  webapp-testing                Test local web apps with Playwright, console capture, and DOM snapshots
  writing-plans                 Generate atomic, test-driven implementation plans
  zen-pitch                     Research a domain, build a requirements spine, and compile a Presentation Zen deck
  zen-presenter                 Marp slide decks following Presentation Zen principles
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

if [[ ! "$SKILL_NAME" =~ ^[a-z0-9-]+$ ]]; then
  echo "Error: Invalid skill name '${SKILL_NAME}'. Only lowercase alphanumeric and hyphens allowed." >&2
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
umask 077
TMPDIR_PATH=$(mktemp -d)
chmod 700 "$TMPDIR_PATH"
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
