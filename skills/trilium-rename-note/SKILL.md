---
name: trilium-rename-note
description: Rename a note in Trilium Notes by changing its title via the rename_note MCP tool. Use when the user asks to rename, retitle, or change the title of a note.
---

# Rename a Note in Trilium Notes

`rename_note` changes a note's title and applies it immediately.

Note the distinction from a branch **prefix**: a note's title is global — changing it renames the note everywhere it appears (a note can be cloned into multiple parents). If the user only wants a note to display differently in one location, that's a prefix on that placement, which these tools can't change on an existing placement (only `clone_note` sets one, on a new clone). Ask which they mean if the note has more than one parent and it isn't clear, and point them to Trilium Notes for a prefix.

If more than one Trilium Notes instance is connected this session, resolve which one to use first — see [Working with multiple instances](reference/shared-rules.md#working-with-multiple-instances).

## Steps

1. **Resolve the note to rename** (by title via `search_notes` or by noteId if given).

2. **Check `parentNoteIds`** via `get_note`. If there's more than one, and the request could plausibly mean "just in this one place," clarify as above.

3. **Ask for the new title** if not already given.

4. **Call `rename_note`** with `noteId` and `newTitle`.

5. **Report back** the note's old and new title.
