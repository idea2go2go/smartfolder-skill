# CLAUDE.md — how to work in the Willow Farm SmartFolder
*(Kit exemplar — fictionalized advisory-tier root file. Match the shape, not the contents.)*

Willow Farm (a country property) is a **SmartFolder**: a navigation layer sits on top of the real
files so anyone — or a future Claude session — can stand at any folder and get the valuable answer
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
Deletion is blocked here. Move anything to remove into **`XX_DELETE-MANUALLY/`** (the owner empties
it from Finder). Same for anything you'd overwrite: stage the old version, don't destroy it.

## Inbox — `XX_ASSETS-TO-FILE/`
The owner's drop-off for new items. When asked to process it, route each item to its folder and
refresh that folder's `_Synthesis.md`. Clear items as they're filed.

## Change tracking — a casual tripwire (non-blocking)
A watcher (`XX_META/smartfolder_watch.py`) catches files added or changed directly (not via the
inbox). It never gates. Behavioral rule: answer the first substantive request normally, then check
`XX_META/_manifests/last_check`; if it isn't today's date, offer once to run the daily check. Full
procedure: `XX_META/Change_Tracking_Procedure.md`.

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

## Top-level orientation (chapters — deeper levels route themselves)
- **`_Willow_Operations_Hub.md`** — start here: maintenance calendar, vendor directory, sensitive-info map.
- **House Systems** — HVAC, generator, well & water, security (each with a MASTER-seeded `_Synthesis.md`).
- **Grounds** — garden, pond, fencing, equipment.
- **Legal · Tax · Insurance** — ownership, coverage, filings.
- **XX_META/** — method spec, recorded profile, change tracker, runbook (owner can ignore).

## Maintenance
Refresh a folder's `_Synthesis.md` (and its as-of date) when its files change; update the Hub when a
vendor, due date, or secret location changes; update this orientation only if a top-level chapter
changes. The design profile and full runbook live in `XX_META/` — future sessions should read the
recorded profile there before adding or removing machinery.
