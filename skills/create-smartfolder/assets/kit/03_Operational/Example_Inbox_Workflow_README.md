# XX_Assets-to-File — Inbox for new files
*(Kit exemplar — a condensed sanctioned-intake workflow. The principle: ALL new content enters
through the inbox, because filing is what produces correct naming, sidecars, index updates, and
entity extraction; files placed directly into project folders rot the indexes. Scale the steps to
your folder — a single-user folder needs no lock and may not need the integrity gate.)*

Drop new files here when you want your AI assistant to file them. This README is the workflow the assistant follows
when asked to process the inbox. If the user says "review but don't file yet," do steps 1–2 only.

## Workflow

**00. Acquire the lock (multi-user folders only).** `_INBOX_LOCK.md` in this folder is
self-documenting: acquire if UNLOCKED (confirm after a sync wait; check for conflicted copies),
stop and report if LOCKED (stale >2h or own-lock exceptions apply). Released in step 9.

**0. Run the integrity scan — a hard gate.**
`python3 <meta>/filing_integrity.py scan` diffs the tree against the manifest from the last pass and
surfaces anything added/changed/moved/removed outside this workflow. **If it finds drift, the
findings are the very next thing the user hears about — before step 1.** Disposition each finding
with the user (retro-file it, bless it in place, investigate), and only then continue. Also read the
review queue and surface any *Pending* items. *Why explicit: the observed failure mode is a session
that detects drift, keeps working, and only mentions it when asked — detection without immediate
reporting defeats the purpose.*

**1. Read every file in the inbox** (excluding the lock file and this README, which live here
permanently). Triage PDFs before ingesting: prefer text extraction for dense documents; reserve
multimodal reads for files where the visuals matter. One large file at a time.

**2. Post a one-paragraph understanding of each file in chat immediately** — what it is, who's
involved, key facts, dates — then continue without pausing. Surface anything surprising or
off-scope now, not in the final report. These paragraphs become the sidecar summaries.

**2a. Cross-reference before routing.** For each named person/company, grep the entity index and
search the file tree for existing folders — an existing folder usually dictates the destination.
Treat near-miss name variants as probable transcription aliases of existing entities (match and
note the alias), not as new entities; flag if unsure.

**3. Route each file with the folder's filing decision tree** (the canonical copy lives in the root
`CLAUDE.md`), then confirm destinations, any new-folder proposals, and sidecar choices with the user
via structured questions before moving anything.

**4. Rename to convention and move.** Move, don't copy — a filed file should no longer exist in the
inbox. Follow the folder's naming rules, including any chronological-prefix exception for
date-led folders.

**5. Write a sidecar per filed document that meets the sidecar triggers** (see the prompt/kit:
expensive-to-read × repeatedly-consulted). Include the step-2 paragraph, key facts with page
pointers, and entities mentioned.

**6. Extract entities** into the folder's entity index (add/revise, never rewrite hand-curated
entries; record aliases).

**7. Close the loop on derived surfaces.** Update the local surfaces the filing touched — the
folder's `INDEX.md` or `_README.md`, the status board row (with its as-of date) if status moved,
`DECISIONS.md` if a dated decision was made, any `_Synthesis.md` now stale — then check the decay
conditions of the surfaces on the root file's distant list. A refresh reconciles the **whole**
surface, not just the section the filing touched. And when a **concrete, named pattern** in this
batch suggests a missing surface, consult the growth menu (`<meta>/GROWTH_MENU.md`) and offer it
in one line; log a decline there.

**8. Meeting extracts (if the folder uses them):** when a multi-initiative meeting record is filed,
every initiative named in its filename codes receives an extract — the codes are a contract.

**9. Re-snapshot and release the lock.**
`python3 <meta>/filing_integrity.py snapshot` records the newly-blessed state; then set the lock
back to UNLOCKED with a one-line outcome.

**10. Report:** what moved where, which surfaces were updated, what's staged for manual deletion,
and anything flagged for the maintainer.
