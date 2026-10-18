# Existing SmartFolders — the full upgrade path

*Read by the skill on demand — when Phase 1 finds SmartFolder scaffolding already present; never
deposited into a user's folder. `SKILL.md`'s *Existing SmartFolders* stub routes here; the
non-negotiables and the invariant core bind on this path exactly as on a fresh build.*

When Phase 1 finds scaffolding already present: read its root file, maintenance procedures (the
runbook, in most folders), and recorded profile
first; treat the folder's established conventions as its tradition (move-don't-rename legacy names;
apply conventions to newly named files). Where the meta folder carries a version baseline, run the
folder's deposited version-upgrade review — a version-against-version diff beats guesswork. *(The
review spec deposited into new folders lives in `references/DEPOSIT_SPEC.md`, §10.)* Otherwise diff
what exists against the invariant core, propose
targeted upgrades only, and preserve hand-curated content everywhere. Include an **accretion
audit**: flag live surfaces that read as baseline-plus-dated-patches and offer chapter-boundary
rewrites (demote the narrative whole to its history home before trimming the live surface). The folder's recorded profile
— not this skill's defaults — governs its posture unless the user says otherwise.

**Deposited machinery never self-heals — so a session invoked here also carries the repairs.** A
SmartFolder maintains itself from what was deposited at build time; a defect fixed in a later
release reaches it only through this section. In any session where this skill *is* invoked on an
existing SmartFolder, check for the following and offer — never force — each repair that applies.
All are offers into the folder's own tradition: the recorded profile governs, and a convention
delta never fights a convention the folder deliberately holds.

- **The monthly version check.** A pre-existing folder without the check: **run it now** (the
  procedure as the kit's `Example_VERSION_BASELINE.md` carries it — throttle, three live-read
  versions, Offer A, the bridge ask, Offer B, the unreachable-and-empty rule) and **offer to
  deposit it** — a `VERSION_BASELINE.md` authored per that exemplar, opened first (recording the
  baseline fields — version, build date, applied-beyond, repository URL — as best the folder's
  own records establish them, if no baseline exists), plus the trigger line in the root manual's
  *Session boundaries* section (creating that section if the root predates it). Deposited once,
  the folder self-checks monthly thereafter, this skill no longer required. A folder with no
  baseline and everything declined has nowhere to park the stamp, so the check may fire again the
  same month — accepted, not solved.
  **A folder that already carries the check may carry it flawed:** where the deposited procedure
  names the releases *index* as load-bearing, offer to repair it to the current form the exemplar
  carries — **all five parts, not only the URL**: `/releases/latest` load-bearing; the
  asymmetric-evidence rule; the in-session-fetch rule (memory, training, or a cached summary is
  not evidence); both tripwires; and the repeated-failure sentence with its `(warned YYMMDD)`
  annotation. A partial repair leaves the folder able to conclude "you are current" from recall,
  or to fail silently forever — which is this defect rebuilt one generation later, in the folders
  the retrofit exists to save. A check reading a stale index concludes "you are current" wrongly,
  silently, and indefinitely.
- **The streamlined version baseline (v6.6.0).** A baseline deposited by an earlier release may
  carry the four-rung procurement ladder, a **reconstructed** route stamp, or an open flag asking
  someone to procure or rebuild the package. Offer the streamlined shape: the recorded fields —
  version, build date, applied-beyond, repository URL — are the whole baseline where no package
  is in hand; nothing is fetched, repackaged, reconstructed, or asked for. **Close or reword any
  open procurement or reconstruction flag** so it no longer reads as an actionable item — in most
  environments it never was one — and **existing deposited archives stay; never delete.** In the
  same pass: **Offer A as v6.5.0 deposited it has no false branch** for a fetch returning
  nothing, which is what the fetch does in most environments — offer the current exemplar's form,
  which hands over the permanent URL when the fetch comes back empty.
- **The retained kit (v6.6.0).** A folder built before v6.6.0 has no retained kit — its growth
  menu points into a deposited zip (which silently assumed unpack capability) or, where the
  package was never in hand, at artifacts it does not possess. Offer to deposit the retained kit
  **from this bundle's own `assets/kit/`** — whole, byte-for-byte, a stable-named `Kit/` subtree
  in the meta home — re-basing the deposited growth menu's pointer paragraph to it and recording
  the version in the baseline. Where drift machinery runs, add the subtree to its ignore-list
  and sanction or bless the deposit **in the same pass**, or the machinery reports every kit
  file as a finding the next day. Existing deposited archives stay (never delete); never
  extract from staged discards.
- **A deposited upgrade review that compares only `SKILL.md` and the kits** (every folder built
  before v6.6.0). Offer the widened comparison the current deposit carries: `SKILL.md`, **the
  whole of `references/`**, and the kits — since v6.6.0 the deposit specification and the upgrade
  path live in `references/`, so a review that never opens that folder can register a new
  version number and miss the changed instruction behind it. One sentence in the folder's
  maintenance procedures; nothing else changes.
- **Manifest keys written with the running OS's path separator (v6.7.0; every watcher and gate
  deposited before it).** A deposited `smartfolder_watch.py` or `filing_integrity.py` that builds
  its manifest keys with `str(…relative_to(…))` writes `01_Contracts/Memo.md` on macOS and
  `01_Contracts\Memo.md` on Windows, so a baseline written on one OS reports every file as drift on
  the other. Offer the patch **as a targeted edit, never a file swap** — deposited copies are
  adapted (paths, ignore-lists, conventions): write every key with `.as_posix()`, and convert `\`
  to `/` as the manifest loads. Existing baselines heal on read; no re-snapshot. In the same edit:
  every watcher `check` writes the `last_check` stamp, the root manual's session-start line names
  `check --daily`, and the watcher ignores `desktop.ini` and `Thumbs.db`. The scripts live inside
  the synced folder, so one patch reaches every machine that works it.
- **A thread-master convention without the end-of-pass `threads` check (v6.7.0; every folder
  that took the row on v6.5.0 or v6.6.0).** The deposited rule freezes a thread when a filing pass
  finds it quiet, and no pass looks. Offer, as targeted edits: the `threads` mode in the folder's
  deposited `filing_integrity.py` (its two constants set to the folder's own prefixes and
  threshold); the thread sweep as the last filing step of the inbox workflow, after every merge and
  before the re-snapshot — by hand where the folder runs no script; rule 3 of the convention and
  the master's threshold slot as the current exemplar carries them; the sidecar's pre-computed
  freeze sentence removed.
- **A session-flags register carrying the v6.3.0–v6.6.0 rules (v6.7.0).** Offer the current
  exemplar's wording: a session reads every Pending flag at session start and delivers only the
  ones addressed to whoever is present; delivery means the headline is in the session's final
  answer, and a firing is recorded only when it was; the stamp alone means the headline was given;
  the *detected miss* sentence removed. **In every v6.6.0 baseline, register or not:** the
  feedback-milestone offer is made in the final answer and logged only when the final answer
  carried it. Existing stamps stand.
- **The write-forward rule without its disposition test (v6.7.0; every folder built before it).**
  Offer the current root exemplar's clause: history of the subject is demoted whole and kept; a
  superseded draft of the record itself comes out, with the decision log its home where the
  reversal was a real decision; a session that has just corrected its own reading of the folder
  writes the corrected reading only. And the name: this is the *State Forward* discipline.
- **Rules resting on capability claims.** Where a deposited rule states a capability as its
  *reason* ("deletion is blocked here"), offer the policy-first rewording ("never delete") —
  Phase 6's finder-plus-judgment sweep is the tool, and it must not fire on genuine preconditions
  that state their false branch.
- **A session-flags register built before the identity rules.** Offer the current exemplar's
  rules: identity established, never assumed; the non-gating announcement where identity is
  absent; the stamp's evidence basis. Existing delivery stamps stand — a retrofit does not
  rewrite history.
- **A deposited growth menu without the open-the-artifact sentence.** Offer the one-line
  addition: before building any item from the menu, open the artifact it points to, then adapt it
  to the folder.
- **The outer-name suffix.** Where the folder's own name does not already end in `SmartFolder`
  (case-insensitive), the Phase 6 offer is worth a look here too — once, both steps, between
  sessions; a folder deliberately named without it has already made its choice.
