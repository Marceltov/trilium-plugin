---
name: trilium-llm-wiki
description: Maintain an LLM wiki inside Trilium Notes following Karpathy's "LLM wiki" pattern - ingest raw sources into interlinked summary, concept, entity and hub pages, answer questions from the wiki, and lint it - using the schema note (#llmWikiSchema) as the rulebook. Use when the user says "ingest", "process the sources", "lint the wiki", "ask the wiki", "file this in the wiki", or mentions the LLM wiki / graphkasten / knowledge base, and to bootstrap the structure when it does not exist yet.
---

# LLM Wiki in Trilium Notes

The pattern: the user curates **raw sources**, the assistant compiles them into a **wiki** of
interlinked pages, and a **schema note** holds the conventions. The maintenance humans give up
on (cross-references, touching 15 pages per source) is the assistant's job. Trilium Notes supplies the
pieces Obsidian-based setups build by hand: labels instead of frontmatter, internal links plus
relations as the graph, the note map for review, saved searches as views, and the journal day
note as the log.

**The schema note is the source of truth, not this file.** This skill only tells you how to find
it and which tools implement each step. Conventions the user changes in the schema win.

## Steps

If more than one Trilium Notes instance is connected this session, resolve which one to use first (the wiki lives in one of them) — see [Working with multiple instances](reference/shared-rules.md#working-with-multiple-instances).

1. **Load the schema.** `searchNotes("#llmWikiSchema", fastSearch=true)`. Exactly one hit is
   expected. `getNoteContent` it and follow it. If there is no hit, go to *Bootstrap* below.

2. **Resolve the structure once per session.** `searchNotes("#llmWikiPart")` returns the six
   parts (`schema`, `locks`, `wiki`, `sources`, `templates`, `views`); `searchNotes("#llmWikiTemplate")`
   returns the four templates. Keep the noteIds; only notes that *own* the marker label count
   (instances inherit a template's labels, so filter on `attribute.noteId == note.noteId`).

3. **Take the write lock before the first write**, and release it when done (schema section
   *Write lock*). Other sessions may be writing to the same wiki, and an ETAPI overwrite leaves no
   revision. Reading needs no lock.

4. **Pick the workflow** from what the user asked. Each is specified in the schema; the tool
   mapping is:

   | Schema step | Tools |
   |---|---|
   | Write lock | claim: `createNote` under *Locks* (`<session>: <task>`); check: `searchNotes("note.parents.labels.llmWikiPart = locks note.utcDateModified >= NOW-1800 orderBy note.utcDateCreated")`, yours must be first; keep alive: `putNoteContentById` on the claim; release: `deleteNoteById` |
   | Pending sources | run the view's query: `getNoteById(view)` → `searchString` label → `searchNotes(query)` |
   | File a loose source | a note directly under *Sources* → move it into `Sources/<year>` (`#wikiSourceGroup=<year>`, create if missing); see `trilium-move-note` |
   | Read a source | `getNoteContent`, `getNoteAttachments` + `getAttachmentContent` |
   | Find existing pages | `searchNotes("#wiki #wikiTopic=<slug>")`, `searchNotes("#wiki <title words>")` |
   | Create a page | `createNote` (type `text`, under the hub) then `postAttribute` relation `template` → template id, then the promoted labels (`wikiTopic`, `wikiStatus`, `aiAssisted`) and, for summaries, relation `wikiSource` → the raw note. Same mechanics as `trilium-create-note-from-template`. |
   | Write / extend a page | `getNoteContent` → edit the HTML → `putNoteContentById`. Never replace a page you did not read first. |
   | Link pages | inline `<a class="reference-link" href="#root/<noteId>">Title</a>`; typed edges via `postAttribute` relation `relatesTo` |
   | Clone into a second topic | `postBranch` with the other hub as `parentNoteId` |
   | Log | `getDayNote(today)` → `getNoteContent` → add an `<li>` to the list under `<h2>Wiki</h2>` (create the heading on the first action of the day) → `putNoteContentById` (see `trilium-journal-note` and the schema's *Log format*) |

5. **Respect the boundaries in the schema:** never edit anything under *Sources* (it is
   `#readOnly`; ETAPI would still allow it, so this is on you), never set `#wikiStatus=reviewed`
   yourself, never create a page without first searching for an existing one, and never leave
   a new page unlinked from its hub.

6. **Report back** in the shape the schema asks for: created pages, updated pages, new stubs,
   issues created, open questions for the user. Link noteIds so the user can jump to them.

## Bootstrap (no schema note found)

Offer the user two ways to create the structure. Both are idempotent and safe to re-run.

- **Script (preferred when you have a shell and the ETAPI is reachable from this machine):**
  `python3 <this skill's folder>/setup.py --url <trilium-url> --token <etapi-token>` creates the
  `LLM Wiki` root with `Schema`, `Locks`, `Graph` and `Review graph` (note maps), `Wiki`, `Sources` (plus the current year folder), `Templates` (4) and `Views` (7) under
  `root` (`--parent <noteId>` to put it elsewhere, `--dry-run` to preview). The schema text is
  `schema.html` in the same folder; `--update-schema` pushes a changed file into an existing note.
  That **replaces the whole note**, including conventions the user added to their schema: only use
  it when the user asks, and on a customised schema merge the new default sections in by hand
  instead.
- **Through the MCP tools** (claude.ai, the Claude apps, no shell): read `setup.py`'s declarations
  (`TEMPLATES`, `VIEWS`, the labels on each part) and create the same notes with `createNote`
  and `postAttribute`, then put `schema.html` into the Schema note with `putNoteContentById`.
  Saved searches are `createNote` with type `search` plus a `searchString` label. Note maps are
  `createNote` with type `text`, then `patchNoteById` to type `noteMap`, plus `mapType` and
  `mapRootNoteId` labels.

After bootstrapping, point the user at the schema note and suggest the first ingest: drop a
web clip or article under *Sources* and say "ingest".

## Notes

- `getInboxNote` is Trilium Notes' general inbox (often the day note). Clips the user wants in the
  wiki should be moved under *Sources/<year>* (`patchBranchById` / `postBranch` + `deleteBranchById`,
  see `trilium-move-note`), otherwise they inherit neither `#readOnly` nor `#wikiSource` and never show
  up as pending.
- Search values with hyphens or spaces must be quoted: `#wikiTopic="machine-learning"`.
- A `!=` test on an inherited label (`#wikiType != hub`) only works as the **first** clause of
  a query (Trilium Notes 0.106). Prefer positive filters (`#wikiType=concept`) where you can.
- One ingest is typically 20 to 40 tool calls. Do them; do not summarise a source into a single
  page and stop.
