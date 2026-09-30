# Multiple instances

You can connect more than one Trilium, for example a home and a work instance. Each needs its own [trilium-mcp container](https://trilium-mcp.marceltov.de/multiple-instances/) and is registered under its own name:

| Instance | MCP server name | Tool prefix |
| -------- | --------------- | ----------- |
| Default | `trilium` | `mcp__trilium__*` |
| Labeled, e.g. `work` | `trilium-work` | `mcp__trilium-work__*` |

## Add, list or remove one

Ask Claude, for example "add my work Trilium" or "which Trilium instances are connected?". The `manage-trilium-instances` skill handles it:

- **Add:** asks for a label (like `work` or `home`), the URL and the ETAPI token, then registers `trilium-<label>`. Restart Claude Code so it connects.
- **List:** shows every configured instance and whether it's connected.
- **Remove:** unregisters the instance you name.

## Which instance a skill uses

With one instance connected, skills just use it. With several, a skill first checks whether you already named one ("in my work notes"); if not, it asks once which instance you mean and sticks with it for the rest of the task.
