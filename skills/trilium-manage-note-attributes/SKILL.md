---
name: trilium-manage-note-attributes
description: Add, update, or remove labels and relations on a note in Trilium Notes via set_attribute, get_attributes and delete_attribute. Use when the user asks to tag a note, add or remove a label/relation, or change an attribute's value — general attribute management, not specifically template promoted attributes (those are covered inline by the template skills).
---

# Manage Note Attributes

Labels (`#name` / `#name=value`) and relations (`~name` pointing at another note) are both "attributes" in Trilium Notes' model. This skill covers ad-hoc tagging and relations generally; the template skills (`trilium-create-note-from-template`, `trilium-apply-template-to-note`) already handle the `~template` relation and promoted-attribute values inline.

**`set_attribute` adds or replaces** (verified against a live instance): if the note already owns an attribute with the same type and name, its value is updated; otherwise a new one is created. So it can't add a *second* label of the same name (`#tag=one` and `#tag=two`); the second call overwrites the first. For a repeated label, tell the user and suggest adding it in Trilium Notes.

If more than one Trilium Notes instance is connected this session, resolve which one to use first — see [Working with multiple instances](reference/shared-rules.md#working-with-multiple-instances).

## Steps

1. **Resolve the target note** (by title via `search_notes` or by noteId if given).

2. **Determine the operation**:
   - **Add an attribute, or change a label's value or a relation's target**: `set_attribute` with `noteId`, `type` (`label` or `relation`), `name`, `value` (for a relation, the target noteId; resolve the target note first). Check `get_attributes` first if the name may already exist, and say that its value will be replaced.
   - **Rename an attribute or change its type**: `delete_attribute` the old one, then `set_attribute` the new one.
   - **Remove an attribute**: find its `attributeId` in `get_attributes` (only ones the note owns, not inherited ones), then `delete_attribute` with `noteId` and `attributeId`.

3. **Confirm before removing or replacing** an attribute that looks structurally significant — a `~template` relation, a `#template` label, or a `label:<field>=promoted,...` definition — since that changes how the note behaves, not just its metadata. Plain tags/labels don't need this.

4. **Report back**: which attribute(s) changed and their new state. Don't dump the note's full attribute list unless the user asks for it.
