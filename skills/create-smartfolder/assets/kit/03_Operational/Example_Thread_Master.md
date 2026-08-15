# Email thread master — Meridian rent-escalation rider
*(Kit exemplar — one half of a **pair**: this append-only master plus its write-forward sidecar,
`Example_Thread_Master_Summary.md`. The pair is the species — ship both, never one. For
conversations a recurring capture path keeps fragmenting: a connector sweep, a scheduled export,
a person forwarding emails as they land. Offered via the growth menu to **capture-fed folders
only**. The convention the pair models is stated in full at the bottom of this file — in an
adopting folder, record it wherever that folder keeps its standing conventions, and point each
master at it.)*

**LIVE thread master — Tier: raw** (verbatim record; the sidecar carries the digest and is where
write-forward lives). Created [260710] by consolidating the first fragment file ledgered below;
the later fragments were absorbed as they landed.
**Appended in place as the thread grows; renamed with the last-message date only at freeze.**

- **Subject line(s):** "RE: 12 Harbor Point — escalation rider" *and* "Meridian lease — CPI floor
  language (call follow-up)" — two subject lines, one thread: the second chain continued the same
  negotiation after the [260714] call.
- **Participants so far:** Jordan Hale (Bluefield Partners, asset manager) · Dana Whitfield
  (Meridian Logistics, VP real estate) · Priya Shah (Corbett & Wilde, Bluefield's outside
  counsel). External participants present, noted for the freeze-time naming call.
- **Join keys:** deal-tracker ticket `BF-2214` ("Meridian lease — open points") + the subject
  lines above. Every capture note carrying this thread states these in its header.
- **Span:** [260701] → [260728]; 9 messages in this master.
- **Event vs capture:** messages are dated on their send date; where the repository saw a message
  later than it was sent, the capture lag is noted inline on that message.
- **Absorbed fragment files** (moved to `XX_DELETE_MANUALLY/`, one manifest line each; **resolve
  any old citation here**):
  - `260706_Inbox_EscalationRiderEmails.md` (messages 1–4) — absorbed [260710]
  - `260715_Inbox_MeridianCpiCallFollowUp.md` (messages 5–6) — absorbed [260716]
  - `260728_Inbox_EscalationCounterFixedThree.md` (messages 7–9) — absorbed [260729]
- **Live as of [260729]** — last message [260728]. This folder's provisional silence threshold:
  **21 days** (recorded [260701] as a guess, adjust on experience — see the freeze rule below).

## The record (one section per message; verbatim text is never edited)

### 1. [260701] 14:02 ET — Dana Whitfield (Meridian) → Jordan Hale (Bluefield)

> Following up on the redline: our board won't take an uncapped CPI rider. Fixed 3% is what we
> can sign this quarter.

*Attachment (Meridian markup of Exhibit F) filed as `260701_LeaseRider_MeridianMarkup.pdf`; this
master lists it, the file itself routes normally.*

### 2. [260703] 09:41 ET — Jordan Hale (Bluefield) → Dana Whitfield (Meridian)

> We can move off uncapped, but a bare fixed 3% shifts the inflation tail to us. Would Meridian
> take CPI with a 3% floor and a 5% collar?

### 3. [260705] 11:15 ET — Dana Whitfield (Meridian) → Jordan Hale (Bluefield)

> A floor-and-collar structure is more than I can approve alone — I'm taking it to the board's
> real estate committee on the 9th. Can we get your counsel and mine on a call the week after?

### 4. [260706] 08:52 ET — Jordan Hale (Bluefield) → Dana Whitfield (Meridian); cc Priya Shah (Corbett & Wilde)

> Works for us. Looping in Priya Shah, our outside counsel — her office will circulate times.
> From our side the agenda is the collar mechanics, plus whatever your committee raises.

### 5. [260714] 16:20 ET — Priya Shah (Corbett & Wilde) → Jordan Hale (Bluefield)

> Call follow-up attached as promised. Note the guarantor question: if the collar language
> changes, Castle Rock's guaranty cap in Exhibit D may need conforming edits.

*Captured [260716], two days after send — the header's event-vs-capture note explains the lag
notation. This message opened the thread's second subject line ("Meridian lease — CPI floor
language (call follow-up)"); same negotiation, same master.*

### 6. [260715] 10:07 ET — Dana Whitfield (Meridian) → Jordan Hale (Bluefield); cc Priya Shah (Corbett & Wilde)

> Useful call, thank you both. The committee wants quarter-end numbers in front of it before it
> moves on the collar question. Expect our position by month-end.

### 7. [260724] 09:30 ET — Jordan Hale (Bluefield) → Dana Whitfield (Meridian)

> Checking in ahead of month-end — anything you need from us to get the committee to a position
> on the escalation rider?

### 8. [260727] 15:44 ET — Dana Whitfield (Meridian) → Jordan Hale (Bluefield)

> Nothing further needed. The committee met this morning; a written counter is coming your way
> tomorrow.

### 9. [260728] 13:26 ET — Dana Whitfield (Meridian) → Jordan Hale (Bluefield); cc Priya Shah (Corbett & Wilde)

> Counter as promised: fixed 3% annual escalation with a one-time CPI true-up at the end of
> year 5 — the committee's answer to your inflation-tail point. The board can sign that structure
> this quarter.

## The convention this pair models

1. **The pair, and the tier assignment — explicit.** A continuing object wants a *pair*, not a
   file: this master is the **append-only raw record** — declared **raw tier**, and so **exempt
   from write-forward**; its sidecar is the derived surface, and **write-forward lives there**.
   One file cannot be both (an unreadable log or a lossy summary). The exemption is narrow: the
   master's own *header* still obeys remove-beats-annotate — reconcile the header's counts and
   span when the ledger below them grows, or the header drifts ("four fragments" above a ledger
   listing six is the recorded field failure).
2. **The grain is the relationship or matter a reader arrives asking about** — never the
   identifier the source system hands over. Task-grain over-merges (one task id can carry several
   relationships); subject-grain over-splits (one negotiation crosses subject lines). Split a
   master only when it stops answering "where does this belong."
3. **The lifecycle lives in the name.** Live masters are **dateless** (dating a live file obliges
   a rename on every edit and breaks every citation — where the folder lacks this live-file rule,
   this convention introduces it). A thread **freezes** — one rename, stamped with the
   **last-message date** — when its content concludes *or* when a filing pass finds it past the
   folder's recorded silence threshold. **Ship the shape, never the number:** the threshold is
   the folder's own, recorded as provisional (the header above carries the slot), because
   **silence in the record is a lower bound on liveness, never a measurement of it** — it
   measures the capture pipeline's lag as much as the conversation's quiet. **Freeze into
   whatever dated family the folder already sorts by; where none exists,
   `YYMMDD_Thread_<Topic>.md`.** Revival is routine, not exceptional: a new message renames the
   master back to dateless-live, former name logged in the header, references repointed in the
   same pass.
4. **Fragments merge into the master — never file beside it.** This holds only when the target is
   **declared** (this standing convention), **discoverable** (live masters listed in their
   folder's `_README.md`/index), and **matchable** (join keys — source-system id(s) plus subject
   line(s) — required in every capture note's header; that one header field is the producer's
   whole burden). **The ledger is the never-delete guarantee:** absorption is a **move, never a
   delete** — the master itemizes what it swallowed and where the originals sit, headed "resolve
   any old citation here."
5. **Open items on a frozen thread do not go quiet.** At freeze, restate any live open items on
   the folder's own status surface — wherever it tracks open work — not only inside the frozen
   pair.
6. **Backfill — the standing convention run N times, not a separate species.** Adopters arrive
   with a backlog. At any volume, **survey and propose before merging**. Then: create the master
   at the chosen grain, absorb fragments oldest-first, **ledger every absorption** (a move, never
   a delete — the originals sit where the ledger says), write the sidecar last from the assembled
   whole — and **do one thread end-to-end and review it before doing the rest.**
7. **The substance floor is discoverability, not a count.** If the live masters outgrow what
   their folder's README can list legibly, the grain is wrong (in the field, eight was
   comfortable; eighty would not be). Pure scaffolding chatter — status flips, empty subtasks —
   earns no master.
8. **Machinery interactions, in a folder that runs any of it.** A hard integrity gate sees every
   append as a legitimate CHANGED — sanctioned-edit blessing (`bless-file` or equivalent) is
   required, or the gate reports constant false drift. Write-forward and never-delete are
   resolved by rules 1 and 4 — resolve them *consciously*, or the convention reads as a
   violation of both.

---

*Kit exemplar (fictionalized — real shapes, invented content). In an adopting folder the pair is
named for its thread (e.g. `EmailThread_MeridianEscalationRider.md` + `_Summary.md`); the sidecar
moves and renames with its master, including at freeze and revival.*
