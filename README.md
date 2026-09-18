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

**Automatic (recommended):** if no instance is configured, a bundled `SessionStart` hook detects this and Claude will offer to run the `manage-trilium-instances` skill, which asks for a URL and token and saves them to the *current Claude Code installation's* `settings.json` — no manual export needed on future launches of that installation. Run the skill again any time to add another instance (give it a label like `work` or `home`), list what's configured, or remove one. If you run multiple installs (e.g. via separate `CLAUDE_CONFIG_DIR`s), each is configured independently. Either way, you'll need to restart Claude Code for a newly added instance to connect.

**Manual:** export the default instance's variables yourself before starting Claude Code, equivalent to:

```bash
export TRILIUM_MCP_URL="https://your-host/mcp"
export TRILIUM_ETAPI_TOKEN="your-etapi-token"
```

Or add them — plus any additional labeled instances — to your Claude Code installation's `settings.json` (defaults to `~/.claude/settings.json`, or `$CLAUDE_CONFIG_DIR/settings.json` if that's set), equivalent to:

```json
{
  "env": {
    "TRILIUM_MCP_URL": "https://your-host/mcp",
    "TRILIUM_ETAPI_TOKEN": "your-etapi-token",
    "TRILIUM_WORK_URL": "https://work-host/mcp",
    "TRILIUM_WORK_TOKEN": "your-work-etapi-token"
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

`TRILIUM_MCP_URL` defaults to `http://localhost:8081/mcp` if unset, matching the local dev stack in `trilium-mcp`. `TRILIUM_ETAPI_TOKEN` and every additional instance's token have no default — create one from that Trilium instance's *Options → ETAPI* screen. Restart Claude Code after editing `settings.json` — the `${VAR}` expansion only happens at startup.

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
