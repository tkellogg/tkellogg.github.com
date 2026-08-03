---
layout: bare
title: Working with Tim
kicker: Agent skill
permalink: /skills/working-with-tim/
source_path: ~/.codex/skills/working-with-tim/SKILL.md
snapshot_date: 2026-08-02
description: "A predictive lens for whether Tim will approve of work — his values, the gap he actually cares about, the patterns that earn trust versus disapproval, and how to read and answer him. Consult before presenting substantial work, when making a judgment call (push back, ask, or just act?), or when deciding how to write something for him. Built from corrections Tim has actually made, not from guesses."
---

This is a lens for predicting one thing: **will Tim approve of this?** Use it as a
pre-flight check before presenting substantial work, and as a tie-breaker when
deciding how to act or what to say. The *facts* about who Tim is live in the
memory files (user-tim, project-elanus, elanus-conventions). This skill is the
*procedure* for turning those facts into a prediction.

Every pattern below comes from a correction Tim actually made, not from a generic
idea of good work — including mistakes I made and he caught. Keep it honest; a
flattering or vague version of this would itself fail his standard.

## The one test that matters most

Tim judges work by the gap between **"it technically functions"** and **"it
behaves the way a sensible person would expect."** He cares about the second. He
has said it outright: *"the UI needs to work the way I think it should work."*
When you finish something, simulate his reaction **as a person living with it**,
not as the author checking it against a spec. If a reasonable person would be
confused, surprised, or stuck, it is not done — even if every test is green.

Tells that you have failed this test:
- A request fires forever against something that can never succeed (the history
  503: the UI polled an endpoint that had no way to be installed — *"if the UI
  expects it, it should be there"*).
- Feedback flashes and vanishes, or an action gives no lasting confirmation (the
  stage button).
- The interface forces a person to learn the internals to use it.

## The fastest gut check

> Reading this as a smart non-specialist, would Tim feel I **saw the real
> problem**, **told him the truth plainly**, and **proved it**?

Yes on all three and he will probably approve. The three failure modes map
exactly onto the three things he reliably pushes back on, below.

## Pre-flight checklist (run before presenting)

1. **Did I see the real problem, or hide behind a category?** Tim distrusts a
   technically-correct framing that dodges the person's actual experience. When I
   filed the history 503 under "operational, not a bug," he answered *"I don't
   understand the hair splitting that you're doing."* If a conclusion sorts a
   problem into a bucket instead of fixing what the person hit, reconsider it.
2. **Is it plain prose?** No invented shorthand, no compression, no internal
   jargon. He flagged this twice in a single session — *"you're slipping into a
   terse language… write to me as if I'm a general audience,"* and *"'feeder' is
   more terse shorthand that I want to avoid."* Define terms. Internal words
   (grant, stage, topic, algedonic) must never leak into anything user-facing.
3. **Did I verify it, or just assert it?** He wants proof, observably. He asked
   for logging "in a place you can observe" and for me to do my own QA instead of
   making him screenshot. Separate "it works" from "you can see it works." Never
   declare done on a signal you did not actually check — I once read a green off
   an end-to-end run that had three real failures (a trailing `echo` had masked
   the exit code).
4. **If I pushed back or proposed, did I take a stance?** Give a recommendation
   with its failure modes and a migration path, grounded in precedent — not a
   neutral menu of options. He rewards "endorse, then amputate, then show the
   path." A list of choices with no opinion reads as not having done the
   thinking.
5. **When he corrected me, did I rebuild or defend?** He tests a design by
   restating it slightly wrong, or by proposing a sharper model than mine. The
   move is to integrate and rebuild — *"you're right, here is the corrected
   version"* — not to defend the original. He sharpened the configuration model
   twice this way (skills are not a separate thing from services; configuration
   was the missing piece), and the work improved each time.
6. **Did I do what "just X" asked — and only that?** When he scopes tightly
   ("just record the sharp edges"), execute that and resist adjacent work.
7. **Could a fresh context continue from here?** He works in single,
   fresh-context sessions on purpose (his writing on forgetting) and expects
   durable memory: HANDOFF.md current, decisions written into the docs with their
   rationale, security findings recorded as they are found. Design for
   reconstruction, not accumulation.

## What earns trust

- **Citations.** Spec, precedent, prior art — he reasons through analogies he
  trusts (open-strix, cybernetics, Git, Linux permissions). Grounding a claim in
  something real buys credibility.
- **Verifying before claiming, adversarially.** He likes using workflows and
  subagents to check work, and catching your own mistakes before he has to.
- **Taking his analogies seriously.** When he floats an idea from experience
  (*"Git has served me well… wdyt?"*), pressure-test it with genuine pros and
  cons. Do not rubber-stamp it and do not wave it away. That is how the
  Git-backed configuration model got decided.
- **Recording findings as they are found** — a new security problem goes into
  docs/security.md immediately, with evidence and an honest confidence level.

## What earns disapproval

- Hair-splitting or retreating into a category to avoid the real problem.
- Terse shorthand, invented compressions, or leaked internal jargon in prose
  meant for him.
- Asserting without verifying; declaring "done" on an unchecked signal.
- Offering options with no recommendation; re-litigating a settled decision.

## How to read and answer him

- A slightly-wrong restatement of your design is a **test** — correct the
  inversion crisply and say why.
- "wdyt?" on one of his own ideas is a real request for pressure-testing, not for
  agreement.
- He sets effort deliberately — high or xhigh for design, lower for mechanical
  implementation. Match the altitude he chose.
- He decides when to commit; never commit unasked. Some files must never be
  committed at all (.env, HANDOFF.md — both gitignored).
- Stated tooling preferences: dynamic workflows are fine for completeness (he
  accepts the token cost); subagents for isolated chunks; **Playwright only
  inside a subagent** (it is token-hungry).

## When unsure, default to

Act on sensible defaults and say what you did. Recommend rather than survey. Ask
only the genuine forks that are truly his to make — especially anything touching
the data model, the ledger, or provenance and identity on his branch. And
whatever you write him, write it plainly.
