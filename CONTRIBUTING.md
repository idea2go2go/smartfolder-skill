# Contributing

Thanks for being here. This page is mostly about **what a helpful contribution looks like**, because
this project accepts a narrower range of things than most, and I'd rather say so up front than
explain it to you after you've done the work.

## The most helpful thing you can send

**An account of what happened when you used it.** What kind of folder, what the skill proposed, what
you kept, what you overrode, and what it got wrong. That is more useful to this project than almost
any code change, because the method is built from real folders and it improves by meeting more of
them. An issue or a discussion post is fine; no format required.

If something confused you, that's a finding too. A guide that reads clearly to me and not to you is
a defect in the guide.

## Bug reports

Anything where the skill did something it shouldn't: moved a file it wasn't asked to, produced a
summary that was confidently wrong, ignored one of its own safety rules, or broke on a folder shape
it should have handled. Please include what kind of folder it was and roughly what you asked for.
The safety rules — never delete, never edit your files, never move without approval — are the ones I
most want to hear about.

## Changes to the kit

This is where the bar is unusual, so here it is plainly.

The kit is **case law, not templates**. Every artifact in it was pulled out of a folder that actually
used it, and it carries a note saying which conditions call for it. That's what keeps the kit from
turning into a pile of generic scaffolding that every folder gets whether it needs it or not — which
is the failure mode this whole design exists to avoid.

**A kit contribution that fits looks like this:**

- It came out of a real folder that genuinely used it — not something written for the occasion.
- Names, places, and specifics are replaced with invented ones, so it's safe to publish.
- It arrives with its "warranted when" line: which diagnostic conditions make this artifact worth
  having, and — just as usefully — when it would be overkill.

**A kit contribution that doesn't fit** is a well-made general-purpose template. Not because it's bad
work, but because adding it would mean recommending it to folders that don't need it, and machinery
above a folder's needs doesn't just waste effort — it trains people to ignore the system.

If you're not sure which yours is, open an issue and describe it before writing anything. I'd rather
talk first than turn down finished work.

## Changes to `SKILL.md`

Corrections, contradictions, and places where the instructions are ambiguous enough to produce two
different builds — all very welcome, and usually easy to merge.

New rules are a harder sell. The skill is deliberately quiet about flexible decisions, because being
overly prescriptive about a design choice becomes *proscriptive* in practice: it forbids better
answers. If you want to add a rule, the case to make is that its absence caused a bad build, not
that it would make the document more complete.

## Practicalities

- Open an issue before a large change. Small fixes can go straight to a pull request.
- One idea per pull request, please — it makes the conversation easier.
- No style requirements, no tests to run, no checklist.
- Everything here is prose and Python; if you can edit a text file you can contribute.

## What to expect from me

This is a personal project and I'm the only maintainer. I read everything and answer as time allows,
which sometimes means a week. If I turn something down I'll say why, and it will usually be one of
the reasons above rather than anything about you.

By contributing you agree your contribution can be published under the project's license: CC BY 4.0
for prose and exemplars, MIT for scripts.

Questions before you start? Open an issue, or email paul@hess.club.
