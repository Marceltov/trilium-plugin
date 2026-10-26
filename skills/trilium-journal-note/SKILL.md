---
name: trilium-journal-note
description: Get or append to Trilium Notes' journal notes — the day, week, month, or year note for a given date — by finding them through their #dateNote/#weekNote/#monthNote/#yearNote labels. Use when the user asks about today's note, a specific day's journal entry, or wants to jot something into their daily/weekly/monthly/yearly note.
---

# Work With Journal (Calendar) Notes

Trilium Notes' journal gives every day, week, month, and year its own note under the note labelled `#calendarRoot`. The built-in MCP server has no journal tool, so find them by their labels (values with hyphens must be quoted):

| Period | Query | Title, for reference |
|---|---|---|
| Day | `#dateNote="2026-10-24"` | `24 - Saturday`, under the month note |
| Week | `#weekNote="2026-W43"` | `Week 43` |
| Month | `#monthNote="2026-10"` | `10 - October`, under the year note |
| Year | `#yearNote="2026"` | `2026`, under `#calendarRoot` |

If more than one Trilium Notes instance is connected this session, resolve which one to use first — see [Working with multiple instances](reference/shared-rules.md#working-with-multiple-instances).

## Steps

1. **Determine which period the user means** and resolve the date — "today" needs today's actual date, not a guess; a relative reference ("last Monday", "next month") needs converting to the matching format first.

2. **Find the note** with `search_notes` and the matching query (`fastSearch: true`).

3. **If it doesn't exist yet**, Trilium Notes creates it the next time someone opens that date in the app. If the user wants to write now, create it in the same place Trilium would: under the parent period's note (day under month, month under year, year under `#calendarRoot`), creating missing parents the same way, with a title in the format of its siblings and the matching label (`set_attribute`, e.g. `dateNote` = `2026-10-24`). Say that you created it.

4. **If the user wants to read it**: `get_note_content` and show it back (it comes as Markdown).

5. **If the user wants to add something**: `append_to_note` with the new text as Markdown (its own paragraph or list item). It keeps what's already there. To insert somewhere other than the end, `get_note_content`, edit, then `set_note_content` with the whole note.

6. **Report back**: which journal note was affected (date/period) and what changed.
