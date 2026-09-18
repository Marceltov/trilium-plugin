#!/bin/bash
# Manual self-check for check-trilium-credentials.sh's instance-detection
# logic. No framework: run `bash scripts/test-check-trilium-credentials.sh`.
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
hook="$script_dir/check-trilium-credentials.sh"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp" "${TMPDIR:-/tmp}"/trilium-plugin-credential-notice-selftest-*' EXIT

fail=0
export CLAUDE_CONFIG_DIR="$tmp"

check() {
  local desc="$1" expected_exit="$2" expect_context="$3" session="$4"
  local status=0 output
  output=$(printf '{"session_id":"%s","hook_event_name":"SessionStart"}' "$session" | "$hook") || status=$?
  if [ "$status" != "$expected_exit" ]; then
    echo "FAIL ($desc): expected exit $expected_exit, got $status"
    fail=1
    return
  fi
  case "$expect_context" in
    yes)
      [[ "$output" == *additionalContext* ]] || { echo "FAIL ($desc): expected additionalContext, got: $output"; fail=1; return; }
      ;;
    no)
      [ -z "$output" ] || { echo "FAIL ($desc): expected no output, got: $output"; fail=1; return; }
      ;;
  esac
  echo "ok ($desc)"
}

echo '{}' > "$tmp/settings.json"
export TRILIUM_ETAPI_TOKEN=x
check "default env var set" 0 no "selftest-1"
unset TRILIUM_ETAPI_TOKEN

check "nothing configured" 0 yes "selftest-2"

cat > "$tmp/settings.json" <<'JSON'
{"mcpServers": {"trilium_work": {"type": "http", "url": "https://work.example/mcp"}}}
JSON
check "labeled instance configured" 0 no "selftest-3"

echo 'not json' > "$tmp/settings.json"
check "malformed settings.json falls back to nudge" 0 yes "selftest-4"

if [ "$fail" -ne 0 ]; then
  echo "SOME TESTS FAILED"
  exit 1
fi
echo "all tests passed"
