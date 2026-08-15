---
name: create-smartfolder
description: "Turn a folder hierarchy into a SmartFolder — a tiered navigation-and-knowledge layer over the real files, so people and future Claude sessions can operate in it with full context and synthesized knowledge without opening every file. Use whenever the user asks to create, build, or convert a folder into a SmartFolder, \"smartfolder-ize\" a directory, add a CLAUDE.md / README / synthesis layer over files, reorganize an archive or document repository so Claude can navigate it, or review, upgrade, or extend existing SmartFolder scaffolding — even if they never say \"SmartFolder\" but describe wanting a folder of records made self-describing, navigable, or Claude-ready. Also use when asked to organize or reorganize a folder without a scheme the user has already chosen, so deciding it requires understanding the contents: look first, then offer this method rather than assuming it. Not for file operations already specified — renaming to a stated pattern, moving named files, de-duplicating."
---

<!--
  ============================================================
  SmartFolder Skill — a skill for building SmartFolders.
  Version: v6.5.0 — last changed [260815].
  v6.5.0: thread masters for capture-fed folders (RM-17); the
  trigger widens to plain organize requests, with an explicit
  offer before any commitment (RM-22); conditional and
  historical content moves to references/ (RM-24); the
  deposited version check re-homed into the kit's new
  Example_VERSION_BASELINE.md (RM-23).
  Full version history: references/VERSION_HISTORY.md (in this
  package; read on demand, never deposited) and CHANGELOG.md
  at github.com/idea2go2go/smartfolder-skill.
  Line budget: this file stays under 550 lines, standing —
  asserted at each release's verification; exceeding it owes
  a disclosure move (to references/ or the kit) before ship.
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

# SmartFolder Skill (v6.5.0)

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

**Two kinds of bundled content, never to be confused.** `assets/kit/` is the **kit**: working
exemplars and scripts that get **adapted and deposited into the user's folder** (Phase 5).
Top-level `references/` is the opposite — files **this skill reads on demand when a branch fires
and never deposits**: `references/UPGRADE_PATH.md` (the full existing-SmartFolder upgrade path)
and `references/VERSION_HISTORY.md` (the full changelog). Nothing from `references/` ever lands
in a built folder.

## Non-negotiables (safety — these override everything else)

1. **Nothing moves, gets renamed, or gets generated until the user approves a plan.** Staged work,
   review gates.
2. **Back up first** (zip/tar the tree) before any move or rename. **Log every move/rename** to a
   `move-log.csv`. After moving, **verify by content hash against the backup** — not just counts.
3. **Never delete.** Instead, move unneeded files to a single manual-delete folder at the root;
   one such folder per SmartFolder. What the staging rule
   protects is a **category, not a location**: staged content never re-enters the folder's
   knowledge layer — never read, quoted, reconciled against, or restored from. **One exception:**
   a single light manifest (`_README.md`), written at staging time by the session that staged —
   one line per item: what moved, when, why, where the surviving copy is — so the owner isn't
   emptying unlabeled files on trust. The separating test: the manifest may be consulted *only*
   to answer a question about the disposal itself ("is it safe to empty this? why is that in
   there?"); any other use, including answering anything about the folder's subject matter, is a
   violation of the rule, not an exercise of the exception. The manifest is not curated, earns no
   maintenance, and **dies with the contents** — when the owner empties the folder, it resets.
4. **macOS bundles are atomic** (`.rtfd`, `.oo3`, `.key`, `.pages`, `.numbers`, `.goodnotes`,
   `.webarchive`, companion `*_data` dirs, and kin): rename if needed, never recurse into or write
   inside.
5. **Never clobber existing guides, indexes, `CLAUDE.md`, or `AGENTS.md`** without explicit OK. If SmartFolder
   scaffolding already exists, this is an **upgrade**, not a build (see *Existing SmartFolders*).
6. **Don't modify file contents.** Only add guide/derived files and (if approved) move/rename. If a
   folder is shared or off-limits, work from a copy.
7. **Never guess.** Flag anything you can't confidently summarize; a confidently wrong summary or
   synthesis is worse than none.

*One procedure in this skill reaches the network — the monthly version check this skill deposits
into every folder it builds (Phase 5); everything else is local files. The check degrades to
silence when the network doesn't answer, so no folder ever depends on connectivity.*

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
   trigger forward. A second conditional offer hangs on the same dial: where several people will
   use the folder across sessions, offer the **session-flags register** (the kit's
   `Example_SESSION_FLAGS.md`) — a person-addressed notification surface for "next time X is
   here, tell or ask them Y," whose content and state live entirely in the register while the
   root file carries only the trigger. Collaborative folders only — a single-writer folder is
   never shown it; the deposited growth menu carries the same conditional row forward, so a
   folder that grows into multi-user life can reach it later.
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
That README's table is the **index** — it answers whether an artifact is warranted; the exemplar is
the **specification of what the artifact is — never of what yours must be**. Open the exemplar
before authoring any surface it models — a step, not a recommendation; per artifact, at authoring
time. Then decide freely: adopt, adapt, or depart — the exemplar is a well-built guide from one
folder's life, and *this* folder's diagnostic, profile, and owner govern what is actually built.
Where your departure changes a form a reader would notice, say so and why, at the point of the
decision.
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

**The front-door gate — after the look, before any commitment.** When this skill fired on a plain
organize-request — a folder to organize with no scheme the user has already chosen — do not
commit silently to either path. Phase 1's mere-piles skip applies first: twelve holiday photos
never hear the offer. Otherwise offer the method, once, in plain terms: *"I have to understand
this folder to organize it well — want me to write down what I learn while I'm in here, so the
next person or session doesn't start over?"* The fork is explicit and both paths are nameable —
**build** (continue into Phase 2) or **just-organize** (do the requested work well and stop). A
declined offer deposits nothing: no scaffolding, no marker, no record of the decline — whether to
raise it again is ordinary conversational judgment. A request that supplied its own scheme was
never this gate's business: execute it, no offer.

**Phase 2 — Diagnose and decide.** Run the diagnostic interview. Then propose, for the user's
approval: the **profile** (dial readings + the allocation they imply + rationale), the
reorganization scope (guides only / group into chapters / full restructure with renaming), the
naming convention, and a **dry-run plan** showing where every folder and loose file lands and which
folders get which derived surfaces. While naming is on the table, mention that at close-out the
skill will suggest appending `SmartFolder` to the folder's own outer name (Phase 6 makes the
offer) — so it is no surprise later.

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
  rules below; a grouped **Session boundaries** section (below); the conventions; a thin top-level
  orientation (the only thing the root enumerates — one line per chapter); a short maintenance note
  pointing to the runbook. Write prescriptive content dateless and present-tense; write descriptive
  content (orientation, state) with as-of dates. **A deposited rule states what to do.** Where it
  genuinely depends on a capability, name the capability as a **condition** and say what happens
  without it — never let a capability claim stand as the **reason** for a rule that applies
  regardless. A rule silent about the environment differing fails in one of two directions: a
  guarantee quietly lost where the claim is false, or a conditional quietly hardened into a
  prohibition by the session that met the false branch first. The kit's `Example_Root_CLAUDE.md` models the
  *shape*, not the contents. Dual profile: deposit `CLAUDE.md` and `AGENTS.md` byte-identical, each
  carrying the reciprocal instruction. (Bonus, not guarantee: current Claude Code strips HTML
  comments from `CLAUDE.md` at injection, so maintainer notes there can be context-free; don't
  rely on it elsewhere, and never in dual folders.)
- **Close the loop — four deposited rules** (≤12 root-file lines; procedure detail goes in the
  runbook). *Locality:* before finishing, update the derived surfaces in the folders you worked
  in. The navigation protocol has already put them in front of you, but state the rule anyway — a
  session editing by absolute path gets no protection from the side effect. *The distant-surface
  list:* then check the decay conditions of the named surfaces that sit outside every work area's
  read path. Build the list with the **distant test** — does this surface make claims about
  material that does not sit beside it? — applied to the **entire surface inventory** this phase
  just built, and re-applied whenever a surface is added later. A surface describing an **external
  state** — what is published, what is installed, what a counterparty holds — is distant **by
  definition**: it is falsified by acts performed entirely elsewhere, so no work area's read path
  ever surfaces it. The list names **surfaces, never events**: each surface's own decay condition
  remains the single source of truth for whether it fired; the root list only supplies awareness
  that the surface exists. Folders where nothing fails the distant test get the two sentences and
  no list. *Reconcile whole:* a refresh reconciles the entire surface against present state, not
  just the section you came for — patching one section is how a stale sentence survives a
  "refresh." Reconcile-whole keeps a surface accurate; it never asks whether a sentence is
  warranted — that is the next rule's job. *State stays out of prescriptive files* — and this rule
  takes priority: **removal beats annotation**. Point-in-time state — versions, counts, item
  lists, statuses — lives on dated status surfaces; a prescriptive file states identity and rules
  and **points at** its state; the root manual in particular never restates what a status surface
  owns. A stale figure in a dateless file is invisible to every decay mechanism above — the root
  manual is the worst case, since it auto-loads into every session and survives compaction. The
  constants that cannot move out (a README describing its own contents, a baseline recording a
  version) carry a **source pointer** to where the truth is checkable — "three scripts (see the
  table below)" — which does its real work at edit time, putting the check in front of whoever
  rewrites the sentence. Annotate only what could not be removed. Once state has moved out, the
  root file's residual dated content is its as-of line and orientation table, which its
  close-the-loop wording names. Do not build an event-indexed obligation table ("if X happened,
  update Y") — that is a central index by another name, and it silently rots when a surface's
  decay condition changes. Where the closeout *hangs* — which machinery, if any, runs it at
  session end — is settled once by the session-boundary prompt below; the deposited wording cites
  that answer rather than restating it.
- **The session-boundary prompt — asked once, of every folder:** *where do this folder's session
  boundaries live?* That is: which machinery, if any, marks session start and session end. Wire
  **both bookends** to the answer — delivery of any person-addressed surface (the session-flags
  register, where adopted) hangs at session start; the close-the-loop pass hangs at session end.
  The answer is whatever the folder already runs: the integrity gate's session-start mode if it
  runs one, the change watcher's sweep if that is all it has, root-file prose alone if it runs
  nothing. A folder with no machinery gets no machinery — the floor answer is exactly the status
  quo. **The prompt's deposit is the root manual's *Session boundaries* section** — every boundary
  duty grouped in one place, one line per duty, each pointing at its owning procedure file: the
  integrity scan where one runs, delivery of the flags register where adopted, the monthly version
  check (its procedure lives in the deposited `VERSION_BASELINE.md`), and the close-the-loop pass. Triggers live here because the root manual is the
  one file guaranteed to be in context — a duty that depends on a session remembering to open some
  other file misses silently — while procedure detail stays in the files each line points to.
  Where the flags register is adopted, its trigger line notes that delivery is **identity-gated
  and non-blocking**: no established identity → announce addressees once and hold content, per the
  register's own rules. A
  duty adopted later, from the growth menu or otherwise, **adds a line to this section rather than
  a rule elsewhere.**
- The **runbook** (how to refresh guides and syntheses, perform a
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
  is the specification of what the surface is — never of what this folder's surface must be; the
  menu is only the index), the offer protocol, a considered-and-declined
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
  payload: unpacked, `SKILL.md` is hundreds of lines of imperative build instructions a browsing
  session might start applying to a folder that is already built; zipped it is inert to casual
  reading and still fully diffable. When the running copy is an installed skill rather than a
  user-visible archive, work down this ladder and record which rung was used: (1) the exact source
  `.skill` archive, when available; (2) with the user's approval, the matching version's release
  asset from the skill's public repository (github.com/idea2go2go/smartfolder-skill → Releases) —
  the authoritative published artifact, recorded with source URL and hash; (3) repackage the
  installed payload byte-for-byte and stamp the baseline **reconstructed**, with file count and
  hash; (4) never fabricate — if no rung is reachable, ask the user for the package.
  **Author the deposited `VERSION_BASELINE.md` per the kit's `Example_VERSION_BASELINE.md`,
  opened first.** It records version, route (original / fetched / reconstructed), file count, and
  hash — and **the exemplar carries the monthly version check complete** (both repository URLs,
  the `Last checked: YYYY-MM` stamp, the throttle and evidence rules), so the deposit specifies
  the check and any ordinary session runs it from the folder alone, this skill nowhere in the
  loop. The root manual carries only the check's trigger line in *Session boundaries*. **"Any
  session" is scoped by the folder's agent-population profile:** single-agent → the trigger lives
  in `CLAUDE.md` and Claude sessions run the check; dual profile → every assistant reading either
  root twin sees the same trigger; a non-Claude assistant joining a single-agent folder's life
  later is a **dial change**, routed through the upgrade review. **The stamp is a write:** in a
  folder running a manifest or drift detector, list `VERSION_BASELINE.md` as a sanctioned write
  target at deposit time, or the check fires an integrity finding every month.
  The runbook gains the **version-upgrade review**: unpack
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
  more, no fewer — swept against the **entire** surface inventory, with every external-state
  surface on it by definition; and every listed surface states its own decay condition.
- Prescriptive, dateless files (the root manual, the runbook, deposited READMEs) carry no
  point-in-time state that a status surface owns; **spot-check a sample** of the source-pointered
  constants that remain against their sources — a sample, not an audit; the pointer's real work
  happens at edit time.
- Sweep the deposited surfaces for capability language — "is blocked", "cannot", "typically
  can't", "available", and kin. **The sweep is a finder, not a verdict**: judge each hit — is the
  capability the rule's genuine **precondition** (keep it, and it must state its false branch), or
  the **justification** for a rule that applies regardless (strike the claim, keep the rule)? It
  must not fire on legitimate conditionals — dual-profile rules, conditional registers, and
  degraded modes are correct as written.
- The root's *Session boundaries* section exists, one line per active duty, each pointing at a
  procedure file that resolves; the deposited `VERSION_BASELINE.md` carries the check procedure,
  both URLs, and the `Last checked` stamp — and where the folder runs integrity machinery, the
  baseline is a sanctioned write target.
- The meta folder exists with runbook + recorded profile + growth menu + version baseline; the
  maintenance loop works without this skill.

**At close-out, once — the outer-name suggestion** *(an offer, deliberately not a verification
check — nothing about it is checkable, and a check that always passes trains people to ignore the
list)*: recommend the user append **`SmartFolder`** to the folder's own name — `Acme Consulting` →
`Acme Consulting SmartFolder` — so a built folder is recognizable from outside any session: in a
file browser, a backup job, a list of connected folders. A space separates by default; the
folder's own separation convention wins (`Acme_Consulting` → `Acme_Consulting_SmartFolder`). Skip
the offer when the name already ends in the suffix, case-insensitively. **The name is the owner's,
and any rename happens only on their say-so.** In most environments the session cannot rename its
own root: the root folder is the handle the environment hands the session, not a file inside the
tree, and renaming it mid-session severs the reference the session runs on. There, the offer states
**both steps**, for the owner to carry out between sessions: rename the folder, then **re-point
whatever holds it under the old name** — in Cowork, re-select the folder; in Claude Code, update
the project's path; in any other assistant, whatever it uses to locate this folder — or a future
session will not find it. **Where the environment does let the session rename the root and re-point
its own reference safely, it may offer to do that itself** — verify the connection afterward, and
the two-step instruction above remains the fallback. Offer once; accept a no without argument and
do not re-raise in this session; record nothing — the outer name is the owner's, and out of this
folder's scope once built.

## Existing SmartFolders (the upgrade path)

When Phase 1 detects SmartFolder scaffolding already present — a root `CLAUDE.md`/`AGENTS.md`,
`_README.md` routers, a meta folder with a runbook or version baseline — this is an **upgrade,
not a build**. **Read `references/UPGRADE_PATH.md` — the full upgrade path, bundled in this
package — before proposing anything.** It carries the version-against-version review route, the
accretion audit, and the standing repairs a session offers because deposited machinery never
self-heals (the version check, capability-resting rules, pre-identity flags registers, the
growth-menu sentence, the outer-name suffix). The non-negotiables bind on this path too, and the
folder's recorded profile — not this skill's defaults — governs unless the user says otherwise.

## Working style

Use a task list; keep updates concise; show samples before mass-applying; ask before underspecified
work. When new content arrives later, any session should be able to run maintenance from the
deposited runbook — add guides for new folders, refresh stale guides and syntheses while preserving
manual edits, and re-run the verification steps — without this skill installed.
