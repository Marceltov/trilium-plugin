<h1 align="center"><a href="https://github.com/Marceltov/trilium-plugin">trilium-plugin</a></h1>

<p align="center">
  <a href="https://github.com/Marceltov/trilium-mcp-proxy">
    <img alt="requires Trilium Notes 0.106+ MCP server" src="https://img.shields.io/badge/requires-Trilium_Notes_0.106%2B_MCP_server-critical">
  </a>
  <a href="https://trilium-plugin.marceltov.de/">
    <img alt="Documentation" src="https://img.shields.io/badge/docs-trilium--plugin.marceltov.de-2f7a27">
  </a>
  <a href="LICENSE">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-blue.svg">
  </a>
</p>

A [Claude Code](https://code.claude.com) plugin for [Trilium Notes](https://triliumnotes.org): skills for working with your notes, plus the MCP connection to Trilium Notes' built-in MCP server.

> [!IMPORTANT]  
> This plugin uses the MCP server built into Trilium Notes 0.106+ (*Options → AI / LLM → MCP server*). Connect to it either:
> 
> - **through [trilium-mcp-proxy](https://github.com/Marceltov/trilium-mcp-proxy)** (recommended): you sign in once with your Trilium Notes password, no token to create or paste. The proxy runs on your own server, so the password never leaves it; or
> - **directly**, with an ETAPI token from *Options → ETAPI*.
>
> The plugin sets up the connection but runs neither. Without Trilium's MCP server switched on and reachable, every tool call fails.

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

**On claude.ai?** Connect Trilium Notes through trilium-mcp-proxy as a connector, then add this repository under *Customize → Plugins → Add → Add marketplace* and add `trilium`. See [Use on claude.ai](https://trilium-plugin.marceltov.de/claude-ai/).

## Related project

This plugin is the **client half**: skills that know Trilium Notes' concepts (templates, promoted attributes, journal notes, clones) and call the tools of Trilium's built-in MCP server. [trilium-mcp-proxy](https://github.com/Marceltov/trilium-mcp-proxy) adds the password login in front of that server. Earlier versions used [trilium-mcp](https://github.com/Marceltov/trilium-mcp), which is archived now that Trilium has its own server.

## License

MIT — see [LICENSE](LICENSE).
