---
name: delete-note
description: Delete a Trilium note (and its entire subtree of child notes) via the deleteNoteById MCP tool, after confirming with the user. Use when the user asks to delete, remove, or get rid of a note in Trilium.
---

# Delete a Trilium Note

`deleteNoteById` deletes the note **and its whole subtree** — verified against a live instance: deleting a parent note deletes all of its child notes too, not just the one note. This is destructive, so always confirm before calling it.

## Steps

1. **Resolve the target note.** If the user gave a noteId, use it directly. Otherwise `searchNotes` by title; if there are multiple matches, list them and ask which one.

2. **Fetch the note before deleting**: `getNoteById` to see its title and `childNoteIds`. If it has children, also note the count — the user needs to know the deletion is not just this one note.

3. **Confirm with the user** (e.g. via `AskUserQuestion`), stating the note's title and, if non-empty, how many child notes will be deleted along with it. If the user declines, stop.

4. **On confirmation**, call `deleteNoteById` with the note's `noteId`.

5. **Report back** that the note (and its subtree, if any) was deleted. Mention that Trilium keeps deleted notes recoverable for a period via `undeleteNote`, in case the user changes their mind.
