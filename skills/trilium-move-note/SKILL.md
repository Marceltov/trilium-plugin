---
name: trilium-move-note
description: Move a note in Trilium Notes to a different parent note via the move_note MCP tool. Use when the user asks to move, relocate, or file a note under a different note.
---

# Move a Note in Trilium Notes

`move_note` moves a note, with its content and children, to a new parent.

A note in Trilium Notes can be cloned into several parents at once. Verified against a live instance: on a cloned note, `move_note` always moves the note's **original** placement (the first entry of `parentNoteIds`) and leaves the clones where they are. The tools can't move a specific other placement.

If more than one Trilium Notes instance is connected this session, resolve which one to use first — see [Working with multiple instances](reference/shared-rules.md#working-with-multiple-instances).

## Steps

1. **Resolve the note to move** (by title via `search_notes` or by noteId if given) and the **destination parent note** (same resolution).

2. **Check its placements** with `get_note` (`parentNoteIds`):
   - One parent: just move it.
   - Several: `move_note` will move the one under the first parent in `parentNoteIds`. If the user means that one, go ahead. If they mean another, say the tools can't do that, and offer to add a clone under the destination (`clone_note`) so they can remove the old placement in Trilium Notes, or to move it there in the app.

3. **Call `move_note`** with `noteId` and `newParentNoteId`.

4. **Report back**: the note's title and its new location (the response names the new parent).
