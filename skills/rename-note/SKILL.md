---
name: rename-note
description: Rename a Trilium note by changing its title via patchNoteById. Use when the user asks to rename, retitle, or change the title of a note.
---

# Rename a Trilium Note

Verified against a live instance: `patchNoteById` accepts `title` directly and applies it immediately — no special handling needed.

Note the distinction from a branch **prefix**: a note's title is global — changing it renames the note everywhere it appears (a note can be cloned into multiple parents). If the user only wants a note to display differently in one specific location without touching its title elsewhere, that's a `prefix` on that location's branch (via `patchBranchById`), not a rename — ask which one they mean if the note has more than one parent and this isn't already clear from context.

If more than one Trilium instance is connected this session, resolve which one to use first — see [Working with multiple instances](../README.md#working-with-multiple-instances).

## Steps

1. **Resolve the note to rename** (by title via `searchNotes` or by noteId if given).

2. **Check `parentNoteIds`/`parentBranchIds`** via `getNoteById`. If there's more than one, and the request could plausibly mean "just in this one place," clarify with the user whether they want the note's actual title changed (affects every location) or a per-location prefix instead.

3. **Ask for the new title** if not already given.

4. **Call `patchNoteById`** with `noteId__path: <note's id>` and `title: <new title>`.

5. **Report back** the note's old and new title.
