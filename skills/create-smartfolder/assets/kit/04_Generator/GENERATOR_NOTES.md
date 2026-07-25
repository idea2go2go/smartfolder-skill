# Generator pattern — for large trees (hundreds of folders)
*(Kit note — `gen_readmes.py` in this folder is the working generator behind the archive precedent.
Before use, adapt its `ROOTS` list, mount autodetection, and `qualifies()` thresholds to the target
folder. Its sample configuration and the area descriptions in its docstrings are invented example
content, written for an archive of that shape — replace both with your own.
Everything below is the pattern it implements.)*

## The pattern

Separate the **deterministic scaffolding** from the **authored prose**:

- The script emits each guide's mechanics — headers, the file map (names, types, date spans, folded
  leaf folders), parent/child links — from a walk of the tree.
- The prose ("For people" descriptions, any synthesis) lives in a **content layer** (e.g.
  `summaries.json`) merged in at generation time. The prose must still be authored from real
  contents — the generator must never auto-fill low-signal filler, and this goes double for syntheses.

## The hash marker (how regeneration preserves human edits)

Each generated guide ends with an invisible marker recording a hash of its generated content:

`<!-- smartfolder-auto:v2 sha256=<hash> — auto-generated; edit freely, manual changes are preserved on regen -->`

On re-run, the generator re-hashes the guide body: if it matches the stored hash, the guide is
untouched and safe to regenerate; if it differs, a human edited it — **skip and preserve.** The
version token (`v2`) allows the marker schema itself to evolve.

## Operational rules

- The generator lives in the SmartFolder's meta folder (deposited in Phase 5), so any future session
  can re-run it as new content arrives: add guides for new folders, refresh untouched guides, prune
  filler, always preserving hand edits. Support `--dry-run`.
- Never generate inside macOS bundles or trash/staging folders.
- At parallel scale, give each sub-agent one disjoint chapter, its own move-log, and a required
  integrity report (source vs. result counts); the main session stamps the hashes.
- Small folders don't need any of this — write guides directly; the as-of line is mandatory, the
  marker optional.
