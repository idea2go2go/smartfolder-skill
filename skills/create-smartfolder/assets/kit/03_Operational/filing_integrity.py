#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Paul Hess (paul@hess.club)
# Part of the SmartFolder Skill kit. Released under the MIT License;
# full text in the LICENSE file at the kit root. Questions: paul@hess.club.
"""Filing integrity scanner for a shared, multi-writer deal workspace.

Detects files added, removed, changed, or moved outside the normal
XX_INBOX filing process, and lists the live thread masters that have gone
quiet past the folder's silence threshold.

Five modes:
  snapshot      Walk the project tree and write the manifest (the "known,
                properly-filed state"). Run after every filing pass, and after
                resolving any drift found by a scan. Blesses the WHOLE tree.
  bless-file    Mute a SINGLE file: upsert (or, if gone, remove) just that one
                path's manifest entry, leaving all other drift still flagged.
                Used to mute a change the user explicitly blessed or flagged
                for later review, without blessing unrelated coexisting drift.
                Usage: filing_integrity.py bless-file "relative/path.ext"
  scan          Walk the tree, diff against the manifest, and print a report:
                ADDED / REMOVED / CHANGED (with size delta) / MOVED.
                Exit code 0 = clean, 1 = drift found, 2 = no manifest yet.
                Always runs — this is the ungated filing-pass scan.
  session-scan  Same as scan, but GATED to run at most once per calendar day.
                Used by the session-start route (see CLAUDE.md). It records the
                date of its last run in last_session_scan.txt; if that date is
                today it prints a "skipping" line and exits 0 without walking
                the tree. The first session-scan of the day stamps the date
                (regardless of outcome) and then runs a normal scan, so drift
                surfaces at most once per day through this route. The filing
                pass uses plain 'scan' and is never affected by the stamp.
  threads       Read-only. Walk the tree reading only thread masters (files
                whose names start with one of THREAD_PREFIXES; their
                _Summary.md sidecars are skipped), take each master's
                last-message date from its message headings — the latest
                [YYMMDD] in the first 30 characters of a heading that
                MESSAGE_HEADING_RE recognizes as a message (level 2-4,
                leading with a number, "Message", or the bracketed date;
                the title and worded section headings never count); never
                the header line, which drifts — and print every live master
                quietest first with the days since its last message. A master
                at or past FREEZE_AFTER_DAYS is marked FREEZE DUE; a master
                with no dated heading prints ?? (open it and date it by hand).
                Exit code 1 if any master is due, else 0. Hashes nothing and
                writes nothing: the filing pass runs it as its last filing
                step, after every merge and before 'snapshot', and decides
                each freeze itself.

Usage (from anywhere; project root is inferred from the script location,
or pass --root explicitly):
  python3 filing_integrity.py snapshot
  python3 filing_integrity.py scan
  python3 filing_integrity.py session-scan
  python3 filing_integrity.py threads
  python3 filing_integrity.py scan --root "/path/to/project"

Design notes:
  - Manifest is a TSV: relative_path <TAB> size_bytes <TAB> sha1. The
    relative path is written with "/" on every OS, and a "\\" in a manifest an
    older version wrote is normalized on load — one baseline serves a folder
    worked from macOS and Windows alike.
  - Excluded from tracking: XX_INBOX/ (the inbox is expected to
    churn), any XX_DELETE_MANUALLY/ folder, hidden files/folders
    (.DS_Store etc.), macOS custom-folder-icon marker files ("Icon\r"),
    OS/app by-products (desktop.ini, Thumbs.db, "~$" lock/temp files),
    and the manifest itself. macOS bundle-package directories (.pages,
    .key, etc.) are atomic: never descended into or content-tracked.
  - "Changed" = same path, different content hash. Mod dates are not used:
    sync tools and Finder touch them without changing content.
  - "Moved" = same content hash disappeared from one path and appeared at
    another (reported as a move, not an add+remove pair).
"""

from __future__ import annotations  # keeps 3.9-compatible annotations (see read_stamp)

import argparse
import datetime
import hashlib
import re
import sys
from pathlib import Path

MANIFEST_NAME = "manifest.tsv"
STAMP_NAME = "last_session_scan.txt"
QUEUE_NAME = "REVIEW_QUEUE.md"
EXCLUDED_DIRS = {"XX_INBOX", "XX_DELETE_MANUALLY", "__pycache__"}
# macOS custom-folder-icon marker files are literally named "Icon" + a trailing
# carriage return ("Icon\r"). They carry a 0-byte data fork (the icon lives in
# the resource fork) and reappear whenever a folder with a custom icon syncs,
# e.g. through Dropbox or after a folder move. Pure OS cruft like .DS_Store, so
# excluded from tracking. Matched exactly so a genuine file named "Icon" is not.
EXCLUDED_FILE_NAMES = {"Icon\r", "desktop.ini", "Thumbs.db"}
# Office lock/temp files ("~$Budget.xlsx"); ".~lock.…#" files are caught by the
# hidden-file rule. These appear when someone merely opens a document and would
# otherwise generate recurring phantom ADDED/REMOVED findings.
EXCLUDED_FILE_PREFIXES = ("~$",)
# macOS bundle-package directories are atomic (skill non-negotiable 4): never
# descend into or track their contents. Mirrors smartfolder_watch.py.
BUNDLE_EXTS = {".pages", ".numbers", ".key", ".rtfd", ".webarchive",
               ".oo3", ".ooutline", ".goodnotes", ".more"}

# --- Thread masters: the 'threads' mode. These constants are this folder's own to set. ---
# A file whose name starts with one of THREAD_PREFIXES is a live thread master (the
# convention names live masters dateless, e.g. "EmailThread_<Topic>.md"; a frozen master
# leads with its last-message date, so it never matches). Sidecars ("*_Summary.md") are
# skipped. FREEZE_AFTER_DAYS is the folder's silence threshold in days: the thread-master
# convention's header mirrors this number — change both together. Silence in the record
# is a lower bound on liveness, so 'threads' lists and marks; the filing pass decides.
THREAD_PREFIXES = ("EmailThread_", "ChatThread_", "Thread_")
FREEZE_AFTER_DAYS = 14
# A heading is a MESSAGE heading when it is level 2-4 and its text leads with a number, the
# word "Message", or the bracketed date: "### 1. [260701] 14:02 ET — ...", "## 3. [260817]",
# "## Message 9 — [260928]", "## [260924] 3:54 PM ET — ...". The H1 title and worded section
# headings ("## Hearing prep [261115]") never count, so a date in a title cannot outrank the
# last message. Adapt this constant to the folder's own heading form, like the two above.
MESSAGE_HEADING_RE = re.compile(r"^#{2,4}\s+(?:\d|Message\b|\[)")
# A message heading carries its date in the first 30 characters: "### 3. [260705] ...".
HEADING_DATE_RE = re.compile(r"\[(\d{6})\]")
HEADING_DATE_SPAN = 30


def script_dir() -> Path:
    return Path(__file__).resolve().parent


def default_root() -> Path:
    # script lives at <root>/09_Meta_and_Index/Filing_Integrity/
    return script_dir().parent.parent


def manifest_path(root: Path) -> Path:
    return root / "09_Meta_and_Index" / "Filing_Integrity" / MANIFEST_NAME


def stamp_path(root: Path) -> Path:
    return root / "09_Meta_and_Index" / "Filing_Integrity" / STAMP_NAME


def queue_path(root: Path) -> Path:
    return root / "09_Meta_and_Index" / "Filing_Integrity" / QUEUE_NAME


def state_files(root: Path) -> set:
    """Scanner control files that are never treated as project content."""
    return {manifest_path(root), stamp_path(root), queue_path(root)}


def today_str() -> str:
    return datetime.date.today().isoformat()


def sha1_of(path: Path) -> str:
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def walk_tree(root: Path) -> dict:
    """Return {relative_path_str: (size, sha1)} for all tracked files."""
    entries = {}
    skip = state_files(root)

    def recurse(d: Path):
        try:
            children = sorted(d.iterdir())
        except PermissionError:
            return
        for p in children:
            if p.name.startswith("."):
                continue  # hidden files/dirs: .DS_Store, .git, etc.
            if p.is_dir():
                if p.name in EXCLUDED_DIRS:
                    continue
                if p.suffix.lower() in BUNDLE_EXTS:
                    continue  # atomic bundle: never descend into or track contents
                recurse(p)
            elif p.is_file():
                if p.name in EXCLUDED_FILE_NAMES or p.name.startswith(EXCLUDED_FILE_PREFIXES):
                    continue  # OS/app by-products, not content
                if p in skip:
                    continue  # scanner state files, not project content
                size = p.stat().st_size
                entries[p.relative_to(root).as_posix()] = (size, sha1_of(p))

    recurse(root)
    return entries


def load_manifest(root: Path) -> dict:
    m = {}
    with open(manifest_path(root), encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            rel, size, digest = line.rsplit("\t", 2)
            # Keys use "/" on every OS; heal a manifest an older version wrote with "\\".
            m[rel.replace("\\", "/")] = (int(size), digest)
    return m


def write_manifest(root: Path, entries: dict):
    mpath = manifest_path(root)
    mpath.parent.mkdir(parents=True, exist_ok=True)
    with open(mpath, "w", encoding="utf-8") as f:
        for rel in sorted(entries):
            size, digest = entries[rel]
            f.write(f"{rel}\t{size}\t{digest}\n")


def human(n: int) -> str:
    """Human-readable byte count."""
    f = float(n)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if f < 1024 or unit == "TB":
            return f"{f:,.0f} {unit}" if unit == "B" else f"{f:,.1f} {unit}"
        f /= 1024
    return f"{n} B"


def read_stamp(root: Path) -> str | None:
    p = stamp_path(root)
    if p.exists():
        return p.read_text(encoding="utf-8").strip()
    return None


def write_stamp(root: Path):
    p = stamp_path(root)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(today_str() + "\n", encoding="utf-8")


def cmd_session_scan(root: Path) -> int:
    """Daily-gated scan for the session-start route.

    Runs a normal scan at most once per calendar day. The filing-pass 'scan'
    is unaffected by the stamp and always runs.
    """
    today = today_str()
    if read_stamp(root) == today:
        print(f"Session integrity scan already run today ({today}); skipping.")
        print("(The filing-pass 'scan' still runs unconditionally.)")
        return 0
    # Stamp before scanning so a given calendar day triggers this route at most
    # once, regardless of the scan's outcome (clean or drift). Drift therefore
    # surfaces once per day here until a filing pass resolves and re-snapshots.
    write_stamp(root)
    print(f"Daily session integrity scan ({today}):\n")
    return cmd_scan(root, hard_gate=False)


def cmd_bless_file(root: Path, target: str) -> int:
    """Mute ONE file by upserting/removing only its manifest entry.

    Unlike 'snapshot' (which rewrites the whole manifest from the current tree
    and would therefore bless *all* current drift), this touches a single path
    and leaves every other drift still flagged. Used to mute a change the user
    explicitly blessed or flagged for later review, without accidentally
    blessing unrelated drift that happens to coexist.
    """
    if not manifest_path(root).exists():
        print("NO MANIFEST: no baseline exists yet. Run 'snapshot' first.")
        return 2

    p = Path(target)
    if not p.is_absolute():
        p = root / target
    try:
        rel = p.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        print(f"Path is outside the project root: {target}")
        return 2

    if p.resolve() in {sf.resolve() for sf in state_files(root)}:
        print("Refusing to bless a scanner state file "
              "(manifest / stamp / review queue).")
        return 2

    m = load_manifest(root)
    if p.exists() and p.is_file():
        size = p.stat().st_size
        digest = sha1_of(p)
        action = "updated" if rel in m else "added"
        m[rel] = (size, digest)
        write_manifest(root, m)
        print(f"Muted (blessed) in manifest [{action}]: {rel}  [{human(size)}]")
        print("Any other drift is left untouched and still flagged.")
        return 0

    # File is not present on disk.
    if rel in m:
        del m[rel]
        write_manifest(root, m)
        print(f"Muted removal (manifest entry dropped): {rel}")
        print("Any other drift is left untouched and still flagged.")
        return 0

    print(f"Nothing to do: '{rel}' is neither on disk nor in the manifest.")
    return 2


def is_thread_master(p: Path) -> bool:
    return (p.suffix.lower() == ".md"
            and p.name.startswith(THREAD_PREFIXES)
            and not p.name.endswith("_Summary.md"))


def thread_masters(root: Path) -> list:
    """Every live thread master under root, with the same exclusions as walk_tree."""
    found = []

    def recurse(d: Path):
        try:
            children = sorted(d.iterdir())
        except PermissionError:
            return
        for p in children:
            if p.name.startswith("."):
                continue
            if p.is_dir():
                if p.name in EXCLUDED_DIRS or p.suffix.lower() in BUNDLE_EXTS:
                    continue
                recurse(p)
            elif p.is_file() and is_thread_master(p):
                found.append(p)

    recurse(root)
    return found


def last_message_date(master: Path):
    """The latest [YYMMDD] found in the first HEADING_DATE_SPAN characters of any
    message heading (a line MESSAGE_HEADING_RE matches). Returns a datetime.date, or
    None when no message heading carries a date. The title, worded section headings,
    and the header line's own dates are never read: the header is derived from the
    headings and drifts, and a dated title would outrank the last message. Two-digit
    years follow the folder convention (SKILL.md): 90-99 -> 1990s, else 2000s."""
    latest = None
    with open(master, encoding="utf-8", errors="replace") as f:
        for line in f:
            if not MESSAGE_HEADING_RE.match(line):
                continue
            for yymmdd in HEADING_DATE_RE.findall(line[:HEADING_DATE_SPAN]):
                try:
                    yy = int(yymmdd[:2])
                    d = datetime.date((1900 if yy >= 90 else 2000) + yy, int(yymmdd[2:4]), int(yymmdd[4:6]))
                except ValueError:
                    continue
                if latest is None or d > latest:
                    latest = d
    return latest


def cmd_threads(root: Path) -> int:
    """List live thread masters quietest first; mark those at or past the threshold.

    Read-only — hashes nothing, writes nothing. Exit 1 if any master is FREEZE DUE.
    """
    today = datetime.date.today()
    dated, undated = [], []
    for m in thread_masters(root):
        rel = m.relative_to(root).as_posix()
        d = last_message_date(m)
        if d is None:
            undated.append(rel)
        else:
            dated.append(((today - d).days, d, rel))
    dated.sort(key=lambda t: (-t[0], t[2]))
    due = [t for t in dated if t[0] >= FREEZE_AFTER_DAYS]

    total = len(dated) + len(undated)
    if total == 0:
        print(f"No live thread masters found (prefixes {', '.join(THREAD_PREFIXES)}).")
        return 0
    print(f"Live thread masters: {total}, quietest first — silence threshold "
          f"{FREEZE_AFTER_DAYS} days, today {today.isoformat()}.")
    for days, d, rel in dated:
        mark = "FREEZE DUE" if days >= FREEZE_AFTER_DAYS else ""
        print(f"  {mark:<10} {days:>4} d  last message [{d.strftime('%y%m%d')}]  {rel}")
    for rel in undated:
        print(f"  {'??':<10} {'--':>4} d  no dated message heading   {rel}  — open it and date it by hand")
    if due:
        print(f"\n{len(due)} FREEZE DUE — propose each freeze to the user (thread-master rule 3): one"
              " rename stamped with the last-message date, the sidecar with it, references"
              " repointed, open items restated on the status surface.")
        return 1
    print("\nNone due.")
    return 0


def cmd_snapshot(root: Path) -> int:
    entries = walk_tree(root)
    write_manifest(root, entries)
    print(f"Manifest written: {manifest_path(root)}")
    print(f"Tracked files: {len(entries)}")
    return 0


def cmd_scan(root: Path, hard_gate: bool = True) -> int:
    if not manifest_path(root).exists():
        print("NO MANIFEST: no baseline exists yet. Run 'snapshot' first.")
        return 2

    old = load_manifest(root)
    new = walk_tree(root)

    added = {p: new[p] for p in new.keys() - old.keys()}
    removed = {p: old[p] for p in old.keys() - new.keys()}
    changed = {
        p: (old[p], new[p])
        for p in old.keys() & new.keys()
        if old[p][1] != new[p][1]
    }

    # Pair removed+added entries with identical hashes as moves/renames.
    moved = []
    removed_by_hash = {}
    for p, (size, digest) in removed.items():
        removed_by_hash.setdefault(digest, []).append(p)
    for p in sorted(added):
        size, digest = added[p]
        if removed_by_hash.get(digest):
            src = removed_by_hash[digest].pop(0)
            moved.append((src, p, size))
    for src, dst, _ in moved:
        del removed[src]
        del added[dst]

    drift = bool(added or removed or changed or moved)
    if not drift:
        print(f"CLEAN: tree matches manifest ({len(new)} tracked files).")
        return 0

    print("DRIFT DETECTED — files differ from the last filing-pass manifest.\n")

    if added:
        print(f"ADDED ({len(added)}) — present now, not in manifest; these did NOT go through the inbox process:")
        for p in sorted(added):
            size, _ = added[p]
            print(f"  + {p}  [{human(size)}]")
        print()

    if changed:
        print(f"CHANGED ({len(changed)}) — same path, different content:")
        for p in sorted(changed):
            (osize, _), (nsize, _) = changed[p]
            delta = nsize - osize
            if delta > 0:
                d = f"grew by {human(delta)}"
            elif delta < 0:
                d = f"shrank by {human(-delta)}"
            else:
                d = "same size, different content"
            print(f"  ~ {p}  [{human(osize)} -> {human(nsize)}; {d}]")
        print()

    if moved:
        print(f"MOVED/RENAMED ({len(moved)}) — identical content at a new path:")
        for src, dst, size in moved:
            print(f"  > {src}  ->  {dst}  [{human(size)}]")
        print()

    if removed:
        print(f"REMOVED ({len(removed)}) — in manifest, no longer present:")
        for p in sorted(removed):
            size, _ = removed[p]
            print(f"  - {p}  [{human(size)}]")
        print()

    if hard_gate:
        print("STOP — HARD GATE: report these findings to the user NOW, before any")
        print("other work (do not read inbox files, do not cross-reference, do not")
        print("file anything). Wait for the user to disposition every finding, then")
        print("run 'snapshot' to refresh the manifest before proceeding.")
    else:
        print("HEADS-UP (non-blocking): report this drift to the user now and")
        print("recommend running a filing pass to disposition and re-snapshot it.")
        print("You may continue with the user's actual request after reporting —")
        print("don't block an unrelated task on this.")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("mode",
                    choices=["snapshot", "scan", "session-scan", "bless-file", "threads"])
    ap.add_argument("target", nargs="?",
                    help="For bless-file: the project-relative path to mute")
    ap.add_argument("--root", type=Path, default=None,
                    help="Project root (default: inferred from script location)")
    args = ap.parse_args()
    root = (args.root or default_root()).resolve()
    if not root.is_dir():
        print(f"Not a directory: {root}", file=sys.stderr)
        return 2
    if args.mode == "snapshot":
        return cmd_snapshot(root)
    if args.mode == "session-scan":
        return cmd_session_scan(root)
    if args.mode == "threads":
        return cmd_threads(root)
    if args.mode == "bless-file":
        if not args.target:
            print("bless-file requires a path argument, e.g.:\n"
                  "  filing_integrity.py bless-file \"00_README.md\"",
                  file=sys.stderr)
            return 2
        return cmd_bless_file(root, args.target)
    return cmd_scan(root)


if __name__ == "__main__":
    sys.exit(main())
