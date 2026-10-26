---
name: trilium-delete-note
description: Delete a note in Trilium Notes (and its entire subtree of child notes) via the delete_note MCP tool, after confirming with the user. Use when the user asks to delete, remove, or get rid of a note in Trilium Notes.
---

# Delete a Note in Trilium Notes

`delete_note` deletes the note in **every** location it's cloned to, and its subtree with it (children that also live elsewhere survive there). This is destructive, so always confirm before calling it.

If more than one Trilium Notes instance is connected this session, resolve which one to use first — see [Working with multiple instances](reference/shared-rules.md#working-with-multiple-instances).

## Steps

1. **Resolve the target note.** If the user gave a noteId, use it directly. Otherwise `search_notes` by title; if there are multiple matches, list them and ask which one.

2. **Fetch the note before deleting**: `get_note` for its title, `parentNoteIds` and `childNotes.totalCount`. If it has children, note the count — the user needs to know the deletion is not just this one note. If it has more than one parent, say that it disappears from all of them: these tools can't remove just one placement.

3. **Confirm with the user** (e.g. via `AskUserQuestion`), stating the note's title and, if non-empty, how many child notes will be deleted along with it. If the user declines, stop.

4. **On confirmation**, call `delete_note` with the note's `noteId`.

5. **Report back** that the note (and its subtree, if any) was deleted. It's a soft delete: the user can restore it in Trilium Notes under *Recent Changes*.
