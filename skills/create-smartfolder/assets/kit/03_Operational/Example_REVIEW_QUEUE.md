# Review Queue — items flagged for the maintainer
*(Kit exemplar — the "mute and record" pattern for multi-user folders with a hard integrity gate.
It solves alert fatigue without silent blessing: muting stops the same drift re-alerting every
colleague daily; recording ensures the maintainer still processes it properly.)*

Items a team member chose to **"flag for the maintainer to review later"** on the non-blocking
session-start route. Each item was muted in the manifest (via `bless-file`, which touches only that
one file) so it stops re-flagging colleagues day after day, and recorded here so it is never lost.

**Why mute *and* record:** leaving an item flagged re-alerts every colleague repeatedly; muting
without recording would bless it silently and lose the content. Muting + queuing does both jobs.
Muting happens **only** on an explicit flag; a team member who simply continues without choosing
leaves the drift flagged, as the safety net.

**Lifecycle:** team member flags → entry added to *Pending* + that one file muted → the maintainer
reviews at the next filing pass (or at session start) → item is processed or accepted → entry moved
to *Resolved* with disposition + date → end-of-pass `snapshot` re-blesses the properly-filed state.

---

## Pending

_(none)_

<!--
Entry template — copy under "## Pending" when an item is flagged:

### [YYMMDD] <relative/path> — <ADDED | CHANGED | MOVED | REMOVED>
- **Finding:** <e.g. CHANGED, 6.1 KB → 6.5 KB (grew 310 B)>
- **Flagged by:** <session user> on [YYMMDD]
- **Note:** <anything the team member said; "none">
- **Muted:** yes (`bless-file`) — won't re-alert until it changes again
-->

---

## Resolved (history)

_(none yet)_

<!--
On resolution, move the entry here and append:
- **Reviewed by maintainer:** [YYMMDD]
- **Disposition:** <filed via inbox / accepted as-is / reverted / other>
-->
