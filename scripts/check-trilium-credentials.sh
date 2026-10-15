#!/bin/bash
# SessionStart hook: flags when no Trilium instance is configured at all, so
# Claude can offer to run manage-trilium-instances instead of the user
# hitting a silent/failed MCP connection.
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
    ok = any(re.match(r"^trilium([-_].+)?$", k) for k in servers)
except Exception:
    ok = False
sys.exit(0 if ok else 1)
' "$claude_json_path"
}

if any_instance_configured; then
  exit 0
fi

# Offer setup once per installation, not every session. After the first
# offer the user knows the skill exists; people who connect another way (a
# claude.ai connector, which this check can't see) or decline aren't asked
# again. The skill stays available whenever the user asks for it.
state_dir="${CLAUDE_PLUGIN_DATA:-${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugin-data/trilium-plugin}"
marker="$state_dir/setup-offered"
if [ -e "$marker" ]; then
  exit 0
fi
mkdir -p "$state_dir" 2>/dev/null && touch "$marker" 2>/dev/null || true

context="No Trilium Notes instance is configured: no trilium/trilium-<label> entry exists in ${claude_json_path}'s mcpServers, so there's no MCP connection to authenticate. Proactively offer to run the trilium:trilium-manage-instances skill with the user now (collects the Trilium Notes MCP server URL and an ETAPI token for a new instance and registers it via 'claude mcp add' for this installation), unless they are already mid-task on something unrelated. This offer is made only once per installation; if the user declines or already reaches it another way (for example a claude.ai connector), drop it."

printf '%s' "$input" | python3 -c '
import json, sys

hook_input = json.load(sys.stdin)
event_name = hook_input.get("hook_event_name", "SessionStart")
context = sys.argv[1]
print(json.dumps({"hookSpecificOutput": {"hookEventName": event_name, "additionalContext": context}}))
' "$context"
