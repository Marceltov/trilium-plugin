# Skills

This directory holds the plugin's skills, one per subdirectory:

```
skills/
  <skill-name>/
    SKILL.md
```

No skills yet — this is a scaffold. See the
[Claude Code plugin docs](https://code.claude.com/docs/en/plugins) for the
`SKILL.md` format, or the `superpowers:writing-skills` skill for a guided
walkthrough.

Skills here should call the MCP tools exposed by
[trilium-mcp](https://github.com/Marceltov/trilium-mcp) (`createNote`,
`searchNotes`, `getNoteById`, `exportNoteSubtree`, …) rather than talking to
the Trilium ETAPI directly.
