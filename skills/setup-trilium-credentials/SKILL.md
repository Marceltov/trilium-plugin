---
name: setup-trilium-credentials
description: Configure the connection to a trilium-mcp deployment by asking the user for their TRILIUM_MCP_URL and TRILIUM_ETAPI_TOKEN and persisting them to the running Claude Code installation's own settings.json (respects CLAUDE_CONFIG_DIR, so each install can be configured separately). Use when the trilium MCP server is unconfigured, disconnected, or missing credentials (including when a SessionStart hook flags this), or when the user asks to set up, configure, or connect the Trilium plugin.
---

# Setup Trilium Credentials

This plugin's `.mcp.json` connects to a `trilium-mcp` server via two environment
variables, expanded at Claude Code startup:

- `TRILIUM_MCP_URL` — the server's URL. Defaults to `http://localhost:8081/mcp`
  if unset.
- `TRILIUM_ETAPI_TOKEN` — the auth token, sent as the `Authorization` header.
  No default; without it, the MCP connection fails.

Claude Code has no built-in prompt for missing `.mcp.json` env vars, so this
skill collects them conversationally and writes them to the **user-level
settings.json of the currently running Claude Code installation** — its
`env` block, which Claude Code reads as ordinary environment variables on
every future launch of *that same installation* — no manual `export` needed
again.

**This is not always `~/.claude/settings.json`.** A user may run several
separate Claude Code installations (e.g. a personal one and a work one),
each pointed at its own config directory via the `CLAUDE_CONFIG_DIR`
environment variable, defaulting to `~/.claude` when unset. Resolve the
correct path for *this* running instance — don't hardcode `~/.claude`:

```bash
echo "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/settings.json"
```

Since the current process inherits this installation's environment, this
always resolves to the config dir of the install the user is actually
talking to right now, so credentials land in the right place even when they
have multiple installs and want each configured separately.

## Steps

1. **Ask for the values**, one at a time (plain question or `AskUserQuestion`
   if available):
   - `TRILIUM_MCP_URL` — the URL of their running `trilium-mcp` deployment.
     Mention the default (`http://localhost:8081/mcp`) and that they can skip
     this one if that default is correct.
   - `TRILIUM_ETAPI_TOKEN` — their ETAPI token, created from Trilium's
     *Options → ETAPI* screen. Required, no default.
   - Never print the token back in a confirmation message or log it.

2. **Resolve the settings file path** with the command above, then read it.
   If it doesn't exist, start from `{}`. It's strict JSON (no comments, no
   trailing commas) — parse it properly, don't regex-edit it.

3. **Merge into the `env` object**, preserving every other key already in the
   file and every other key already in `env`:
   ```json
   {
     "env": {
       "TRILIUM_MCP_URL": "<value or default>",
       "TRILIUM_ETAPI_TOKEN": "<value>"
     }
   }
   ```
   Only write `TRILIUM_MCP_URL` if the user gave a non-default value, or if a
   value already exists there — no need to pin the default explicitly.

4. **Write the file back** as valid JSON.

5. **Tell the user to restart Claude Code** (or start a new session). The
   `.mcp.json` `${VAR}` expansion happens once at startup, so this change
   will not take effect in the current session.

6. **If working inside the `trilium-plugin` repo itself** (or any project
   where the server previously failed to connect), check that project's
   `.claude/settings.local.json` for a `disabledMcpjsonServers` array
   containing `"trilium"` — Claude Code disables a server there after a
   connection failure, so it may need to be removed for the server to
   reconnect after restart.
