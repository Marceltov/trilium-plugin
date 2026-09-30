<h1 align="center"><a href="https://github.com/Marceltov/trilium-plugin">trilium-plugin</a></h1>

<p align="center">
  <a href="https://github.com/Marceltov/trilium-mcp">
    <img alt="requires trilium-mcp sidecar" src="https://img.shields.io/badge/requires-trilium--mcp_sidecar_running-critical">
  </a>
  <a href="https://trilium-plugin.marceltov.de/">
    <img alt="Documentation" src="https://img.shields.io/badge/docs-trilium--plugin.marceltov.de-2f7a27">
  </a>
  <a href="LICENSE">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-blue.svg">
  </a>
</p>

A [Claude Code](https://code.claude.com) plugin for [Trilium](https://triliumnotes.org): skills for working with your notes, plus the MCP connection to a running [trilium-mcp](https://github.com/Marceltov/trilium-mcp) server.

> [!IMPORTANT]  
> This plugin does **not** run, host, or bundle the MCP server. It's a thin client: it only works if you already have [`trilium-mcp`](https://github.com/Marceltov/trilium-mcp) deployed and reachable as a **container sidecar** next to your Trilium instance (see its [quick start](https://trilium-mcp.marceltov.de/getting-started/)). Installing this plugin alone gets you nothing — without a running `trilium-mcp` sidecar and valid credentials, every tool call fails.

**Full documentation: [trilium-plugin.marceltov.de](https://trilium-plugin.marceltov.de/)**

- [Install and connect](https://trilium-plugin.marceltov.de/install/): install the plugin and register your Trilium
- [Multiple instances](https://trilium-plugin.marceltov.de/multiple-instances/): home and work Trilium side by side
- [Skills](https://trilium-plugin.marceltov.de/skills/): everything the plugin can do

## Install

```
/plugin marketplace add Marceltov/trilium-plugin
/plugin install trilium
```

Then start a new session: Claude offers to connect your Trilium if none is configured.

## Related project

This plugin is the **client half**: skills that call MCP tools. [`trilium-mcp`](https://github.com/Marceltov/trilium-mcp) is the **server half** — the container sidecar that exposes Trilium's ETAPI as those MCP tools in the first place. You need both: deploy `trilium-mcp` next to your Trilium instance, then install this plugin to get skills that use it.

## License

MIT — see [LICENSE](LICENSE).
