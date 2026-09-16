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

The plugin needs `TRILIUM_MCP_URL` and `TRILIUM_ETAPI_TOKEN`, matching the host and token from your `trilium-mcp` deployment (see [Connecting a client](https://github.com/Marceltov/trilium-mcp#connecting-a-client)).

**Automatic (recommended):** if `TRILIUM_ETAPI_TOKEN` isn't set, a bundled `SessionStart` hook detects this and Claude will offer to run the `setup-trilium-credentials` skill, which asks for the URL and token and saves them to the *current Claude Code installation's* `settings.json` — no manual export needed on future launches of that installation. If you run multiple installs (e.g. via separate `CLAUDE_CONFIG_DIR`s), each is configured independently; run the skill once per install. You can also trigger it yourself by asking Claude to set up the Trilium connection.

**Manual:** export the variables yourself before starting Claude Code:

```bash
export TRILIUM_MCP_URL="https://your-host/mcp"
export TRILIUM_ETAPI_TOKEN="your-etapi-token"
```

Or add them to the `env` block of your Claude Code installation's `settings.json` (defaults to `~/.claude/settings.json`, or `$CLAUDE_CONFIG_DIR/settings.json` if that's set) — this is exactly what the automatic setup above does for you:

```json
{
  "env": {
    "TRILIUM_MCP_URL": "https://your-host/mcp",
    "TRILIUM_ETAPI_TOKEN": "your-etapi-token"
  }
}
```

`TRILIUM_MCP_URL` defaults to `http://localhost:8081/mcp` if unset, matching the local dev stack in `trilium-mcp`. `TRILIUM_ETAPI_TOKEN` has no default — create one from Trilium's *Options → ETAPI* screen.

## Skills

See [`skills/`](skills/) for the full list with details. At a glance:

- `setup-trilium-credentials` — configures the MCP connection.
- `create-note`, `delete-note`, `move-note`, `rename-note`, `search-notes`, `manage-note-attributes` — everyday note management.
- `create-note-from-template`, `apply-template-to-note`, `find-template-instances` — Trilium's template feature.
- `journal-note` — the day/week/month/year journal notes.
- `export-note-subtree` — export a note and its subtree as readable markdown or HTML.

## Related project

This plugin is the **client half**: skills that call MCP tools. [`trilium-mcp`](https://github.com/Marceltov/trilium-mcp) is the **server half** — the container sidecar that exposes Trilium's ETAPI as those MCP tools in the first place. You need both: deploy `trilium-mcp` next to your Trilium instance, then install this plugin to get skills that use it.

## License

MIT — see [LICENSE](LICENSE).
