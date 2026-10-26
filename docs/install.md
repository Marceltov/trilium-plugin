# Install and connect

## 1. Turn on Trilium Notes' MCP server

This plugin uses the MCP server built into Trilium Notes 0.106+ (*Options → AI / LLM → MCP server*). Connect to it either:

- **through [trilium-mcp-proxy](https://github.com/Marceltov/trilium-mcp-proxy)** (recommended): you sign in once with your Trilium Notes password, no token to create or paste. The proxy runs on your own server, so the password never leaves it; or
- **directly**, with an ETAPI token from *Options → ETAPI*.

For the proxy, follow its [quick start](https://trilium-mcp-proxy.marceltov.de/getting-started/).

## 2. Install the plugin

In Claude Code:

```
/plugin marketplace add Marceltov/trilium-plugin
/plugin install trilium
```

## 3. Connect your Trilium Notes instance

Start a new Claude Code session. If no Trilium Notes instance is configured, the plugin's `SessionStart` hook flags it and Claude offers to run the `trilium-manage-instances` skill. It offers this once per installation, in the first session after you install the plugin; after that, ask for it yourself whenever you like, for example "set up the Trilium Notes plugin".

The skill asks how you connect and for the URL (the proxy's, or your Trilium Notes URL with `/mcp`), and registers the instance under the name `trilium`, scoped to your user so every project sees it. Through the proxy: after the restart below, run `/mcp`, pick `trilium` and choose **Authenticate**; a browser opens on the proxy's login page and you sign in with your Trilium Notes password. Directly: the skill asks for an ETAPI token (*Options → ETAPI*) and sends it as an `Authorization: Bearer` header. Configure instances only through this skill, so the names match what the other skills look for.

Restart Claude Code afterwards: a newly registered server only connects on the next launch.

If you use several Claude Code installations (separate `CLAUDE_CONFIG_DIR`s), each is configured on its own.
