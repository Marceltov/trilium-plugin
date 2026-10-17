---
name: trilium-manage-instances
description: Configure connections to one or more Trilium Notes MCP server deployments — add a new instance (URL, signed in with OAuth or, as a fallback, an ETAPI token; optionally labeled), list which are configured/connected, or remove one. Every instance is registered as a user-scoped MCP server via `claude mcp add` (no settings.json editing, no bundled .mcp.json). Use when the trilium MCP server is unconfigured, disconnected, or missing credentials (including when a SessionStart hook flags this), when the user asks to set up, configure, or connect the Trilium Notes plugin, or when they want to add, remove, or list additional Trilium Notes instances.
---

# Manage Trilium Notes Instances

Every Trilium Notes instance — including the first/default one — is its own MCP server registered with the `claude mcp add` CLI command, scoped `user` so it's available to every project under the current Claude Code installation. The default instance is named `trilium`; each additional one is `trilium-<label>` (e.g. `trilium-work`), the naming the Trilium Notes MCP server docs use too. Instances registered earlier as `trilium_<label>` still count. Claude Code exposes each server's tools under its own prefix (`mcp__trilium__*`, `mcp__trilium-work__*`, …); skills resolve which prefix to use per task — see [Working with multiple instances](reference/shared-rules.md#working-with-multiple-instances).

**This skill is the only way instances get configured.** Go through `claude mcp add`/`list`/`get`/`remove` only. Never write an `mcpServers` block into settings.json (it rejects the key) and never create a `.mcp.json`.

## On claude.ai, the desktop app or Cowork

There is no `claude` CLI there; a Trilium Notes MCP server is connected as a **custom connector** instead. If Trilium Notes tools are already available, say so and stop. Otherwise explain the steps, with the Trilium Notes MCP server's public HTTPS URL ending in `/mcp`:

1. The server needs OAuth enabled (`MCP_BASE_URL` and `MCP_OAUTH_SECRET` set); claude.ai can't send a token header.
2. *Customize → Connectors → Add custom connector*: a name (for example `Trilium Notes`) and the URL, keep the detected OAuth choices, then sign in with the Trilium Notes password.
3. Switch the connector on in the chat (**+ → Connectors**).

Details: https://trilium-mcp.marceltov.de/claude-ai/. Everything below applies to Claude Code only.

## Determine the operation

Figure out from the request whether the user wants to **add** a new instance, **list** what's configured, or **remove** one. Default to **add** when the trigger is a missing-credentials nudge and the user hasn't said otherwise.

## Add an instance

1. **Check whether the default instance is already configured before asking anything**, if this is meant to be the first/default instance. Two independent signals both indicate it's already in place:
   - The `mcp__trilium__*` tools are already listed as available in *this* session (see the system-reminder of connected MCP tools) — this proves the current registration is valid and connected.
   - Run `claude mcp get trilium` — exit code 0 means it's already registered (the output includes its scope and live connection status; never print the token, which the `get` output doesn't show anyway).

   If either signal is true, **stop here** — report that it's already configured (naming the scope from `claude mcp get`'s output, e.g. "user config") and finish. Only continue if the user explicitly wants an *additional* instance, or neither signal is true.

2. **If this is an additional instance (not the first), ask for a label** — a short name like `work` or `home`. Sanitize it: lowercase, replace every run of characters outside `[a-z0-9]` with `-`, strip leading/trailing `-`. If the result is empty, ask for a different one. Then run `claude mcp get trilium-<label>` — exit 0 means that name is already taken (its error output for a *miss* conveniently lists every configured server too, useful for suggesting a free label) — ask for a different label rather than silently overwriting an existing instance.

   Skip this step entirely for the first/default instance — it always stays unlabeled (server name `trilium`).

3. **Ask for the remaining values**, one at a time (plain question or `AskUserQuestion` if available):
   - The instance's MCP URL. For the default instance, `http://localhost:8081/mcp` is a common value for a local dev `trilium-mcp` stack — offer it as a suggestion, but there's no automatic fallback anymore, so still ask. For a labeled instance, there's no natural default — just ask.
   - Whether the server has OAuth enabled (`MCP_BASE_URL` and `MCP_OAUTH_SECRET` set). That is the default and needs nothing else. Only if it doesn't, ask for an ETAPI token from that Trilium Notes instance's *Options → ETAPI* screen, and never print the token back or log it.

4. **Register the instance.** With OAuth (the default):

       claude mcp add --transport http <name> "<url>" -s user

   Without OAuth, as a fallback, pass the token as a header:

       claude mcp add --transport http <name> "<url>" -H "Authorization: <token>" -s user

   `<name>` is `trilium` for the default instance or `trilium-<label>` for an additional one. `-s user` makes it available to every project under this installation. A token appears in the command's arguments (visible in the tool call, and briefly in process listings while it runs); there's no CLI option to supply it another way, so don't print or log it anywhere else.

5. **Tell the user to restart Claude Code** (or start a new session): a newly added server only connects into a session's tool list after a restart. With OAuth, they then run `/mcp`, pick the server and choose **Authenticate**; a browser opens and they sign in with the Trilium Notes password. Claude Code stores and refreshes the token itself.

## List instances

1. Run `claude mcp list` — it health-checks every configured server fresh, including ones just added this session, and works regardless of what's already loaded into the current session's tool list.
2. From its output, keep only lines whose server name matches `trilium([-_].+)?` (a literal `trilium`, plus any `trilium-<label>` or older `trilium_<label>`). Each line ends with a connection status (e.g. "✔ Connected" or "✘ Failed to connect — ...").
3. Report the list: label (or "default" for `trilium`), and connected/not-connected per that status. Never print token values.

## Remove an instance

1. Ask which instance (by label, or "default" for `trilium`) if not already clear.
2. Run `claude mcp remove trilium` for the default, or `claude mcp remove <name>` with the instance's exact server name (e.g. `trilium-work`) for an additional one (no `-s` needed — it removes from whichever scope it's registered in).
3. Tell the user to restart Claude Code for the removal to take effect.
