# Use on claude.ai

The Trilium Notes plugin works on claude.ai too, in chat on the web, in the Claude desktop app and in Cowork. You connect Trilium Notes as a connector and add the plugin from this repository; the skills are the same as in Claude Code.

## 1. Connect Trilium Notes as a connector

Connectors sign in with OAuth, which [trilium-mcp-proxy](https://trilium-mcp-proxy.marceltov.de/) adds in front of Trilium's built-in MCP server. With the proxy running at a public HTTPS URL: *Customize → Connectors → Add custom connector*, enter the proxy's URL ending in `/mcp`, and sign in with your Trilium Notes password on the proxy's login page. See [Connect a client](https://trilium-mcp-proxy.marceltov.de/connecting/) in the proxy docs.

## 2. Add the plugin

1. Open *Customize → Plugins*, click **Add** and choose *Add marketplace → Add from a repository*.
2. Enter `Marceltov/trilium-plugin`.
3. Open the `trilium` plugin from that marketplace and click **Add**.

In a chat, type `/` to see the skills, for example `/trilium-search-notes`, or just ask and let Claude pick the right one. New versions arrive through the repository; there is nothing to re-upload.

The plugin's setup hook only runs in Claude Code and Cowork; in chat it is shown greyed out and does nothing. `trilium-manage-instances` notices the connector and explains how to add one if it's missing.
