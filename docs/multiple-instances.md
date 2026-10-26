# Multiple instances

You can connect more than one Trilium Notes instance, for example a home and a work instance. Each has its own MCP URL (its own trilium-mcp-proxy, or its own Trilium Notes URL with `/mcp`) and is registered under its own name:

| Instance | MCP server name | Tool prefix |
| -------- | --------------- | ----------- |
| Default | `trilium` | `mcp__trilium__*` |
| Labeled, e.g. `work` | `trilium-work` | `mcp__trilium-work__*` |

## Add, list or remove one

Ask Claude, for example "add my work Trilium Notes instance" or "which Trilium Notes instances are connected?". The `trilium-manage-instances` skill handles it:

- **Add:** asks for a label (like `work` or `home`) and the URL, then registers `trilium-<label>`. Restart Claude Code, then sign in through `/mcp` → **Authenticate** (or, connecting directly, the skill asks for an ETAPI token instead).
- **List:** shows every configured instance and whether it's connected.
- **Remove:** unregisters the instance you name.

## Which instance a skill uses

With one instance connected, skills just use it. With several, a skill first checks whether you already named one ("in my work notes"); if not, it asks once which instance you mean and sticks with it for the rest of the task.
