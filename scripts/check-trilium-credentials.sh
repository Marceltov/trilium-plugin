#!/bin/bash
# SessionStart + UserPromptSubmit hook: flags a missing TRILIUM_ETAPI_TOKEN so
# Claude can offer to run the setup-trilium-credentials skill instead of the
# user hitting a silent/failed MCP connection. Registered on both events so
# the check also fires on the first prompt after the plugin is installed
# mid-session (plugins activate immediately, but .mcp.json only re-expands on
# the next full restart) rather than only at the next session start.
set -euo pipefail

input=$(cat)

if [ -n "${TRILIUM_ETAPI_TOKEN:-}" ]; then
  exit 0
fi

session_id=$(printf '%s' "$input" | python3 -c 'import json, sys; print(json.load(sys.stdin).get("session_id", ""))')

# UserPromptSubmit fires on every message; SessionStart and UserPromptSubmit
# both run this script. Only surface the reminder once per session (whichever
# fires first) instead of re-nagging on every prompt until credentials land.
if [ -n "$session_id" ]; then
  marker="${TMPDIR:-/tmp}/trilium-plugin-credential-notice-${session_id}"
  if [ -e "$marker" ]; then
    exit 0
  fi
  touch "$marker"
fi

settings_path="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/settings.json"

context="The trilium-plugin MCP server (\"trilium\") is not configured: TRILIUM_ETAPI_TOKEN is not set, so its .mcp.json cannot authenticate. Proactively offer to run the trilium-plugin:setup-trilium-credentials skill with the user now (collects TRILIUM_MCP_URL and TRILIUM_ETAPI_TOKEN, persists them to this installation's own settings.json at ${settings_path}), unless they are already mid-task on something unrelated."

printf '%s' "$input" | python3 -c '
import json, sys

hook_input = json.load(sys.stdin)
event_name = hook_input.get("hook_event_name", "SessionStart")
context = sys.argv[1]
print(json.dumps({"hookSpecificOutput": {"hookEventName": event_name, "additionalContext": context}}))
' "$context"
