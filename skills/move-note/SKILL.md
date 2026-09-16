---
name: move-note
description: Move a Trilium note to a different parent note, by creating a branch under the new parent and deleting the old one. Use when the user asks to move, relocate, or file a note under a different note.
---

# Move a Trilium Note

There is no move-specific endpoint. Verified against a live instance: `patchBranchById` rejects `parentNoteId` outright (`PROPERTY_NOT_ALLOWED` — it only accepts `prefix`, `notePosition`, `isExpanded`). A note's placement in the tree is its branch, and moving a note means creating a new branch under the destination parent (`postBranch`) and deleting the old branch (`deleteBranchById`) — not the note itself.

Note that a Trilium note can be cloned into multiple parents at once (multiple branches, one note). If the note has more than one `parentBranchIds` entry, moving one placement must not touch the others — be precise about which branch you're deleting.

## Steps

1. **Resolve the note to move** (by title via `searchNotes` or by noteId if given) and the **destination parent note** (same resolution).

2. **Fetch the note** via `getNoteById` and look at `parentBranchIds`/`parentNoteIds`:
   - If there's exactly one parent, that's the branch to remove.
   - If there's more than one, ask the user which current location they mean to move (unless they already specified the source parent), and match it to the corresponding branch id (`<parentNoteId>_<noteId>`).

3. **Create the new placement**: `postBranch` with `noteId: <note's id>`, `parentNoteId: <destination parent id>` (and `notePosition` if the user cares about ordering).

4. **Remove the old placement**: `deleteBranchById` with the branch id identified in step 2. Do this only after step 3 succeeds — never delete the old branch first, since a note must always have at least one placement.

5. **Confirm the move**: `getNoteById` on the note and check `parentNoteIds` now shows the destination (and, if there was only one parent before, no longer shows the old one).

6. **Report back**: the note's title and its new location.
