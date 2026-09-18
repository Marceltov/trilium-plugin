---
name: manage-trilium-instances
description: Configure connections to one or more trilium-mcp deployments — add a new instance (URL + ETAPI token, optionally labeled), list which are configured/connected, or remove one — persisting to the running Claude Code installation's own settings.json (respects CLAUDE_CONFIG_DIR, so each install can be configured separately). Use when the trilium MCP server is unconfigured, disconnected, or missing credentials (including when a SessionStart hook flags this), when the user asks to set up, configure, or connect the Trilium plugin, or when they want to add, remove, or list additional Trilium instances.
---

# Manage Trilium Instances

This plugin's `.mcp.json` connects to a default `trilium` MCP server via two environment variables, expanded at Claude Code startup: `TRILIUM_MCP_URL` (defaults to `http://localhost:8081/mcp`) and `TRILIUM_ETAPI_TOKEN` (no default; without it the connection fails). Each *additional* Trilium instance is its own separately-named MCP server, `trilium_<label>`, backed by its own env vars `TRILIUM_<LABEL>_URL` / `TRILIUM_<LABEL>_TOKEN`, added to the same settings.json. Claude Code exposes each server's tools under its own prefix (`mcp__trilium__*`, `mcp__trilium_work__*`, …); skills resolve which prefix to use per task — see [Working with multiple instances](../README.md#working-with-multiple-instances).

Claude Code has no built-in prompt for missing `.mcp.json` env vars or for adding new MCP servers, so this skill collects everything conversationally and writes it to the **user-level settings.json of the currently running Claude Code installation** — its `env` and `mcpServers` blocks, which Claude Code reads on every future launch of *that same installation*. No manual `export` or manual JSON editing needed.

**This is not always `~/.claude/settings.json`.** A user may run several separate Claude Code installations (e.g. a personal one and a work one), each pointed at its own config directory via the `CLAUDE_CONFIG_DIR` environment variable, defaulting to `~/.claude` when unset. Resolve the correct path for *this* running instance — don't hardcode `~/.claude`, using a command equivalent to:

    echo "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/settings.json"

## Determine the operation

Figure out from the request whether the user wants to **add** a new instance, **list** what's configured, or **remove** one. Default to **add** when the trigger is a missing-credentials nudge and the user hasn't said otherwise.

## Add an instance

1. **Check whether the default instance is already configured before asking anything**, if this is meant to be the first/default instance. Two independent signals both indicate it's already in place:
   - The `mcp__trilium__*` tools are already listed as available in *this* session (see the system-reminder of connected MCP tools) — this proves the token in use right now is valid.
   - Resolve the settings file path (command above) and read it: if `env.TRILIUM_ETAPI_TOKEN` is already a non-empty string, it was persisted by a previous run of this skill.

   If either signal is true, **stop here** — report that it's already configured (naming the settings.json path, never the token value) and finish. Only continue if the user explicitly wants an *additional* instance, or neither signal is true.

2. **If this is an additional instance (not the first), ask for a label** — a short name like `work` or `home`. Sanitize it: lowercase, replace every run of characters outside `[a-z0-9_]` with `_`, strip leading/trailing `_`. If the result is empty, collides with `trilium` or a label already present in `mcpServers` (read the settings file to check), or if the resulting `TRILIUM_<LABEL>_URL`/`TRILIUM_<LABEL>_TOKEN` names already exist in `env` (this specifically rules out the labels `mcp` and `etapi`, which would collide with the default instance's env vars), ask for a different one — never silently overwrite an existing instance.

   Skip this step entirely for the first/default instance — it always stays unlabeled (server name `trilium`, env vars `TRILIUM_MCP_URL`/`TRILIUM_ETAPI_TOKEN`).

3. **Ask for the remaining values**, one at a time (plain question or `AskUserQuestion` if available):
   - The instance's MCP URL. For the default instance, mention it defaults to `http://localhost:8081/mcp` and can be skipped. For a labeled instance, there is no default — required.
   - Its ETAPI token, created from that Trilium instance's *Options → ETAPI* screen. Required, no default.
   - Never print the token back in a confirmation message or log it.

4. **Resolve the settings file path** (reuse the read from step 1 if already done) and merge in:
   - Default instance: `env.TRILIUM_MCP_URL` (only if given a non-default value, or already present) and `env.TRILIUM_ETAPI_TOKEN`.
   - Labeled instance (label `foo`): `env.TRILIUM_FOO_URL`, `env.TRILIUM_FOO_TOKEN`, and an `mcpServers.trilium_foo` entry equivalent to:

         {
           "type": "http",
           "url": "${TRILIUM_FOO_URL}",
           "headers": { "Authorization": "${TRILIUM_FOO_TOKEN}" }
         }

   Preserve every other key already in the file, in `env`, and in `mcpServers`. It's strict JSON (no comments, no trailing commas) — parse it properly, don't regex-edit it.

5. **Write the file back** as valid JSON.

6. **Tell the user to restart Claude Code** (or start a new session) — `${VAR}` expansion in `mcpServers`/`env` happens once at startup, so this change will not take effect in the current session.

7. **If working inside the `trilium-plugin` repo itself** (or any project where a server previously failed to connect), check that project's `.claude/settings.local.json` for a `disabledMcpjsonServers` array containing the server's name — Claude Code disables a server there after a connection failure, so it may need to be removed for the server to reconnect after restart.

## List instances

1. Resolve and read the settings file. Collect every `mcpServers` key matching `trilium(_.+)?` (a literal `trilium`, plus any `trilium_<label>`).
2. Cross-reference against the `mcp__trilium(_.+)?__*` tool prefixes actually present in *this* session (from the system-reminder of connected MCP tools) to mark each as connected or configured-but-not-connected (e.g. added since the last restart).
3. Report the list: label (or "default" for `trilium`), and connected/not-connected. Never print token values.

## Remove an instance

1. Ask which instance (by label, or "default" for `trilium`) if not already clear.
2. Resolve and read the settings file. Delete the matching `mcpServers.trilium_<label>` entry (or, for the default, `mcpServers.trilium` if present) and its corresponding `env` keys.
3. Write the file back.
4. Tell the user to restart Claude Code for the removal to take effect.
