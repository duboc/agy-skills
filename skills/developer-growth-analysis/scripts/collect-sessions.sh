#!/usr/bin/env bash
# collect-sessions.sh — Aggregates Gemini CLI session data within a time window
#
# Usage: collect-sessions.sh [HOURS]
#   HOURS: lookback window in hours (default: 48)
#
# Output: JSON summary of sessions to stdout
# Requires: bash 4+, python3 (for JSON parsing and timestamp math)

set -euo pipefail

HOURS="${1:-48}"
GEMINI_DIR="${HOME}/.gemini"
TMP_DIR="${GEMINI_DIR}/tmp"
PROJECTS_FILE="${GEMINI_DIR}/projects.json"

if [[ ! -d "$TMP_DIR" ]]; then
  echo '{"error": "Gemini CLI tmp directory not found at '"${TMP_DIR}"'"}' >&2
  exit 1
fi

# Use python3 for reliable cross-platform timestamp handling and JSON parsing
python3 - "$TMP_DIR" "$PROJECTS_FILE" "$HOURS" << 'PYEOF'
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

tmp_dir = Path(sys.argv[1])
projects_file = Path(sys.argv[2])
hours = int(sys.argv[3])

cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)

# Load project name mappings (path -> name)
project_names = {}
if projects_file.exists():
    try:
        with open(projects_file) as f:
            data = json.load(f)
            # projects.json maps path -> name
            project_names = data.get("projects", {})
    except (json.JSONDecodeError, KeyError):
        pass

# Reverse mapping: hash-dir-name -> project name
# Some dirs use the project name directly, others use hashes
hash_to_name = {}
for path, name in project_names.items():
    hash_to_name[name] = name

results = {
    "cutoff": cutoff.isoformat(),
    "hours": hours,
    "projects": {},
    "sessions": [],
    "summary": {
        "total_sessions": 0,
        "total_user_messages": 0,
        "total_gemini_messages": 0,
        "total_tool_calls": 0,
        "projects_active": 0,
    }
}

for project_dir in sorted(tmp_dir.iterdir()):
    if not project_dir.is_dir():
        continue

    chats_dir = project_dir / "chats"
    if not chats_dir.exists():
        continue

    dir_name = project_dir.name
    project_label = hash_to_name.get(dir_name, dir_name)

    for session_file in sorted(chats_dir.glob("session-*.json")):
        try:
            with open(session_file) as f:
                session = json.load(f)
        except (json.JSONDecodeError, IOError):
            continue

        last_updated = session.get("lastUpdated", "")
        if not last_updated:
            continue

        try:
            session_time = datetime.fromisoformat(last_updated.replace("Z", "+00:00"))
        except ValueError:
            continue

        if session_time < cutoff:
            continue

        # Extract session summary
        messages = session.get("messages", [])
        user_messages = []
        gemini_messages = []
        tool_calls = []
        models_used = set()

        for msg in messages:
            msg_type = msg.get("type", "")
            content = msg.get("content", "")

            if msg_type == "user":
                user_messages.append(content)
            elif msg_type == "gemini":
                gemini_messages.append(content)
                model = msg.get("model", "")
                if model:
                    models_used.add(model)

                for tc in msg.get("toolCalls", []):
                    tool_info = {
                        "name": tc.get("name", ""),
                        "description": tc.get("description", ""),
                        "status": tc.get("status", ""),
                    }
                    args = tc.get("args", {})
                    if isinstance(args, dict):
                        # Include command if it's a shell call
                        if "command" in args:
                            tool_info["command"] = args["command"]
                        if "description" in args:
                            tool_info["tool_description"] = args["description"]
                    tool_calls.append(tool_info)

        # Calculate token totals
        total_tokens = 0
        for msg in messages:
            tokens = msg.get("tokens", {})
            total_tokens += tokens.get("total", 0)

        session_summary = {
            "session_id": session.get("sessionId", ""),
            "project_dir": dir_name,
            "project_name": project_label,
            "start_time": session.get("startTime", ""),
            "last_updated": last_updated,
            "user_messages": user_messages,
            "user_message_count": len(user_messages),
            "gemini_message_count": len(gemini_messages),
            "tool_call_count": len(tool_calls),
            "tool_calls": tool_calls,
            "models_used": list(models_used),
            "total_tokens": total_tokens,
        }

        results["sessions"].append(session_summary)
        results["summary"]["total_sessions"] += 1
        results["summary"]["total_user_messages"] += len(user_messages)
        results["summary"]["total_gemini_messages"] += len(gemini_messages)
        results["summary"]["total_tool_calls"] += len(tool_calls)

        if project_label not in results["projects"]:
            results["projects"][project_label] = {
                "session_count": 0,
                "total_user_messages": 0,
            }
        results["projects"][project_label]["session_count"] += 1
        results["projects"][project_label]["total_user_messages"] += len(user_messages)

results["summary"]["projects_active"] = len(results["projects"])

# Sort sessions by start time
results["sessions"].sort(key=lambda s: s.get("start_time", ""))

print(json.dumps(results, indent=2, ensure_ascii=False))
PYEOF
