#!/bin/bash
# SessionStart hook: flags a missing TRILIUM_ETAPI_TOKEN so Claude can offer
# to run the setup-trilium-credentials skill instead of the user hitting a
# silent/failed MCP connection.
set -euo pipefail

# Drain the hook's stdin JSON input (session_id, cwd, ...); unused here.
cat >/dev/null

if [ -n "${TRILIUM_ETAPI_TOKEN:-}" ]; then
  exit 0
fi

settings_path="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/settings.json"

context="The trilium-plugin MCP server (\"trilium\") is not configured: TRILIUM_ETAPI_TOKEN is not set, so its .mcp.json cannot authenticate. Proactively offer to run the trilium-plugin:setup-trilium-credentials skill with the user now (collects TRILIUM_MCP_URL and TRILIUM_ETAPI_TOKEN, persists them to this installation's own settings.json at ${settings_path}), unless they are already mid-task on something unrelated."

json_context=$(printf '%s' "$context" | python3 -c 'import json, sys; print(json.dumps(sys.stdin.read()))')

printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":%s}}\n' "$json_context"
