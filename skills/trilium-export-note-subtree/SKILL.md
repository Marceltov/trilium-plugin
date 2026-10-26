---
name: trilium-export-note-subtree
description: Export a note in Trilium Notes and its subtree as one readable Markdown document, built from get_subtree and get_note_content. Use when the user asks to export, dump, or get a readable copy of a note and its children — e.g. for backup, review, or pasting elsewhere.
---

# Export a Note Subtree

Trilium's built-in MCP server has no ZIP export, so this skill assembles the export itself: `get_subtree` for the structure, `get_note_content` for each note (text notes come back as Markdown). For a full-fidelity backup with attachments and attributes, point the user at Trilium Notes' own *Export* (right-click a note → *Export*) instead.

If more than one Trilium Notes instance is connected this session, resolve which one to use first — see [Working with multiple instances](reference/shared-rules.md#working-with-multiple-instances).

## Steps

1. **Resolve the note to export** (by title via `search_notes` or by noteId if given). For the whole document use `root`, but warn that it can be large.

2. **Get the structure**: `get_subtree` with the noteId and `depth` up to 5. Each level lists at most 10 children; where a note has more (compare with `get_child_notes`), fetch its children with `get_child_notes`, and repeat `get_subtree` on notes at the depth limit that still have children.

3. **Read each note** with `get_note_content`. Skip or just list notes whose content isn't text (canvas, mind maps, files and images); list attachments by name (`get_note`) without inlining them.

4. **Assemble one Markdown document**: each note as a heading at its tree depth (`#`, `##`, …) followed by its content, in tree order.

5. **Present the result.** For a small export, show it inline. For a large one, save it to a file (ask where, or use the note's title) rather than flooding the conversation, and say which notes were skipped or only listed.
