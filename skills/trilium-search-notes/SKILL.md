---
name: trilium-search-notes
description: Search for notes in Trilium Notes by title, content, or attributes using the search_notes MCP tool and Trilium Notes' query syntax. Use when the user asks to find, search for, list, or look up notes — general lookups, not specifically notes derived from a template (use find-template-instances for that).
---

# Search Notes in Trilium Notes

A thin wrapper around `search_notes`, which takes a query string in Trilium Notes' own search syntax — the same syntax used in the app's search box. `load_skill("search_syntax")` returns the full reference from the server. For searching specifically by template relationship, use the `trilium-find-template-instances` skill instead.

## Query syntax basics

- Plain words do a fulltext search over titles (and content, unless `fastSearch` is set): `project plan`
- `#labelName` matches notes carrying that label; `#labelName = 'value'` matches an exact value; other comparators (`*=*`, `>=`, `<=`, etc.) work too. Values with hyphens or spaces must be quoted.
- `~relationName.title = 'X'` or `~relationName.noteId = 'id'` matches notes whose relation points at a note with that title/id.
- Combine clauses with `AND`/`OR`, scope with `note.type`, `note.dateCreated`, etc., and sort with `orderBy` inside the query — load the syntax reference rather than guessing at an unfamiliar clause.

If more than one Trilium Notes instance is connected this session, resolve which one to use first — see [Working with multiple instances](reference/shared-rules.md#working-with-multiple-instances).

## Steps

1. **Clarify what the user is looking for** if it's ambiguous: a keyword search, a label/attribute filter, a relation filter, or some combination. Don't invent a query more specific than what they asked for.

2. **Compose the search string** from the query syntax above. Prefer the simplest query that captures the request — a bare keyword search over content unless the user names labels, relations, or a specific note type.

3. **Call `search_notes`** with `query`. Consider:
   - `limit` (default 10) if the user wants more or fewer results.
   - `ancestorNoteId` if the user wants to search only within a subtree.
   - `fastSearch: true` if the user explicitly wants title/attribute-only matching without scanning content (faster, less thorough).
   - `includeArchivedNotes: true` only if the user asks to include archived notes — they're excluded by default.

4. **If zero results come back** and the query used a label/relation filter, don't just report "nothing found" — consider whether the attribute name might be slightly different than assumed, and say so rather than guessing at variations silently.

5. **Present results concisely**: title, noteId, and whichever attribute values are relevant to what the user asked about — not the full JSON payload per note.
