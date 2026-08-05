# Changelog — SmartFolder Skill

All notable changes to the SmartFolder Skill, one story per version, newest first.
The skill turns a folder of files into a SmartFolder — a self-describing,
self-maintaining knowledge layer over your real files. Install and docs:
[README](README.md) · [Latest release](https://github.com/idea2go2go/smartfolder-skill/releases/latest)

## v6.3.0 — 2026-08-05

Five improvements, in plain terms:

- **Notes that wait for the right person.** Folders used by several people can now
  keep *session flags*: a note addressed to one person, delivered the next time
  they sit down with the folder — a question for a colleague, a heads-up for the
  owner. One line up front, details on request, and it never nags. The kit gains a
  full worked exemplar (`Example_SESSION_FLAGS.md`), and every folder is now asked
  once where its session boundaries live, so both session-start delivery and
  session-end tidy-up have a defined home.
- **Folders check for their own updates — politely.** Each new SmartFolder is
  built carrying the update check *inside it*, so the folder looks after itself
  and this skill needn't be installed for that to work. About once a month, a
  session working in the folder compares your installed skill and the folder's
  own baseline against the latest published release. If something is newer, it
  says what changed in plain language and offers to fetch the new package for
  you; installing stays in your hands, in Claude. Nothing changes without your
  say-so, an offline folder simply carries on and quietly tries again later, and
  an already-built folder can be offered the same check the next time you use
  the skill on it.
- **A label on the discard pile.** Nothing is ever deleted; discards are staged in
  a set-aside folder the owner empties by hand. That folder now keeps a one-line
  note per item — what was staged, when, and why — so emptying it never means
  deleting unlabeled files on trust.
- **Housekeeping names that explain themselves.** The drop-off folder is now
  simply `XX_INBOX`, and the set-aside folder is `XX_DELETE_MANUALLY` (existing
  folders keep their old names unless you ask for the rename). Along the way this
  fixed a bug where the guide generator could write guides into the very folder it
  was supposed to leave alone.
- **Pages that resist going stale.** The rules the skill deposits now keep dated
  facts — counts, versions, statuses — on the dated status pages and out of the
  permanent instruction files, and the finishing checklist reliably covers the
  far-away pages (like "what's published where") that used to slip.

## v6.2.0 — 2026-07-28

The biggest update yet — seven improvements:

- **Plays well with the other AI assistants that work in folders.** Every
  SmartFolder's operating manual now also ships as an `AGENTS.md` twin — the open
  instruction format read by ChatGPT Work, Codex, Cursor, GitHub Copilot, and a
  growing ecosystem of tools — kept verifiably in step with Claude's copy.
  Folders used only with Claude are unchanged.
- **Asks first about other people's files.** If the folder holds an absent
  owner's files, the skill suggests a warm one-page note before anything moves;
  the kit adds a model owner letter and a "your records, made answerable" welcome
  guide for non-technical owners.
- **A growth menu.** Each finished folder carries a menu of what it could grow
  next — trackers, dashboards, protections — offered only when a real pattern in
  your files calls for it.
- **Upgrades by comparison, not guesswork.** Each folder keeps the exact skill
  package that built it, so a future upgrade is a precise, reviewable diff — and
  the folder's own established conventions always win unless you say otherwise.
- **Summaries that stay current.** Any session that lands new information
  finishes by bringing every affected summary and status page up to date —
  including the big-picture ones far from where the work happened.
- **A playbook for shared folders.** Folders with strict filing rules get a
  complete, friendly drift-disposition reference, with no-blame wording.
- **A feedback path.** If your folder's assistant invents a genuinely useful new
  kind of surface, it can — only with your OK, and with none of your data —
  write the idea up for you to send the developer.

Also: display name corrected to *SmartFolder Skill*; kit README script count
corrected.

## v6.1.1 — 2026-07-25

First public release, at this repository. A hygiene patch over v6.1: the kit
scripts' sample configuration and docstring examples use invented placeholder
content throughout. No functional change.

## Earlier

v6.1 and its predecessors predate the public channel and shipped privately; their
history is summarized in each release's `Readme.txt`.

---

Questions, problems, or ideas: paul@hess.club
