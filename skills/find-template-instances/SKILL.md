---
name: find-template-instances
description: Search for Trilium notes instantiated from a given template, optionally filtered by promoted-attribute values, using ~template relation search syntax. Use when the user asks to list, find, or query notes created from a template (e.g. "show me all Server notes" or "which notes use the Meeting template").
---

# Find Notes Derived From a Template

Read-only — no confirmation needed. Composes entirely from `searchNotes` using Trilium's relation-target search syntax (https://triliumnext.github.io/Docs/Wiki/search.html); no template-specific endpoint exists.

## Steps

1. **Resolve the template.** If the user gave a noteId, use it directly. Otherwise `searchNotes("#template")` and match by title; if ambiguous, list candidates and ask.

2. **Build the base query.** By noteId (preferred — exact): `~template.noteId = '<templateNoteId>'`. By title only, if you don't want to resolve an id first: `~template.title = '<templateTitle>'`.

3. **Add promoted-attribute filters if the user wants them**, AND'd onto the base query, e.g. `#hostName = 'foo'`. Use the comparator that fits the field's dataType (`=`, `>=`, `<=`, `*=*` for substring, etc. — see the search syntax doc linked above) for `number`/`date` fields.

4. **Call `searchNotes`** with the composed query string. Pass `limit` if the user wants only the top N results, and `orderBy`/`orderDirection` if they want a particular sort (e.g. by a promoted date field).

5. **Present results concisely**: title, noteId, and only the promoted-attribute values relevant to what the user asked about — not the full JSON payload per note.
