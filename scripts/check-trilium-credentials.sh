#!/bin/bash
# SessionStart + UserPromptSubmit hook: flags when no Trilium instance is
# configured at all, so Claude can offer to run manage-trilium-instances
# instead of the user hitting a silent/failed MCP connection. Registered on
# both events so the check also fires on the first prompt after the plugin
# is installed mid-session (plugins activate immediately, but a newly added
# MCP server only connects on the next full restart) rather than only at the
# next session start.
set -euo pipefail

input=$(cat)

claude_json_path="${CLAUDE_CONFIG_DIR:-$HOME}/.claude.json"

any_instance_configured() {
  if [ ! -f "$claude_json_path" ]; then
    return 1
  fi
  python3 -c '
import json, re, sys
try:
    with open(sys.argv[1]) as f:
        servers = json.load(f)["mcpServers"]
    ok = any(re.match(r"^trilium(_.+)?$", k) for k in servers)
except Exception:
    ok = False
sys.exit(0 if ok else 1)
' "$claude_json_path"
}

if any_instance_configured; then
  exit 0
fi

session_id=$(printf '%s' "$input" | python3 -c 'import json, sys; print(json.load(sys.stdin).get("session_id", ""))')

# UserPromptSubmit fires on every message; SessionStart and UserPromptSubmit
# both run this script. Only surface the reminder once per session (whichever
# fires first) instead of re-nagging on every prompt until an instance lands.
if [ -n "$session_id" ]; then
  marker="${TMPDIR:-/tmp}/trilium-plugin-credential-notice-${session_id}"
  if [ -e "$marker" ]; then
    exit 0
  fi
  touch "$marker"
fi

context="No Trilium instance is configured: no trilium/trilium_<label> entry exists in ${claude_json_path}'s mcpServers, so there's no MCP connection to authenticate. Proactively offer to run the trilium-plugin:manage-trilium-instances skill with the user now (collects a URL and token for a new instance and registers it via 'claude mcp add' for this installation), unless they are already mid-task on something unrelated."

printf '%s' "$input" | python3 -c '
import json, sys

hook_input = json.load(sys.stdin)
event_name = hook_input.get("hook_event_name", "SessionStart")
context = sys.argv[1]
print(json.dumps({"hookSpecificOutput": {"hookEventName": event_name, "additionalContext": context}}))
' "$context"
