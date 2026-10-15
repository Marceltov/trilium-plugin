---
hide:
  - toc
---

<div class="tm-hero" markdown>

# Skills for your Trilium Notes instance notes in Claude Code

<p class="tm-hero__lead">The Trilium Notes plugin gives Claude Code ready-made skills for Trilium Notes: create, move, rename and search notes, manage attributes, work with templates and journal notes, and export a subtree. It also sets up the connection to your Trilium Notes MCP server for you.</p>

[Install it](install.md){ .md-button .md-button--primary } [Browse the skills](skills.md){ .md-button }

</div>

```
/plugin marketplace add Marceltov/trilium-plugin
/plugin install trilium
```

!!! warning "Needs a running Trilium Notes MCP server"

    This plugin is only the client half. It does not run or bundle the MCP server: you need [Trilium Notes MCP server](https://trilium-mcp.marceltov.de/) deployed next to your Trilium Notes instance first (see its [quick start](https://trilium-mcp.marceltov.de/getting-started/)). Without it, every tool call fails.

## What it does

- **Sets up the connection.** If no Trilium Notes instance is configured, a `SessionStart` hook notices in your first session and Claude offers, once, to register one: it asks for the URL and ETAPI token and runs `claude mcp add` for you.
- **Knows Trilium Notes' features.** Skills cover templates, promoted attributes, journal notes and subtree export, so Claude uses the right ETAPI calls instead of guessing.
- **Works on claude.ai too.** Add this repository as a plugin marketplace on claude.ai, next to a Trilium Notes MCP server connector. See [Use on claude.ai](claude-ai.md).
- **Handles several instances.** Connect a home and a work Trilium Notes instance side by side; skills ask which one you mean when it isn't clear. See [Multiple instances](multiple-instances.md).
- **Asks before destructive changes.** Deleting a note or applying a template to an existing one is confirmed with you first.
