---
name: journal-note
description: Get or append to Trilium's journal notes — the day, week, month, or year note for a given date — via getDayNote/getWeekNote/getMonthNote/getYearNote. Use when the user asks about today's note, a specific day's journal entry, or wants to jot something into their daily/weekly/monthly/yearly note.
---

# Work With Journal (Calendar) Notes

Trilium's journal feature gives every day, week, month, and year its own note, created on first access. These MCP tools return (and create, if missing) that note:

- `getDayNote(date)` — `YYYY-MM-DD`
- `getWeekNote(week)` — ISO week, `YYYY-Www`
- `getMonthNote(month)` — `YYYY-MM`
- `getYearNote(year)` — `YYYY`

Note content is HTML (`text/html` notes), not plain text — appending requires wrapping additions in a tag (e.g. `<p>...</p>`), not just concatenating a raw string, or the addition won't render as a separate block.

If more than one Trilium instance is connected this session, resolve which one to use first — see [Working with multiple instances](../README.md#working-with-multiple-instances).

## Steps

1. **Determine which period the user means** (day, week, month, or year) and resolve the date — "today" needs today's actual date, not a guess; a relative reference ("last Monday", "next month") needs converting to the matching format before calling the tool.

2. **Fetch the note** with the matching `get*Note` tool. This both resolves the noteId and creates the note if it didn't already exist — mention if it was just created versus already there (compare `dateCreated` to now, roughly).

3. **If the user wants to read it**: `getNoteContent` and show it back (rendered sense, not raw HTML tags, unless they ask for the source).

4. **If the user wants to add something**: `getNoteContent` first, append the new text wrapped as its own block (e.g. `<p>New content</p>`) to the existing HTML, then `putNoteContentById` with the combined content. Don't overwrite what's already there.

5. **Report back**: which journal note was affected (date/period) and what changed.
