---
name: export-note-subtree
description: Export a Trilium note and its entire subtree as readable markdown or HTML text via exportNoteSubtree. Use when the user asks to export, dump, or get a readable copy of a note and its children — e.g. for backup, review, or pasting elsewhere.
---

# Export a Note Subtree

`exportNoteSubtree` fetches Trilium's ZIP export of the subtree rooted at a note, unpacks it, and returns each note's path followed by its text content — no ZIP handling needed on the caller's side. Binary attachments (images, files) are listed by name but not inlined.

There is no corresponding working import in this plugin: `importZip` was tested against a live instance and is broken as exposed by the MCP tool (it takes no file-content parameter, and calling it returns an HTTP 500). Don't offer it as an option.

If more than one Trilium instance is connected this session, resolve which one to use first — see [Working with multiple instances](../README.md#working-with-multiple-instances).

## Steps

1. **Resolve the note to export** (by title via `searchNotes` or by noteId if given). Use `"root"` if the user wants the entire document exported.

2. **Determine the format** — `markdown` (default, most readable) or `html`. Ask only if the user's intent isn't clear; default to markdown otherwise.

3. **Call `exportNoteSubtree`** with `noteId` and `format`.

4. **Present the result.** For a small export, show it inline. For a large one, save it to a file (ask where, or use a sensible default like the note's title) rather than flooding the conversation — mention that any binary attachments were only listed by name, not included, in case the user needs those separately.
