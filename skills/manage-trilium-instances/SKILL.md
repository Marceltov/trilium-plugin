---
name: manage-trilium-instances
description: Configure connections to one or more trilium-mcp deployments — add a new instance (URL + ETAPI token, optionally labeled), list which are configured/connected, or remove one. Every instance is registered as a user-scoped MCP server via `claude mcp add` (no settings.json editing, no bundled .mcp.json). Use when the trilium MCP server is unconfigured, disconnected, or missing credentials (including when a SessionStart hook flags this), when the user asks to set up, configure, or connect the Trilium plugin, or when they want to add, remove, or list additional Trilium instances.
---

# Manage Trilium Instances

Every Trilium instance — including the first/default one — is its own MCP server registered with the `claude mcp add` CLI command, scoped `user` so it's available to every project under the current Claude Code installation. The default instance is named `trilium`; each additional one is `trilium_<label>` (e.g. `trilium_work`). Claude Code exposes each server's tools under its own prefix (`mcp__trilium__*`, `mcp__trilium_work__*`, …); skills resolve which prefix to use per task — see [Working with multiple instances](../README.md#working-with-multiple-instances).

**Do not write to settings.json, and don't rely on a bundled `.mcp.json`.** Earlier versions of this plugin shipped a project-scoped `.mcp.json` for the default instance (env-var driven) and had this skill write an `mcpServers` block into settings.json for additional ones — settings.json rejects a top-level `mcpServers` key outright (schema validation error: "Unrecognized field: mcpServers"), so that never actually worked for additional instances, and the bundled `.mcp.json` has been removed. Every instance now goes through `claude mcp add`/`list`/`get`/`remove`, which persist to that installation's own MCP config independently of settings.json — no manual JSON editing, and no need to resolve `CLAUDE_CONFIG_DIR` by hand.

## Determine the operation

Figure out from the request whether the user wants to **add** a new instance, **list** what's configured, or **remove** one. Default to **add** when the trigger is a missing-credentials nudge and the user hasn't said otherwise.

## Add an instance

1. **Check whether the default instance is already configured before asking anything**, if this is meant to be the first/default instance. Two independent signals both indicate it's already in place:
   - The `mcp__trilium__*` tools are already listed as available in *this* session (see the system-reminder of connected MCP tools) — this proves the current registration is valid and connected.
   - Run `claude mcp get trilium` — exit code 0 means it's already registered (the output includes its scope and live connection status; never print the token, which the `get` output doesn't show anyway).

   If either signal is true, **stop here** — report that it's already configured (naming the scope from `claude mcp get`'s output, e.g. "user config") and finish. Only continue if the user explicitly wants an *additional* instance, or neither signal is true.

2. **If this is an additional instance (not the first), ask for a label** — a short name like `work` or `home`. Sanitize it: lowercase, replace every run of characters outside `[a-z0-9_]` with `_`, strip leading/trailing `_`. If the result is empty, ask for a different one. Then run `claude mcp get trilium_<label>` — exit 0 means that name is already taken (its error output for a *miss* conveniently lists every configured server too, useful for suggesting a free label) — ask for a different label rather than silently overwriting an existing instance.

   Skip this step entirely for the first/default instance — it always stays unlabeled (server name `trilium`).

3. **Ask for the remaining values**, one at a time (plain question or `AskUserQuestion` if available):
   - The instance's MCP URL. For the default instance, `http://localhost:8081/mcp` is a common value for a local dev `trilium-mcp` stack — offer it as a suggestion, but there's no automatic fallback anymore, so still ask. For a labeled instance, there's no natural default — just ask.
   - Its ETAPI token, created from that Trilium instance's *Options → ETAPI* screen. Required, no default.
   - Never print the token back in a confirmation message or log it.

4. **Register the instance** by running:

       claude mcp add --transport http <name> "<url>" -H "Authorization: <token>" -s user

   where `<name>` is `trilium` for the default instance or `trilium_<label>` for an additional one. `-s user` makes it available to every project under this installation. The token appears in this command's arguments (visible in the tool call, and briefly in process listings while it runs) — there's no CLI option to supply it another way; don't additionally print or log it anywhere else.

5. **Tell the user to restart Claude Code** (or start a new session) — a newly `claude mcp add`-ed server only connects into the current session's tool list after a restart.

## List instances

1. Run `claude mcp list` — it health-checks every configured server fresh, including ones just added this session, and works regardless of what's already loaded into the current session's tool list.
2. From its output, keep only lines whose server name matches `trilium(_.+)?` (a literal `trilium`, plus any `trilium_<label>`). Each line ends with a connection status (e.g. "✔ Connected" or "✘ Failed to connect — ...").
3. Report the list: label (or "default" for `trilium`), and connected/not-connected per that status. Never print token values.

## Remove an instance

1. Ask which instance (by label, or "default" for `trilium`) if not already clear.
2. Run `claude mcp remove trilium` for the default, or `claude mcp remove trilium_<label>` for an additional one (no `-s` needed — it removes from whichever scope it's registered in).
3. Tell the user to restart Claude Code for the removal to take effect.
