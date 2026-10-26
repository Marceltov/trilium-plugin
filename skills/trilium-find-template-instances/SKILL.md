---
name: trilium-find-template-instances
description: Search for notes in Trilium Notes instantiated from a given template, optionally filtered by promoted-attribute values, using ~template relation search syntax. Use when the user asks to list, find, or query notes created from a template (e.g. "show me all Server notes" or "which notes use the Meeting template").
---

# Find Notes Derived From a Template

Read-only — no confirmation needed. Composes entirely from `search_notes` using Trilium Notes' relation-target search syntax (https://docs.triliumnotes.org/; `load_skill("search_syntax")` returns the full reference); no template-specific tool exists.

If more than one Trilium Notes instance is connected this session, resolve which one to use first — see [Working with multiple instances](reference/shared-rules.md#working-with-multiple-instances).

## Steps

1. **Resolve the template.** If the user gave a noteId, use it directly. Otherwise `search_notes("#template")` and match by title; if ambiguous, list candidates and ask.

2. **Build the base query.** By noteId (preferred — exact): `~template.noteId = '<templateNoteId>'`. By title only, if you don't want to resolve an id first: `~template.title = '<templateTitle>'`.

3. **Add promoted-attribute filters if the user wants them**, AND'd onto the base query, e.g. `#hostName = 'foo'`. Use the comparator that fits the field's dataType (`=`, `>=`, `<=`, `*=*` for substring, etc.) for `number`/`date` fields. Sorting goes into the query too: `orderBy #date desc`.

4. **Call `search_notes`** with the composed `query`. Pass `limit` if the user wants only the top N results (the default is 10, so raise it for "all").

5. **Present results concisely**: title, noteId, and only the promoted-attribute values relevant to what the user asked about — not the full JSON payload per note.
