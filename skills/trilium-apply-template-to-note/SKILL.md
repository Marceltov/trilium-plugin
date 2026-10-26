---
name: trilium-apply-template-to-note
description: Retroactively attach an existing note in Trilium Notes to a template via a ~template relation, which merges the template's child-note structure, content, and promoted attributes onto that note. Use when the user asks to convert, retrofit, or "make this note use" an existing template. This overwrites the target note's content and adds child notes to it — always confirm before writing.
---

# Apply an Existing Template to an Existing Note

Same underlying mechanism as `trilium-create-note-from-template` (attaching a `~template` relation), but applied to a note that may already have real content and children — which makes this the destructive one of the template skills. Once the `~template` relation is attached, the target note's **content is replaced** with the template's content, and the template's child notes are cloned in as new children under the target. This is not reversible by simply deleting the relation.

If more than one Trilium Notes instance is connected this session, resolve which one to use first — see [Working with multiple instances](reference/shared-rules.md#working-with-multiple-instances).

## Steps

1. **Resolve the target note** (by title via `search_notes` or by noteId if given) and the **template note** (same resolution as `trilium-create-note-from-template` step 1: noteId if given, else `search_notes("#template")` matched by title, asking if ambiguous).

2. **Before writing anything**, fetch both notes' current state (`get_note` + `get_note_content` for each) and summarize for the user: the target's current content (non-empty? roughly how much?) and existing child-note count — call out specifically if either is non-trivial, since both are at risk — and the template's child-note count and title, so the user knows what's about to be merged in.

3. **Get explicit confirmation** (e.g. via `AskUserQuestion`) before proceeding. If the user declines, stop — do not attach the relation.

4. **On confirmation**, `set_attribute` with `type: relation`, `name: template`, `value: <template noteId>`, `noteId: <target noteId>`. If the target already has a `~template` relation, this **replaces** it (`set_attribute` updates an attribute of the same name) — say so in step 2.

5. **Re-fetch the target note** to confirm the relation applied, then walk the user through the promoted-attribute value prompts exactly as in `trilium-create-note-from-template` steps 5–7.

6. **Report back**: confirm the relation is attached, how many child notes were added, and which promoted attributes were set.
