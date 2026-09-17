# SmartFolder Skill

**A Claude skill that turns a folder of files into a folder that explains itself.**

[![Download the skill](https://img.shields.io/badge/Download%20the%20skill-latest%20release-2ea44f?style=for-the-badge)](https://github.com/idea2go2go/smartfolder-skill/releases/latest/download/SmartFolder-Skill.skill)

---

Individual files contain data, but knowledge comes from synthesizing that data across files to tell
a story: trends, status, correlations, relationships, discrepancies. Finding or using knowledge
usually means digging through tons of raw files and putting it all together in your head. A
SmartFolder lets the data speak to you and tell its own story. In one property archive, the
synthesis noticed that a heating zone had failed in two separate summers, traced both failures to
the same overlooked reservoir, and wrote down the seasonal pattern behind them — a story no single
invoice told, waiting in twenty-three files for someone to read them all at once.

This skill teaches Claude how to turn any ordinary folder into a **SmartFolder**: a folder that
explains itself. Claude studies the files, helps reorganize and rename them where that would be
useful, and adds a layer of guides and summaries around them. The result is a folder that you, your
AI, and your human collaborators can all open and quickly understand without reading every file.

You, your AI, and your human collaborators can all work within and update the same folder, while the
SmartFolder infrastructure continues to synthesize and update its knowledge layers. That knowledge
lives in the folder itself, not in an ephemeral chat session where you have to re-explain everything
to each new session. You need Claude to build a SmartFolder, but once built it works with Claude,
ChatGPT, or any LLM that can follow a CLAUDE.md or AGENTS.md file, or that can fake it! Each
participant, human or AI, starts with everything that is already known and leaves something useful
for whoever comes next. Over time, the folder becomes the knowledge base instead of the
conversation.

SmartFolders can be used for old archives, property and medical records, family paperwork, and other
folders that have grown hard to navigate. But I also built it for active project work. You can
browse the folder directly, work through an AI that understands it, or share it with other people
and their AIs — for instance through Dropbox — without losing the common understanding that holds
the work together. Your starting point can be a messy historical folder or an organized active
project folder, large or small.

Your original files are never edited or deleted. The skill works in careful stages, shows you its
plan, and asks for approval before it moves or renames anything.

## Install

**Claude desktop app / Cowork**

[Download the skill](https://github.com/idea2go2go/smartfolder-skill/releases/latest/download/SmartFolder-Skill.skill),
then open Claude → **Settings → Skills** and upload the file. `Readme.txt` in the
[release](https://github.com/idea2go2go/smartfolder-skill/releases) covers this route in plain
language.

**Claude Code**

```
/plugin marketplace add idea2go2go/smartfolder-skill
/plugin install create-smartfolder@smartfolder
```

Then `/reload-plugins`. Adding the marketplace registers the catalog; the second command installs.
To receive later versions automatically, open `/plugin`, choose **Marketplaces**, select
**smartfolder**, and enable auto-update.

## Use

Give Claude access to a folder and say, *"Turn this folder into a SmartFolder."* Then tell it, in
your own words, what the folder is, who uses it, and what you want from it. Claude will explore the
folder, ask you a few questions, show you a plan, and do one section as a sample before going
further.

A first conversion of a large folder can take a while and may span more than one session. That's
normal. Afterwards, the folder maintains itself: ask Claude to *"file the new items"* or *"refresh
the summaries"* whenever things change.

**Get a Markdown reader.** The guides and summaries are `.md` files. Conventional editors open
them as cluttered plain text — the formatting that makes them fast to scan only appears in a
Markdown reader, and it changes how usable the folder feels. Recommendations under *More*.

## What's new in v6.6.0

**Sharing a SmartFolder through Dropbox, Google Drive, or a similar service now comes with the one
setting that makes it work.** Everyone sharing the folder makes it fully available offline on their
own machine — otherwise the files on that machine are placeholders, and an assistant reading them
stalls or comes up empty. The skill now says so wherever it matters: in the design questions, at
first exploration, in the owner guide, and later on for folders that only begin being shared after
they are built.

Plus: simpler version record-keeping — a folder always records which release built it, keeps the
skill package only when one is already at hand, and the update offer hands you the download link
when a fetch comes back empty instead of trying to rebuild it; an opt-in, anonymized feedback
channel — offered at the end of a build and a few times a year after, counts and patterns only,
composed only if you say yes, sent only by you; and every folder now keeps its own copy of the
kit's example library, so it can go on growing years from now with no package, no installed skill,
and no network.

[Full notes on the release page.](https://github.com/idea2go2go/smartfolder-skill/releases/latest)
Every version's story is in [CHANGELOG.md](CHANGELOG.md).

## More

- **A Markdown reader** — the guides and summaries are `.md`; a lightweight reader makes them far
  nicer to read than a plain editor does. On a Mac, [Marked](https://markedapp.com); on Windows,
  [MDHero](https://mdhero.app); any equivalent works.
- **[SKILL.md](skills/create-smartfolder/SKILL.md)** — the whole method, readable without
  installing anything: the diagnostic, the tier model, three worked precedents, the build phases.
- **[The kit](skills/create-smartfolder/assets/kit/)** — a kit of working artifacts to adapt,
  including three Python scripts that do real work.
- **[CONTRIBUTING.md](CONTRIBUTING.md)** — what a helpful contribution looks like.

If you build something with it, I'd like to hear how it went. Open an
[issue](https://github.com/idea2go2go/smartfolder-skill/issues), start a
[discussion](https://github.com/idea2go2go/smartfolder-skill/discussions), or email me at
paul@hess.club. This is a personal project and I answer as time allows, so a quiet week isn't a
closed door.

**License:** prose and exemplars [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); bundled
scripts carry their own MIT notice.

*Created by Paul Hess.*
