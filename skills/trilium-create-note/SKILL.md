---
name: trilium-create-note
description: Create a new plain note in Trilium Notes (title, content, type, and parent location) via the create_note MCP tool. Use when the user asks to create, add, jot down, or capture a new note in Trilium Notes and no template is involved.
---

# Create a Note in Trilium Notes

A thin wrapper around `create_note` for the common case: one new note, no template. For notes instantiated from a template, use the `trilium-create-note-from-template` skill instead.

If more than one Trilium Notes instance is connected this session, resolve which one to use first — see [Working with multiple instances](reference/shared-rules.md#working-with-multiple-instances).

## Steps

1. **Determine the parent location.** If the user names a note (by title or noteId) to file it under, resolve that with `search_notes` if needed. Otherwise default to Trilium Notes' inbox: the note labelled `#inbox` (`search_notes("#inbox", fastSearch=true)`), or, without one, today's day note (see `trilium-journal-note`). That is Trilium Notes' normal catch-all for undirected new notes.

2. **Determine title and content.** Ask for whatever the user didn't already give. Content may be empty if the user just wants a placeholder note. Text notes take **Markdown**; Trilium Notes stores it as formatted text.

3. **Determine the note type.** Default to `text` unless the user asks for another type `create_note` offers (`code`, `book`, `mermaid`, `canvas`, `search`, `mindMap`, `relationMap`, `render`, `webView`). A `code` note also needs a `mime` (ask if unclear). File and image notes can't be created through these tools; say so.

4. **Call `create_note`** with `parentNoteId`, `title`, `type`, `content` (and `mime` for code).

5. **Report back** the new note's title and noteId. Don't dump the full JSON response — the user cares whether it worked and where to find it, not the raw payload.

6. If the user also wants labels/relations on the note, use `set_attribute` after creation — this skill only covers the note itself.
