# SmartFolder Kit v6 — companion artifacts bundled with the Create SMARTFOLDER skill
<!-- Created by Paul Hess (paul@hess.club) — questions and suggestions welcome. -->

**What this is.** Working artifacts whose shapes and discipline come from three live SmartFolders
(the prompt's three precedents), assembled [260706]. The two Python scripts are working code; their
sample configuration and the example content in their docstrings are invented. Every markdown
exemplar is **fictionalized** — real shapes and discipline, invented content — so the kit is safe to
share.

**License clause (repeated from the prompt, because it governs this kit too):** these are starting
points to **adapt, never to transplant wholesale**. The diagnostic decides what a folder needs; an
artifact from a strict operational folder is over-engineering in a quiet archive. Scripts need their
root paths, folder-name conventions, and ignore-lists adapted to the target folder before first use.

## What's here, and when each artifact is warranted

| Artifact | What it is | Warranted when (the dials) |
|---|---|---|
| `01_Universal/Example_Root_CLAUDE.md` | Shape model for the resident Tier-1 root file | Always — every SmartFolder has exactly one |
| `01_Universal/Example_README_Annotating.md` | Guide that annotates and routes, no file enumeration | Live/fast-moving folders; well-named files |
| `01_Universal/Example_README_Enumerating.md` | Guide with a full annotated file map + hash marker | Archives (low change velocity); opaque filenames |
| `01_Universal/Example_Synthesis.md` | Model `_Synthesis.md` with provenance, decay, breadcrumb | Any folder whose whole exceeds its parts |
| `01_Universal/Example_Sidecar_Summary.md` | Per-file cache digest with last-mile pointers | Expensive-to-read files consulted repeatedly |
| `02_Advisory/smartfolder_watch.py` | Non-blocking change tripwire (size/mtime/hash hybrid) | Humans edit files directly; advisory posture |
| `02_Advisory/Change_Tracking_Procedure.md` | The tripwire's behavioral procedure (daily stamp, 4-option offer) | Same as above |
| `02_Advisory/Example_manifest_rows.tsv` | Baseline manifest format the watcher reads/writes | Same as above |
| `02_Advisory/Example_Operations_Hub.md` | One-page cross-folder hub (calendar / directory / sensitive-info map) | Wisdom-dominant folders with many system areas |
| `03_Operational/filing_integrity.py` | Hard integrity gate: SHA1 manifest, scan/snapshot/session-scan/bless-file | Multiple writers; drift is expensive; gating posture |
| `03_Operational/Example_Inbox_Workflow_README.md` | Sanctioned-intake workflow (all content enters via an inbox) | Multiple writers; index/entity machinery to protect |
| `03_Operational/Example_INBOX_LOCK.md` | Courtesy lock for simultaneous sessions over file sync | Two+ people may run filing passes concurrently |
| `03_Operational/Example_STATUS_BOARD.md` | One-screen, per-row-dated status board | Status-dominant folders (live workstreams) |
| `03_Operational/Example_DECISIONS.md` | Append-only dated decision log with sources | Decisions worth auditing later |
| `03_Operational/Example_REVIEW_QUEUE.md` | Mute-and-record queue for flagged drift | Hard gate + multiple non-owner users |
| `04_Generator/gen_readmes.py` + `GENERATOR_NOTES.md` | The archive precedent's working guide generator (verbatim — adapt its roots/thresholds) + the pattern it implements | Large trees (hundreds of folders) |

## Escalation logic, in one line each

- **No integrity machinery:** one user, changes flow through Claude → as-of dates are protection enough.
- **The advisory tier (02):** humans edit directly but stakes are personal → a tripwire that *offers*.
- **The operational tier (03):** several writers, live workstream, shared indexes → intake discipline,
  a lock, and a scan that *gates* filing passes (while the daily session-scan stays non-blocking).

Pick the *lowest* tier the diagnostic supports. Machinery above a folder's needs doesn't just waste
effort — it trains users to ignore the system.
