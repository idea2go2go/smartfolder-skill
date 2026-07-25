#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Paul Hess (paul@hess.club)
# Part of the Create SMARTFOLDER kit. Released under the MIT License;
# full text in the LICENSE file at the kit root. Questions: paul@hess.club.
"""Generate a per-folder _README.md "SmartFolder" index across the Rowan, Tess,
and Shared archives — v5 aligned.

What this does (v5 model):
- A _README.md only in folders that carry real signal. Tiny/deep leaf folders are
  FOLDED INTO the parent's guide instead of getting a thin filler guide of their own
  (v5 "keep it proportional"). See qualifies().
- Each guide carries a dated `**As of YYMMDD.**` header (v5 freshness rule).
- Each guide: a `## For people` description, then a `## For Claude / AI sessions`
  map of THIS folder's own files plus a one-glance list of its immediate subfolders
  (linked when the subfolder has its own guide, inlined when it was folded in).
- Synthesis-aware: a folder that contains a `_Synthesis.md` always keeps a guide and
  gets a headline link to it; the generator never writes or overwrites a _Synthesis.md.

Operational guards:
- macOS bundles (.oo3/.ooutline/.rtfd/.goodnotes/.webarchive/.key/.numbers/.pages/.more)
  AND companion data dirs (e.g. Audacity `Foo.aup` + `Foo_data/`) are atomic single
  documents: listed as one item, never recursed into.
- Delete_Manually is a trash-staging area: one _README.md at its top, no recursion.
- Never modify or delete archive files. Guides for folders that no longer qualify are
  MOVED (not deleted) into <root>/Delete_Manually/pruned_guides_<stamp>/ with a
  move-log.csv, so the change is fully reversible.

Manual-edit protection (unchanged):
- Every _README.md we write ends with an invisible HTML-comment marker holding a hash
  of the body. On re-run: matching hash -> refresh; human-edited -> SKIP and preserve;
  markerless -> SKIP unless --stamp.

Usage:
    python3 gen_readmes.py             # apply: refresh guides + prune filler
    python3 gen_readmes.py --dry-run   # report what WOULD change; write/move nothing
    python3 gen_readmes.py --stamp     # also adopt/stamp markerless files (migration)
"""

import os
import re
import sys
import csv
import json
import glob
import shutil
import hashlib
import datetime
from collections import Counter

# --- locate the session mount automatically (paths change every session) ----
def _find_mnt():
    # Prefer an explicit env override, else discover the mount that holds the roots.
    env = os.environ.get("SMARTFOLDER_MNT")
    if env and os.path.isdir(env):
        return env
    for cand in sorted(glob.glob("/sessions/*/mnt")):
        if os.path.isdir(os.path.join(cand, "Rowan")):
            return cand
    # Fallback: assume we're being run from somewhere under the mount.
    return os.environ.get("SMARTFOLDER_MNT", "/sessions/_/mnt")

_MNT = _find_mnt()

# SAMPLE CONFIGURATION — replace with the target folder's own roots before first use.
# The names below are invented placeholders, not real folders.
ROOTS = [
    ("Rowan", f"{_MNT}/Rowan", "child"),
    ("Tess", f"{_MNT}/Tess", "child"),
    ("School and Camp Shared Info",
     f"{_MNT}/School and Camp Shared Info Rowan Tess", "shared"),
]

# v5 As-of stamp (YYMMDD). Defaults to today; override with SMARTFOLDER_ASOF=YYMMDD
# (useful to keep a whole regeneration consistently dated, e.g. across a midnight-UTC boundary).
TODAY = os.environ.get("SMARTFOLDER_ASOF") or datetime.date.today().strftime("%y%m%d")

# --- authored summaries injection ------------------------------------------
_SUMMARIES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "summaries.json")

def _load_summaries():
    try:
        with open(_SUMMARIES_PATH, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return {}

SUMMARIES = _load_summaries()

# Atomic single-document directories: bundle extensions + companion data dirs.
BUNDLE_EXT = (".oo3", ".ooutline", ".rtfd", ".goodnotes", ".webarchive",
              ".key", ".numbers", ".pages", ".more")
DATA_DIR_SUFFIXES = ("_data", "_files", "_fichiers")  # e.g. Audacity Foo.aup + Foo_data
README = "_README.md"
SYNTH = "_Synthesis.md"

# --- proportionality thresholds (v5: keep guides only where they carry signal) ---
KEEP_DEPTH = 2        # depth <= this always keeps a guide (root=0, area=1, chapter=2)
MIN_FILES_DEEP = 5    # at depth >= 3 a leaf needs at least this many own items to keep a guide

# --- manual-edit protection -------------------------------------------------
MARKER_VERSION = 2
MARKER_RE = re.compile(r"^<!-- smartfolder-auto:v\d+ sha256=([0-9a-f]{64})")


def make_marker(body):
    h = hashlib.sha256(body.encode("utf-8")).hexdigest()
    return (f"<!-- smartfolder-auto:v{MARKER_VERSION} sha256={h} — "
            f"auto-generated; edit freely, manual changes are preserved on regen -->\n")


def split_marker(text):
    lines = text.splitlines(keepends=True)
    idx = len(lines) - 1
    while idx >= 0 and lines[idx].strip() == "":
        idx -= 1
    if idx >= 0:
        m = MARKER_RE.match(lines[idx].strip())
        if m:
            return "".join(lines[:idx]), m.group(1)
    return text, None


def is_manually_edited(text):
    """True=human edited, False=pristine ours, None=no marker."""
    body, stored = split_marker(text)
    if stored is None:
        return None
    return hashlib.sha256(body.encode("utf-8")).hexdigest() != stored

MEDIA_EXT = {
    "jpg", "jpeg", "png", "gif", "tif", "tiff", "heic", "bmp", "jfx", "xcf", "webp",
    "mpg", "mpeg", "mp4", "mov", "avi", "m4v", "3gp", "wmv",
    "wav", "mp3", "m4a", "aif", "aiff", "aac",
}
DOC_EXT = {"pdf", "doc", "docx", "rtf", "txt", "pages", "odt", "md"}
SHEET_EXT = {"xls", "xlsx", "csv", "numbers", "tsv"}
SLIDE_EXT = {"ppt", "pptx", "key"}

LIST_ALL_CAP = 250
MEDIA_SUMMARY_THRESHOLD = 40
MEDIA_FRACTION = 0.6
LOWINFO_THRESHOLD = 60
LOWINFO_FRACTION = 0.7


def plural(n, word):
    return f"{n} {word}" + ("" if n == 1 else "s")


def is_bundle(name):
    return name.lower().endswith(BUNDLE_EXT)


def stem(name):
    if is_bundle(name):
        return name.rsplit(".", 1)[0]
    if "." in name and not name.startswith("."):
        return name.rsplit(".", 1)[0]
    return name


_LOWINFO_RE = re.compile(r"^[a-z]{0,8}[-_ ]?\d{1,7}$", re.IGNORECASE)


def is_lowinfo(name):
    return bool(_LOWINFO_RE.match(stem(name).strip()))

# ---------------------------------------------------------------- date parsing

TERMS = {"winter": 12, "spring": 2, "summer": 6, "fall": 9, "autumn": 9}


def parse_dates(name):
    out = set()
    low = name.lower()
    for m in re.finditer(r"(\d{2})\s*(winter|spring|summer|fall|autumn)", low):
        yy = int(m.group(1))
        if 5 <= yy <= 30:
            out.add((2000 + yy, TERMS[m.group(2)]))
    for run in re.findall(r"\d{4,8}", name):
        n = len(run)
        if n == 8:
            y, mo = int(run[0:4]), int(run[4:6])
            if 2000 <= y <= 2035 and 1 <= mo <= 12:
                out.add((y, mo))
        elif n == 6:
            yy, mo = int(run[0:2]), int(run[2:4])
            if 5 <= yy <= 30 and 1 <= mo <= 12:
                out.add((2000 + yy, mo))
        elif n == 4:
            yy, mo = int(run[0:2]), int(run[2:4])
            if 5 <= yy <= 30 and 1 <= mo <= 12:
                out.add((2000 + yy, mo))
    return out


def span_str(dates):
    if not dates:
        return ""
    lo, hi = min(dates), max(dates)
    f = lambda d: f"{d[0]}-{d[1]:02d}"
    return f(lo) if lo == hi else f"{f(lo)}–{f(hi)}"


def ext_of(name):
    if is_bundle(name):
        return name.lower().rsplit(".", 1)[-1]
    if "." in name and not name.startswith("."):
        return name.rsplit(".", 1)[-1].lower()
    return ""


def type_breakdown(files):
    c = Counter(ext_of(f) or "(no ext)" for f in files)
    return ", ".join(f"{n}×{ext}" for ext, n in c.most_common())


# ---------------------------------------------------------------- fs scan

def skip_name(name):
    if name in (README, SYNTH):
        return True
    if name in (".DS_Store", ".localized"):
        return True
    if name.rstrip("\r") == "Icon":
        return True
    if name.startswith("._") or name.startswith(".DS_Store"):
        return True
    return False


def classify_entries(path):
    """Return (files, subdirs). 'files' = real files + atomic bundle/data dirs."""
    try:
        entries = sorted(os.listdir(path), key=str.lower)
    except OSError:
        return [], []
    names = set(entries)
    files, subdirs = [], []
    for e in entries:
        if skip_name(e):
            continue
        full = os.path.join(path, e)
        if os.path.isdir(full):
            if is_bundle(e) or _is_data_dir(e, names):
                files.append(e)         # atomic: list as a single item
            else:
                subdirs.append(e)
        else:
            files.append(e)
    return files, subdirs


def _is_data_dir(name, sibling_names):
    """True for a companion data dir like Foo_data next to Foo.aup."""
    low = name.lower()
    for suf in DATA_DIR_SUFFIXES:
        if low.endswith(suf):
            base = name[: -len(suf)]
            if any(s != name and stem(s) == base for s in sibling_names):
                return True
    return False


# ---------------------------------------------------------------- tree model

def scan(label, kind, path, rel, depth, path_label):
    files, subdirs_names = classify_entries(path)
    has_synth = os.path.exists(os.path.join(path, SYNTH))
    has_summary = (f"{label}|{rel}" in SUMMARIES) if rel else False

    children = []
    if rel != "Delete_Manually":          # never recurse into the trash staging tree
        for d in subdirs_names:
            child_rel = d if rel == "" else f"{rel}/{d}"
            children.append(
                scan(label, kind, os.path.join(path, d), child_rel, depth + 1, path_label))

    node = {
        "label": label, "kind": kind, "path": path, "rel": rel, "name":
            (label if rel == "" else rel.split("/")[-1]),
        "depth": depth, "files": files, "subdir_names": subdirs_names,
        "children": children, "has_synth": has_synth, "has_summary": has_summary,
        "path_label": path_label,
    }
    node["qualifies"] = _qualifies(node)
    return node


def _qualifies(node):
    if node["rel"] == "":
        return True                                   # root
    if node["depth"] <= KEEP_DEPTH:
        return True                                   # areas + chapters
    if node["has_summary"] or node["has_synth"]:
        return True                                   # authored / has synthesis
    if len(node["files"]) >= MIN_FILES_DEEP:
        return True                                   # substantial leaf
    if any(c["qualifies"] for c in node["children"]):
        return True                                   # ancestor of something kept
    return False


_LINK_RE = re.compile(r"\]\(<([^>]+)/_README\.md>\)")


def honor_human_links(node):
    """If THIS folder's guide was hand-edited/markerless and links to a child guide,
    force-keep that child (and, transitively, its qualifying chain) so the human's
    reference doesn't break. Respects explicit human intent over the size threshold."""
    target = os.path.join(node["path"], README)
    if os.path.exists(target) and node["children"]:
        try:
            txt = open(target, encoding="utf-8").read()
        except OSError:
            txt = ""
        if is_manually_edited(txt) in (True, None):   # human-touched or foreign
            linked = {m.group(1).strip("./") for m in _LINK_RE.finditer(txt)}
            for c in node["children"]:
                if c["name"] in linked and not c["qualifies"]:
                    c["qualifies"] = True
    for c in node["children"]:
        honor_human_links(c)


# ---------------------------------------------------------------- rendering

ROOT_CHILD = (
    "This is the top of {child}'s personal life archive — a curated, mostly "
    "chronological record of {child}'s keepsakes, accomplishments, and the full arc "
    "of {child}'s education, with older operational clutter kept but tucked a level "
    "down. Dates drive the organization: most files and folders lead with a `YYMM` "
    "code so they sort in time order. The main areas are **Report Cards** (the "
    "consolidated academic record), **Keepsakes** (sentimental items), **Education** "
    "(the school-and-learning timeline), plus **Jobs & Career**, **Housing**, "
    "**Health & Medical**, **Finances**, **Trips & Misc**, and the buried "
    "**Early Childhood Archive**. See `CLAUDE.md` in this folder for the full "
    "organizing philosophy, naming conventions, and gotchas."
)

ROOT_SHARED = (
    "This folder holds material that belongs to a **school or program itself** rather "
    "than to one child — the shared companion to the individual Rowan and Tess "
    "archives. It covers only institutions **both** children attended (Lakeshore "
    "Montessori, Ridgeview Academy, the Fairview Hebrew School) plus the by-year "
    "**Summer Camps** "
    "archive. Anything specific to one child lives in that child's own folder instead. "
    "See `CLAUDE.md` in this folder for the filing rule of thumb."
)

AREA = {
    "Report Cards": (
        "{child}'s single, consolidated **academic record**, kept as one flat, "
        "chronological folder so the whole academic story reads in date order. It "
        "collects not just report cards and transcripts but every date-tagged academic "
        "accomplishment: standardized and individual tests, academic awards and "
        "certificates, and school progress notes with genuine child-specific commentary. "
        "Files follow `YYMM Venue Descriptor.ext`."
    ),
    "Keepsakes": (
        "{child}'s **sentimental pile**: cards, notes and letters, creative writing, "
        "programs, voice and video, photos and artwork, identity/legal documents, and "
        "the non-academic awards (sailing, music, sports, Jewish life and B'nai Mitzvah, "
        "and so on). Parent-written year reports live here too. Organized by theme rather "
        "than strictly by date."
    ),
    "Education": (
        "The **school-and-learning timeline** for {child}. Each chapter is its own folder "
        "named with its start date (`YYMM Name`, with a range like `YYMM Name YYMM-YYMM` "
        "for multi-year spans), so the whole journey — preschool, each school, summer "
        "programs, camps, the high-school search, the college search, science fairs — reads "
        "top to bottom in the order it happened."
    ),
    "Early Childhood Archive": (
        "The buried **early-years layer** for {child}: nanny and sitter records, "
        "playgroups, baby-proofing and products, birth plan and announcement, early "
        "activities and development notes. Kept for the record but tucked a level down so "
        "it doesn't crowd the things reached for now."
    ),
    "Jobs & Career": (
        "{child}'s **work history and career development** — one subfolder per role or "
        "search, dated. Includes applications, acceptances, onboarding paperwork, work "
        "product, pay records, and résumés."
    ),
    "Housing": (
        "{child}'s **residences and housing paperwork** — one dated subfolder per place "
        "(dorms, sublets, apartments), holding leases, roommate agreements, and related "
        "financial statements."
    ),
    "Health & Medical": (
        "{child}'s **health and medical records** — a small area covering early/baby "
        "medical history, X-rays, studies, and the like."
    ),
    "Finances": (
        "{child}'s **personal finance records** — a small area (e.g., 529 college-savings "
        "plans, statements, and related paperwork)."
    ),
    "Trips & Misc": (
        "**Travel and one-off items** for {child} that don't belong to another area — one "
        "subfolder per trip or topic."
    ),
    "_To Sort": (
        "A **staging area** for {child}'s items not yet filed into the archive. Contents "
        "here are provisional and awaiting a permanent home."
    ),
    "Delete_Manually": (
        "A **staging area for deletion** — things the automated tools flagged but couldn't "
        "remove (duplicates, dropped files, empty leftovers, pruned filler guides). Safe to "
        "empty from Finder when ready. Nothing here is part of the live archive, so this "
        "guide intentionally does not index its subfolders in detail."
    ),
    "Schools (Reference)": (
        "School-wide **reference material** for institutions both children attended — "
        "Lakeshore Montessori, Ridgeview Academy, and the Fairview Hebrew School. Handbooks, "
        "newsletters, directories, calendars, and general info live here; anything about "
        "one child's own experience lives in that child's folder."
    ),
    "Summer Camps": (
        "The by-year archive (≈2011–2024) of **summer-camp logistics**, brochures, "
        "registrations, and research shared across both children. Camps that were clearly "
        "one child's notable experience were promoted into that child's Education timeline; "
        "this is the shared/administrative remainder."
    ),
}


_ASOF_RE = re.compile(r"\*\*As of\s+([0-9]{4,8})\.?\*\*")


def _synth_asof(path):
    try:
        head = open(path, encoding="utf-8").read(2000)
    except OSError:
        return ""
    m = _ASOF_RE.search(head)
    return m.group(1) if m else ""


def all_dates(node):
    dates = set()
    for f in node["files"]:
        dates |= parse_dates(f)
    if node["rel"]:
        dates |= parse_dates(node["name"])
    return dates


def human_section(node):
    label, kind, rel, name = node["label"], node["kind"], node["rel"], node["name"]
    if rel == "":
        blurb = (ROOT_SHARED if kind == "shared" else ROOT_CHILD).format(child=label)
    else:
        parts = rel.split("/")
        if len(parts) == 1 and name in AREA:
            blurb = AREA[name].format(child=label)
        elif f"{label}|{rel}" in SUMMARIES:
            blurb = SUMMARIES[f"{label}|{rel}"]
        else:
            crumb = " › ".join(parts[:-1]) if len(parts) > 1 else ""
            loc = f"under **{crumb}**" if crumb else "a top-level area"
            nf = plural(len(node["files"]), "item")
            ns = (f" across {plural(len(node['subdir_names']), 'subfolder')}"
                  if node["subdir_names"] else "")
            blurb = f"*{name}* sits {loc} in {label}'s archive. It holds {nf}{ns}."

    if node["has_synth"]:
        sdate = _synth_asof(os.path.join(node["path"], SYNTH))
        datetag = f" (as of {sdate})" if sdate else ""
        blurb += (f"\n\n**Whole-folder synthesis{datetag}:** see "
                  "[`_Synthesis.md`](<_Synthesis.md>) for the holistic story across these "
                  "files (derived AI analysis — the raw files win on any conflict).")

    extra = []
    if node["subdir_names"]:
        shown = ", ".join(f"`{s}`" for s in node["subdir_names"][:8])
        more = "" if len(node["subdir_names"]) <= 8 else f", +{len(node['subdir_names'])-8} more"
        extra.append(f"Subfolders: {shown}{more}.")
    sp = span_str(all_dates(node))
    if sp:
        extra.append(f"Date span at this level: {sp}.")
    return blurb + ("\n\n" + " ".join(extra) if extra else "")


def files_block(files):
    if not files:
        return "_No files directly at this level._"
    n = len(files)
    media_frac = sum(1 for f in files if ext_of(f) in MEDIA_EXT) / n
    lowvalue_frac = sum(1 for f in files if ext_of(f) in MEDIA_EXT or is_lowinfo(f)) / n
    big_media = n > MEDIA_SUMMARY_THRESHOLD and media_frac >= MEDIA_FRACTION
    big_lowinfo = n > LOWINFO_THRESHOLD and lowvalue_frac >= LOWINFO_FRACTION

    if big_media or big_lowinfo:
        dates = set()
        for f in files:
            dates |= parse_dates(f)
        sp = span_str(dates)
        kind = "media folder" if big_media else "auto-named bulk folder"
        head = f"### Files here ({len(files)} — {kind}, summarized)\n\n"
        lead = ("Predominantly media files" if big_media
                else "A large set of sequentially/auto-named files")
        body = (f"{lead} ({type_breakdown(files)})."
                + (f" Date span ≈ {sp}." if sp else "") + " Sample names:\n\n")
        sample = files[:10]
        body += "\n".join(f"- `{s}`" for s in sample)
        body += f"\n\n_…and {len(files) - len(sample)} more files in this folder._"
        return head + body

    head = f"### Files here ({len(files)})\n\n"
    shown = files[:LIST_ALL_CAP]
    lines = []
    for f in shown:
        tag = "  — _macOS bundle (single document)_" if is_bundle(f) else ""
        lines.append(f"- `{f}`{tag}")
    body = "\n".join(lines)
    if len(files) > LIST_ALL_CAP:
        body += f"\n- _…and {len(files) - LIST_ALL_CAP} more files._"
    return head + body


def _child_meta(child):
    dates = all_dates(child)
    meta = plural(len(child["files"]), "file")
    if child["subdir_names"]:
        meta += f", {plural(len(child['subdir_names']), 'subfolder')}"
    sp = span_str(dates)
    if sp:
        meta += f"; {sp}"
    return meta


def subdirs_block(node, linkable=True):
    children = node["children"]
    names = node["subdir_names"]
    if not names:
        return "_No subfolders; this is a leaf folder._"

    if not linkable:   # Delete_Manually: shallow, non-indexed
        note = "_Staging area — subfolders are not individually indexed._\n"
        lines = [f"### Subfolders ({len(names)}) — glance only\n", note]
        for d in names:
            sf, ss = classify_entries(os.path.join(node["path"], d))
            meta = plural(len(sf), "file")
            if ss:
                meta += f", {plural(len(ss), 'subfolder')}"
            lines.append(f"- `{d}/` — {meta}")
        return "\n".join(lines)

    note = ("_Linked subfolders have their own `_README.md`; folded-in ones are described "
            "here (they were too small to warrant a separate guide)._\n")
    lines = [f"### Subfolders ({len(children)}) — glance only\n", note]
    for child in children:
        meta = _child_meta(child)
        d = child["name"]
        if child["qualifies"]:
            lines.append(f"- [`{d}/`](<{d}/_README.md>) — {meta}")
        else:
            # folded in: keep its signal inline (sample item or subfolder names)
            sample = child["files"][:3] or child["subdir_names"][:3]
            tail = ""
            if sample:
                tail = " — e.g. " + ", ".join(f"`{s}`" for s in sample)
                if len(child["files"] or child["subdir_names"]) > 3:
                    tail += ", …"
            lines.append(f"- `{d}/` (folded in) — {meta}{tail}")
    return "\n".join(lines)


def notes_block(node):
    files = node["files"]
    notes = []
    if files:
        notes.append(f"File types here: {type_breakdown(files)}.")
    if any(is_bundle(f) for f in files):
        notes.append("Contains macOS bundle documents (`.oo3`/`.rtfd`/etc.) — each is a "
                     "single item; do not descend into them.")
    if not notes:
        return ""
    return "### Notes\n\n" + "\n".join(f"- {n}" for n in notes)


def render(node):
    rel, name, label = node["rel"], node["name"], node["label"]
    title = label if rel == "" else name
    dates = all_dates(node)
    disp_path = node["path_label"] if rel == "" else f"{node['path_label']}/{rel}"
    sp = span_str(dates)

    # qualifying children count (for an honest subfolder tally)
    qn = sum(1 for c in node["children"] if c["qualifies"])
    sub_tally = plural(len(node["subdir_names"]), "subfolder")
    if node["children"] and qn != len(node["children"]):
        sub_tally += f" ({qn} with own guide)"

    meta = (f"**Path:** `{disp_path}`  ·  **This level:** "
            f"{plural(len(node['files']), 'file')}, {sub_tally}")
    if sp:
        meta += f"  ·  **Dates:** {sp}"

    if rel == "":
        nav = "*Top of the SmartFolder index. See `CLAUDE.md` here for the overall scheme.*"
    else:
        nav = ("*Part of the SmartFolder index. Parent: [`../_README.md`](<../_README.md>). "
               "See `CLAUDE.md` at the archive root for the overall scheme.*")

    parts = [
        f"# {title} — folder guide",
        ("*`_README.md` — a quick human summary first, then a detailed map for "
         "Claude/AI sessions. It describes this folder's own contents in detail and "
         "names its subfolders at a glance; each subfolder has its own `_README.md` "
         "(tiny ones are folded into this guide).*"),
        f"**As of {TODAY}.**",
        "## For people",
        human_section(node),
        "## For Claude / AI sessions",
        meta,
        files_block(node["files"]),
        subdirs_block(node, linkable=(rel != "Delete_Manually")),
    ]
    nb = notes_block(node)
    if nb:
        parts.append(nb)
    parts.append("---\n" + nav)
    return "\n\n".join(parts) + "\n"


# ---------------------------------------------------------------- walk + apply

STAMP = False
DRY = False
stats = {"created": [], "refreshed": [], "skipped_edited": [], "skipped_unmarked": [],
         "pruned": [], "prune_flagged": []}
prune_log = []   # (original_path, staged_path)


def write_readme(target, body):
    if DRY:
        return
    with open(target, "w", encoding="utf-8") as fh:
        fh.write(body + make_marker(body))


def _staging_dir(root_path):
    return os.path.join(root_path, "Delete_Manually", f"pruned_guides_{TODAY}")


def prune_guide(node, root_path):
    """A non-qualifying folder: move our pristine guide out; preserve human edits."""
    target = os.path.join(node["path"], README)
    if not os.path.exists(target):
        return
    try:
        existing = open(target, encoding="utf-8").read()
    except OSError:
        return
    edited = is_manually_edited(existing)
    if edited is True or edited is None:
        stats["prune_flagged"].append(target)         # human-touched / foreign: leave it
        return
    # pristine ours -> stage it (reversible), don't delete
    rel_flat = node["rel"].replace("/", "∕")
    staged = os.path.join(_staging_dir(root_path), f"{rel_flat}__README.md")
    stats["pruned"].append(target)
    prune_log.append((target, staged))
    if not DRY:
        os.makedirs(os.path.dirname(staged), exist_ok=True)
        shutil.move(target, staged)


def apply_node(node, root_path):
    if node["qualifies"]:
        body = render(node)
        target = os.path.join(node["path"], README)
        if not os.path.exists(target):
            write_readme(target, body)
            stats["created"].append(target)
        else:
            existing = ""
            try:
                existing = open(target, encoding="utf-8").read()
            except OSError:
                pass
            edited = is_manually_edited(existing)
            if edited is True:
                stats["skipped_edited"].append(target)
            elif edited is None:
                if STAMP:
                    write_readme(target, body)
                    stats["refreshed"].append(target)
                else:
                    stats["skipped_unmarked"].append(target)
            else:
                write_readme(target, body)
                stats["refreshed"].append(target)
    else:
        prune_guide(node, root_path)

    if node["rel"] == "Delete_Manually":
        return
    for c in node["children"]:
        apply_node(c, root_path)


def main():
    global STAMP, DRY
    STAMP = "--stamp" in sys.argv
    DRY = "--dry-run" in sys.argv

    trees = []
    for label, root, kind in ROOTS:
        if not os.path.isdir(root):
            print(f"!! root not found: {root}")
            continue
        trees.append((root, scan(label, kind, root, "", 0, os.path.basename(root))))

    for _root_path, tree in trees:
        honor_human_links(tree)

    for root_path, tree in trees:
        apply_node(tree, root_path)

    # write the prune move-log(s)
    if prune_log and not DRY:
        for root_path, _ in trees:
            rows = [(o, s) for (o, s) in prune_log if s.startswith(_staging_dir(root_path))]
            if not rows:
                continue
            os.makedirs(_staging_dir(root_path), exist_ok=True)
            logp = os.path.join(_staging_dir(root_path), "move-log.csv")
            with open(logp, "w", newline="", encoding="utf-8") as fh:
                w = csv.writer(fh)
                w.writerow(["original_path", "staged_path"])
                w.writerows(rows)

    c, r = len(stats["created"]), len(stats["refreshed"])
    se, su = stats["skipped_edited"], stats["skipped_unmarked"]
    pr, pf = stats["pruned"], stats["prune_flagged"]
    mode = "DRY-RUN (nothing written/moved)" if DRY else "APPLIED"
    print(f"[{mode}]  as-of {TODAY}")
    print(f"created: {c}   refreshed: {r}   "
          f"skipped(edited): {len(se)}   skipped(no marker): {len(su)}")
    print(f"pruned(filler guides moved to Delete_Manually): {len(pr)}   "
          f"prune-flagged(human-edited, left in place): {len(pf)}")
    for t in pf:
        print("  LEFT (human-edited, not pruned):", t)
    print(f"guides remaining on disk (qualifying): {c + r + len(se) + len(su)}")


if __name__ == "__main__":
    main()
