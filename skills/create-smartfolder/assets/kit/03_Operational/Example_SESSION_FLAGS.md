# Session flags — person-addressed notes for whoever is here next
*(Kit exemplar — a person-addressed notification register for folders several people use. A
conditional surface: offered only where the writers-and-users dial shows collaborative use; a
single-writer folder never needs it. The tier split is the load-bearing idea — the root file
carries only the trigger; THIS file carries all content and state, so adding, answering, or
retiring a flag is never a root-file edit.)*

**As of [260708]. Tier 3 — this folder's cross-session, cross-person channel.** A flag answers
"next time person X is in a session here, tell or ask them Y": a question raised for a colleague,
a decision deferred to the maintainer, a defect that needs relaying. Without this surface those
get lost, get manually re-raised each time, or bloat the root file.

## How flags work (the seven rules)

1. **Identity-matched firing.** Every flag names its addressee by email; it is delivered only when
   that person is the session user — the same identity basis as any other user-conditional rule.
2. **Retrieval is unconditional; delivery is filtered.** The session-start step prints *every*
   Pending flag into context on every run; only the flags addressed to the person present are
   delivered. Firing that depends on a session remembering to open this file misses silently.
3. **Headline first, detail on request.** Delivery is the entry's one-line `Headline:` plus an
   offer of detail; the full `Ask / tell` body waits until the person engages. Non-blocking —
   state it, then get on with what was actually asked.
4. **Once per session, stamped.** One mention per session, appended to the entry's `Fired:` line
   as `[YYMMDD] (chat)` or `[YYMMDD] (Slack)`. No engagement leaves it Pending, to re-fire next
   session. A Pending flag whose addressee has had sessions but no fresh stamp is a **detected
   miss** — say so, and deliver late.
5. **Delivery routing — interactive vs. autonomous.** Interactive session → chat. Scheduled or
   unattended run (nobody is reading a chat) → deliver out-of-band (here: Slack DM) and note it in
   the run's digest — never write into the void. Autonomous re-delivery is throttled to once per
   7 days, gated on the last `(Slack)` stamp; interactive delivery stays once per session,
   ungated.
6. **Answering and applying are separate steps.** Record the answer close to verbatim, move the
   entry to *Resolved*, and create any follow-on flag it calls for — a flag may exist to carry a
   notification onward to a third person. **A raiser who already knows the next step names it in
   the `Ask / tell`** ("once you answer, create a new flag for X to action on…"), so the chain is
   requested at raise time and produced mechanically at resolution, not left to someone
   remembering — FLAG-01 → FLAG-03 below is the worked case. If an answer changes a convention or
   a fact elsewhere,
   route it to its real home and note the provenance: this register is the *conversation*, never
   the destination.
7. **Optional `Escalate:` clause.** *"If still Pending on/after [YYMMDD], also notify person B"* —
   because an addressee who never opens a session leaves a flag Pending forever. The subtle
   consequence: checking flags for the current user means evaluating **two** sets — flags
   addressed to them, *and* flags whose escalation names them and whose date has arrived. Miss the
   second and the fallback silently never fires. Escalations stamp `Escalated:` and re-nudge at
   most weekly.

**Scope.** Flags are person-addressed asks and tells that must survive the session boundary. Tasks
belong on the status board and decisions in the decision log; a flag may point at either, never
replace them.

**Where firing hangs.** Delivery wires to wherever this folder's session boundaries live — named
in the root file; here, the integrity script's session-start step. **Known residual failure
mode:** a session whose start trigger never runs delivers nothing. This register cannot fire
itself, and hardened retrieval does not fix a trigger that was skipped.

## Pending

### FLAG-04 → Jordan (jordan@bluefield.example)
- **Status:** Pending · raised [260629] by Alex
- **Headline:** Did the CPI-floor concession come up in your [260630] Meridian call?
- **Ask / tell:** The rent-escalation rider is the last open point on HP-LEASE. If Meridian raised
  the CPI floor on the [260630] call, the execution draft's rider needs their language before the
  status board row can move. One sentence back is enough.
- **Fired:** [260701] (chat)
- **Escalate:** if still Pending on/after [260713], also notify Alex (alex@bluefield.example)

### FLAG-05 → Alex (alex@bluefield.example)
- **Status:** Pending · raised [260630] by Sam
- **Headline:** The structural study's sidecar flags a load figure that contradicts the vendor
  deck.
- **Ask / tell:** The [260619] structural study says the roof passes with the racking change at
  4.1 psf; Kestrel's deck from the same week says 4.6. The sidecar carries both figures with
  last-mile pointers. Maintainer's call which number the HP-SOLAR board row and the
  interconnection application should carry.
- **Fired:** [260701] (chat) — no engagement; re-fires next session

### FLAG-06 → Jordan (jordan@bluefield.example) — conditional, date-gated
- **Status:** Pending · raised [260625] by Alex
- **Condition:** arms only once the interconnection application shows as filed
- **Headline:** When the interconnection application goes in, confirm the rebate paperwork went
  with it.
- **Ask / tell:** The utility's rebate window closes [260801]; filing the application without the
  rebate attachment forfeits it silently. When the application is filed, confirm the attachment
  went in the same submission.
- **Fired:** —
- **Evidence note [260708]:** the portal now shows *submitted — pending documents*. The literal
  condition ("filed") has partially cleared while the substance (a complete submission) has not —
  **do not resolve this flag on the mechanical test**; it stays Pending until the attachment is
  confirmed.

## Resolved (history)

### FLAG-01 → Jordan (jordan@bluefield.example) — resolved [260626]
- **Headline:** Which insurance certificate did Meridian actually receive?
- **Ask / tell:** The entity index shows two certificate versions issued in June; the countersign
  package must reference the one Meridian holds. **Once you answer, create a new flag for Sam
  (sam@bluefield.example) to action the result** — whichever version Meridian is missing, Sam is
  the one who sends it.
- **Fired:** [260624] (chat)
- **Answered [260626]:** "They have the [260618] certificate — the [260622] reissue was never
  sent."
- **Applied to:** entity index (certificate row corrected, provenance noted).
- **Follow-on:** FLAG-03 raised to Sam, as this flag's Ask / tell requested — send Meridian the
  [260622] reissue.

### FLAG-02 → Alex (alex@bluefield.example) — resolved [260627]
- **Headline:** A vendor invoice was retro-filed from outside the inbox; the scan blessed it.
- **Ask / tell:** Found during the [260626] filing pass; retro-filed with sidecar, dispositioned
  as retro-file, manifest re-snapshotted. Telling, not asking — no action needed unless the vendor
  folder's convention should change.
- **Fired:** [260627] (chat)
- **Answered [260627]:** "Fine as handled; no convention change."
- **Applied to:** nothing — no convention change.
- **Follow-on:** none.

### FLAG-03 → Sam (sam@bluefield.example) — resolved [260629]
*(Spawned by FLAG-01's answer, exactly as its Ask / tell requested — the raiser specified the
chain in advance, so resolving FLAG-01 mechanically produced this flag rather than relying on
someone remembering the next step.)*
- **Headline:** Meridian never received the [260622] certificate reissue — please send it.
- **Ask / tell:** The countersign package references the reissue; Meridian holds only the [260618]
  version. Send the reissue and note it in Correspondence.
- **Fired:** [260628] (Slack) — autonomous morning sweep; noted in the run digest
- **Answered [260629]:** "Sent [260629]; filed under Correspondence with a one-line note."
- **Applied to:** Correspondence folder (the reissue plus note).
- **Follow-on:** none.

<!-- Entry template — copy, fill, delete the comments.

### FLAG-NN → Addressee Name (email)            [append "— conditional, date-gated" if it applies]
- **Status:** Pending · raised [YYMMDD] by <name>
- **Condition:** (conditional flags only — the objective event that arms this flag)
- **Headline:** One sentence, readable in isolation.
- **Ask / tell:** The full body — enough that the addressee can act without hunting.
- **Fired:** — (append [YYMMDD] (chat) or [YYMMDD] (Slack) per delivery)
- **Escalate:** if still Pending on/after [YYMMDD], also notify <person B> (email)     (optional)

On resolution: record the answer near-verbatim ("Answered [YYMMDD]:"), name what it was applied
to, spawn any follow-on flag, and move the entry under Resolved.
-->

---

*Derived surface — this register is the conversation, never the destination; answers route to
their real homes. Decays when: any flag is added, delivered, answered, or escalated without its
entry being updated. To refresh: ask your AI assistant to update this register.*
