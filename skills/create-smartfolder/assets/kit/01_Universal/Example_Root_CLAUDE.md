# CLAUDE.md — how to work in the Willow Farm SmartFolder
*(Kit exemplar — fictionalized advisory-tier root file, shown in the single-agent profile. Match
the shape, not the contents.)*

> **Dual profile:** this file also exists byte-identically as `AGENTS.md`. Copy this guard,
> verbatim, near the top of **both** files: *"This file exists twice, byte-identical: `CLAUDE.md`
> and `AGENTS.md`; `AGENTS.md` is canonical on divergence — repair by re-copying from it. Any
> change to one must be applied to the other before the task completes; verify with
> `cmp AGENTS.md CLAUDE.md` — silence means identical."*

Willow Farm (a country property) is a **SmartFolder**: a navigation layer sits on top of the real
files so anyone — or a future AI session — can stand at any folder and get the valuable answer
without opening every file. You find things **by location, not a central index**. The method spec and
the change-tracker live in `XX_META/` (the owner can ignore it).

## How to navigate (read top-down; stop when you have enough)
1. This file — protocol, conventions, behavioral rules, and the orientation below.
2. The Operations Hub (`_Willow_Operations_Hub.md`) for cross-cutting questions, or go straight to
   the relevant area's `_Synthesis.md`.
3. Branch by question type: whole-folder story → that folder's `_Synthesis.md`; one specific file →
   its `<stem>_Summary.md` sidecar → the raw file. Descend only as far as the question needs.

## Navigation protocol
Every meaningful folder has a `_README.md`; before working in or answering about a folder, read it
first. Tiny/leaf folders are covered by the parent's guide; if a folder has none, read the parent's.

## Freshness & precedence
- Every guide and derived surface carries an `As of [YYMMDD]` line. When sources disagree, the more
  recent as-of date wins.
- A `_Synthesis.md` (or any derived surface) is AI analysis — a raw file wins over it on conflict.
- The live directory listing outranks any guide's file map.
- When a derived surface is materially behind its folder's newest content, proactively **offer to
  refresh it** before relying on it.

## Conventions (true regardless of date)
- Guides `_README.md`; whole-folder analysis `_Synthesis.md`; per-file digests `<stem>_Summary.md`.
- Names lead with a date (`YYMMDD`/`YYMM`, no dashes); PascalCase within one concept, underscores
  between concepts; theme-first: `DATE_Type_Specifier.ext`.
- macOS bundles (`.pages/.numbers/.key/.rtfd`) are atomic — never recurse into or write inside them.

## Deletion & staging
Deletion is blocked here. Move anything to remove into **`XX_DELETE_MANUALLY/`** (the owner empties
it from Finder). Same for anything you'd overwrite: stage the old version, don't destroy it.
Staged content never re-enters this folder's knowledge layer — not read, quoted, reconciled
against, or restored from. One exception: keep a light `_README.md` manifest there, one line per
staged item (what, when, why, where the surviving copy is), written when you stage. It is consulted
only to answer questions about the disposal itself, and it resets when the owner empties the folder.

## Inbox — `XX_INBOX/`
The owner's drop-off for new items. When asked to process it, route each item to its folder and
refresh that folder's `_Synthesis.md`. Clear items as they're filed.

## Session boundaries (the start-and-end duties, grouped — one line each; detail lives where the line points)
- **Session start:** after answering the first substantive request, if `XX_META/_manifests/last_check`
  isn't today's date, offer the change check once (detail: *Change tracking*, below).
- **Once a calendar month:** run the version check — procedure and `Last checked` stamp in
  `XX_META/VERSION_BASELINE.md`. Current month already stamped → nothing to do.
- **Before finishing:** close the loop (rules below).

*A duty adopted later — a flags register, an integrity scan — adds one line here, never a rule
elsewhere. Triggers live in this file because it is the one file guaranteed to be read; a duty
parked anywhere else misses silently.*

## Change tracking — a casual tripwire (non-blocking)
A watcher (`XX_META/smartfolder_watch.py`) catches files added or changed directly (not via the
inbox). It never gates; its session-start offer is the first line of *Session boundaries* above.
Full procedure: `XX_META/Change_Tracking_Procedure.md`.

## Keeping live surfaces current (write forward, not backward)
- A live surface (the Hub, the `_Synthesis.md` of a system still in service) leads with the
  present: current state + what's next. A newcomer's first screen should answer "where do things
  stand?" without summing dated patches.
- Refreshing means REWRITING that front matter, not appending a dated note on top. Small dated
  deltas may accrete between rewrites — but at a chapter boundary (a system or vendor replaced, a
  project closed) rewrite the surface state-first and move the old regime, whole and dated, into a
  labeled history section with one pointer. History is never deleted — that's what makes rewriting
  safe.
- When a surface reads as more history than present, a rewrite is due — offer it (procedure in
  the `XX_META/` runbook).

## Close the loop (when your work changed files)
- Before finishing, update the derived surfaces in the folders you worked in — the navigation
  protocol has already put them in front of you.
- Then check the decay conditions of the surfaces that sit outside any one work area's read path.
  Here that list is: **`_Willow_Operations_Hub.md`** (it makes claims about vendors, due dates, and
  secret locations across every area). A surface describing a state *outside this folder* — what a
  contractor holds, what was filed with the county — would join this list by definition; none
  exists today.
- A refresh reconciles the **whole** surface against present state, not just the section you came
  for — patching one section is how a stale sentence survives a "refresh."
- Point-in-time state (counts, versions, statuses) lives on dated surfaces, never in this file —
  this manual states rules and points at state. A fact here that needs a date is in the wrong file.

## Top-level orientation (chapters — deeper levels route themselves)
- **`_Willow_Operations_Hub.md`** — start here: maintenance calendar, vendor directory, sensitive-info map.
- **House Systems** — HVAC, generator, well & water, security (each with a MASTER-seeded `_Synthesis.md`).
- **Grounds** — garden, pond, fencing, equipment.
- **Legal · Tax · Insurance** — ownership, coverage, filings.
- **XX_META/** — method spec, recorded profile, change tracker, version baseline, runbook (owner can ignore).

## Maintenance
Refresh a folder's `_Synthesis.md` (and its as-of date) when its files change; update the Hub when a
vendor, due date, or secret location changes; update this orientation only if a top-level chapter
changes. The design profile and full runbook live in `XX_META/` — future sessions should read the
recorded profile there before adding or removing machinery.
