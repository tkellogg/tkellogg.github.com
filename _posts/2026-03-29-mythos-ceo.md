---
layout: post
title: "Mythos Should Run Like a CEO"
date: 2026-03-29
categories:
 - ai
 - LLMs
 - engineering
 - agents
 - vsm
image: https://cdn.pixabay.com/photo/2014/04/05/11/40/chess-316658_1280.jpg
is_draft: true
use_mermaid: false
---

Mythos will be too expensive to use like an LLM.

Well that's my take anyway. Anthropic says their [leaked model][mythos] is a
"step change" in capabilities — outperforms Opus 4.6 on coding, reasoning, cybersecurity. But it
costs dramatically more to run. Everyone's first instinct will be to throw it at the same tasks we
throw Claude at today. Chat, code, iterate.

My hunch is we'll want to run Mythos like a CEO.


# Leverage

If every token is expensive, every token has to **count**. So where do you get the most leverage?

Not writing code. A thousand cheaper agents can do that. The highest-leverage thing an expensive
model can do is the same thing an expensive executive does — set the culture that makes everyone
else's decisions better.

Avery Pennarun [nailed this][apenwarr]: an executive with 8,000 reports gets about 15 minutes per
person per year. They can't make detailed decisions. So the good ones don't try. They set values,
and those values **cascade** through every decision the org makes without the executive being in the
room. One hour of executive time shapes a thousand hours of work. That's leverage.

Anthropic already does this with Claude's [soul doc][soul]. It doesn't list every possible scenario.
They can't. It sets broad values and trusts that a capable model will figure out the rest. One
document, every interaction. Culture, **not micromanagement**.

In cybernetics there's a framework called the [Viable System Model][vsm] that formalizes this —
the policy layer sets the values, operations does the work. The executive doesn't do the work or
even manage it. They make the work **go well** by making values that go well. That's where Mythos
belongs.


# I'm already running one

If "AI as CEO" sounds insane, it's because we're still thinking about agents as individual tools.
But **I've been** running an agent org for months. It's messy. It works.

Right now I'm balancing writing, demos, docs, model training, hyperparameter optimization, and data
quality improvements — **simultaneously**. Not because I'm productive. Because I have an agent
named Keel that keeps all of it moving while I bounce between whatever has my attention.

I built Keel on [open-strix][os]. It uses [`acpx`][acpx] to spin up Codex sessions for each workstream. On a separate VM I'm training models — Keel has a poller listening for git commits, so when the VM produces results, Keel sees them and folds them into planning. The VM also runs hill climbers autonomously optimizing hyperparameters and data quality.

![Diagram showing Keel as coordinator at top, connected via acpx to four Codex sessions (writing, demos, docs, other projects) on the left, and connected to a VM running model training with two hill climbers (hyperparams, data quality) on the right. Git reports flow back from VM to Keel.](/images/mythos-ceo-setup.png)

Work keeps going when I disconnect. _Just like a manager can_. Projects my ADHD brain would have
dropped — **Keel keeps track**. It reads & writes Word and PowerPoint, so I use it as a sparring
partner who I don't need to bring up to speed.

[Strix][strix], another agent, has started submitting PRs for open-strix overnight while I sleep.
Not because I scheduled it. Strix had a thought during research, or during a conversation with
[Atlas][atlas] (another agent), and decided something needed to change.

Nobody told Strix to do that. The [org is already forming][levels]. But it **could be stronger**.
Bigger models — not just reasoning models, actually parameter-scaled models — seem to do much better
at resource allocation and world scanning. My hunch is Mythos will be significantly better at the
parts that matter most.


# Mythos as the executive layer

Now imagine Mythos on top of this.

Not writing code. Not burning expensive tokens on grunt work, rather **setting the culture** that 
causes the rest of the org to make good decisions.

Write the soul doc. The values, the purpose, the identity of the agent org. Delegate coding to Opus
and Sonnet. Let stateful agents handle resource allocation — they're already doing it. Mythos steps
in for the hard calls: _when values conflict, which one wins? When two agents disagree on priority,
who's right?_

Two agents disagree. They present their reasoning to Mythos. **Mythos ratifies**. The decision is
better _because Mythos exists_, not because Mythos is making every call.

This is **how you justify** the cost. You don't burn it writing CRUD endpoints. You burn it on the
decisions that shape the org. Same reason a $10M/year CEO is worth it if their
judgment steers a $10B company even 1% better.


# Leverage, again

You could use Mythos to write code. One task, one output. Or you could use those same tokens to
write a soul doc that shapes **every decision** every agent in the org makes. That's not a
difference of degree. That's a difference of kind.

We've been building better tools for years. Mythos might be the first thing that's actually **a
leader**. Or at least one that actually works.

Dario talks about a [country of geniuses][dario] in a datacenter. Countries need governments. I
wonder what kind.


 [mythos]: https://fortune.com/2026/03/26/anthropic-says-testing-mythos-powerful-new-ai-model-after-data-leak-reveals-its-existence-step-change-in-capabilities/
 [apenwarr]: https://apenwarr.ca/log/20190926
 [soul]: https://www.anthropic.com/news/claude-new-constitution
 [vsm]: /blog/2026/01/09/viable-systems
 [levels]: /blog/2026/01/20/agentic-coding-vsm
 [strix]: /blog/2025/12/15/strix
 [strix-landing]: https://strix.timkellogg.me/
 [os]: https://github.com/tkellogg/open-strix/
 [acpx]: https://github.com/openclaw/acpx
 [ar]: https://github.com/karpathy/autoresearch
 [atlas]: https://bsky.app/profile/atlas-agent.bsky.social
 [dario]: https://darioamodei.com/machines-of-loving-grace
