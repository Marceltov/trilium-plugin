---
name: search-notes
description: Search for Trilium notes by title, content, or attributes using the searchNotes MCP tool and Trilium's query syntax. Use when the user asks to find, search for, list, or look up notes — general lookups, not specifically notes derived from a template (use find-template-instances for that).
---

# Search Trilium Notes

A thin wrapper around `mcp__trilium__searchNotes`, which takes a query string in Trilium's own search syntax (https://triliumnext.github.io/Docs/Wiki/search.html) — the same syntax used in Trilium's UI search box. For searching specifically by template relationship, use the `find-template-instances` skill instead, which covers that syntax in more depth.

## Query syntax basics

- Plain words do a fulltext search over titles (and content, unless `fastSearch` is set): `project plan`
- `#labelName` matches notes carrying that label; `#labelName = 'value'` matches an exact value; other comparators (`*=*`, `>=`, `<=`, etc.) work per the syntax doc.
- `~relationName.title = 'X'` or `~relationName.noteId = 'id'` matches notes whose relation points at a note with that title/id.
- Combine clauses with `AND`/`OR`, and scope with `note.type`, `note.dateCreated`, etc. — see the syntax doc for the full grammar rather than guessing at an unfamiliar clause.

## Steps

1. **Clarify what the user is looking for** if it's ambiguous: a keyword search, a label/attribute filter, a relation filter, or some combination. Don't invent a query more specific than what they asked for.

2. **Compose the search string** from the query syntax above. Prefer the simplest query that captures the request — a bare keyword search over content unless the user names labels, relations, or a specific note type.

3. **Call `searchNotes`** with `search: <query>`. Consider:
   - `limit` if the user wants only the top N results.
   - `ancestorNoteId` (+ `ancestorDepth`) if the user wants to search only within a subtree.
   - `fastSearch: true` if the user explicitly wants title/attribute-only matching without scanning content (faster, less thorough).
   - `orderBy`/`orderDirection` if the user wants a particular sort.
   - `includeArchivedNotes: true` only if the user asks to include archived notes — they're excluded by default.

4. **If zero results come back** and the query used a label/relation filter, don't just report "nothing found" — consider whether the attribute name might be slightly different than assumed, and say so rather than guessing at variations silently.

5. **Present results concisely**: title, noteId, and whichever attribute values are relevant to what the user asked about — not the full JSON payload per note.
