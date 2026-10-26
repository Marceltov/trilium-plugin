---
name: trilium-create-note-from-template
description: Create a new note in Trilium Notes instantiated from an existing template note, by creating a blank note and attaching a ~template relation, then prompting for the template's promoted-attribute values. Use when the user asks to create a note "from" or "using" a template (e.g. "create a new Server note from the Server template").
---

# Create a Note From a Template

In Trilium Notes, a "template" is just a note carrying the `#template` label. Instantiating one is not a special call — it's: create a blank note, then attach a `~template` relation to the template note. Verified against a live instance through Trilium's built-in MCP server: once that relation exists, Trilium Notes' **backend** automatically clones the template's child notes (as real, independently-editable notes, not references), copies its content onto the new note, and folds the template's promoted-attribute definitions into the new note's attribute list. This composes entirely from `create_note`, `set_attribute` and `get_note`.

If more than one Trilium Notes instance is connected this session, resolve which one to use first — see [Working with multiple instances](reference/shared-rules.md#working-with-multiple-instances).

## Steps

1. **Resolve the template note.** If the user gave a noteId, use it directly. Otherwise `search_notes("#template")` and match by title (case-insensitive substring). If more than one match, list them and ask which one. If none match, say so — don't guess.

2. **Determine the new note's title and parent location.** Ask for the title if not given. Default the parent to Trilium Notes' inbox (as in `trilium-create-note` step 1) unless the user names a location.

3. **Create a blank note**: `create_note` with empty `content`, type `text` (or whatever type the user wants the new note to be), at the chosen parent.

4. **Attach the template relation**: `set_attribute` with `type: relation`, `name: template`, `value: <template noteId>`, `noteId: <new note id>`.

5. **Re-fetch the new note** via `get_note`. Its `attributes` now include the template's promoted-attribute *definitions*: entries whose `name` is `label:<fieldName>` (or `relation:<fieldName>`) and whose `value` starts with `promoted` (syntax: `promoted,single|multiple,<dataType>[,alias]`).

6. **Prompt for each promoted field's value**, one at a time (or via `AskUserQuestion` if the field looks like a bounded choice). Use the parsed `dataType` (`text`, `number`, `date`, `url`, `boolean`) to shape the prompt. Skip fields the user leaves blank rather than writing an empty label, unless they say it's required.

7. **Write each provided value**: `set_attribute` with `type: label`, `name: <fieldName>`, `value: <given value>`, `noteId: <new note id>`. `set_attribute` **replaces** an attribute of the same name, so a `multiple` field can only hold one value through these tools; tell the user if they give several, and suggest adding the rest in Trilium.

8. **Report back**: the new note's title and noteId, how many child notes were cloned from the template (`childNotes.totalCount` on the refreshed note), and which promoted attributes were set. Mention that the note's content currently mirrors the template's content verbatim — offer to help customize it further if the user wants that now.
