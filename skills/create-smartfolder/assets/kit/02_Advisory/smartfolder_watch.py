#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Paul Hess (paul@hess.club)
# Part of the SmartFolder Skill kit. Released under the MIT License;
# full text in the LICENSE file at the kit root. Questions: paul@hess.club.
"""
smartfolder_watch.py - casual, non-blocking change-tracker for THIS SmartFolder (single-property).

Self-contained: it lives in <PropertyRoot>/XX_META/ and watches the property folder it sits inside.
Catches files ADDED or CHANGED directly in the folder (i.e. NOT dropped in XX_ASSETS-TO-FILE), so
they can be offered up for proper filing and the markdown summaries don't fall behind the repository.

Two verbs (no property argument - it watches its own parent folder):
  snapshot           write/refresh the baseline inventory
  check [--daily]    diff the live tree vs the baseline; report ADDED/CHANGED/REMOVED
                     --daily : run at most once per calendar day (silent if already run today)

Design: hybrid detection (trust size+mtime; re-hash only when mtime moved but size didn't - the
Dropbox sync-touch case); stateless (re-snapshot to re-baseline; the baseline is only re-written when
content is filed or dismissed). Tracks the owner's RAW files INCLUDING `MASTER *.docx`; ignores the
inbox, trash/staging, XX_META itself, hidden/OS-cruft, office lock/temp files, and AI-derived
guides (_README.md / _Synthesis.md / *_Summary.md / hub). macOS bundles tracked atomically.
See this folder's CLAUDE.md "Change tracking". Manifest: XX_META/_manifests/manifest.tsv
"""

import sys, os, hashlib, datetime
from pathlib import Path

SCRIPT_DIR   = Path(__file__).resolve().parent          # <PropertyRoot>/XX_META
ROOT         = SCRIPT_DIR.parent                         # <PropertyRoot>
MANIFEST_DIR = SCRIPT_DIR / "_manifests"
MANIFEST     = MANIFEST_DIR / "manifest.tsv"
STAMP        = MANIFEST_DIR / "last_check"

PRUNE_DIRS = {
    "XX_META", "XX_ASSETS-TO-FILE", "XX_DELETE-MANUALLY",
    "_backups", "_manifests", "_data", ".git",
}
BUNDLE_EXTS = {".pages", ".numbers", ".key", ".rtfd", ".webarchive",
               ".oo3", ".ooutline", ".goodnotes", ".more"}


def is_excluded_file(name):
    n = name.rstrip("\r\n")
    if n in (".DS_Store", "Icon", "CLAUDE.md", "AGENTS.md"): return True  # OS cruft + resident guides
    if name.startswith("."):                  return True
    if name.startswith("~$") or name.endswith(".tmp"): return True
    if name.endswith("_Summary.md"):          return True
    if name.startswith("_") and name.endswith(".md"): return True
    return False


def sha1_file(path, chunk=1 << 20):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def bundle_signature(path):
    total, newest = 0, 0
    for root, _dirs, files in os.walk(path):
        for fn in files:
            try:
                st = os.stat(os.path.join(root, fn))
            except OSError:
                continue
            total += st.st_size
            newest = max(newest, int(st.st_mtime))
    return total, newest


def walk_tree():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in PRUNE_DIRS]
        keep = []
        for d in dirnames:
            if os.path.splitext(d)[1].lower() in BUNDLE_EXTS:
                full = Path(dirpath) / d
                size, mtime = bundle_signature(full)
                yield (str(full.relative_to(ROOT)), size, mtime, True)
            else:
                keep.append(d)
        dirnames[:] = keep
        for fn in filenames:
            if is_excluded_file(fn):
                continue
            full = Path(dirpath) / fn
            try:
                st = full.stat()
            except OSError:
                continue
            yield (str(full.relative_to(ROOT)), st.st_size, int(st.st_mtime), False)


def do_snapshot():
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for rel, size, mtime, is_bundle in walk_tree():
        rows.append((rel, size, mtime, "" if is_bundle else sha1_file(ROOT / rel)))
    rows.sort()
    with open(MANIFEST, "w", encoding="utf-8") as f:
        f.write("# relative_path\tsize\tmtime\tsha1   (empty sha1 = macOS bundle, metadata-only)\n")
        for rel, size, mtime, h in rows:
            f.write(f"{rel}\t{size}\t{mtime}\t{h}\n")
    print(f"snapshot {ROOT.name}: {len(rows)} files baselined -> XX_META/_manifests/manifest.tsv")
    return 0


def load_manifest():
    if not MANIFEST.exists():
        return None
    m = {}
    with open(MANIFEST, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            p = line.rstrip("\n").split("\t")
            if len(p) >= 4:
                m[p[0]] = (int(p[1]), int(p[2]), p[3])
    return m


def do_check(daily=False):
    today = datetime.date.today().isoformat()
    if daily and STAMP.exists() and STAMP.read_text().strip() == today:
        return 0
    base = load_manifest()
    if base is None:
        print("no baseline yet - run:  snapshot")
        return 2
    current = {rel: (size, mtime, b) for rel, size, mtime, b in walk_tree()}
    added, changed, removed = [], [], []
    for rel, (size, mtime, is_bundle) in current.items():
        if rel not in base:
            added.append((rel, size)); continue
        bsize, bmtime, bhash = base[rel]
        if size != bsize:
            changed.append((rel, size - bsize))
        elif mtime != bmtime:
            if is_bundle or sha1_file(ROOT / rel) != bhash:
                changed.append((rel, 0))
    for rel in base:
        if rel not in current:
            removed.append(rel)
    if daily:
        MANIFEST_DIR.mkdir(parents=True, exist_ok=True); STAMP.write_text(today)
    n = len(added) + len(changed) + len(removed)
    if n == 0:
        print(f"check {ROOT.name}: CLEAN - everything matches the baseline.")
        return 0
    print(f"check {ROOT.name}: {n} finding(s). These did NOT come through XX_ASSETS-TO-FILE, so the "
          f"summaries don't yet reflect them:")
    if added:
        print(f"\n  ADDED ({len(added)}):")
        for rel, size in sorted(added): print(f"    + {rel}  ({size:,} bytes)")
    if changed:
        print(f"\n  CHANGED ({len(changed)}):")
        for rel, d in sorted(changed):
            print(f"    ~ {rel}" + (f"  ({'+' if d >= 0 else ''}{d:,} bytes)" if d else ""))
    if removed:
        print(f"\n  REMOVED ({len(removed)}):")
        for rel in sorted(removed): print(f"    - {rel}")
    return 1


def main():
    a = sys.argv[1:]
    if not a or a[0] not in ("snapshot", "check"):
        print("usage: smartfolder_watch.py {snapshot|check} [--daily]"); return 2
    return do_snapshot() if a[0] == "snapshot" else do_check(daily="--daily" in a)


if __name__ == "__main__":
    sys.exit(main())
