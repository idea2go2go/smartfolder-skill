# Change tracking — full procedure
*(Kit artifact — modelled on a live advisory-tier SmartFolder. The companion script is
`smartfolder_watch.py` in this kit folder. Adapt the ignore-lists and the maintainer's name.)*

*Read-on-demand operational detail for the casual change-tracker. The behavioral rule (when/why to
run it) lives in the root `CLAUDE.md`; this file is the how.*

## What it is

A small, non-blocking watcher — `XX_META/smartfolder_watch.py` — that notices files **added or
changed directly in the folder** (i.e. not dropped in the inbox), so they can be offered up for
filing and the derived summaries don't quietly fall behind the raw files. It is a friendly tripwire,
**never a gate**: it informs, then the session continues with whatever was asked.

Everything it needs lives in `XX_META/`: the script, the baseline
(`_manifests/manifest.tsv` — one line per tracked file: `relative_path · size · mtime · sha1`), and
the daily stamp (`_manifests/last_check`).

## The two commands

- `python3 XX_META/smartfolder_watch.py snapshot` — write/refresh the baseline ("this is the new normal").
- `python3 XX_META/smartfolder_watch.py check [--daily]` — diff the live tree vs the baseline; print
  `ADDED` / `CHANGED` / `REMOVED` (or `CLEAN`).

## The once-per-day gate (the `last_check` stamp)

`check --daily` first reads `last_check`. If it already contains today's ISO date, the command exits
silently. Otherwise it runs the check and writes today's date. So repeated `--daily` calls across
sessions in one day are no-ops after the first — the stamp is the whole mechanism. A plain `check`
ignores the stamp and always runs (the "any stray files?" on-demand path).

**Behavioral trigger (lives in the root `CLAUDE.md`):** answer the first substantive request of the
session first; then, at the end of that first reply, read `last_check`. If it is not today's date,
**offer** to run the daily check — do not run it unprompted. Ask at most once per session; if
declined, don't nag — the stamp advances only when the check actually runs, so a deferred day simply
re-prompts next session. Nothing found → say nothing. Something found → mention it in a line or two,
**still do the request**, then make the offer below.

## The offer when drift is found (an offer, not an order; no-blame)

Briefly name what changed (path + size delta), note it bypassed the inbox so the summaries don't yet
reflect it, and — in a shared folder the person present may not be who changed it, so keep it light —
offer four choices:

1. **File it in (default).** Route and name the file, update that folder's `_Synthesis.md` (and offer
   to fold relevant bits into any hand-authored master note), then re-`snapshot`.
2. **Draft a note to the maintainer.** Compose a short, copy-pasteable note in chat describing the
   file(s), for the owner to send to whoever maintains this SmartFolder. Leave the file in place; do
   **not** re-snapshot.
3. **Remind me next time.** Do nothing; it resurfaces at the next check as a standing nudge.
4. **Dismiss as not-for-filing (rare).** Only for genuine non-content (sanctioned Claude output or
   confirmed junk). Re-`snapshot` to clear it. Deliberately the least-used path.

## Re-baseline discipline (why a CLEAN check is meaningful)

Re-`snapshot` **only** after (1) filing or (4) dismissal — never to silence a finding. Because the
baseline is rewritten only when content is genuinely filed or declared non-content, a CLEAN check
truly means "everything in this folder is reflected in the summaries." (The tool is stateless — no
per-file mute; a finding stops surfacing only by being filed or dismissed.)

## What's tracked vs ignored

- **Tracked:** the owner's raw files, including any hand-authored master notes (so direct edits to
  them are caught).
- **Ignored:** the inbox, trash/staging, `XX_META` itself, hidden/OS cruft (`.DS_Store`, dotfiles),
  office lock/temp files (`~$…`, `.tmp`), `CLAUDE.md`, and all Claude-derived guides (`_README.md`,
  `_Synthesis.md`, `*_Summary.md`, hubs).
- **macOS bundles** are tracked as a single unit (size + newest mtime), never recursed into.

## Detection method (why checks stay near-instant)

Hybrid: if size and mtime both match the baseline, trust unchanged (no hashing). If size differs, it
changed. If size matches but mtime moved, re-hash; a matching hash means a sync-only touch (treated
unchanged), otherwise it genuinely changed. Only files that look different are ever re-read.

*To refresh: ask Claude to update this procedure.*
