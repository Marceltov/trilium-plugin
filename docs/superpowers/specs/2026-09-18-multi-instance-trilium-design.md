# Multi-instance Trilium support

## Problem

The plugin connects to exactly one Trilium instance. `.mcp.json` declares a single MCP server named `trilium`, whose URL and token come from `TRILIUM_MCP_URL` / `TRILIUM_ETAPI_TOKEN`, expanded once at Claude Code startup. Every skill calls tools under the fixed `mcp__trilium__*` prefix. A user with several Trilium instances (e.g. home and work, each with its own already-running `trilium-mcp` sidecar at its own URL) has no way to work with more than one in a session.

## Goals

- Work with two or more Trilium instances in the same conversation (not just switch which one a session targets).
- Support an open-ended, growing number of instances — no hardcoded slot limit.
- No new service to build or deploy; reuse Claude Code's native multi-MCP-server support.
- Zero change in behavior for today's single-instance users.

## Non-goals

- Live/hot-adding an instance mid-session without a restart. Claude Code expands `${VAR}` references in `mcpServers` only at startup; this is a hard platform constraint, not something this plugin can work around.
- Building a proxy/aggregator MCP server that multiplexes instances behind one tool namespace (rejected approach, see below).
- Managing or discovering `trilium-mcp` sidecars themselves — this plugin only connects to already-running ones.

## Rejected approach: proxy MCP server

An aggregator server taking an `instance` argument per call, dispatching to the right upstream `trilium-mcp`, would give one stable tool namespace regardless of instance count. Rejected because it requires building, deploying, and maintaining a new service just to avoid something Claude Code already does natively (connecting to N named MCP servers at once). Adds real operational surface for no capability gain over the chosen approach.

## Chosen approach: one named MCP server per instance

Claude Code connects to every server listed in `mcpServers` (merged from `.mcp.json` and the user's `settings.json`) and namespaces each server's tools as `mcp__<serverName>__<tool>`. Each Trilium instance becomes its own named server entry; skills pick the right prefix per task based on conversation context.

### Naming convention

- The default instance keeps the existing server name `trilium` and existing env vars `TRILIUM_MCP_URL` / `TRILIUM_ETAPI_TOKEN` — unchanged from today, so nothing breaks for single-instance users.
- Each additional instance gets a user-chosen label, sanitized to `[a-z0-9_]+` (lowercased, non-matching characters stripped/replaced with `_`). This produces:
  - Server name: `trilium_<label>` (e.g. `trilium_work`)
  - Env vars: `TRILIUM_<LABEL>_URL` / `TRILIUM_<LABEL>_TOKEN` (e.g. `TRILIUM_WORK_URL`)

### Where configuration lives

New instance entries are written to the *user-level* `settings.json` (`$CLAUDE_CONFIG_DIR/settings.json`, defaulting to `~/.claude/settings.json`) — never to this plugin's own `.mcp.json`, which is shared/versioned and can't hold anyone's personal instance list or secrets. This mirrors exactly what `setup-trilium-credentials` already does for the default instance's env vars today; it's extended to also write an `mcpServers` entry per instance.

Example, after adding a `work` instance:

```json
{
  "env": {
    "TRILIUM_WORK_URL": "https://work.example/mcp",
    "TRILIUM_WORK_TOKEN": "abc123"
  },
  "mcpServers": {
    "trilium_work": {
      "type": "http",
      "url": "${TRILIUM_WORK_URL}",
      "headers": { "Authorization": "${TRILIUM_WORK_TOKEN}" }
    }
  }
}
```

No separate registry/manifest file is needed — the `mcpServers` keys in `settings.json` matching `trilium(_.+)?` *are* the list of configured instances, and the currently-connected subset is directly observable each session as the set of `mcp__trilium(_.+)?__*` tool prefixes present.

### Component: `manage-trilium-instances` skill (replaces `setup-trilium-credentials`)

Extends the existing credential-setup skill with add/list/remove for named instances, keeping its existing default-instance behavior intact:

- **Add**: ask for a label (skip for the first/default instance — it stays unlabeled `trilium`), URL, and token; sanitize the label; if the sanitized label is empty, or collides with `trilium` or an already-configured label, ask for a different one instead of silently overwriting; write the env vars and `mcpServers` entry into `settings.json`; tell the user to restart Claude Code for it to take effect.
- **List**: read `settings.json`'s `mcpServers` keys matching `trilium(_.+)?`, cross-reference against the `mcp__trilium(_.+)?__*` prefixes actually present in the current session to show configured-vs-connected status.
- **Remove**: delete the matching `mcpServers` entry and its env vars from `settings.json`; tell the user to restart.

Same duplicate-detection and "never print the token back" rules as today's skill apply per-instance.

### Component: instance resolution shared by all note-operation skills

A single "Working with multiple instances" section is added to `skills/README.md`, referenced by a one-line pointer from every note-operation skill (`create-note`, `delete-note`, `move-note`, `rename-note`, `search-notes`, `manage-note-attributes`, `journal-note`, `export-note-subtree`, `create-note-from-template`, `apply-template-to-note`, `find-template-instances`) instead of duplicating the logic in each file. Each skill's own MCP tool references change from the literal `mcp__trilium__<tool>` to "the resolved instance's `mcp__trilium(_.+)?__<tool>`".

Resolution logic (followed by Claude at skill-invocation time — this is prose instruction, not code):

1. Note which `mcp__trilium(_.+)?__*` prefixes are actually available this session.
2. Exactly one exists → use it, no question asked (today's behavior, unchanged).
3. More than one exists → check whether the user already named an instance in the conversation (by label or by something identifying, e.g. "the work one") and match it to the corresponding prefix.
4. Still ambiguous → ask once which instance, listing the available labels.
5. Use that single resolved prefix for every MCP tool call for the remainder of the current operation.

### Component: `hooks/check-trilium-credentials.sh`

Currently only checks `TRILIUM_ETAPI_TOKEN`. Changes to: pass (exit 0, no nudge) if that default var is set, **or** `settings.json` has any `mcpServers` key matching `trilium(_.+)?`. Only nudge the user to run `manage-trilium-instances` when zero instances are configured at all.

### Component: README

Document adding additional instances via `manage-trilium-instances`, and describe the instance-resolution behavior (ask-when-ambiguous) so users understand why they might get asked "which instance?" mid-task.

## Testing

No test framework in this repo (skills are markdown instructions, hook is a shell script). Verification is manual:

- Hook script: run it with 0, 1 (default only), and 2+ (`trilium(_.+)?`) instances configured in a scratch `settings.json`, confirm exit code / nudge behavior matches each case.
- Skill instructions: manually walk through `manage-trilium-instances` add/list/remove against a scratch `settings.json` copy, confirm correct JSON merge (existing keys preserved) and correct sanitization of a messy label (e.g. `"Home Office!"` → `home_office`).
- End-to-end: with two real/stubbed `trilium-mcp` endpoints configured, ask a note-operation skill to act "on the work one" and confirm it resolves to `mcp__trilium_work__*` calls; ask again with no instance named while 2 are connected and confirm it asks.

## Rollout / compatibility

Single-instance users are unaffected: the default `trilium` server name and env vars are untouched, and skills fall through to "exactly one prefix, use it" with no new question ever surfacing. Multi-instance behavior only activates once a second instance is actually configured and connected.
