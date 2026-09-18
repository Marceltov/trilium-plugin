# Skills

This directory holds the plugin's skills, one per subdirectory:

```
skills/
  <skill-name>/
    SKILL.md
```

- **`manage-trilium-instances`** — configures the connection to one or more Trilium instances by asking the user and persisting to `~/.claude/settings.json`. Triggered automatically by the `SessionStart` hook in `hooks/` when no instance is configured.
- **`create-note`** — creates a plain new note (title, content, type, parent), no template involved.
- **`delete-note`** — deletes a note and its entire subtree of children, after confirming with the user.
- **`move-note`** — moves a note to a different parent (creates a new branch, deletes the old one).
- **`rename-note`** — changes a note's title.
- **`search-notes`** — general-purpose note search by title, content, or attributes.
- **`manage-note-attributes`** — add, update, or remove labels and relations on a note.
- **`journal-note`** — get or append to the day/week/month/year journal note for a date.
- **`export-note-subtree`** — export a note and its subtree as readable markdown or HTML.
- **`create-note-from-template`** — creates a new note from an existing template note (`~template` relation) and prompts for the template's promoted-attribute values.
- **`apply-template-to-note`** — retroactively attaches an existing note to a template. Mutates the target note's content and children, so it confirms with the user before writing.
- **`find-template-instances`** — searches for notes derived from a given template, optionally filtered by promoted-attribute values.

See the [Claude Code plugin docs](https://code.claude.com/docs/en/plugins) for the `SKILL.md` format, or the `superpowers:writing-skills` skill for a guided walkthrough.

Skills here should call the MCP tools exposed by [trilium-mcp](https://github.com/Marceltov/trilium-mcp) (`createNote`, `searchNotes`, `getNoteById`, `exportNoteSubtree`, …) rather than talking to the Trilium ETAPI directly.

## Working with multiple instances

A user may have more than one Trilium instance connected at once — each shows up as its own MCP server, so tool names are namespaced per instance: `mcp__trilium__searchNotes` for the default instance, `mcp__trilium_work__searchNotes` for one labeled `work`, and so on (see `manage-trilium-instances`). Every skill that calls Trilium MCP tools resolves which instance to use like this:

1. Note which `mcp__trilium(_.+)?__*` tool prefixes are actually available this session.
2. Exactly one exists → use it, no question asked.
3. More than one exists → check whether the user already named an instance in the conversation (by label, or something identifying like "the work one") and match it to the corresponding prefix.
4. Still ambiguous → ask once which instance, listing the available labels.
5. Use that one resolved prefix for every MCP tool call for the rest of the current task.
