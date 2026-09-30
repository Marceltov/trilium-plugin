# Skills

Claude picks a skill automatically when your request matches it, so you just ask in plain words ("move my meeting notes under Projects"). Each skill calls the [trilium-mcp](https://trilium-mcp.marceltov.de/) tools rather than the ETAPI directly.

## Connection

- **`manage-trilium-instances`**: Configures the connection to one or more Trilium instances: add, list or remove them, each registered with `claude mcp add`. Offered automatically by the `SessionStart` hook when no instance is configured.

## Everyday notes

- **`create-note`**: Creates a plain new note (title, content, type, parent), no template involved.
- **`delete-note`**: Deletes a note and its entire subtree of children, after confirming with the user.
- **`move-note`**: Moves a note to a different parent (creates a new branch, deletes the old one).
- **`rename-note`**: Changes a note's title.
- **`search-notes`**: General-purpose note search by title, content, or attributes.
- **`manage-note-attributes`**: Add, update, or remove labels and relations on a note.

## Journal and export

- **`journal-note`**: Get or append to the day/week/month/year journal note for a date.
- **`export-note-subtree`**: Export a note and its subtree as readable markdown or HTML.

## Templates

- **`create-note-from-template`**: Creates a new note from an existing template note (`~template` relation) and prompts for the template's promoted-attribute values.
- **`apply-template-to-note`**: Retroactively attaches an existing note to a template. Mutates the target note's content and children, so it confirms with the user before writing.
- **`find-template-instances`**: Searches for notes derived from a given template, optionally filtered by promoted-attribute values.

The sources are in [`skills/`](https://github.com/Marceltov/trilium-plugin/tree/main/skills), one `SKILL.md` per skill.
