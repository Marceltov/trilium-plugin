---
name: create-note
description: Create a new plain Trilium note (title, content, type, and parent location) via the createNote MCP tool. Use when the user asks to create, add, jot down, or capture a new note in Trilium and no template is involved.
---

# Create a Trilium Note

A thin wrapper around `createNote` for the common case: one new note, no template. For notes instantiated from a template, use the `create-note-from-template` skill instead.

If more than one Trilium instance is connected this session, resolve which one to use first — see [Working with multiple instances](../README.md#working-with-multiple-instances).

## Steps

1. **Determine the parent location.** If the user names a note (by title or noteId) to file it under, resolve that with `searchNotes` if needed. Otherwise default to today's inbox note via `getInboxNote` (pass today's date) — Trilium's normal catch-all location for undirected new notes.

2. **Determine title and content.** Ask for whatever the user didn't already give. Content may be empty if the user just wants a placeholder note.

3. **Determine the note type.** Default to `text` unless the user asks for `code`, `file`, `image`, `search`, `book`, or `relationMap`. For `code`, `file`, or `image` types, also determine the `mime` type (ask if unclear).

4. **Call `createNote`** with `parentNoteId`, `title`, `type`, `content` (and `mime` if applicable).

5. **Report back** the new note's title and noteId. Don't dump the full JSON response — the user cares whether it worked and where to find it, not the raw payload.

6. If the user also wants labels/relations on the note, use `postAttribute` after creation — this skill only covers the note itself.
