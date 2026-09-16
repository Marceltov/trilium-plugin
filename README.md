# trilium-plugin

A [Claude Code](https://code.claude.com) plugin for [Trilium](https://triliumnotes.org): Skills for working with your notes, plus the MCP connection to a running [trilium-mcp](https://github.com/Marceltov/trilium-mcp) server.

This repo does **not** run or host the MCP server. `trilium-mcp` runs as a container sidecar next to your Trilium instance (see that repo's Quick Start). 
This plugin only points Claude Code at wherever you've already deployed it, and adds skills that use its tools.

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

See [`skills/`](skills/) — `setup-trilium-credentials` configures the connection; otherwise this is a scaffold.

## License

MIT — see [LICENSE](LICENSE).
