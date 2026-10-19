# The SmartFolder Interview: how a SmartFolder gets designed

*Overview of the interview process in the SmartFolder Skill, current with v6.7.0. Written [260903] for walking a newcomer through the concept; brought up to v6.6.0 [260929], confirmed unchanged by v6.7.0, and punctuated to the repository's public style [261018].*

The skill's stance is that a SmartFolder is **designed, not templated**. The interview is the core of the method, not a preamble to it. Only the safety non-negotiables and the invariant tier model are fixed; everything else is decided per folder.

---

## How it's sequenced

**Phase 0: Intent.** Absorb what you say you want in your own words; confirm scope (this folder only, or siblings too?). Touch nothing.

**Phase 1: Explore and report.** A read-only walk of the tree: folder and file counts, depth, biggest areas, file-type mix, the naming and date conventions *actually in use* (which may differ per subfolder), and oddities that would change the plan: problem characters, extensionless legacy files, scanned PDFs with no text layer, mislabeled files. On a cloud-synced folder (Dropbox, Google Drive, and the like), files that stall or come back empty usually mean online-only placeholders rather than broken files, so it names the fix once instead of diagnosing file by file: the folder must be made available offline, on each machine. It also notes synthesis candidates (folders whose files together tell a story) and folders that are mere piles of like items with no greater whole, which get skipped.

This look happens **before** the real interview, so the questions are grounded in what's actually there rather than asked in the abstract.

**The front-door gate.** If the request was just "organize this folder," with no scheme already chosen, the skill doesn't commit silently to either path. It offers the method once, in plain terms:

> *"I have to understand this folder to organize it well. Want me to write down what I learn while I'm in here, so the next person or session doesn't start over?"*

Two nameable paths: **build** (continue) or **just-organize** (do the requested work well and stop). A declined offer deposits nothing: no scaffolding, no marker, no record of the decline.

---

## The interview itself: seven dials

Run in Phase 2, informed by what Phase 1 found.

| # | Dial | What it asks |
|---|---|---|
| 1 | **Writers and users** | Who adds or edits files: Claude only, one human, several? Through a sanctioned intake path or directly? How technical is each? And **whose files are they?** |
| 2 | **Change velocity** | Archival, slow-drip, or live and fast-moving? |
| 3 | **Dominant question type** | Will people mostly ask *where is X?* (navigation), *how does this work / what matters?* (wisdom), or *where do things stand?* (status) |
| 4 | **Enforcement posture** | Should integrity machinery *offer* (advisory, non-blocking) or *gate* (hard checks before work proceeds)? |
| 5 | **Authority model** | Raw files only? Hand-authored primary notes that must stay primary and in sync? Volatile facts needing one dated source-of-truth surface? |
| 6 | **Audience and tone** | Who reads the guides, and how plain must the language be? |
| 7 | **Agent population** | Claude only, or other AI tools that work in folders too? |

### Two dials with consequences worth calling out

**Dial 1 carries two conditional offers.** If the folder holds files belonging to an owner who isn't driving the build, the skill suggests winning their buy-in *before* the plan executes: a warm, non-technical one-page note saying what will move and why, with nothing deleted. And where several people will use the folder across sessions, it offers a session-flags register: a person-addressed notification surface for "next time X is here, tell them Y." Both are conditional offers, never standing steps; a single-writer folder never sees the second one.

Dial 1 also carries one plain statement rather than an offer. Where the folder is shared over a cloud-sync service, the skill says so while the multi-writer arrangement is being designed: **every collaborator's machine** must hold the folder offline ("Make Available Offline" in Dropbox, offline access in Google Drive, or the equivalent), or that person's sessions read placeholders. It is a per-machine setting, not a one-time folder setting.

**Dial 7 decides the root-file profile.** Claude only → a single root `CLAUDE.md`. Anything else → byte-identical `CLAUDE.md` and `AGENTS.md`, each carrying a reciprocal keep-in-sync instruction, with `AGENTS.md` canonical on divergence. The question is asked in plain product terms without assuming you know what any of them are. If unsure, it chooses single; converting later is one copy plus two lines.

---

## What the answers decide

**Dial 3 is the big one.** The derived-layer budget gets spent where the dominant question lives:

- **Navigation-heavy** → rich `_README.md` coverage with annotated file maps
- **Wisdom-heavy** → syntheses, and perhaps a one-page hub
- **Status-heavy** → status boards, decision logs, indexes, per-file summary sidecars

**Control machinery scales with write-traffic × writer count:** none, then a casual tripwire, then intake discipline with locks and hard integrity gates. Never more than the traffic justifies.

**File-map richness scales down as change velocity rises.** A good renaming pass and a detailed file map are substitutes; in a fast-moving folder, annotate and route rather than enumerate.

**Tone goes to the least technical reader** who will use the folder.

**Proportionality governs everything:** every artifact must pay rent in real signal against its maintenance cost. No rote guides, no unwarranted syntheses, no machinery the folder's needs don't justify.

---

## Three precedents, cited as case law

The skill ships three real SmartFolders built with this method. They share the invariant core *exactly* and spend their budgets completely differently, which is the point.

**The Archive:** 22 years, ~6,700 files, family records. One technical user, near-zero change velocity, dominant question "where is X?" → a `_README.md` in every meaningful folder with full annotated file maps (stable, because content rarely changes); only two syntheses, at genuine arc points; no sidecars, no locks, no boards.

**The Advisory folder:** estate and property records shared with a non-technical owner who edits files directly. Questions are operational: "what's due? how does this system work?" → ~40 per-system syntheses seeded from the owner's hand-authored notes (which stay primary), plus a one-page Operations Hub. Integrity is a non-blocking daily tripwire that *offers* dispositions and never gates. Warm, jargon-decoded tone.

**The Operational folder:** a live multi-user deal workspace on Dropbox. Several writers, daily change, dominant question "where do things stand?" → a one-screen status board, per-initiative decision logs, summary sidecars on most documents. Control machinery is hard: all new content enters through an inbox workflow under a lock, with a content-hash manifest and a session-start scan.

> These are precedents, not menus. Cite them, interpolate between them, depart from them. The test is whether the scaffolding serves *this* folder's diagnostic, not whether it resembles an example.

---

## How the interview closes

Phase 2 ends with a proposal for approval:

- **The profile:** dial readings, the allocation they imply, and the rationale
- **Reorganization scope:** guides only / group into chapters / full restructure with renaming
- **The naming convention**
- **A dry-run plan** showing where every folder and loose file lands, and which folders get which derived surfaces

While naming is on the table, the skill also mentions that at close-out it will suggest adding `SmartFolder` to the folder's own outer name, so the suggestion is no surprise later.

Nothing moves, gets renamed, or gets generated until that plan is approved. Then **Phase 3 builds one chapter end-to-end as a sample**, judged together on whether the guides and syntheses are *genuinely useful*, not merely present, before anything scales.

The profile itself gets deposited into the finished folder, so future sessions inherit the design intent rather than re-deriving it. And a newer version of the skill is treated as a newer opinion, not an authority over a folder already in use; the recorded profile governs unless the owner says otherwise.
