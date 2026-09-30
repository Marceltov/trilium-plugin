# Install and connect

## 1. Deploy trilium-mcp

The plugin talks to Trilium through a running [trilium-mcp](https://trilium-mcp.marceltov.de/) server. Set that up first with its [quick start](https://trilium-mcp.marceltov.de/getting-started/), and create an ETAPI token under *Options → ETAPI* in Trilium.

## 2. Install the plugin

In Claude Code:

```
/plugin marketplace add Marceltov/trilium-plugin
/plugin install trilium
```

## 3. Connect your Trilium

Start a new Claude Code session. If no Trilium is configured, the plugin's `SessionStart` hook flags it and Claude offers to run the `manage-trilium-instances` skill. You can also ask for it yourself at any time, for example "set up the Trilium plugin".

The skill asks for the trilium-mcp URL and your ETAPI token and registers the instance under the name `trilium`, scoped to your user so every project sees it. Configure instances only through this skill, so the names match what the other skills look for.

Restart Claude Code afterwards: a newly registered server only connects on the next launch.

If you use several Claude Code installations (separate `CLAUDE_CONFIG_DIR`s), each is configured on its own.
