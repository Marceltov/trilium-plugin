# Use on claude.ai

The Trilium Notes plugin works on claude.ai too, in chat on the web, in the Claude desktop app and in Cowork. You connect the Trilium Notes MCP server as a connector and add the plugin from this repository; the skills are the same as in Claude Code.

## 1. Connect the Trilium Notes MCP server as a connector

Claude.ai signs in with OAuth, so the server needs `MCP_BASE_URL` and `MCP_OAUTH_SECRET` set and a public HTTPS URL. Then add it as a custom connector: see [Claude.ai](https://trilium-mcp.marceltov.de/claude-ai/) in the Trilium Notes MCP server docs for the steps.

## 2. Add the plugin

1. Open *Customize → Plugins*, click **Add** and choose *Add marketplace → Add from a repository*.
2. Enter `Marceltov/trilium-plugin`.
3. Open the `trilium` plugin from that marketplace and click **Add**.

In a chat, type `/` to see the skills, for example `/trilium-search-notes`, or just ask and let Claude pick the right one. New versions arrive through the repository; there is nothing to re-upload.

The plugin's setup hook only runs in Claude Code and Cowork; in chat it is shown greyed out and does nothing. `trilium-manage-instances` notices the connector and explains how to add one if it's missing.
