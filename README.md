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

A [Claude Code](https://code.claude.com) plugin for [Trilium Notes](https://triliumnotes.org): skills for working with your notes, plus the MCP connection to a running [Trilium Notes MCP server](https://github.com/Marceltov/trilium-mcp).

> [!IMPORTANT]  
> This plugin does **not** run, host, or bundle the MCP server. It's a thin client: it only works if you already have a [Trilium Notes MCP server](https://github.com/Marceltov/trilium-mcp) deployed and reachable as a **container sidecar** next to your Trilium Notes instance (see its [quick start](https://trilium-mcp.marceltov.de/getting-started/)). Installing this plugin alone gets you nothing — without a running `trilium-mcp` sidecar and valid credentials, every tool call fails.

**Full documentation: [trilium-plugin.marceltov.de](https://trilium-plugin.marceltov.de/)**

- [Install and connect](https://trilium-plugin.marceltov.de/install/): install the plugin and register your Trilium Notes instance
- [Multiple instances](https://trilium-plugin.marceltov.de/multiple-instances/): home and work Trilium Notes instance side by side
- [Skills](https://trilium-plugin.marceltov.de/skills/): everything the plugin can do

## Install

```
/plugin install trilium --marketplace Marceltov/trilium-plugin
```

On Claude Code before 2.1.275, add the marketplace first:

```
/plugin marketplace add Marceltov/trilium-plugin
/plugin install trilium
```

Then start a new session: Claude offers to connect your Trilium Notes instance if none is configured.

**On claude.ai?** Connect the Trilium Notes MCP server as a connector, then add this repository under *Customize → Plugins → Add → Add marketplace* and add `trilium`. See [Use on claude.ai](https://trilium-plugin.marceltov.de/claude-ai/).

## Related project

This plugin is the **client half**: skills that call MCP tools. The [Trilium Notes MCP server](https://github.com/Marceltov/trilium-mcp) is the **server half** — the container sidecar that exposes Trilium Notes' ETAPI as those MCP tools in the first place. You need both: deploy `trilium-mcp` next to your Trilium Notes instance, then install this plugin to get skills that use it.

## License

MIT — see [LICENSE](LICENSE).
