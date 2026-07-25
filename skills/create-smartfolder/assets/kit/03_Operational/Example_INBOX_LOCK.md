# Inbox processing lock
*(Kit exemplar — a courtesy lock for shared folders synced over Dropbox or similar. It is a
persistent toggle, never deleted. Note the dual audience: a plain-English note for humans, machine
instructions for Claude.)*

**STATUS: UNLOCKED**

- **Last holder:** Alex (alex@bluefield.example), via Claude (Cowork)
- **Acquired:** [260701] 13:28 ET (17:28 UTC)
- **Released:** [260701] 13:44 ET (17:44 UTC) — filing pass, 3 files
- **Outcome:** Filed the [260628] lease redline (+ sidecar), the structural study, and one vendor
  invoice; indexes and board updated; scan CLEAN; snapshot refreshed.

---

## If you're a person reading this: you don't need to do anything

This file is housekeeping between the Claude assistants that work in this shared folder. When
someone asks their Claude to file the inbox, their Claude marks this file LOCKED while it works and
UNLOCKED when it finishes; a second Claude that sees the lock politely waits its turn.

- **Keep dropping files into this folder exactly as you always have** — always safe, LOCKED or not.
- **Please don't edit, move, or delete this file.** It lives here permanently by design.
- If it has said LOCKED for many hours and that seems wrong, mention it to the maintainer — or ask
  your own Claude, which knows how to handle a stale lock safely.

---

## Protocol for Claude sessions (machine instructions)

1. **Read this file first**, before any filing pass.
2. If **UNLOCKED** — overwrite the block above the first `---` with `STATUS: LOCKED`, the user's
   name/email, the Claude model/surface, an `[YYMMDD] HH:MM (tz)` timestamp, and a one-line
   description of the pass. Wait ~30 seconds for sync, re-read to confirm you are still the holder,
   and check this folder for `... (conflicted copy) ...` siblings (created on simultaneous writes —
   if one exists, both parties back off, stage the conflicted copies for manual deletion, retry in a
   few minutes). Then proceed.
3. If **LOCKED** — do not process; tell your user who holds it and since when. Exceptions: a lock
   **older than 2 hours** is probably a crashed session — say so and ask whether to take it over
   (never silently); a lock naming **the same user** is likely their own interrupted session — offer
   immediate re-acquire, out loud.
4. **On finish** (after the final integrity snapshot), set `STATUS: UNLOCKED` and record the release
   (holder, timestamps, one-line outcome). Keep at most three release entries, dropping the oldest.
   Note explicitly if the pass ended incomplete. **Never delete this file.**

**Honest caveat:** sync latency makes this a strong courtesy mechanism, not a true mutex — the
30-second confirm-and-recheck catches most races; the conflicted-copy check catches the rest. When
in doubt, coordinate by message.
