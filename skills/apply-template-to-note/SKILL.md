---
name: apply-template-to-note
description: Retroactively attach an existing Trilium note to a template via a ~template relation, which merges the template's child-note structure, content, and promoted attributes onto that note. Use when the user asks to convert, retrofit, or "make this note use" an existing template. This overwrites the target note's content and adds child notes to it — always confirm before writing.
---

# Apply an Existing Template to an Existing Note

Same underlying mechanism as `create-note-from-template` (attaching a `~template` relation), but applied to a note that may already have real content and children — which makes this the destructive one of the template skills. Verified against a live instance: once the `~template` relation is attached, the target note's **content is replaced** with the template's content (they end up sharing a blob), and the template's child notes are cloned in as new children under the target. This is not reversible by simply deleting the relation.

If more than one Trilium instance is connected this session, resolve which one to use first — see [Working with multiple instances](../README.md#working-with-multiple-instances).

## Steps

1. **Resolve the target note** (by title via `searchNotes` or by noteId if given) and the **template note** (same resolution as `create-note-from-template` step 1: noteId if given, else `searchNotes("#template")` matched by title, asking if ambiguous).

2. **Before writing anything**, fetch both notes' current state (`getNoteById` + `getNoteContent` for each) and summarize for the user: the target's current content (non-empty? roughly how much?) and existing child-note count — call out specifically if either is non-trivial, since both are at risk — and the template's child-note count and title, so the user knows what's about to be merged in.

3. **Get explicit confirmation** (e.g. via `AskUserQuestion`) before proceeding. If the user declines, stop — do not attach the relation.

4. **On confirmation**, `postAttribute` with `type: relation`, `name: template`, `value: <template noteId>`, `noteId: <target noteId>`.

5. **Re-fetch the target note** to confirm the relation applied, then walk the user through the promoted-attribute value prompts exactly as in `create-note-from-template` steps 5–7 (find the template's promoted attribute definitions surfaced on the target, ask for values, write them with `postAttribute`).

6. **Report back**: confirm the relation is attached, how many child notes were added, and which promoted attributes were set.
