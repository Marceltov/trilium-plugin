#!/bin/bash
# SessionStart + UserPromptSubmit hook: flags when no Trilium instance is
# configured at all, so Claude can offer to run manage-trilium-instances
# instead of the user hitting a silent/failed MCP connection. Registered on
# both events so the check also fires on the first prompt after the plugin
# is installed mid-session (plugins activate immediately, but .mcp.json only
# re-expands on the next full restart) rather than only at the next session
# start.
set -euo pipefail

input=$(cat)

settings_path="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/settings.json"

any_instance_configured() {
  if [ -n "${TRILIUM_ETAPI_TOKEN:-}" ]; then
    return 0
  fi
  if [ ! -f "$settings_path" ]; then
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
' "$settings_path"
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

context="No Trilium instance is configured: neither TRILIUM_ETAPI_TOKEN nor any trilium/trilium_<label> entry in mcpServers is set, so no MCP connection can authenticate. Proactively offer to run the trilium-plugin:manage-trilium-instances skill with the user now (collects a URL and token for a new instance, persists them to this installation's own settings.json at ${settings_path}), unless they are already mid-task on something unrelated."

printf '%s' "$input" | python3 -c '
import json, sys

hook_input = json.load(sys.stdin)
event_name = hook_input.get("hook_event_name", "SessionStart")
context = sys.argv[1]
print(json.dumps({"hookSpecificOutput": {"hookEventName": event_name, "additionalContext": context}}))
' "$context"
