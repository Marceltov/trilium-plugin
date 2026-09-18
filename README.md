<h1 align="center"><a href="https://github.com/Marceltov/trilium-plugin">trilium-plugin</a></h1>

<p align="center">
  <a href="https://github.com/Marceltov/trilium-mcp">
    <img alt="requires trilium-mcp sidecar" src="https://img.shields.io/badge/requires-trilium--mcp_sidecar_running-critical">
  </a>
  <a href="LICENSE">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-blue.svg">
  </a>
</p>

A [Claude Code](https://code.claude.com) plugin for [Trilium](https://triliumnotes.org): skills for working with your notes, plus the MCP connection to a running [trilium-mcp](https://github.com/Marceltov/trilium-mcp) server.

> [!IMPORTANT]  
> This plugin does **not** run, host, or bundle the MCP server. It's a thin client: it only works if you already have [`trilium-mcp`](https://github.com/Marceltov/trilium-mcp) deployed and reachable as a **container sidecar** next to your Trilium instance (see that repo's Quick Start). Installing this plugin alone gets you nothing — without a running `trilium-mcp` sidecar and valid credentials, every tool call fails.

## Contents

- [Contents](#contents)
- [Install](#install)
- [Configure the connection](#configure-the-connection)
- [Skills](#skills)
- [Related project](#related-project)
- [License](#license)

## Install

```
/plugin marketplace add Marceltov/trilium-plugin
/plugin install trilium
```

## Configure the connection

The plugin needs at least one Trilium instance configured — a URL and ETAPI token matching a running `trilium-mcp` deployment (see [Connecting a client](https://github.com/Marceltov/trilium-mcp#connecting-a-client)). You can configure more than one instance; each becomes its own named MCP connection, and skills ask which instance you mean whenever more than one is connected and it isn't already clear from context.

**Automatic (recommended):** if no instance is configured, a bundled `SessionStart` hook detects this and Claude will offer to run the `manage-trilium-instances` skill, which asks for a URL and token and registers them as an MCP server for the *current Claude Code installation* — no manual setup needed on future launches of that installation. Run the skill again any time to add another instance (give it a label like `work` or `home`), list what's configured, or remove one. If you run multiple installs (e.g. via separate `CLAUDE_CONFIG_DIR`s), each is configured independently. Either way, you'll need to restart Claude Code for a newly added instance to connect.

**Manual:** register the default instance yourself with the Claude Code CLI:

```bash
claude mcp add --transport http trilium "https://your-host/mcp" \
  -H "Authorization: your-etapi-token" -s user
```

`-s user` scopes it to your current Claude Code installation, so it's available in every project. Create the token from that Trilium instance's *Options → ETAPI* screen. Restart Claude Code after running this — a newly registered server only connects on the next launch.

### Working with multiple instances

You're not limited to one Trilium instance. Each additional one is registered the same way, just under its own label — `trilium_<label>` (e.g. `trilium_work`) instead of the bare `trilium` — and shows up under its own tool prefix (`mcp__trilium_work__*`) alongside the default `mcp__trilium__*`. Skills that operate on notes check how many `trilium(_.+)?` prefixes are connected and, if more than one, ask which instance you mean before doing anything.

```bash
claude mcp add --transport http trilium_work "https://work-host/mcp" \
  -H "Authorization: your-work-etapi-token" -s user
```

Run `claude mcp list` to see everything configured and its connection status, or `claude mcp remove trilium_work` to remove one. The `manage-trilium-instances` skill wraps all of this conversationally — it asks for a label, URL and token, and runs the right command for you.

## Skills

See [`skills/`](skills/) for the full list with details. At a glance:

- `manage-trilium-instances` — configures the connection to one or more Trilium instances.
- `create-note`, `delete-note`, `move-note`, `rename-note`, `search-notes`, `manage-note-attributes` — everyday note management.
- `create-note-from-template`, `apply-template-to-note`, `find-template-instances` — Trilium's template feature.
- `journal-note` — the day/week/month/year journal notes.
- `export-note-subtree` — export a note and its subtree as readable markdown or HTML.

## Related project

This plugin is the **client half**: skills that call MCP tools. [`trilium-mcp`](https://github.com/Marceltov/trilium-mcp) is the **server half** — the container sidecar that exposes Trilium's ETAPI as those MCP tools in the first place. You need both: deploy `trilium-mcp` next to your Trilium instance, then install this plugin to get skills that use it.

## License

MIT — see [LICENSE](LICENSE).
