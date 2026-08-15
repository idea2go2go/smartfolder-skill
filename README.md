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
to each new session. And not only your AI — the folder explains itself to other assistants too, in a
format they already read. Each participant, human or AI, starts with everything that is already
known and leaves something useful for whoever comes next. Over time, the folder becomes the
knowledge base instead of the conversation.

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

## What's new in v6.5.0

**Threaded knowledge — email and chat chains — now gets one home.** With the new **thread
masters** convention, saved email files or connector sweeps of emails, chats, or apps appear in
one file with a well-organized sidecar summary and status, rather than lots of fragmented files
with redundant chain information. Every absorbed fragment is ledgered, so nothing is lost.

Plus: you no longer need to know this skill exists to benefit from it — ask Claude to *"organize
this folder"* without saying how, and it looks at what's there first, then offers a choice (build
the full self-describing folder, or just the tidying; if you already said how, it simply does
that, no offer); the always-loaded instructions got about 20% leaner, deliberately paired with
that wider trigger so casual requests stay cheap; and the kit gains a complete worked example of
the folder's version-baseline file, now home to the monthly update check.

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
