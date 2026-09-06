# The Phase-5 deposit specification — everything a finished SmartFolder carries

*Read by the skill on demand — when Phase 5 begins; never deposited into a user's folder.
`SKILL.md`'s Phase-5 stub routes here and is the index, never the spec: **read this file
completely before authoring any deposit, and reopen it whenever Phase 5 resumes after a session
boundary** — the stub survives compaction; this file does not. The non-negotiables and the
invariant core bind here exactly as everywhere else.*

**Contents** — the deposit classes, in the order specified below:

1. The root manual — `CLAUDE.md`, and its `AGENTS.md` twin in the dual profile
2. Close the loop — four deposited rules
3. The session-boundary prompt and the *Session boundaries* section
4. The maintenance procedures — a runbook by default
5. The recorded profile; adapted kit scripts; move logs; the backup manifest
6. The growth menu
7. The retained kit — the menu's implementation library, whole and byte-for-byte
8. The version baseline — record always, archive when in hand, never procure
9. The developer-feedback offer at build close-out
10. The version-upgrade review — deposited among the maintenance procedures

---

## 1. The root manual

The root **`CLAUDE.md`** containing: what this SmartFolder is; the navigation protocol and descent
rule; the freshness/precedence rules; the refresh and write-forward rules; the close-the-loop
rules below; a grouped **Session boundaries** section (below); the conventions; a thin top-level
orientation (the only thing the root enumerates — one line per chapter); a short maintenance note
pointing to the maintenance procedures (the runbook, in most folders — see §4). Write prescriptive
content dateless and present-tense; write descriptive content (orientation, state) with as-of
dates. **A deposited rule states what to do.** Where it genuinely depends on a capability, name
the capability as a **condition** and say what happens without it — never let a capability claim
stand as the **reason** for a rule that applies regardless. A rule silent about the environment
differing fails in one of two directions: a guarantee quietly lost where the claim is false, or a
conditional quietly hardened into a prohibition by the session that met the false branch first.
The kit's `Example_Root_CLAUDE.md` models the *shape*, not the contents. Dual profile: deposit
`CLAUDE.md` and `AGENTS.md` byte-identical, each carrying the reciprocal instruction. (Bonus, not
guarantee: current Claude Code strips HTML comments from `CLAUDE.md` at injection, so maintainer
notes there can be context-free; don't rely on it elsewhere, and never in dual folders.)

## 2. Close the loop — four deposited rules

(≤12 root-file lines; procedure detail goes in the maintenance procedures.) *Locality:* before
finishing, update the derived surfaces in the folders you worked in. The navigation protocol has
already put them in front of you, but state the rule anyway — a session editing by absolute path
gets no protection from the side effect. *The distant-surface list:* then check the decay
conditions of the named surfaces that sit outside every work area's read path. Build the list
with the **distant test** — does this surface make claims about material that does not sit beside
it? — applied to the **entire surface inventory** this phase just built, and re-applied whenever
a surface is added later. A surface describing an **external state** — what is published, what is
installed, what a counterparty holds — is distant **by definition**: it is falsified by acts
performed entirely elsewhere, so no work area's read path ever surfaces it. The list names
**surfaces, never events**: each surface's own decay condition remains the single source of truth
for whether it fired; the root list only supplies awareness that the surface exists. Folders
where nothing fails the distant test get the two sentences and no list. *Reconcile whole:* a
refresh reconciles the entire surface against present state, not just the section you came for —
patching one section is how a stale sentence survives a "refresh." Reconcile-whole keeps a
surface accurate; it never asks whether a sentence is warranted — that is the next rule's job.
*State stays out of prescriptive files* — and this rule takes priority: **removal beats
annotation**. Point-in-time state — versions, counts, item lists, statuses — lives on dated
status surfaces; a prescriptive file states identity and rules and **points at** its state; the
root manual in particular never restates what a status surface owns. A stale figure in a dateless
file is invisible to every decay mechanism above — the root manual is the worst case, since it
auto-loads into every session and survives compaction. The constants that cannot move out (a
README describing its own contents, a baseline recording a version) carry a **source pointer** to
where the truth is checkable — "three scripts (see the table below)" — which does its real work
at edit time, putting the check in front of whoever rewrites the sentence. Annotate only what
could not be removed. Once state has moved out, the root file's residual dated content is its
as-of line and orientation table, which its close-the-loop wording names. Do not build an
event-indexed obligation table ("if X happened, update Y") — that is a central index by another
name, and it silently rots when a surface's decay condition changes. Where the closeout *hangs* —
which machinery, if any, runs it at session end — is settled once by the session-boundary prompt
below; the deposited wording cites that answer rather than restating it.

## 3. The session-boundary prompt

**Asked once, of every folder:** *where do this folder's session boundaries live?* That is: which
machinery, if any, marks session start and session end. Wire **both bookends** to the answer —
delivery of any person-addressed surface (the session-flags register, where adopted) hangs at
session start; the close-the-loop pass hangs at session end. The answer is whatever the folder
already runs: the integrity gate's session-start mode if it runs one, the change watcher's sweep
if that is all it has, root-file prose alone if it runs nothing. A folder with no machinery gets
no machinery — the floor answer is exactly the status quo. **The prompt's deposit is the root
manual's *Session boundaries* section** — every boundary duty grouped in one place, one line per
duty, each pointing at its owning procedure file: the integrity scan where one runs, delivery of
the flags register where adopted, the monthly version check (its procedure lives in the deposited
`VERSION_BASELINE.md`), and the close-the-loop pass. Triggers live here because the root manual
is the one file guaranteed to be in context — a duty that depends on a session remembering to
open some other file misses silently — while procedure detail stays in the files each line points
to. Where the flags register is adopted, its trigger line notes that delivery is
**identity-gated and non-blocking**: no established identity → announce addressees once and hold
content, per the register's own rules. A duty adopted later, from the growth menu or otherwise,
**adds a line to this section rather than a rule elsewhere.**

## 4. The maintenance procedures — a runbook by default

The deposit is **the maintenance procedures**: how to refresh guides and syntheses, perform a
chapter-boundary rewrite (seal the arc, rewrite state-first), add a chapter, handle intake, close
a task (local surfaces, then the distant list via each surface's own decay condition, then the
root-files parity check where the dual profile applies), run the version-upgrade review (§10), and
re-verify — everything maintenance needs without this skill. **Consolidated in a runbook by
default.** A folder whose machinery already owns its procedures may instead distribute them
beside that machinery, **recording the arrangement in the recorded profile** so Phase 6's check
and every future session can find them; the default needs no recording beyond the runbook itself.

## 5. The recorded profile; scripts; logs; the backup manifest

The **recorded profile**: the dial settings and rationale from Phase 2, so future sessions
inherit the design intent instead of re-deriving it. Beside it: any **adapted kit scripts** and
the generator if one was built, the **move logs**, and the **backup manifest**.

## 6. The growth menu

**`GROWTH_MENU.md`**, adapted from the kit's exemplar: the two-axis menu — derived surfaces and
control machinery, allocated by different rules — of what this folder could grow later, with
trigger heuristics, implementation pointers into the retained kit (§7 — the artifact is the
specification of what the surface is — never of what this folder's surface must be; the menu is
only the index), the offer protocol, a considered-and-declined log, and the "invent freely" close
carrying the invention-gated developer feedback offer. The deposited intake procedure (or the
sweep flow where no inbox exists) gains one step: when a **concrete, named pattern** in the
current filings suggests a missing surface, consult the menu and offer it in one line ("three
filings this month touch the easement — want a tracker?"). The menu is for building from, not
just consulting — trigger fired, user approved, implement it. Never build unprompted or pitch in
the abstract; declined ideas are logged and not re-offered until circumstances materially change.
**Zero new lines in the root file** — the menu is on-demand meta content.

## 7. The retained kit — the menu's implementation library

**Phase 5 always deposits an exact, complete, byte-for-byte copy of `assets/kit/` into the
folder's meta home** — whether or not the `.skill` package is in hand — as a **directly readable
subtree with a stable name**: `Kit/`, adapted to the folder's own meta-naming convention. The
whole kit: `00_KIT_README.md`, every exemplar, the scripts, `LICENSE` — no zip, no subsetting
("all," not "most": the menu is open-ended, byte-identity is mechanically verifiable, and
subsets invite name-divergence). This is why the deposited growth menu's pointers and the
feedback procedure resolve locally, with no package, no installed skill, and no network. **It is
not provenance** — never describe it as the package that built the folder (that is §8's
business) — and its **version is recorded in `VERSION_BASELINE.md` and in the kit README's own
assembled-line stamp, never in the directory name**, so pointers survive upgrades unchanged.

**An immutable reference library:** open an artifact and adapt it *out* into the folder proper;
never edit or execute the retained source in place — adapted scripts and surfaces live where the
recorded profile and maintenance procedures put them. **The exclusions run *toward* the kit,
never *into* it — nothing is ever removed from the retained copy:** it is not user content, so
it earns no generated guides, sidecars, syntheses, or per-subfolder coverage (its own
`00_KIT_README.md` stays its index); censuses and statistics report it **once, as retained
infrastructure**, never counting its files as the owner's corpus; and where the folder runs
drift machinery, the subtree joins the ignore-lists and the deposit is sanctioned or blessed at
deposit time — or the machinery reports every kit file as a finding. At an approved
version-upgrade review, compare the retained kit against the newer bundle's kit and **replace it
only as part of the adopted upgrade**, staging the superseded copy (never delete). Boundary:
this guarantee holds where the full bundle's kit is readable at build time; it does not repair
the raw-`SKILL.md`/no-install gap.

## 8. The version baseline — record always, archive when in hand, never procure

Deposit a stamped **`VERSION_BASELINE.md`** in the meta folder recording, always: the skill
**version** that built the folder, the **build date**, any roadmap items **applied beyond** the
baseline, and the **repository URL** (`github.com/idea2go2go/smartfolder-skill`). Where the
`.skill` package this build ran from is **already in hand** — a user-visible archive, not merely
an installed skill — deposit the zip beside the file too, with its file count and hash: the zip,
not an unpacked payload (unpacked, `SKILL.md` is hundreds of lines of imperative build
instructions a browsing session might start applying to a folder that is already built; zipped it
is inert to casual reading and still fully diffable). **Where no package is in hand, the recorded
fields are the whole baseline — complete as recorded, not a degraded form.** Do not fetch,
repackage, or reconstruct an archive, and do not ask the owner to produce one: every published
version sits permanently at its tagged release, which the recorded URL reaches whenever content
is needed (§10) — and the retained kit (§7) already carries the artifacts later life consumes.

**Author the deposited file per the kit's `Example_VERSION_BASELINE.md`, opened first.** The
exemplar carries the recorded fields, **the monthly version check complete** (both repository
URLs, the `Last checked: YYYY-MM` stamp, the throttle and evidence rules), and the
feedback-milestone step with its offers log (§9) — so the deposit specifies the check and any
ordinary session runs it from the folder alone, this skill nowhere in the loop. The root manual
carries only the check's trigger line in *Session boundaries*. **"Any session" is scoped by the
folder's agent-population profile:** single-agent → the trigger lives in `CLAUDE.md` and Claude
sessions run the check; dual profile → every assistant reading either root twin sees the same
trigger; a non-Claude assistant joining a single-agent folder's life later is a **dial change**,
routed through the upgrade review. **The stamp is a write:** in a folder running a manifest or
drift detector, list `VERSION_BASELINE.md` as a sanctioned write target at deposit time, or the
check fires an integrity finding every month.

Exception: where the folder's own subject matter *is* the skill, deposit a stamped pointer to the
local copy rather than a duplicate that can silently drift.

## 9. The developer-feedback offer

At build close-out, **offer — never compose unasked**, in roughly this wording, adapted to the
folder: *"The developer of this skill has requested that you optionally provide statistics on the
SmartFolder that we just built. I can create an anonymized file for you to review and send to him
if you wish. Depending on your repository size, this could take 5 to 10 minutes."* The time
sentence stays — consent is informed by the cost. **Only on a yes:** compose the draft from the
retained kit's `Example_Feedback_Email.md` (§7 — `Kit/01_Universal/`, directly readable in the
meta home; opened first — it carries the statistics specification, the
anonymization rules, and the definitions that make numbers comparable), and file it in the meta
folder beside the recorded profile, dated and named unmistakably as a draft
(`YYMMDD_Draft_FeedbackEmail.md`, opening line: *composed as an example for your review; nothing
has been sent*). **The skill and its deposits never send anything; the owner reviews and sends.**
The offer re-fires at 1, 3, and 12 months after build, then every 12 months thereafter — the
schedule rides the deposited monthly version check, **evaluated at every check attempt,
delivered or not** (an unreachable repository never silences a milestone; the network's answer
is irrelevant to a birthday), and stamped at each firing in the check's feedback-offers log (the
exemplar carries the step and the log; no new machinery, no new root-file lines). Offered once per milestone; a decline stamps the firing and never suppresses
the next milestone; an explicit *"never ask again"* goes to the growth menu's
considered-and-declined log and ends the schedule.

## 10. The version-upgrade review

Deposited among the maintenance procedures (§4). The procedure: obtain the baseline version's
content — **from the deposited archive when one is in hand; otherwise from the repository's
tagged release for the recorded baseline version** (every newer package also summarizes the
deltas in its `references/VERSION_HISTORY.md`, and the public `CHANGELOG.md` carries the same
story) → diff `SKILL.md` (non-negotiables, invariant core, dials, phases, verification) **and
the whole of `references/`** — the deposit specification, the upgrade path, the version history:
behavioral instructions live there now, and a change to one escapes any review that reads
`SKILL.md` alone — and `diff -rq` the kits → classify each delta (new invariant → probably adopt; new optional surface
or machinery → a growth-menu question subject to its triggers, never an automatic yes; changed
convention → only where it does not fight the folder's established tradition) → audit and
**recommend, changing nothing** → on approval apply, update the recorded profile, log contested
decisions, re-verify → re-stamp the baseline and, where a newer package is in hand, deposit it
and retire the old artifact (staged, never deleted). **A newer skill is a newer opinion, not an
authority over a folder already in use** — the recorded profile governs unless the owner says
otherwise.
