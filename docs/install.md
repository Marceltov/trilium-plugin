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

=== "Automatic (recommended)"

    Start a new Claude Code session. If no Trilium is configured, the plugin's `SessionStart` hook flags it and Claude offers to run the `manage-trilium-instances` skill. It asks for the trilium-mcp URL and your ETAPI token and registers them with `claude mcp add`, scoped to your user so every project sees it.

    You can also start it yourself at any time, for example by asking Claude to "set up the Trilium plugin".

=== "Manual"

    Register the server yourself:

    ```bash
    claude mcp add --transport http trilium "https://trilium-mcp.example.com/mcp" \
      -H "Authorization: YOUR_TRILIUM_ETAPI_TOKEN" -s user
    ```

    The skills expect the default instance to be named `trilium`.

Restart Claude Code afterwards: a newly registered server only connects on the next launch. `claude mcp list` shows whether it's connected.

If you use several Claude Code installations (separate `CLAUDE_CONFIG_DIR`s), each is configured on its own.
