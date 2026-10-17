# Install and connect

## 1. Deploy the Trilium Notes MCP server

The plugin talks to Trilium Notes through a running [Trilium Notes MCP server](https://trilium-mcp.marceltov.de/). Set that up first with its [quick start](https://trilium-mcp.marceltov.de/getting-started/) and enable OAuth on it (`MCP_BASE_URL` and `MCP_OAUTH_SECRET`), so Claude signs in with your Trilium Notes password and you don't need an ETAPI token.

## 2. Install the plugin

In Claude Code:

```
/plugin marketplace add Marceltov/trilium-plugin
/plugin install trilium
```

## 3. Connect your Trilium Notes instance

Start a new Claude Code session. If no Trilium Notes instance is configured, the plugin's `SessionStart` hook flags it and Claude offers to run the `trilium-manage-instances` skill. It offers this once per installation, in the first session after you install the plugin; after that, ask for it yourself whenever you like, for example "set up the Trilium Notes plugin".

The skill asks for the Trilium Notes MCP server URL and registers the instance under the name `trilium`, scoped to your user so every project sees it. After the restart below, run `/mcp`, pick `trilium` and choose **Authenticate**: a browser opens and you sign in with your Trilium Notes password. If your MCP server has no OAuth, the skill asks for an ETAPI token (*Options → ETAPI*) instead and sends it as a header. Configure instances only through this skill, so the names match what the other skills look for.

Restart Claude Code afterwards: a newly registered server only connects on the next launch.

If you use several Claude Code installations (separate `CLAUDE_CONFIG_DIR`s), each is configured on its own.
