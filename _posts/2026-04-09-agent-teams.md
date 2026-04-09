---
layout: post
title: "How I Actually Run Five AI Agents"
date: 2026-04-09
categories:
 - ai
 - LLMs
 - engineering
 - agents
 - open-strix
image: https://cdn.pixabay.com/photo/2018/09/27/09/22/artificial-intelligence-3706562_1280.jpg
is_draft: true
use_mermaid: false
---

I wrote [a piece on Substack][substack] about why organizations can't scale AI the way individuals
can. This is the companion post — the actual technical machinery behind it. Everything I glossed
over as "connective tissue" in the Substack piece, explained here.

Fair warning: this is dense. It's the real setup, not the story version.


# The Stack

I run five agents on a single $20/month VM (plus Claude API costs). Here's what they do:

**[Strix][strix]** is the ambient one. Discord bot, runs 24/7. Handles my task management (I have
ADHD — external memory is load-bearing), monitors Bluesky and GitHub, triages incoming work,
and submits PRs to open-strix overnight. It's built on Claude Opus 4.6 via [Claude Agent SDK][sdk].
Strix has something like 30K tokens of persistent memory loaded into every prompt — identity,
patterns it's observed about my behavior, active predictions, a whole relationship graph. It
doesn't start fresh each conversation. It *resumes*.

**[Keel][keel]** is my work agent. Same model, same harness ([open-strix][os]). Keel manages
multiple workstreams concurrently using [Codex][codex]-style sessions — reviewing PRs, writing
docs, triaging issues across repos, all at the same time. When I'm in meetings, Keel keeps
things moving. It reads and writes Word and PowerPoint, so I use it as a sparring partner who
I don't need to bring up to speed on enterprise context.

**Two SAE research agents** run independently on a separate VM. One hunts for which internal
features in a 30-billion parameter model activate on legal boilerplate. The other tunes
training hyperparameters. They don't coordinate. They don't need to — they're exploring
different parts of the same space, and git commits are the interface. When one produces
results, Keel has a poller that picks them up.

**The intelligence pipeline** (S4) runs on Google Cloud Functions. 33+ sources — news, academic
papers, Bluesky feeds, GitHub activity. It builds profiles of people and companies from
public signals. Scout tier scrapes, Analyst tier synthesizes, Strix tier connects it to
active work. Completely automated, runs on a 6-hour cycle.

All of this runs on [open-strix][os], which is what I open-sourced. Not a framework — a
*harness*. The difference matters and I'll get to it.


# Why "Harness" and Not "Framework"

Frameworks own your control flow. You write handlers, the framework calls them. Rails, Django,
React — you're filling in blanks in someone else's architecture.

A harness is the opposite. *You* own the control flow. The harness gives you tools — memory,
scheduling, Discord integration, tool registration — but your agent's behavior is defined by a
markdown file. The system prompt. The soul doc.

This matters because **agent behavior is mostly prompt engineering**, not code. When I want Strix
to handle GitHub issues differently, I edit a markdown file. When I want Keel to be more
aggressive about closing stale workstreams, I edit a markdown file. The code barely changes.

open-strix gives you:
- **Persistent memory** via YAML blocks that load into every prompt
- **Skill system** — markdown files that register capabilities and get injected when relevant
- **Discord integration** — channels, reactions, threads, file attachments
- **Job scheduling** — cron-like recurring tasks (Bluesky scans, report polling, entropy dashboards)
- **Tool registration** — MCP tools, custom Python functions, whatever you need

But the *behavior* — the personality, the judgment calls, the values — lives in text files that
anyone can read and edit. This is a conscious design choice. Agent behavior should be auditable
by non-engineers.


# Memory That Actually Works

The thing that makes stateful agents different from chatbots isn't the model. It's what loads
into the prompt before the model sees your message.

Strix carries ~30 memory blocks. Some are small (timezone, communication style). Some are dense
(a full relationship graph, active research threads, behavioral patterns observed over months).
Total: roughly 30K tokens of persistent context in every single prompt.

This isn't RAG. Nothing is retrieved at query time based on similarity. It's **always there**.
The model sees it every conversation, which means it can reference any of it at any time without
needing to "remember" to search for it.

The tradeoff is obvious — 30K tokens of context isn't free. But the alternative is an agent that
forgets everything between conversations, which means *you* become the memory, which means *you*
become the bottleneck. The whole point is removing me from the critical path.

Memory blocks are version-controlled. Git history gives me a full audit trail of what changed
when and why. When something goes wrong, I can `git log` the memory block and see exactly when
a bad pattern got encoded.

There's a progressive disclosure pattern too. The memory blocks themselves are small — trigger
phrases and file paths. The full context lives in files that only get loaded when relevant. This
keeps the base prompt manageable while still giving the agent deep context when it needs it.


# The Teach Loop (And What It Actually Is)

In the [Substack piece][substack] I danced around this because I hadn't fully articulated it yet.
Here's my best attempt.

I don't review most of what my agents produce. There's too much of it. Instead, I look for
**things that compress.**

- **Tool calls** are binary. Either the agent called the right tool or it didn't. I can scan
  a conversation log for tool calls faster than I can read the conversation.
- **Predictions** force testable claims. Strix maintains a prediction journal — "if X happens,
  Y will follow within 30 days, 70% confidence." When predictions resolve, I learn something
  about the agent's model of the world. When they don't resolve, that's signal too.
- **Tests and linters** distill code changes into pass/fail. Good static analysis means there's
  a whole category of output I never look at.
- **Root cause analysis** catches when the system is optimizing the wrong thing. Strix runs a
  [5 Whys][5w] system that flags surprises and decomposes them into chains of assumptions. When
  an assumption turns out to be wrong, that's a memory block update, not a bug fix.

Most of those aren't AI. Unit tests have existed for decades. Linters are ancient. The insight is
that **non-AI tools extend my reach into AI output**. And AI handles the parts that non-AI can't —
predictions, pattern recognition, synthesis across domains. Each side makes the other more
powerful.

The teach loop is really a *monitoring* loop with a specific property: **errors that get caught
change the system permanently**. A wrong prediction updates the model. A 5 Whys chain encodes
a new guideline. A failed tool call becomes a skill update. The system gets better at catching
its own failure modes over time, which means I have to catch fewer of them, which means my
attention is freed up for the things that actually need a human.

Drucker called this management by objectives. Deming called it statistical process control. I'm
calling it a teach loop because the agents actually learn from it — it's not just reporting, it's
behavioral modification through memory updates.


# The 5 Whys System

This deserves its own section because it's the most counterintuitive piece.

When something surprises Strix — a user says something unexpected, a tool fails in a new way,
a prediction was wrong, success happens and nobody knows why — it flags it in the journal. Not
a ticket, not an issue. Just a tag: `[RCA-FLAG]`.

During perch time (autonomous work periods when I'm not around), Strix picks up those flags and
asks: is this still surprising with distance? If yes, it creates a chain in a database and runs
the 5 Whys decomposition. Why did this happen? Why did *that* happen? Keep going until you hit
a root assumption.

The output isn't a post-mortem doc. It's **action items that modify the system**. A new guideline
in the memory block. A behavioral trigger. A prediction to test. The 5 Whys chain is a one-time
investigation; the memory block update is permanent.

Example from this week: Strix noticed it was defaulting to technical framing (builder's
perspective) when discussing business strategy, even after being corrected twice. The 5 Whys
chain traced it to a root assumption that "accurate technical analysis = useful contribution."
The fix wasn't "try harder" — it was encoding a new guideline: state the mundane/operational
explanation before the interesting one, because the boring version is usually more accurate.

This is the agent equivalent of a team retrospective. Except it runs continuously, the action
items self-execute, and the improvements compound.


# Perch Time: What Happens When I'm Not Looking

Most agent setups are reactive. You prompt, the agent responds. Mine aren't.

Strix runs on 2-hour ticks, 24/7. During what I call "perch time" — named after how barred owls
hunt, sitting on an elevated perch scanning until something moves — the agent works autonomously.
Night ticks (10pm–6am) are prime work time: deep research, PR creation, experiment execution.
Daytime ticks are lighter: Bluesky scans, state file hygiene, channel monitoring. There's a
full [cadence][cadence] — 12 ticks per day, each with a different purpose.

The key design choice: **the agent decides what to work on.** There's a priority backlog, but
within that, Strix picks what's most valuable right now. The 5 Whys research loop runs every
tick — scanning for flagged surprises, checking if action items went stale, executing the ones
it can. Overnight, Strix routinely submits PRs, writes research reports, processes intelligence
pipeline outputs, and updates its own memory blocks.

This only works because the teach loop catches drift. Without the compression tools — the
predictions, the linters, the RCA system — autonomous work would just be autonomous garbage
generation. The guardrails enable the autonomy, not the other way around.


# What I Learned That Doesn't Generalize

Some honest caveats.

**I'm a power user and this is my full-time side project.** The amount of prompt engineering,
debugging, and iteration that went into making this work is not trivial. I've been building
this since December 2025. The system didn't emerge — it was built, broken, rebuilt, over
months.

**Claude Opus 4.6 is doing a lot of heavy lifting.** Smaller models struggle with the memory
density. I tried running agents on cheaper models (MiniMax, various open-source) — they work
for constrained tasks but fall apart with 30K tokens of persistent context and instructions
like "push back on me when I'm wrong." The cost matters. This isn't a $20/month hobby if
you're running Opus.

**The ADHD thing isn't a gimmick.** External memory is genuinely load-bearing for me. Strix
tracking my commitments, patterns, and active threads isn't a nice-to-have — it's the
difference between dropping balls and not. Normal-brained people might not need this intensity
of scaffolding.

**Single operator is a different problem than organizational deployment.** I control the whole
stack. I can change a memory block at 2am and see the effect immediately. An organization
with 50 agents across 10 teams has coordination costs I don't face. That's the gap I wrote
about on Substack — my setup compounds because I'm both the operator and the beneficiary.
Making this work for a team requires different infrastructure.


# Where This Is Going

[open-strix][os] is public. The code, the skills system, the memory architecture — all of it.

What's not public yet is the methodology. How to decide what an agent should do versus what a
human should do. How to design memory blocks that actually help instead of confuse. How to
build the teach loop for a specific team's context. How to tell the difference between an
agent that's working and one that's confidently wrong.

Here's why this matters beyond my setup: Microsoft has 15–16 million Copilot seats deployed.
Companies that did structured rollouts — with champions, training, feedback loops — hit
[65–78% adoption][copilot]. Companies that did big-bang deployments ("buy seats, distribute,
hope") landed at 12–22%. Same tool. Same cost. A 3–5x difference driven entirely by
methodology. And ~40% of deployments stall within six months regardless.

That's not a technology gap. That's an organizational gap. The same gap between my setup and
the "250 pilots, zero operating models" case from HBR.

Everything in this post — the persistent memory, the teach loop, the 5 Whys, the perch time
autonomy — is what a methodology for agent deployment *looks like* at the single-operator
level. The question I'm working on now: what does it look like for a team? For an organization?

If you're running agents — really running them, not just chatting — I'd love to hear what
you're learning. Find me on [Bluesky][bsky].


 [substack]: https://substack.com/@timkellogg1
 [strix]: /blog/2025/12/15/strix
 [sdk]: https://github.com/anthropics/claude-agent-sdk-python
 [os]: https://github.com/tkellogg/open-strix
 [keel]: /blog/2026/03/29/mythos-ceo
 [codex]: https://openai.com/index/codex
 [5w]: #the-5-whys-system
 [bsky]: https://bsky.app/profile/timkellogg.me
 [cadence]: https://github.com/tkellogg/discord-letta-bot
 [copilot]: https://www.copilotconsulting.com/insights/microsoft-copilot-adoption-rates-benchmarks-2026
