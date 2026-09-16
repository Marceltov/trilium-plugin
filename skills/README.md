# Skills

This directory holds the plugin's skills, one per subdirectory:

```
skills/
  <skill-name>/
    SKILL.md
```

- **`setup-trilium-credentials`** — configures `TRILIUM_MCP_URL` /
  `TRILIUM_ETAPI_TOKEN` by asking the user and persisting them to
  `~/.claude/settings.json`. Triggered automatically by the `SessionStart`
  hook in `hooks/` when the token is missing.
- **`create-note`** — creates a plain new note (title, content, type,
  parent), no template involved.
- **`create-note-from-template`** — creates a new note from an existing
  template note (`~template` relation) and prompts for the template's
  promoted-attribute values.
- **`apply-template-to-note`** — retroactively attaches an existing note to
  a template. Mutates the target note's content and children, so it
  confirms with the user before writing.
- **`find-template-instances`** — searches for notes derived from a given
  template, optionally filtered by promoted-attribute values.

See the [Claude Code plugin docs](https://code.claude.com/docs/en/plugins)
for the `SKILL.md` format, or the `superpowers:writing-skills` skill for a
guided walkthrough.

Skills here should call the MCP tools exposed by
[trilium-mcp](https://github.com/Marceltov/trilium-mcp) (`createNote`,
`searchNotes`, `getNoteById`, `exportNoteSubtree`, …) rather than talking to
the Trilium ETAPI directly.
