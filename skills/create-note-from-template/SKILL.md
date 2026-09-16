---
name: create-note-from-template
description: Create a new Trilium note instantiated from an existing template note, by creating a blank note and attaching a ~template relation, then prompting for the template's promoted-attribute values. Use when the user asks to create a note "from" or "using" a template (e.g. "create a new Server note from the Server template").
---

# Create a Note From a Template

In Trilium, a "template" is just a note carrying the `#template` label. Instantiating one is not a special ETAPI call — it's: create a blank note, then attach a `~template` relation to the template note. Verified against a live instance: once that relation exists, Trilium's **backend** automatically clones the template's child notes (as real, independently-editable notes, not references), copies its content onto the new note, and folds the template's promoted-attribute definitions into the new note's attribute list. There is no template-specific MCP/ETAPI endpoint — this composes entirely from `createNote`, `postAttribute`, `getNoteById`.

## Steps

1. **Resolve the template note.** If the user gave a noteId, use it directly. Otherwise `searchNotes("#template")` and match by title (case-insensitive substring). If more than one match, list them and ask which one. If none match, say so — don't guess.

2. **Determine the new note's title and parent location.** Ask for the title if not given. Default the parent to today's inbox note (`getInboxNote`) unless the user names a location.

3. **Create a blank note**: `createNote` with empty `content`, type `text` (or whatever type the user wants the new note to be), at the chosen parent.

4. **Attach the template relation**: `postAttribute` with `type: relation`, `name: template`, `value: <template noteId>`, `noteId: <new note id>`.

5. **Re-fetch the new note** via `getNoteById`. Its `attributes` array now includes the template's own owned attributes (this is how promoted fields surface — they are not yet copied as real values on the new note). Find promoted-attribute *definitions* among them: entries whose `name` matches `label:<fieldName>` and whose `value` starts with `promoted` (syntax: `promoted,single|multiple,<dataType>[,alias]`), and whose `noteId` is the *template's*, not the new note's.

6. **Prompt for each promoted field's value**, one at a time (or via `AskUserQuestion` if the field looks like a bounded choice). Use the parsed `dataType` (`text`, `number`, `date`, `url`, `boolean`) to shape the prompt. Skip fields the user leaves blank rather than writing an empty label, unless they say it's required.

7. **Write each provided value**: `postAttribute` with `type: label`, `name: <fieldName>`, `value: <given value>`, `noteId: <new note id>`.

8. **Report back**: the new note's title and noteId, how many child notes were cloned from the template (`childNoteIds.length` on the refreshed note), and which promoted attributes were set. Mention that the note's content currently mirrors the template's content verbatim (they share a blob until the note is edited) — offer to help customize it further if the user wants that now.
