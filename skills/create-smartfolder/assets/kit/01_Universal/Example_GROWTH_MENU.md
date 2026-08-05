# Growth menu — what this folder could grow, and how to build it
*(Kit exemplar — deposited into each SmartFolder's meta folder in Phase 5, adapted to that folder:
keep both tables whole, fill in the "Adopted?" column from the recorded profile, and start the
considered-and-declined log with anything the build discussed and turned down.)*

**As of [YYMMDD].** A SmartFolder inherits the surfaces and machinery it was built with, but not
the menu of what else could exist. This is that menu. It covers **two axes** that are allocated by
different rules and are easy to confuse:

- **Derived surfaces** hold digested knowledge. Allocation rule: *spend the budget where the
  dominant question lives.*
- **Control machinery** holds no knowledge at all — a manifest is a list of hashes, a detector is
  a script. Allocation rule: *scale with write-traffic × writer count, and pick the lowest tier
  the diagnostic supports.*

Mixing them produces exactly the wrong instinct — reaching for a hard gate because a folder feels
important, or skipping a synthesis because the folder feels quiet.

## How to use this

**This menu is for building from, not just consulting — when a trigger fires and the user
approves, implement it.** But never build unprompted, and never pitch in the abstract.

1. A **concrete, named pattern** appears in real material — not a hunch that a surface would be
   nice.
2. Consult this menu and **offer** it in one line, naming the pattern: *"three filings this month
   touch the easement — want a tracker?"*
3. If accepted: build it from the implementation pointer — **read the referenced kit artifact
   rather than reconstructing it from this file's one-line description.** Then amend the recorded
   profile, add a row to the relevant folder guide, and log the decision. **If the new surface is
   distant** — it makes claims about material that does not sit beside it — **add it to the root
   file's close-the-loop list** (both root files, in a dual-agent folder); when retiring a distant
   surface, remove it from that list in the same pass.
4. If declined: **log it below** and do not re-offer until circumstances materially change.
   Repeated pitching is proposal fatigue — the recurring form of over-machinery.

**On the implementation pointers.** They name artifacts in the SmartFolder Skill kit, written
against **v6.3.0**. The kit travels inside the `.skill` package deposited beside this menu as the
version baseline — unpack it when a pointer is needed. **The artifact is the specification and
this menu is only the index**: where they disagree, the artifact wins. A newer skill version is a
newer *edition* of both — an input to the version-upgrade review, which the recorded profile
governs; it never overrides this folder's recorded decisions on its own. If the artifact is
missing, the "what it is" column carries enough to act on — carefully, and say so.

## Axis 1 — derived surfaces

Every one obeys the shared discipline: an `As of [YYMMDD]` line; claims anchored in-narrative;
**provenance**; a **decay condition**; a label as derived AI analysis (raw wins on conflict); the
breadcrumb *"To refresh: ask your AI assistant to update this"*; and written **forward** — present
state first, rewritten at chapter boundaries rather than patched.

| Surface | What it removes | Offer it when… | Build from | Adopted? |
|---|---|---|---|---|
| **Synthesis** (`_Synthesis.md`) | Reading a whole folder to learn its story | A folder's files together tell an arc no one of them tells | `01_Universal/Example_Synthesis.md` | |
| **Status board** | Getting an archaeology answer to "where do things stand?" | Several workstreams move at different speeds and someone returns after a gap | `03_Operational/Example_STATUS_BOARD.md` | |
| **Decision log** | Re-litigating settled questions | Decisions recur and their *reasoning* matters later, not just the verdict | `03_Operational/Example_DECISIONS.md` | |
| **Sidecar summary** | Re-reading an expensive file | Read-cost × consultation-frequency is high: long PDFs, transcripts, scans, authority documents | `01_Universal/Example_Sidecar_Summary.md` | |
| **Longitudinal tracker** | Chasing one subject across many files and years | A single subject threads through many filings over time — a negotiation, a recurring fault, an open question | No exemplar; nearest is the synthesis | |
| **Cross-folder hub** | Hunting for recurring obligations | Obligations, contacts, or dates surface repeatedly across several chapters | `02_Advisory/Example_Operations_Hub.md` | |
| **Computed view** (dashboard, table) | Manual counting | The structured layer is large enough that a script answers better than prose | No exemplar; build to the shared discipline | |
| **Changelog / release notes** | Reconstructing what changed between versions | More than two versions of something exist and other people hold older ones | No exemplar | |
| **Entity index** | Remembering who is involved in what | Names recur across many files and someone needs "everything touching X" | No exemplar | |
| **Annotating vs enumerating guide** | Either a stale file map or an opaque folder | Enumerate where names can't speak for themselves; annotate where change velocity is high | `01_Universal/Example_README_Annotating.md`, `Example_README_Enumerating.md` | |
| **Owner welcome guide** ("your records, made answerable") | A non-technical owner never learning what their folder can now do | A non-technical owner uses the folder — at handoff, or when one is invited in later | `01_Universal/Example_Owner_Guide.md`; deliver as a polished PDF at the root | |
| **Session flags** (person-addressed register) | Cross-session asks and tells getting lost, manually re-raised, or bloating the root file | Several people use the folder and someone who won't be present until a future session needs to be told or asked something — *collaborative folders only; a single-writer folder is never shown this row* | `03_Operational/Example_SESSION_FLAGS.md` — the register holds all content and state; the root file carries only the trigger, and delivery wires to wherever the folder's session boundaries live | |

## Axis 2 — control machinery

**Escalation logic, in one line each.** Pick the *lowest* tier the diagnostic supports; machinery
above a folder's needs trains people to ignore the system.

- **No machinery:** one writer, changes flow through AI sessions → as-of dates are protection
  enough.
- **Advisory:** humans edit directly but the stakes are personal → a tripwire that *offers*.
- **Operational:** several writers, live workstream, shared indexes → intake discipline, a lock,
  and a scan that *gates* filing passes.

| Machinery | What it does | Warranted when… | Build from | Adopted? |
|---|---|---|---|---|
| **Drift detector + manifest** | Non-blocking tripwire: hashes tracked files against a baseline and reports files added, changed, moved, or removed outside the sanctioned path | Humans edit files directly and you want to *know*, not to *block* | `02_Advisory/smartfolder_watch.py`, `Change_Tracking_Procedure.md`, `Example_manifest_rows.tsv` | |
| **Hard integrity gate** | SHA-1 manifest with `snapshot` / `scan` / `session-start` / `bless-file` modes; drift blocks a filing pass until dispositioned | Multiple writers, drift is expensive to repair, and indexes depend on discipline | `03_Operational/filing_integrity.py` + `Example_Drift_Disposition_Matrix.md` | |
| **Content-hash guide markers** | The third integrity species — protects *generated guides* so a regeneration preserves hand edits instead of overwriting them | A generator emits scaffolding across a large tree that humans then edit | `04_Generator/gen_readmes.py`, `GENERATOR_NOTES.md` | |
| **Inbox workflow + lock** | All new content enters through one folder and is filed by a defined procedure; a courtesy lock prevents two concurrent filing passes | Multiple writers plus index or entity machinery worth protecting | `03_Operational/Example_Inbox_Workflow_README.md`, `Example_INBOX_LOCK.md` | |
| **Review queue** | Mute-and-record: flagged drift is muted for colleagues and queued for the maintainer, so nobody is nagged and nothing is lost | A detector exists *and* people other than the maintainer meet its findings | `03_Operational/Example_REVIEW_QUEUE.md` | |
| **Owner buy-in note** | A warm, ask-first one-page note before reorganizing, merging, or renaming files someone else added — so nothing seems to vanish on them *(a social courtesy, not machinery — listed here because its trigger is shaped like the others')* | The folder starts holding files of a person who is not driving the build: an owner invited in to participate directly, a colleague dropping in their own material | `01_Universal/Example_Owner_Letter.md` (optional companion: the separate `data-owner-letter` skill renders it as a polished PDF) | |

**Two hazards worth knowing before building the detectors** (full detail:
`Example_Drift_Disposition_Matrix.md`): `snapshot` blesses *everything* currently on disk, so
never use it to mute one item — that is `bless-file`'s job; and sync-provider hydration lag can
make a snapshot record pre-edit content for every file a session touched, so verify from the
shell that edits landed before snapshotting.

## Invent freely

Both lists are open. If this folder's real questions call for a species neither names, build that
instead and add a row — including the trigger that justified it, so the next reader can judge
whether it still applies.

**And if what you invented looks generally useful** — a species of surface or machinery that other
SmartFolders could plausibly want — ask the user, once and casually, whether they'd like to send
the idea to Paul Hess (paul@hess.club), the developer of the SmartFolder Skill. If yes, offer to
compose a thorough markdown write-up **for their review, which they email themselves**: what the
species is and what it removes or protects; the concrete trigger that fired; how it was built and
how it complies with the shared discipline; which axis it belongs to, with a candidate "offer it
when…" row; and enough of the design to generalize it without ever seeing this folder. **Describe
the pattern, never the data** — no file contents, names, paths, or identifying details. Nothing is
ever sent by the skill or its surfaces, and no response or adoption is promised. If declined, drop
the offer without record.

## Considered and declined

| Date | Item | Why not | What would change it |
|---|---|---|---|
| | | | |

---

*Provenance: adapted from the SmartFolder Skill kit exemplar (v6.3.0), filled in from this
folder's recorded profile as of the date above. Decays when: the skill version this folder is
measured against changes, or any declined item's trigger fires. To refresh: ask your AI assistant
to update this.*
