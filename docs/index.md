---
hide:
  - toc
---

<div class="tm-hero" markdown>

# Skills for your Trilium notes in Claude Code

<p class="tm-hero__lead">trilium-plugin gives Claude Code ready-made skills for Trilium: create, move, rename and search notes, manage attributes, work with templates and journal notes, and export a subtree. It also sets up the connection to your trilium-mcp server for you.</p>

[Install it](install.md){ .md-button .md-button--primary } [Browse the skills](skills.md){ .md-button }

</div>

```
/plugin marketplace add Marceltov/trilium-plugin
/plugin install trilium
```

!!! warning "Needs a running trilium-mcp server"

    This plugin is only the client half. It does not run or bundle the MCP server: you need [trilium-mcp](https://trilium-mcp.marceltov.de/) deployed next to your Trilium first (see its [quick start](https://trilium-mcp.marceltov.de/getting-started/)). Without it, every tool call fails.

## What it does

- **Sets up the connection.** If no Trilium is configured, a `SessionStart` hook notices and Claude offers to register one: it asks for the URL and ETAPI token and runs `claude mcp add` for you.
- **Knows Trilium's features.** Skills cover templates, promoted attributes, journal notes and subtree export, so Claude uses the right ETAPI calls instead of guessing.
- **Handles several instances.** Connect a home and a work Trilium side by side; skills ask which one you mean when it isn't clear. See [Multiple instances](multiple-instances.md).
- **Asks before destructive changes.** Deleting a note or applying a template to an existing one is confirmed with you first.
