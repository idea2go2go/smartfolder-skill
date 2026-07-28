---
name: create-smartfolder
description: Turn a folder hierarchy into a SmartFolder — a tiered navigation-and-knowledge layer (root CLAUDE.md, an AGENTS.md twin for multi-agent folders, per-folder _README.md routers, folder syntheses, sidecar summaries, and status surfaces) so people and future Claude sessions can operate in it with full context and synthesized knowledge without opening every file. Use this skill whenever the user asks to create, build, or convert a folder into a SmartFolder, "smartfolder-ize" a directory, add a CLAUDE.md / README / synthesis layer over files, reorganize an archive or document repository so Claude can navigate it, or review, upgrade, or extend an existing SmartFolder's scaffolding — even if they never say "SmartFolder" but describe wanting a folder of records made self-describing, navigable, or Claude-ready. Ships with a kit of working scripts and exemplars in assets/kit/.
---

<!--
  ============================================================
  SmartFolder Skill — a skill for building SmartFolders.
  Version: v6.2.0 — last changed [260728].
  v6.2.0: drift-disposition matrix added to the kit (item 1);
  agent-population dial with guarded CLAUDE.md/AGENTS.md
  duplication and a Phase-6 parity probe (item 2);
  conditional owner buy-in with owner-letter and
  owner-guide exemplars (item 3); growth menu deposited,
  two axes (item 4);
  version baseline deposited with an upgrade-review
  procedure (item 5); write-time close-the-loop rules
  (item 7); developer feedback offer in the growth menu
  (item 8); display name corrected to "SmartFolder Skill";
  kit README script count corrected.
  v6.1.1: kit script sample configuration and docstring
  examples use invented placeholder content throughout.
  No functional change.
  v6.1: added the write-forward (state-first) discipline for
  live surfaces, deposited into each SmartFolder's CLAUDE.md.
  Created by Paul Hess (paul@hess.club).
  If you have questions, suggestions, or problems using this
  skill, please contact Paul at paul@hess.club.
  The bundled kit (assets/kit/) draws its shapes and discipline
  from Paul's live SmartFolders; the exemplars, and the sample
  configuration and example content in the scripts, are invented.

  License: CC BY 4.0 (creativecommons.org/licenses/by/4.0) for
  all prose and exemplars; the bundled scripts (*.py) are
  released under the MIT License (full text in assets/kit/LICENSE).
  (c) 2026 Paul Hess.
  ============================================================
-->

# SmartFolder Skill (v6.2.0)

Turn the target folder into a **SmartFolder**: a self-maintaining navigation-and-knowledge layer
over the real files, so the user, other people, and future Claude sessions can operate in it with
full context — finding things by location, and drawing on synthesized knowledge that no single file
contains — without opening every file.

## How this skill runs

This is **interactive, customized work**, not a template application. The user will describe their
intentions and goals in their own words — treat that as the *requirements* and this skill as the
*method*. Expect an interview; the design is worked out together through the phases below, each
ending at a review gate.

> **Design stance.** Only the invariants and safety rules below are fixed. Everything else is
> decided per folder through a needs diagnostic, guided by principles, three real precedents, and
> the bundled kit. Detailed specification of flexible decisions is deliberately avoided: being
> overly prescriptive about flexible design choices becomes *proscriptive* in implementation — it
> forbids better designs. Where this skill is silent, design from the principles and precedents
> rather than asking for a rule.

## Non-negotiables (safety — these override everything else)

1. **Nothing moves, gets renamed, or gets generated until the user approves a plan.** Staged work,
   review gates.
2. **Back up first** (zip/tar the tree) before any move or rename. **Log every move/rename** to a
   `move-log.csv`. After moving, **verify by content hash against the backup** — not just counts.
3. **Never delete.** Stage discards into a single manual-delete folder at the root (many
   environments block deletion anyway). One such folder per SmartFolder; never read or reconcile
   against its contents.
4. **macOS bundles are atomic** (`.rtfd`, `.oo3`, `.key`, `.pages`, `.numbers`, `.goodnotes`,
   `.webarchive`, companion `*_data` dirs, and kin): rename if needed, never recurse into or write
   inside.
5. **Never clobber existing guides, indexes, `CLAUDE.md`, or `AGENTS.md`** without explicit OK. If SmartFolder
   scaffolding already exists, this is an **upgrade**, not a build (see *Existing SmartFolders*).
6. **Don't modify file contents.** Only add guide/derived files and (if approved) move/rename. If a
   folder is shared or off-limits, work from a copy.
7. **Never guess.** Flag anything you can't confidently summarize; a confidently wrong summary or
   synthesis is worse than none.

## The invariant core (every SmartFolder shares these)

**The tier model — read top-down, stop when you have enough:**
- **Tier 1 (resident):** one resident root manual — `CLAUDE.md`; in the dual profile it exists as
  two byte-identical files, `CLAUDE.md` and `AGENTS.md` (see *Root files by agent population*) —
  the only content that auto-loads every session and
  survives compaction. Protocol + conventions + behavioral rules + a thin top-level orientation.
  Keep it lean (under ~150 lines); detail lives in the files it points to.
- **Tier 2 (on demand):** a `_README.md` in each meaningful folder — a **local router** describing
  its own folder and mapping its immediate children. Tiny/leaf folders fold into the parent's guide.
- **Tier 3 (on demand):** derived, digested knowledge — per-file sidecars (`<stem>_Summary.md`),
  folder syntheses (`_Synthesis.md`), and whatever status surfaces the folder's needs call for
  (boards, decision logs, indexes, hubs). Which of these exist, and in what proportion, is the main
  design decision (see *The diagnostic*).
- **Raw files:** the bottom of the waterfall — opened only when a digest won't do.

**Navigation is by location, not a central index.** The root file states the protocol — *before
working in or answering about a folder, read its `_README.md` first* — and each guide routes to its
own children. Nothing global to keep in sync. Only the root file is named `CLAUDE.md`; per-folder
guides stay `_README.md` (nested `CLAUDE.md` auto-loading is a Claude-Code-specific, after-the-fact
behavior — the explicit protocol is portable across products and predictable).

**Root files by agent population (dial 7).** Single-agent folders keep one root `CLAUDE.md` and pay
none of what follows. Where the dial says other assistants may work the folder, use **guarded
duplication**: byte-identical `CLAUDE.md` and `AGENTS.md`, each carrying a one-line reciprocal
instruction — any change to one is applied to the other before the task completes. **`AGENTS.md` is
canonical on divergence**; repair by re-copying from it, and add a root-files-differ check
(`cmp AGENTS.md CLAUDE.md` — silence means identical) to the folder's integrity script, or to its
runbook verification list if it runs none. **Never assemble either root file with `@` imports:**
some surfaces inject `CLAUDE.md` verbatim with no import expansion, so an imported manual arrives
empty — no error, no trace. Why duplication: the project-root file is re-read from disk and
re-injected after compaction, which conversation content is not, so a real file — not a pointer to
one — is what survives a long session on every surface; and duplication's failure mode, divergence,
is mechanically detectable where a stub's mid-session staleness is not. In dual folders, deposited
wording is agent-neutral ("ask your AI assistant"), lock files record the holder "via
<assistant/surface>", and nothing relies on HTML comments being invisible — other agents read them
as content. The root file is context, not enforcement: deposited wording never promises compliance.

**Every derived surface is dated and ranked:**
- Every guide, synthesis, and status surface carries an **`As of [YYMMDD]`** line.
- **Recency wins:** when two dated surfaces disagree, the more recent as-of date wins.
- **Raw beats derived:** a synthesis or summary is AI interpretation; the raw file wins on conflict.
- **The filesystem beats the map:** a live directory listing outranks any guide's file map.

**Derived knowledge surfaces — where the added value lives.** The derived layer holds knowledge
that no single file contains and that would otherwise require tedious browsing of many files.
**Synthesis (`_Synthesis.md`) is the archetype**: it exists only where the whole exceeds the parts,
correlating, combining, and commenting across a folder's files to yield the holistic story — arcs,
patterns, cost roll-ups, cross-system connections, recurring failure modes. Synthesis has siblings,
distinguished by the kind of tedium they remove: a **status board** (currency over time — one dated
line per workstream plus its next gate); a **longitudinal tracker** (one subject — a medical issue,
a negotiation arc, an easement — threaded across many files and years); a **decision log**
(append-only dated record of what was decided, with sources); **cross-folder maps and hubs**
(maintenance calendars, vendor directories, sensitive-info maps, entity indexes); and **computed
views** (dashboards, charts, extract tables built from the structured layer). The taxonomy is open —
invent the species this folder's questions call for.

All species share one discipline: an `As of [YYMMDD]` header; claims anchored in-narrative ("through
[date]…"); stated **provenance** (what it was derived from, as of what state — which doubles as the
staleness test) and a **decay condition** (when it might begin to be wrong); a label as derived AI
analysis (raw wins); and the one-line breadcrumb *"To refresh: ask your AI assistant to update
this."* The discipline belongs to **every** derived surface, Tier-2 guides included: a
`_README.md`'s descriptive front matter carries its as-of line, provenance, and decay condition
like any Tier-3 species. The behavioral rule — **offer to refresh any derived surface materially
behind its sources before relying on it** — lives once, in the root file, not in each file.

**Write forward, not backward (live surfaces).** A live surface — one whose subject is still
moving: a board row, a README's front matter, the synthesis of an ongoing system — leads with the
present: current state + what's next, one screen, written from now looking forward. The test: a
newcomer's first screen answers "where do things stand?" without summing dated patches. Refreshing
means **rewriting the front matter, not appending a dated delta** — appending is the writer's cheap
path, but it shifts the cost onto every future reader. Small deltas may accrete between rewrites;
at a **chapter boundary** (a close, a kill, a pivot, a replacement) the surface is rewritten
state-first and the accumulated narrative is **demoted whole** into a labeled history section or a
sealed, dated index, with one pointer from the front matter — never deleted or summarized away
(that is what makes rewriting safe). Tripwire: front matter carrying more history than present
state is a boundary in disguise — a rewrite is due. Archival syntheses of completed arcs already
comply: their "present" is the finished story. Deposit this rule in each SmartFolder's root
`CLAUDE.md` (procedure in the runbook) — accretion is a maintenance-time failure, and the skill
won't be there.

**Sidecars (`<stem>_Summary.md`) are caches, not commentary.** A sidecar pays rent when the raw
file's read-cost × consultation-frequency is high. Typical triggers: long or dense PDFs and
transcripts (re-reading a 60-page transcript can cost a session 100K+ tokens); scanned, OCR'd, or
handwritten material where extraction is slow or error-prone; formats Claude reads poorly or not at
all (the sidecar is then the only machine access); authority documents — contracts, reports, rulings
— whose exact terms will be asked about repeatedly (capture the key terms plus last-mile pointers:
"signature page is p. 14"); files whose payload is visual; and files a synthesis leans on, where the
sidecar doubles as the synthesis's provenance anchor. Skip routine items, media dumps, and anything
the folder's README or synthesis already covers. Sidecars move with their file.

**Self-orientation from anywhere:** each `_README.md` opens with one line noting it is part of a
SmartFolder whose protocol lives in the root `CLAUDE.md` — so a session that mounts a subfolder can
still find the system.

**Proportionality:** every artifact must pay rent — real signal against its maintenance cost. No
rote guides, no unwarranted syntheses, no machinery a folder's needs don't justify.

**Self-containment:** the finished SmartFolder carries its own maintenance payload (see Phase 5).
After the build, this skill is only needed to seed *new* SmartFolders — never to maintain this one.

**Naming (the default house convention — adapt to the folder's own tradition where one exists):**
- **Dates lead**, as `YYMMDD` or `YYMM`, no dashes; `YYYY` only when just the year is known. Decode
  2-digit years by century (≥90 → 1900s). If the archive spans the century boundary or the 1980s,
  raise it in Phase 2 — string sorting breaks across centuries — and agree on handling.
- **PascalCase** within one concept, **underscores** between concepts; **theme-first** so like items
  cluster: `DATE_Type_Specifier.ext` (e.g. `2312_WaterReport_FairfaxCounty.pdf`).
- Where a name is vague or wrong, **peek inside and name by real content**; add missing extensions;
  fix problem characters (colons, `#`, hidden/non-breaking spaces, trailing spaces). Bulk-rename
  with globs, not hardcoded names, and verify each rename happened.
- Bulk media/photo dumps: batch-name, don't curate each; describe the group in the guide.

## The diagnostic (design through interview, not menu)

Before proposing scaffolding, learn the folder's needs — from the user's stated intentions, from
Phase-1 exploration, and by asking (AskUserQuestion works well here). The dials:

1. **Writers and users.** Who adds or edits files — Claude only, one human, several humans? Via a
   sanctioned intake path or directly? How technical is each? **And whose files are they?** If
   this reveals the minority case — the folder holds files of an owner who is not driving or
   coordinating the build — suggest winning the owner's buy-in before the plan executes: a warm,
   non-technical one-page note saying what will move and why, with nothing deleted (the kit's
   `Example_Owner_Letter.md` models the shape and tone). Most folders are built by, with, or under
   the authority of their owner and pass through with no mention — this is a conditional offer,
   never a standing step. Usage changes over time, so the deposited growth menu carries the same
   trigger forward.
2. **Change velocity.** Archival (rarely changes), slow-drip, or live and fast-moving?
3. **Dominant question type.** What will people mostly ask here — *navigation* ("where is X?"),
   *wisdom* ("how does this work? what matters? what's due?"), or *status* ("where do things
   stand?")?
4. **Enforcement posture.** Should integrity machinery *offer* (advisory, non-blocking) or *gate*
   (hard checks before work proceeds)?
5. **Authority model.** Raw files only? Hand-authored primary notes that must stay primary and be
   kept in sync? Volatile facts needing a single dated source-of-truth surface?
6. **Audience and tone.** Who reads the guides — and how plain must the language be?
7. **Agent population.** Will AI assistants other than Claude work this folder? The relevant
   population is assistants that work *in folders*, not chat alone. Ask in plain product terms,
   without assuming the user knows what any of these are: *"Will this folder be used only with
   Claude (Cowork or Claude Code), or also with other AI tools that work in your folders —
   OpenAI's ChatGPT Work or Codex, Google's Gemini (Spark or CLI), Microsoft Copilot, Cursor, or
   something else — now
   or someday?"* Only Claude → single profile: one root `CLAUDE.md`, none of
   the dual tax. Anything else → the dual profile (see *Root files by agent population*). If the
   user is unsure, choose single: converting later is one copy plus the reciprocal lines.

**Allocation principles (the actual design law):**
- **Spend the derived-layer budget where the dominant question lives.** Navigation-heavy → rich
  `_README.md` coverage. Wisdom-heavy → syntheses (and perhaps a one-page hub). Status-heavy →
  boards, decision logs, indexes, sidecars.
- **Control machinery scales with write-traffic × writer count:** none → a casual tripwire →
  intake discipline with locks and hard integrity gates. Never more than the traffic justifies.
- **File-map richness:** enumerate files only where names can't speak for themselves, and scale
  enumeration down as change velocity rises — a good renaming pass and a file map are substitutes;
  in a fast-moving folder, annotate and route rather than list.
- **Tone to the least technical reader** who will use the folder.
- **Invent freely; skip freely.** Derive machinery this list doesn't name if the needs call for it;
  omit anything here that doesn't pay rent. Confirm significant inventions with the user before
  building.

## Precedents (case law, not templates)

Three real SmartFolders built with this method. Note what they share (the invariant core, exactly)
and how each spends its budget differently — driven by its needs, not by a feature list.

- **The Archive** — a 22-year, ~6,700-file family records archive; one technical user; near-zero
  change velocity; dominant question "where is X?". Allocation: a `_README.md` in every meaningful
  folder with full annotated file maps (stable, because content rarely changes); only two syntheses,
  placed at genuine arc points (the whole academic record; a school-search saga); no sidecars, no
  locks, no boards. A generator script emits guide scaffolding and stamps content-hash markers so
  re-runs preserve hand edits; a documented periodic sweep handles intake.
- **The Advisory folder** — estate/property records shared with a non-technical owner; owner edits
  files directly; dominant questions operational ("what's due? how does this system work?").
  Allocation: ~40 per-system syntheses seeded from the owner's hand-authored MASTER notes (which
  stay primary, with a stated sync protocol), plus a one-page Operations Hub (maintenance calendar,
  vendor directory, sensitive-info map). Integrity is a **non-blocking daily tripwire** — a watcher
  that detects direct changes and *offers* dispositions, never gates. Warm, jargon-decoded tone;
  gotchas storytold; polished owner-facing PDFs at the root.
- **The Operational folder** — a live, multi-user deal workspace shared on Dropbox; several writers;
  daily change; dominant question "where do things stand?". Allocation: a one-screen status board,
  per-initiative decision logs and document indexes, and per-file summary sidecars on most documents
  so raw files rarely need reopening. Control machinery is **hard**: all new content enters through
  an inbox workflow under a courtesy lock; a content-hash manifest with a session-start scan and a
  review queue makes colleague edits surface within a day; prescriptive tone; explicit lifecycle
  (closed initiatives archived with closing memos).

**License clause:** these are precedents, not menus. Cite them, interpolate between them, depart
from them — the test is whether the resulting scaffolding serves *this* folder's diagnostic, not
whether it resembles an example.

## The companion kit (bundled — `assets/kit/`)

Working artifacts drawn from the three precedents ship with this skill: the integrity and
change-tracking scripts, a guide generator, an inbox workflow and lock file, a drift-disposition
matrix, and growth menu / owner letter / owner guide / status board /
decision log / review queue / operations hub / synthesis / guide / sidecar exemplars. Integrity
machinery comes in **three species** — the advisory tripwire (offers), the hard gate (blocks), and
the generator's content-hash markers (protect generated guides from regeneration) — and the matrix
is the hard gate's companion reference, not a rung the advisory tier is climbing toward. **Start from
`assets/kit/00_KIT_README.md`**, which maps each artifact to the diagnostic dials that warrant it.
Kit artifacts are **starting points to adapt, never to transplant wholesale**: the markdown
exemplars are fictionalized (real shapes, invented content), the scripts' sample configuration and
example content are likewise invented, and the scripts need their paths, conventions, and
ignore-lists adapted to the target folder. Scripts destined for the target
SmartFolder are copied into its meta folder in Phase 5.

## The build (phases — each ends at a review gate)

**Phase 0 — Intent.** Absorb the user's stated goals and constraints; confirm scope (this folder
only, or siblings too?). Touch nothing.

**Phase 1 — Explore and report.** Walk the tree: folder/file counts, depth, biggest areas,
file-type mix, the naming/date conventions actually in use (they may differ per subfolder — honor
detected conventions rather than imposing one rule everywhere). Detect existing instruction files
(`CLAUDE.md`, READMEs, `AGENTS.md`, `.claude/`) → route to the upgrade path. Flag oddities that
change the plan: problem characters, no-extension legacy files, scanned PDFs with no text layer,
locked files, mislabeled files. Note synthesis candidates — folders whose files together tell a
story — and folders that are mere piles of like items (no greater whole; skip).

**Phase 2 — Diagnose and decide.** Run the diagnostic interview. Then propose, for the user's
approval: the **profile** (dial readings + the allocation they imply + rationale), the
reorganization scope (guides only / group into chapters / full restructure with renaming), the
naming convention, and a **dry-run plan** showing where every folder and loose file lands and which
folders get which derived surfaces.

**Phase 3 — Sample.** One chapter end-to-end. Judge it together on whether the guides and any
synthesis are *genuinely useful* — not just present.

**Phase 4 — Apply.** Execute moves/renames with logging and hash verification; author guides and
syntheses **from real contents** — never auto-fill filler prose. Size the approach to the job: a
generator script for scaffolding on large trees (prose in a separate content layer; content-hash
markers so re-runs preserve human edits; hand-written guides just carry their as-of line), direct
writing on small ones. At scale, fan out parallel sub-agents on disjoint scopes with their own move
logs and required integrity reports; keep judgment calls and shared-file writes single-threaded.

**Phase 5 — Deposit the infrastructure.** The SmartFolder must be self-contained:
- The root **`CLAUDE.md`** containing: what this SmartFolder is; the navigation protocol and descent
  rule; the freshness/precedence rules; the refresh and write-forward rules; the close-the-loop
  rules below; the conventions; a thin top-level
  orientation (the only thing the root enumerates — one line per chapter); a short maintenance note
  pointing to the runbook. Write prescriptive content dateless and present-tense; write descriptive
  content (orientation, state) with as-of dates. The kit's `Example_Root_CLAUDE.md` models the
  *shape*, not the contents. Dual profile: deposit `CLAUDE.md` and `AGENTS.md` byte-identical, each
  carrying the reciprocal instruction. (Bonus, not guarantee: current Claude Code strips HTML
  comments from `CLAUDE.md` at injection, so maintainer notes there can be context-free; don't
  rely on it elsewhere, and never in dual folders.)
- **Close the loop — three deposited rules** (≤10 root-file lines; procedure detail goes in the
  runbook). *Locality:* before finishing, update the derived surfaces in the folders you worked
  in. The navigation protocol has already put them in front of you, but state the rule anyway — a
  session editing by absolute path gets no protection from the side effect. *The distant-surface
  list:* then check the decay conditions of the named surfaces that sit outside every work area's
  read path. Build the list with the **distant test** — does this surface make claims about
  material that does not sit beside it? — applied to the surface inventory this phase just built.
  The list names **surfaces, never events**: each surface's own decay condition remains the single
  source of truth for whether it fired; the root list only supplies awareness that the surface
  exists. Folders where nothing fails the distant test get the two sentences and no list.
  *Reconcile whole:* a refresh reconciles the entire surface against present state, not just the
  section you came for — patching one section is how a stale sentence survives a "refresh." Do not
  build an event-indexed obligation table ("if X happened, update Y") — that is a central index by
  another name, and it silently rots when a surface's decay condition changes.
- A **meta folder** holding: the **runbook** (how to refresh guides and syntheses, perform a
  chapter-boundary rewrite — seal the arc, rewrite state-first — add a chapter, handle intake,
  close a task — local surfaces, then the distant list via each surface's own decay condition,
  then the root-files parity check where the dual profile applies — run the version-upgrade
  review below, and re-verify — everything maintenance needs without this skill), the **recorded
  profile** (the dial settings and rationale from Phase 2, so future sessions inherit the design
  intent instead of re-deriving it), any adapted kit scripts and the generator if one was built,
  move logs, and the backup manifest.
- The **growth menu** (`GROWTH_MENU.md`, adapted from the kit's exemplar): the two-axis menu —
  derived surfaces and control machinery, allocated by different rules — of what this folder could
  grow later, with trigger heuristics, implementation pointers into the deposited kit (the artifact
  is the specification; the menu is only the index), the offer protocol, a considered-and-declined
  log, and the "invent freely" close carrying the developer feedback offer. The deposited intake
  procedure (or the sweep flow where no inbox exists) gains one step: when a **concrete, named
  pattern** in the current filings suggests a missing surface, consult the menu and offer it in one
  line ("three filings this month touch the easement — want a tracker?"). The menu is for building
  from, not just consulting — trigger fired, user approved, implement it. Never build unprompted or
  pitch in the abstract; declined ideas are logged and not re-offered until circumstances
  materially change. **Zero new lines in the root file** — the menu is on-demand meta content.
- The **version baseline**: deposit the **`.skill` zip itself** — the package this build ran from —
  in the meta folder beside a stamped **`VERSION_BASELINE.md`** recording which release built the
  folder and which roadmap items, if any, were applied beyond it. The zip, not the unpacked
  payload: unpacked, `SKILL.md` is three hundred lines of imperative build instructions a browsing
  session might start applying to a folder that is already built; zipped it is inert to casual
  reading and still fully diffable. When the running copy is an installed skill rather than a
  user-visible archive, work down this ladder and record which rung was used: (1) the exact source
  `.skill` archive, when available; (2) with the user's approval, the matching version's release
  asset from the skill's public repository (github.com/idea2go2go/smartfolder-skill → Releases) —
  the authoritative published artifact, recorded with source URL and hash; (3) repackage the
  installed payload byte-for-byte and stamp the baseline **reconstructed**, with file count and
  hash; (4) never fabricate — if no rung is reachable, ask the user for the package.
  `VERSION_BASELINE.md` records version, route (original / fetched / reconstructed), file count,
  and hash. The runbook gains the **version-upgrade review**: unpack
  baseline and new release → diff `SKILL.md` (non-negotiables, invariant core, dials, phases,
  verification) and `diff -rq` the kits → classify each delta (new invariant → probably adopt; new
  optional surface or machinery → a growth-menu question subject to its triggers, never an
  automatic yes; changed convention → only where it does not fight the folder's established
  tradition) → audit and **recommend, changing nothing** → on approval apply, update the recorded
  profile, log contested decisions, re-verify → re-stamp the baseline and retire the old artifact.
  **A newer skill is a newer opinion, not an authority over a folder already in use** — the
  recorded profile governs unless the owner says otherwise. Exception: where the folder's own
  subject matter *is* the skill, deposit a stamped pointer to the local copy rather than a
  duplicate that can silently drift.

**Phase 6 — Verify.**
- Coverage invariant: every meaningful folder has a `_README.md` or is explicitly covered by its
  parent's; no filler guides or unwarranted syntheses crept in.
- Root `CLAUDE.md` is lean, loads as project instructions, states protocol + precedence + refresh
  rule; orientation links resolve.
- Every derived surface carries its as-of line, provenance, and a decay condition; flag any derived
  surface whose sources are newer than its as-of date.
- No derived files inside bundles or trash; internal links resolve; content-hash check against the
  backup shows no loss; spot-check summaries and syntheses against raw contents.
- Dual profile only: `cmp AGENTS.md CLAUDE.md` is silent, and a **parity probe** passes for every
  agent that will work the folder — plant unguessable content in the root files, ask each agent to
  quote it back, check for **exact match**, and give explicit permission to answer "I see none."
  Never ask an agent to confirm it "has the instructions": a session without them will confabulate
  a plausible answer rather than report absence.
- The root file's close-the-loop list names exactly the surfaces that fail the locality test — no
  more, no fewer — and every listed surface states its own decay condition.
- The meta folder exists with runbook + recorded profile + growth menu + version baseline; the
  maintenance loop works without this skill.

## Existing SmartFolders (the upgrade path)

When Phase 1 finds scaffolding already present: read its root file, runbook, and recorded profile
first; treat the folder's established conventions as its tradition (move-don't-rename legacy names;
apply conventions to newly named files). Where the meta folder carries a version baseline, run the
runbook's version-upgrade review — a version-against-version diff beats guesswork. Otherwise diff
what exists against the invariant core, propose
targeted upgrades only, and preserve hand-curated content everywhere. Include an **accretion
audit**: flag live surfaces that read as baseline-plus-dated-patches and offer chapter-boundary
rewrites (demote the narrative whole to its history home before trimming the live surface). The folder's recorded profile
— not this skill's defaults — governs its posture unless the user says otherwise.

## Working style

Use a task list; keep updates concise; show samples before mass-applying; ask before underspecified
work. When new content arrives later, any session should be able to run maintenance from the
deposited runbook — add guides for new folders, refresh stale guides and syntheses while preserving
manual edits, and re-run the verification steps — without this skill installed.
