---
name: manage-note-attributes
description: Add, update, or remove labels and relations on a Trilium note via postAttribute, patchAttributeById, and deleteAttributeById. Use when the user asks to tag a note, add or remove a label/relation, or change an attribute's value — general attribute management, not specifically template promoted attributes (those are covered inline by the template skills).
---

# Manage Note Attributes

Labels (`#name` / `#name=value`) and relations (`~name` pointing at another note) are both "attributes" in Trilium's model. This skill covers ad-hoc tagging and relations generally; the template skills (`create-note-from-template`, `apply-template-to-note`) already handle the `~template` relation and promoted-attribute values inline.

**Patching is limited** (verified by the tool descriptions and consistent with `patchNoteById`/`patchBranchById` behavior elsewhere in this plugin): `patchAttributeById` can only update a label's `value`/`position`, or a relation's `position`. It cannot change an attribute's `name`, `type`, or (for a relation) its target. To change any of those, delete the old attribute (`deleteAttributeById`) and create a new one (`postAttribute`) — don't attempt to patch around it.

## Steps

1. **Resolve the target note** (by title via `searchNotes` or by noteId if given).

2. **Determine the operation**:
   - **Add a new attribute**: ask for the name, whether it's a label or relation, and the value (for a relation, resolve the target note first). `postAttribute` with `noteId`, `type`, `name`, `value`.
   - **Change an existing label's value**: find the attribute (via `getNoteById`'s `attributes` array, matching `name`), then `patchAttributeById` with `attributeId__path` and the new `value`.
   - **Change a relation's target, or rename any attribute**: this isn't a patch — `deleteAttributeById` the old one, then `postAttribute` a new one with the desired `name`/`type`/`value`.
   - **Remove an attribute**: find its `attributeId` the same way, then `deleteAttributeById`.

3. **Confirm before removing** an attribute that looks structurally significant — a `~template` relation, a `#template` label, or a `label:<field>=promoted,...` definition — since removing these changes how the note behaves, not just its metadata. Plain tags/labels don't need this.

4. **Report back**: which attribute(s) changed and their new state. Don't dump the note's full attribute list unless the user asks for it.
