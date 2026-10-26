# Skills

This directory holds the plugin's skills, one per subdirectory:

```
skills/
  <skill-name>/
    SKILL.md
    reference/shared-rules.md   generated copy of ../../shared/rules.md, committed
```

- **`trilium-manage-instances`** — configures the connection to one or more Trilium Notes instances by asking the user and registering each with `claude mcp add`. Offered once per installation by the `SessionStart` hook in `hooks/`, in the first session without a configured instance.
- **`trilium-create-note`** — creates a plain new note (title, content, type, parent), no template involved.
- **`trilium-delete-note`** — deletes a note and its entire subtree of children, after confirming with the user.
- **`trilium-move-note`** — moves a note to a different parent (creates a new branch, deletes the old one).
- **`trilium-rename-note`** — changes a note's title.
- **`trilium-search-notes`** — general-purpose note search by title, content, or attributes.
- **`trilium-manage-note-attributes`** — add, update, or remove labels and relations on a note.
- **`trilium-journal-note`** — get or append to the day/week/month/year journal note for a date.
- **`trilium-export-note-subtree`** — export a note and its subtree as one readable Markdown document.
- **`trilium-create-note-from-template`** — creates a new note from an existing template note (`~template` relation) and prompts for the template's promoted-attribute values.
- **`trilium-apply-template-to-note`** — retroactively attaches an existing note to a template. Mutates the target note's content and children, so it confirms with the user before writing.
- **`trilium-find-template-instances`** — searches for notes derived from a given template, optionally filtered by promoted-attribute values.

See the [Claude Code plugin docs](https://code.claude.com/docs/en/plugins) for the `SKILL.md` format, or the `superpowers:writing-skills` skill for a guided walkthrough.

Skills here should call the tools of Trilium Notes' built-in MCP server (`create_note`, `search_notes`, `get_note`, `set_attribute`, …), directly or through trilium-mcp-proxy, rather than talking to the Trilium Notes ETAPI directly. Text notes go in and come out as Markdown.

## Writing skills here

- Names start with `trilium-`: on claude.ai, skills are called without the plugin name, so the prefix keeps them apart from other plugins' skills.
- The rules every skill shares (which instance to use, connectors) live in [`shared/rules.md`](../shared/rules.md). Edit only that file and run `scripts/sync-shared.sh`; the Checks workflow fails when a copy in `skills/*/reference/` is out of date. Skills link to their own copy as `reference/shared-rules.md`, so every skill folder is complete on its own.
- Write for both Claude Code and claude.ai. Where they differ, phrase it as a condition ("if you have a shell", "if you can start subagents") instead of assuming Claude Code.
