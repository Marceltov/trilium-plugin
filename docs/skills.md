# Skills

Claude picks a skill automatically when your request matches it, so you just ask in plain words ("move my meeting notes under Projects"). Each skill calls the tools of Trilium Notes' built-in MCP server rather than the ETAPI directly.

## Connection

- **`trilium-manage-instances`**: Configures the connection to one or more Trilium Notes instances: add, list or remove them, each registered with `claude mcp add`. Offered once by the `SessionStart` hook, in the first session without a configured instance.

## Everyday notes

- **`trilium-create-note`**: Creates a plain new note (title, content, type, parent), no template involved.
- **`trilium-delete-note`**: Deletes a note and its entire subtree of children, after confirming with the user.
- **`trilium-move-note`**: Moves a note to a different parent (creates a new branch, deletes the old one).
- **`trilium-rename-note`**: Changes a note's title.
- **`trilium-search-notes`**: General-purpose note search by title, content, or attributes.
- **`trilium-manage-note-attributes`**: Add, update, or remove labels and relations on a note.

## Journal and export

- **`trilium-journal-note`**: Get or append to the day/week/month/year journal note for a date.
- **`trilium-export-note-subtree`**: Export a note and its subtree as one readable Markdown document.

## Templates

- **`trilium-create-note-from-template`**: Creates a new note from an existing template note (`~template` relation) and prompts for the template's promoted-attribute values.
- **`trilium-apply-template-to-note`**: Retroactively attaches an existing note to a template. Mutates the target note's content and children, so it confirms with the user before writing.
- **`trilium-find-template-instances`**: Searches for notes derived from a given template, optionally filtered by promoted-attribute values.

## Knowledge base

Building an LLM wiki (Karpathy's pattern: sources in, linked summary, concept, entity and hub pages out) is its own plugin now: [trilium-llm-wiki](https://trilium-llm-wiki.marceltov.de/). It can be installed next to this one and uses the same connection.

The sources are in [`skills/`](https://github.com/Marceltov/trilium-plugin/tree/main/skills), one `SKILL.md` per skill.
