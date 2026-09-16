# trilium-plugin

A [Claude Code](https://code.claude.com) plugin for [Trilium](https://triliumnotes.org):
skills for working with your notes, plus the MCP connection to a running
[trilium-mcp](https://github.com/MarcelBruckner/trilium-mcp) server.

This repo does **not** run or host the MCP server. `trilium-mcp` runs as a
container sidecar next to your Trilium instance (see that repo's Quick Start).
This plugin only points Claude Code at wherever you've already deployed it,
and adds skills that use its tools.

## Install

```
/plugin marketplace add MarcelBruckner/trilium-plugin
/plugin install trilium-plugin
```

## Configure the connection

Set these two environment variables before starting Claude Code, matching
the host and token from your `trilium-mcp` deployment
(see [Connecting a client](https://github.com/MarcelBruckner/trilium-mcp#connecting-a-client)):

```bash
export TRILIUM_MCP_URL="https://your-host/mcp"
export TRILIUM_ETAPI_TOKEN="your-etapi-token"
```

`TRILIUM_MCP_URL` defaults to `http://localhost:8081/mcp` if unset, matching
the local dev stack in `trilium-mcp`. `TRILIUM_ETAPI_TOKEN` has no default —
create one from Trilium's *Options → ETAPI* screen.

## Skills

See [`skills/`](skills/) — none are included yet; this is a scaffold.

## License

MIT — see [LICENSE](LICENSE).
