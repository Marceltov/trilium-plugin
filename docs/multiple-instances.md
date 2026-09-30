# Multiple instances

You can connect more than one Trilium, for example a home and a work instance. Each needs its own [trilium-mcp container](https://trilium-mcp.marceltov.de/multiple-instances/) and is registered under its own name:

| Instance | MCP server name | Tool prefix |
| -------- | --------------- | ----------- |
| Default | `trilium` | `mcp__trilium__*` |
| Labeled, e.g. `work` | `trilium_work` | `mcp__trilium_work__*` |

## Add one

Ask Claude to add another Trilium instance. The `manage-trilium-instances` skill asks for a label (like `work` or `home`), the URL and the ETAPI token, and runs the right command. Or register it yourself:

```bash
claude mcp add --transport http trilium_work "https://trilium-work.example.com/mcp" \
  -H "Authorization: YOUR_WORK_ETAPI_TOKEN" -s user
```

Restart Claude Code so it connects. `claude mcp list` shows every instance and its status, and `claude mcp remove trilium_work` removes one; the skill can list and remove them too.

## Which instance a skill uses

With one instance connected, skills just use it. With several, a skill first checks whether you already named one ("in my work notes"); if not, it asks once which instance you mean and sticks with it for the rest of the task.
