# Version baseline — which release built this folder, and the monthly check
*(Kit exemplar — the deposited `VERSION_BASELINE.md` of a finished SmartFolder. Phase 5 deposits
one in every meta folder, beside the `.skill` package it records. The monthly version check lives
here **in full — deposited, not referenced** — so any ordinary session working the folder can run
it from this file alone, the skill nowhere in the loop; the root manual carries only the trigger
line, in its *Session boundaries* section. This exemplar is mostly procedure rather than mostly
structure: the procedure IS the artifact, and the deposit is what executes monthly in the field.)*

**As of [260901].** This folder was built by the **SmartFolder Skill v6.5.0** [260820]. This file
records the exact package that built it and carries the folder's own monthly update check.

## The recorded baseline

- **Version:** v6.5.0
- **Package:** `SmartFolder Skill v6.5.0.skill`, deposited beside this file — the zip, not an
  unpacked payload: zipped it is inert to casual reading and still fully diffable.
- **Route: original** — the exact `.skill` archive this build ran from. *(The other routes, used
  when the running copy was an installed skill: **fetched** — the matching version's release asset
  from the repository, recorded with source URL and hash; **reconstructed** — the installed
  payload repackaged byte-for-byte and stamped as such, with file count and hash. Never
  fabricated: with no route reachable, the builder asks the user for the package.)*
- **File count:** 30 files in the archive
- **SHA-256:** `c7d4e19a5b02f6883e51a90bd47c6f12e08a3d9b1c5f7042a6e8d90314bfc275`
- **Applied beyond baseline:** none *(record here any roadmap items applied ahead of a release)*

**This file is a sanctioned write target.** The check stamps and annotates this file, so in a
folder running a manifest or drift detector, `VERSION_BASELINE.md` is listed as a sanctioned
write target at deposit time — otherwise the check fires an integrity finding every month.

## The three fields the check depends on

- **The latest-release URL** — `github.com/idea2go2go/smartfolder-skill/releases/latest`. The
  check reads it; **load-bearing, not descriptive**. It is the canonical latest-release redirect:
  it resolves to the release's own `…/releases/tag/vX.Y.Z` page, so the version arrives in the
  **resolved URL itself** rather than in page markup a stale render can mangle. No endpoint is
  proof against a stale cache, which is why the evidence rules below stand regardless; the
  releases *index* page may be read as optional corroboration, and where the two disagree,
  `/releases/latest` wins.
- **The permanent download URL** —
  `github.com/idea2go2go/smartfolder-skill/releases/latest/download/SmartFolder-Skill.skill`,
  stable across releases; Offer A fetches it.
- **The `Last checked` stamp** — at the bottom of this file, beside the check log.

## The monthly version check — the procedure, complete

**Who runs it:** any session working this folder, as scoped by the recorded profile's
agent-population dial — in a single-agent folder, Claude sessions, via the root manual's trigger
line; in the dual profile, any assistant reading either root twin sees the same trigger. The
check needs nothing but this file and one fetch. Offer, never force, at every step.

- **Throttle — and the stamp records an *answer*, never an attempt.** At most one delivered check
  per calendar month: `Last checked: YYYY-MM` current → skip silently. Set the stamp only when
  the check concludes with a **usable published-release answer** — including "you are current" —
  or when its offers were delivered and declined. **Never stamp an unreachable, empty, or
  unparseable result:** note the failed attempt (date, reason) in the check log below and retry
  silently at the next session boundary. Retries are invisible — a failed check never reaches an
  offer, so there is nothing to nag with; the anti-nag rule governs *offers*, and an
  answered-and-declined month re-raises only at the next month.
- **Three versions, read fresh:** the folder's **baseline** (this file); the **skill installed on
  this machine, read live** — a Claude session reads the version line of the installed skill's
  `SKILL.md` at its skill location; and the **latest published release**, from the latest-release
  URL above. Three terms because they answer three different questions: installed ahead of
  baseline → offer the assessment directly; published ahead of installed → Offer A first;
  installed ahead of published (a machine running a pre-release) → correctly, nothing.
  **Degradation is per-session:** where no installed version is readable — a non-Claude
  assistant, or Claude without the skill — the middle term is absent and the check runs
  baseline-vs-published. This file never records what is installed: folders travel across
  machines, and only the live session knows its own.
- **Offer A — the published release is ahead** (of the installed skill; of the baseline, in the
  degraded case). Name what changed in plain language — the release's own headline, never a
  generic "updates available" — and offer to **download the package itself**: one fetch of the
  permanent URL above, saved where the user can reach it. **Installing happens in Claude** —
  Settings → Skills → upload (desktop route), or `/plugin update` (marketplace route) — and that
  is a fact about the process, not the assistant: a Claude session walks the user through it; a
  non-Claude session says installing happens in Claude, hands over the downloaded bundle, and
  continues identically. No session installs or replaces Claude's installed skill itself; none
  can. Warn, verbatim concern: **upload the whole `.skill` bundle** — a chat "save skill" update
  replaces only the prompt file and strands the old kit.
- **The bridge from A to B is an explicit ask, never an assumption.** Once the user holds the
  newer version — installed, or accepted as a download — ask: *"you have vX.Y now — want
  recommendations for bringing this SmartFolder up to it?"* Offer B runs only on a yes. If A was
  declined or skipped, still proceed to B on its own condition.
- **Offer B — a newer skill than the baseline is in hand, and the user said yes:** the runbook's
  **version-upgrade review** (the runbook in this meta folder carries the procedure), unchanged.
  The assessment needs the newer version's *content*, and a downloaded `.skill` bundle serves
  exactly as well as an installed skill. Recommendations only; the recorded profile governs — **a
  newer skill is a newer opinion, not an authority over a folder already in use.** No baseline at
  all → route through the full diagnostic instead of a diff, and deposit a baseline on
  completion as if built fresh.
- **Unreachable is not an answer — and neither is emptiness.** Network or repository unreachable
  → skip Offer A silently (note it in the log, don't fail the check), still consider Offer B from
  local facts, and **leave the month unstamped** — the stamp is folder-global while environments
  are per-session, so a sandboxed session's failure must not silence a capable session's check
  for the rest of the month. **An empty or unparseable response is unreachable, never an
  answer:** release pages commonly render client-side and return empty bodies as successes, so
  distinguish *"the repository said this is latest"* from *"nothing usable came back"* — only the
  first may conclude the folder is current. **And "you are current" takes better evidence than
  "something newer exists":** *newer exists* may be concluded from any single read; *you are
  current* may be concluded only from `/releases/latest`, fetched **in this session** — a version
  recalled from memory, training, or a cached search summary is not evidence, and is treated as
  unreachable (note the attempt, do not stamp, retry at the next session boundary). **Two
  tripwires, both free:** a published version *below* this folder's own baseline is impossible —
  treat it as a stale-cache artifact, never as an answer; and one empty read anywhere in a pass
  marks the endpoint degraded and disqualifies any "current" conclusion drawn in that pass.
  **Repeated failures may speak once:** if the check log shows three or more consecutive failed
  passes, say so once — *"this folder has not been able to check for updates since [date]"* —
  then **annotate that newest failure note `(warned YYMMDD)`**, so a later session can tell
  "three failures, never warned" from "three failures, already warned," and does not repeat it. A
  successful pass clears the run; a fresh run of three carries no annotation and is eligible
  again.

## The stamp and the check log

**Last checked: 2026-09**

*(Newest first. A failed attempt is noted here, never stamped; a delivered check updates the
stamp above and may add a one-line record.)*

- [260901] Pass delivered — published v6.5.0 = installed v6.5.0 = baseline; current. Stamped
  2026-09.
- [260828] Attempt failed — repository unreachable from a sandboxed session. Month left
  unstamped; retried at a later session boundary.

---

*Status surface — deposited [260820] at build close-out; the check re-stamps it monthly and the
version-upgrade review re-stamps it at each adopted upgrade. Decays when: a newer release is
adopted without re-stamping, or the repository URLs change. To refresh: ask your AI assistant to
update this.*
