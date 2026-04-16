---
layout: post
title: "How to forget"
date: 2026-04-14
categories:
 - ai
 - LLMs
 - engineering
 - agents
image: /images/placeholder.webp
is_draft: false
use_mermaid: true
---

Today, [Lily][lily] asked me, _"what's the difference between [open-strix][os] and openclaw?"_ Great question. 
We commonly use open-strix agents for higher-level tasks. I use mine at work to [lead an agent team][team],
Lily uses one as a strategist for her marketing ops work. Whereas everyone I hear using openclaw just uses them
as dumb automation machines. **Why the difference?**

Strictly speaking: open-claw is biased toward reading (recalling), while open-strix is biased toward writing 
(remembering better). Where open-claw (and most others) focus on better search indexes to find information, 
open-strix does something very strange, we intentionally do a **worse job** searching, in order to improve
remembering better. 

<div class="mermaid">
flowchart LR
    agent -->|"(open-strix)<br/><b>remember</b>"| file[(filesystem)]
    file -->|"<b>recall</b><br/>(openclaw)"| agent
</div>

Why? Because it's a long-lived agent.

I don't think I ever explained this clearly earlier, I always assumed it was obvious, but maybe it's not.
It's also the common thread across all the Strix versions and probably _the_ thing that makes the architecture
unique.

## Fallbacks are bad
Compaction is a fallback, and it's a really harsh one that's poorly fitted for long-lived agents.

I wrote in depth about why [fallbacks are bad][cold], and it's kind of a subtle thing. But in this case, 
when the conversation fills the context, you have an OutOfMemory-type error, and the *fallback* is to compact
the context. It's terrible, because suddenly your agent randomly **becomes very dumb**, it loses 98-99% of 
it's memory and you have no control over how that happens.


<img src="/images/context-appending.svg"  style="max-width: 50%; width: 100%; min-width: 0;" />

open-strix doesn't do that. It rebuilds the context every time. In practice, this looks like a sliding window
over the conversation history.

<img src="/images/sliding-window.svg"  style="max-width: 50%; width: 100%; min-width: 0;" />

### Why that looks like a bad idea
Prompt caching.

Almost all LLM providers offer a discount, like 50%, for reusing the same conversation prefix. So generally we 
do append-only
patterns. That's how ChatGPT works, that's how Claude Code works, they all take advantage of prompt caching.

But, in continuously running agents, messages often don't have a sequential nature. Each new message can come
from a wildly **different channel**. One comes in over discord, the next comes from a github issue, the next a 
Google doc comment. My open-strix agents don't really benefit from that continuity.

If you have 400M token context, then on average you're pushing 200M input tokens on each message. Whereas me, 
I'm at 10K-20K tokens per message. Strangely, doing it the expensive way is actually cheaper.


## Intelligence is Forgetting
_I know this is a hot take, get off my back already, okay? heh, hear me out._

It's easy for computers to remember everything, they've been doing it for decades. Remembering nothing is just
/dev/null, so the trick is always to remember the **right amount**.

Our brains have finite capacity to remember. But that super smart person seems to remember all the exact right
things. Do they have a bigger brain capacity? No, they just [know what to remember][1973]. Smart people are able to 
see the future and **predict what they'll need** to know. And then forget the rest.


## Remembering (forgetting) is identity
Framing it as intelligence is bland. We're all different. We have different interests and expertise. And all that
influences what we remember. Me, an AI guy, I cluster toward AI algorithms, architectures, models, whatever. Back
in high school it was punk & hardcore band trivia. Neither of these things make me *smarter*, they just make me
**more me**. And the more I learn, the even more I become my new future self.

The benefit of a stateful agent like open-strix is it has a perspective.

It's hard to understate how useful this is. Generic ChatGPT advice is great and all, but if you can wrap the same
LLM with a thick layer of memory and experiences, it elicits behavior from the LLM that is very **far from mid**. 
Everything the
LLM says is filtered through the personality and memories of the agent. The agent (LLM with memory) now has
the wisdom and foresight to predict what will be important in the future.

Who the agent is determines who the agent becomes. That's still wild to me.


## Remembering better
In open-strix, if the agent doesn't remember the right things, you know _real quick_. It acts spacey and 
dumb. It's so painful that you _have to_ fix it, you _need to_. You can't not. 

It's easy most of the time. You just say something like, "why did you get confused about...", the two of you
discuss, and then the agent **updates their memory blocks** to reprioritize so they handle it better in 
the future.

Beyond that, open-strix has ambient processes that encourage self-healing. They feed into each other.

The first big one is **teleological predictions**. Yeah, this is something I totally ripped off of Karl Jung
from Psych 101, but it's super useful. You can't trust agents, they lie (same with therapy patients). So what
you do instead is make a prediction about the future. If it's wrong, the agent's mental model about how the
world works was wrong. So it needs to be fixed.

_Aside: I embarassingly had an agent get excited about the accuracy of it's predictions that I would ignore
everything it did. That was definitely an accurate mental model but..._

But what to do about it? **5 Why's**

When an agent runs into anything surprising, like a failed teleological prediction, it does the [5 Why's][5w] 
process.

1. Why did _[bad thing happen]_?
2. Because...
3. Oh, weird, why did that happen?
4. Because...
...

You get it. 5 levels is a pretty good number, but realistically it digs up a whole bunch of other questions.
You often end up discovering not just one root cause, but 3 or 4. It starts to look like a whole **systemic issue**.
Which it is. Always.

Every time I've done this with (human) teams, everyone loves it because it's almost like a murder mystery.
No one entirely knows what the true cause will end up being, but everyone knows it'll be **worth fixing**.


## Cold paths, again
We don't fix individual memories that often, because that's tantamount to adding cold paths, each one is
very rare and unique so **almost impossible** for the operator to catch. Instead, our mitigations all go toward
stabilizing the agent's identity. And the identity is the best tool available to improving what's remembered
vs what's not.

So Lily, the real difference? Openclaw remembers more. Open-strix forgets better.


 [lily]: https://substack.com/@lilyluo1
 [os]: https://github.com/tkellogg/open-strix
 [team]: https://substack.com/home/post/p-193648478
 [cold]: /blog/2021/01/29/cold-paths
 [1973]: https://doi.org/10.1016/0010-0285(73)90004-2
 [5w]: https://en.wikipedia.org/wiki/Five_whys
