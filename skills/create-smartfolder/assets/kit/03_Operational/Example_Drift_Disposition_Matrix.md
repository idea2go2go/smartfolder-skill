# Drift disposition matrix — what to do with each finding type
*(Kit exemplar — the hard integrity gate's companion reference, fictionalized from a live
multi-writer workspace. It sits **behind** `filing_integrity.py`: the script detects; this file is
the judgment reference for dispositioning what it detects.)*

**Warranted when:** the diagnostic already warrants the hard gate — multiple writers, drift
expensive to repair, indexes and entity machinery that depend on filing discipline. **Do not
transplant this into advisory folders because thorough feels better.** The advisory tier's casual
four-option offer (file it / note to the maintainer / remind me later / dismiss) is a deliberate
counterpart for folders where stakes are personal, not a lesser version awaiting upgrade. Folders
with no detector need none of this. Pick the lowest tier the diagnostic supports.

**The three integrity species, so you reach for the right one:** the **advisory tripwire**
(`smartfolder_watch.py`) *offers* and never blocks; the **hard gate** (`filing_integrity.py`)
blocks a filing pass until drift is dispositioned; the **generator's content-hash markers**
(`gen_readmes.py`) protect *generated guides* from being overwritten on re-runs — guide
protection, a different job from drift detection. This matrix serves the second species only.

## First rule: report before anything else

When `scan` finds drift, the findings are the very next thing the user hears — before reading
inbox files, before any other work. The observed failure mode is a session that detects drift,
keeps working, and mentions it later. Report every finding with the size information the script
prints, disposition each with the user, and only then resume.

## The matrix

### ADDED — a file the manifest doesn't know about

It skipped the inbox. Flag it with path and size, restate the rule kindly (new content enters
through the inbox, because filing is what produces correct naming, sidecars, entity extraction,
and index updates), and offer:

1. **Retro-file it (recommended for anything with real content).** Move it to the inbox and run
   the normal workflow — it may land back in the same folder, but named, summarized, and indexed.
   **This is the only path that reads the file**, captures its people and companies into the
   entity index, and writes its sidecar.
2. **Bless it in place.** It enters the manifest at the next snapshot. **Blessing records a hash
   and nothing else** — no read, no sidecar, no entities, and nothing will do those later; a
   blessed file belongs to no batch and never resurfaces as a reminder. Reserve this for files
   with no entity or index value.

Files the assistant itself created this session as sanctioned work (sidecars, a regenerated
board) are expected — note them, don't treat them as violations.

### CHANGED — same path, different content

**Not presumed bad** — someone may have edited it on purpose. Report the size delta and direction,
then ask what follow-up the edit needs: re-read the content; update its sidecar; re-run entity
extraction; update affected indexes; or accept with no follow-up (noting that accepting skips
re-extraction — new names in the edit won't reach the entity index). Call out a large shrink
explicitly: it can mean truncation or an overwrite with the wrong file.

### MOVED / RENAMED — identical content at a new path

Ask whether it was intentional. If yes: check whether indexes and sidecars referencing the old
path need updating, and whether the new name follows the folder's convention. If no: offer to
move it back.

### REMOVED — a manifested file no longer present

A person did this (assistant sandboxes typically cannot delete). Normal if it was staged into the
manual-delete folder during a sanctioned cleanup; otherwise flag possible accidental loss, and
flag any indexes or sidecars now pointing at nothing.

### After resolution

Run `snapshot` so the manifest reflects the agreed state. **Never snapshot over unresolved drift —
snapshot is approval.**

## `snapshot` vs `bless-file` — the load-bearing distinction

`snapshot` rewrites the whole manifest, blessing *everything* currently on disk — including any
unrelated drift that happens to coexist. Use it only at the end of a filing pass, when the whole
tree is meant to be the new baseline. `bless-file` upserts one path and leaves all other drift
flagged. **Muting one item is always `bless-file`, never `snapshot`** — snapshot-as-mute is the
silent-approval failure.

## The review-queue lifecycle (mute and record)

For drift that surfaces to someone who isn't the maintainer, "flag it for review" does two things,
in this order: **(1) append a *Pending* entry** to the review queue (path, finding, who flagged
it, any note), **then (2) mute that one file** with `bless-file`. Record first, then mute — never
mute without recording. The maintainer processes *Pending* items at the next filing pass and moves
each to *Resolved* with disposition and date; the end-of-pass snapshot re-blesses the properly
filed state. Only an *explicit* flag or bless mutes anything; "just continue" leaves drift flagged
as the safety net. (Format: `Example_REVIEW_QUEUE.md`.)

**What CLEAN means once muting exists:** a CLEAN scan alone no longer means "all filed." CLEAN
*and* an empty Pending queue = all filed; CLEAN *with* a non-empty queue = filed-or-pending. Check
both. A muted file that changes again re-flags as normal drift — handle it fresh and reconcile the
stale queue entry at review time.

## Raising drift with someone who didn't make the change (sample wording, not a script)

The person present is often not the person who edited, and carries no context that filing
discipline matters here. No-blame, and an easy out:

> Before I dig into that — a quick heads-up. I run a light file-integrity check at the start of
> the day, and it looks like `Deal_Room/Vendor_Notes.md` was edited outside the usual filing
> process since the last checkpoint (it grew by about 310 B). That's often perfectly fine — someone may
> have updated it on purpose, and it needn't have been you. It only matters because direct changes
> don't get re-summarized or re-indexed. Nothing has to happen right now: I can file it in
> properly, flag it for the maintainer to look at later, or note that it's fine as-is — and I'll
> leave the file exactly as it is either way. Now, on to what you actually asked.

Preserve the substance (what changed, that it may well be fine, that they choose — including
choosing nothing), adapt everything else to the person and the moment.

## Two operational hazards that generalize

- **Sync hydration lag.** On synced volumes, file tools may write through a provider whose mount
  the scanner reads late — a `snapshot` taken right after edits can record **pre-edit content for
  every file the session touched**, surfacing later as phantom CHANGED findings. Before the final
  snapshot, verify from the shell that each edited file contains its newest change. If a scan
  flags exactly the set of files a logged session edited, suspect this first.
- **App and OS by-products.** Office `~$…` locks, `.~lock…#` files, `desktop.ini`, `Thumbs.db`,
  `.DS_Store` appear and vanish when someone merely opens or browses. Keep them in the scanner's
  ignore-list or they generate recurring phantom findings.
