#!/bin/bash
# Copy shared/rules.md into every skill as reference/shared-rules.md, so each
# skill folder is self-contained (claude.ai uploads one folder per skill).
# With --check, change nothing and exit 1 if a copy is missing or stale.
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
src="$root/shared/rules.md"
check=false
[ "${1:-}" = "--check" ] && check=true

stale=0
for skill in "$root"/skills/*/; do
  skill="${skill%/}"
  [ -f "$skill/SKILL.md" ] || continue
  dest="$skill/reference/shared-rules.md"
  if cmp -s "$src" "$dest"; then
    continue
  fi
  if $check; then
    echo "out of date: ${dest#"$root"/}"
    stale=1
  else
    mkdir -p "$skill/reference"
    cp "$src" "$dest"
    echo "updated: ${dest#"$root"/}"
  fi
done

if $check && [ "$stale" -ne 0 ]; then
  echo "run scripts/sync-shared.sh and commit the result"
  exit 1
fi
