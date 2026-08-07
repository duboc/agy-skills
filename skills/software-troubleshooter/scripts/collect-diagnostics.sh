#!/usr/bin/env bash
set -euo pipefail

# collect-diagnostics.sh
# Gathers project and environment context for code troubleshooting.
# Works on macOS and Linux.

echo "========================================"
echo "  Project Diagnostics Report"
echo "  Generated: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo "  Directory: $(pwd)"
echo "========================================"
echo ""

# --- Git Status ---
if command -v git &>/dev/null && git rev-parse --is-inside-work-tree &>/dev/null 2>&1; then
  echo "## Git Info"
  echo "Branch: $(git branch --show-current 2>/dev/null || echo 'detached')"
  echo "Last commit: $(git log --oneline -1 2>/dev/null || echo 'none')"
  echo ""

  echo "## Recent Commits (last 10)"
  git log --oneline -10 2>/dev/null || echo "No commits"
  echo ""

  echo "## Uncommitted Changes"
  CHANGES=$(git status --short 2>/dev/null)
  if [[ -n "$CHANGES" ]]; then
    echo "$CHANGES"
  else
    echo "Working tree clean"
  fi
  echo ""

  echo "## Recently Modified Files (last 5 commits)"
  git diff --name-only HEAD~5..HEAD 2>/dev/null || echo "Not enough history"
  echo ""
fi

# --- Project Structure ---
echo "## Project Structure (top 2 levels)"
if command -v tree &>/dev/null; then
  tree -L 2 --dirsfirst -I 'node_modules|.git|__pycache__|.venv|venv|dist|build|.next|target' 2>/dev/null || ls -la
else
  find . -maxdepth 2 -not -path './.git/*' -not -path './node_modules/*' -not -path './__pycache__/*' -not -path './.venv/*' -not -path './venv/*' -not -path './dist/*' -not -path './build/*' -not -path './.next/*' -not -path './target/*' 2>/dev/null | head -60
fi
echo ""

# --- Package Manager and Dependencies ---
echo "## Dependencies"

if [[ -f "package.json" ]]; then
  echo "Node.js project detected"
  if command -v node &>/dev/null; then
    echo "Node: $(node --version 2>&1)"
  fi
  if command -v npm &>/dev/null; then
    echo "npm: $(npm --version 2>&1)"
  fi
  if [[ -f "package-lock.json" ]]; then
    echo "Lock file: package-lock.json"
  elif [[ -f "yarn.lock" ]]; then
    echo "Lock file: yarn.lock"
  elif [[ -f "pnpm-lock.yaml" ]]; then
    echo "Lock file: pnpm-lock.yaml"
  else
    echo "Lock file: NONE (dependency versions may vary)"
  fi
fi

if [[ -f "requirements.txt" ]] || [[ -f "pyproject.toml" ]] || [[ -f "setup.py" ]]; then
  echo "Python project detected"
  if command -v python3 &>/dev/null; then
    echo "Python: $(python3 --version 2>&1)"
  elif command -v python &>/dev/null; then
    echo "Python: $(python --version 2>&1)"
  fi
  if command -v pip3 &>/dev/null; then
    echo "pip: $(pip3 --version 2>&1 | head -1)"
  fi
fi

if [[ -f "go.mod" ]]; then
  echo "Go project detected"
  if command -v go &>/dev/null; then
    echo "Go: $(go version 2>&1)"
  fi
  echo "Module: $(head -1 go.mod 2>/dev/null)"
fi

if [[ -f "Cargo.toml" ]]; then
  echo "Rust project detected"
  if command -v rustc &>/dev/null; then
    echo "Rust: $(rustc --version 2>&1)"
  fi
fi

if [[ -f "build.gradle" ]] || [[ -f "build.gradle.kts" ]] || [[ -f "pom.xml" ]]; then
  echo "Java/JVM project detected"
  if command -v java &>/dev/null; then
    echo "Java: $(java -version 2>&1 | head -1)"
  fi
fi

echo ""

# --- Config Files ---
echo "## Configuration Files Found"
for f in .env .env.local .env.production .env.development \
         tsconfig.json jsconfig.json babel.config.js webpack.config.js vite.config.ts vite.config.js \
         Dockerfile docker-compose.yml docker-compose.yaml \
         Makefile CMakeLists.txt \
         .eslintrc .eslintrc.json .prettierrc \
         pytest.ini setup.cfg tox.ini \
         .github/workflows/*.yml .github/workflows/*.yaml; do
  if [[ -e "$f" ]]; then
    echo "  $f"
  fi
done
echo ""

# --- OS and Runtime ---
echo "## System"
echo "OS: $(uname -s) $(uname -r)"
echo "Arch: $(uname -m)"
echo ""

echo "========================================"
echo "  End of Diagnostics Report"
echo "========================================"
