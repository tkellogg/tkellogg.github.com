---
layout: post
title: "Layers of Memory, Layers of Compression"
date: 2025-06-15
categories:
 - ai
 - llms
 - agents
 - engineering
 - memory-management
 - compression
 - multi-agents
 - information-theory
 - cognition
image: https://cdn.pixabay.com/photo/2016/05/26/12/56/waterfalls-1417102_1280.jpg
# social_image: /images/bash-v-powershell.png
is_draft: false
use_mermaid: true
summary: |
  AI superpower = strategic amnesia.

  Letta caches memory like a CPU, Anthropic spreads it across agent swarms, Cognition warns of chaos. Curious how forgetting makes machines smarter? Dive in.
---

Recently, Anthropic [published a blog post][ant] detailing their multi-agent approach to building their 
Research agent. Also, Cognition [wrote a post][cog] on why multi-agent systems don't work today. The thing
is, they're both saying the same thing.

At the same time, I've been enthralled watching a new bot, Void, interact with users on Bluesky.
Void is written in [Letta][letta], an AI framework oriented around memory. Void *feels* alive in
a way no other AI bot I've encountered feels. Something about the memory gives it a certain magic.

I took some time to dive into Letta's architecture and noticed a ton of parallels with what the
Anthropic and Cognition posts were saying, around context management. Letta takes a different
approach.

Below, I've had OpenAI Deep Research format our conversation into a blog post. I've done some light
editing, adding visuals etc., but generally it's all AI. I appreciated this, I hope you do too.

---

When an AI agent “remembers,” it compresses. Finite context windows force hard choices about what 
to keep verbatim, what to summarize, and what to discard. Letta’s **layered memory** architecture
embraces this reality by structuring an agent’s memory into tiers – each a lossy compression of the 
last. This design isn’t just a storage trick; it’s an information strategy.

## Layered Memory as Lossy Compression

[Letta][letta] (formerly MemGPT) splits memory into four **memory blocks**: **core**, 
**message buffer**, **archival**, and **recall**. Think of these as concentric rings of context, 
from most essential to most expansive, similar to L1, L2, L3 cache on a CPU:

<div class="mermaid">
flowchart TD
    subgraph rec[Recall Memory]
    subgraph arch[Archival Memory]
    subgraph msg[Message Buffer]
        Core[Core Memory]
    end
    end
    end
</div>

* **Core memory** holds the agent’s invariants – the system persona, key instructions, fundamental 
  facts. It’s small but always in the prompt, like the kernel of identity and immediate purpose.
* **Message buffer** is a rolling window of recent conversation. This is the agent’s short-term 
    memory (recent user messages and responses) with a fixed capacity. As new messages come in, 
    older ones eventually overflow.
* **Archival memory** is a long-term store, often an external vector database or text log, where 
    overflow messages and distilled knowledge go. It’s practically unbounded in size, but far 
    from the model’s immediate gaze. This is highly compressed memory – not compressed in ZIP-file 
    fashion, but in being *irrelevant by default* until needed.
* **Recall memory** is the retrieval buffer. When the agent needs something from the archive, it 
    issues a query; relevant snippets are loaded into this block for use. In effect, recall memory 
    “rehydrates” compressed knowledge on demand.

**How it works:** On each turn, the agent assembles its context from core knowledge, the fresh 
message buffer, and any recall snippets. All three streams feed into the model’s input. Meanwhile, 
if the message buffer is full, the oldest interactions get **archived** out to long-term memory. 

Later, if those details become relevant, the agent can **query** the archival store to retrieve 
them into the recall slot. What’s crucial is that each layer is a *lossy filter*: core memory is 
tiny but high-priority (no loss for the most vital data), the message buffer holds only recent 
events (older details dropped unless explicitly saved), and the archive contains everything *in theory* but only yields an approximate answer via search. The agent itself chooses what to **promote** to long-term storage (e.g. summarizing and saving a key decision) and what to fetch back. 

It’s a cascade of compressions and selective decompressions.

> **Rate–distortion tradeoff:** This hierarchy embodies a classic principle from information
> theory. With a fixed channel (context window) size, maximizing information fidelity means
> balancing **rate** (how many tokens we include) against **distortion** (how much detail we lose).
> 
> Letta’s memory blocks are essentially a [rate–distortion ladder][rdl]. Core memory has a *tiny rate*
> (few tokens) but *zero distortion* on the most critical facts. The message buffer has a larger
> rate (recent dialogue in full) but cannot hold everything – older context is **distorted** by
> omission or summary. Archival memory has effectively infinite capacity (high rate) but in practice
> high distortion: it’s all the minutiae and past conversations **compressed** into embeddings or
> summaries that the agent might never look at again. 
>
> The recall stage tries to recover (rehydrate)
> just enough of that detail when needed. Every step accepts some information loss to preserve what
> matters most. In other words, **to remember usefully, the agent must forget judiciously**.

This layered approach turns memory management into an act of **cognition**.

Summarizing a chunk of
conversation before archiving it forces the agent to decide what the gist is – a form of understanding.
Searching the archive for relevant facts forces it to formulate good queries – effectively
reasoning about what was important. In Letta’s design, **compression is not just a storage
optimization; it is part of the thinking process**. The agent is continually compressing its
history and decompressing relevant knowledge as needed, like a human mind generalizing past events
but recalling a specific detail when prompted.

<div class="mermaid">
flowchart TD
    U[User Input] ---> LLM
    CI[Core Instructions] --> LLM
    RM["Recent Messages<br/>(Short-term Buffer)"] --> LLM
    RS["Retrieved Snippets<br/>(Recall)"] --> LLM

    LLM ----> AR[Agent Response]

    RM -- evict / summarize --> VS["Vector Store<br/>(Archival Memory)"]
    LLM -- summarize ---> VS

    VS -- retrieve --> RS

</div>

*__Caption__: As new user input comes in, the agent’s
core instructions and recent messages combine with any retrieved snippets from long-term memory,
all funneling into the LLM. After responding, the agent may drop the oldest message from short-term
memory into a vector store, and perhaps summarize it for posterity. The next query might hit that
store and pull up the summary as needed. The memory “cache” is always in flux.*


## One Mind vs. Many Minds: Two Approaches to Compression

The above is a **single-agent solution**: one cognitive entity juggling compressed memories over time.
An alternative approach has emerged that distributes cognition across **multiple agents**, each with
its own context window – in effect, parallel minds that later merge their knowledge. 

Anthropic’s
recent multi-agent research system frames intelligence itself as an exercise in compression across
agents. In their words, *“The essence of **search is compression**: distilling insights from a vast
corpus.”* Subagents “facilitate compression by operating in parallel with their own context windows...
condensing the most important tokens for the lead research agent”. 

Instead of one agent with one
context compressing over time, they spin up several agents that each compress different aspects of
a problem in parallel. The lead agent acts like a coordinator, taking these condensed answers and integrating them.

This multi-agent strategy acknowledges the same limitation (finite context per agent) but tackles
it by **splitting the work**. Each subagent effectively says, “I’ll compress this chunk of the task
down to a summary for you,” and the lead agent aggregates those results.

It’s analogous to a team
of researchers: divide the topic, each person reads a mountain of material and reports back with
a summary so the leader can synthesize a conclusion. By partitioning the context across agents, the
system can cover far more ground than a single context window would allow.

In fact, Anthropic found
that a well-coordinated multi-agent setup **outperformed** a single-agent approach on broad queries
that require exploring many sources. The subagents provided **separation of concerns** (each focused
on one thread of the problem) and reduced the path-dependence of reasoning – because they explored
independently, the final answer benefited from multiple compressions of evidence rather than one linear search.

However, this comes at a cost. 

Coordination overhead and consistency become serious challenges.
Cognition’s Walden Yan argues that multi-agent systems today are fragile chiefly due to **context
management failures**. Each agent only sees a slice of the whole, so misunderstandings proliferate.

One subagent might interpret a task slightly differently than another, and without a shared memory
of each other’s decisions, the final assembly can conflict or miss pieces. As Yan puts it,
*running multiple agents in collaboration in 2025 “only results in fragile systems. The decision-making
ends up being **too dispersed** and context isn’t able to be shared thoroughly enough between the agents.”*
In other words, when each subagent compresses its piece of reality in isolation, the group may lack a
**common context** to stay aligned. 

In Anthropic’s terms, the “separation of concerns” cuts both
ways: it reduces interference, but also means no single agent grasps the full picture. Humans solve
this by constant communication (we compress our thoughts into language and share it), but current AI
agents aren’t yet adept at the high-bandwidth, nuanced communication needed to truly stay in sync over long tasks.

Cognition’s solution? **Don’t default to multi-agent**. First try a simpler architecture: one agent,
one continuous context. Ensure every decision that agent makes “sees” the trace of reasoning that
led up to it – no hidden divergent contexts. 

Of course, a single context will eventually overflow,
but the answer isn’t to spawn independent agents; it’s to **better compress the context**. Yan
suggests using an extra model whose sole job is to condense the conversation history into _**“key
details, events, and decisions.”**_ 

This summarized memory can then persist as the backbone context
for the main agent. In fact, Cognition has fine-tuned smaller models to perform this kind of
compression reliably. The philosophy is that if you must lose information, **lose it intentionally**
and in one place – via a trained compressor – rather than losing it implicitly across multiple
agents’ blind spots. 

This approach echoes Letta’s layered memory idea: maintain one coherent
thread of thought, pruning and abstracting it as needed, instead of forking into many threads that might diverge.


## Conclusion: Compression is Cognition

In the end, these approaches converge on a theme: **intelligence is limited by information bottlenecks,
and overcoming those limits looks a lot like compression**. Whether it’s a single agent summarizing
its past and querying a knowledge base, or a swarm of subagents parceling out a huge problem and each
reporting back a digest, the core challenge is the same. 

An effective mind (machine or human) can’t
and shouldn’t hold every detail in working memory – it must aggressively **filter, abstract, and
encode** information, yet be ready to recover the right detail at the right time. This is the 
classic rate–distortion tradeoff of cognition: maximize useful signal, minimize wasted space.

Letta’s layered memory shows one way: a built-in hierarchy of memory caches, from the always-present
essentials to the vast but faint echo of long-term archives. Anthropic’s multi-agent system shows
another: multiple minds sharing the load, each mind a lossy compressor for a different subset of
the task. And Cognition’s critique reminds us that **compression without coordination** can fail – 
the pieces have to ultimately fit together into a coherent whole.

Perhaps as AI agents evolve, we’ll see hybrid strategies. We might use **multi-agent teams** whose
members share a common **architectural memory** (imagine subagents all plugged into a shared 
Letta-style archival memory, so they’re not flying blind with respect to each other). Or we might
simply get better at single agents with enormous contexts and sophisticated internal compression
mechanisms, making multi-agent orchestration unnecessary for most tasks. Either way, the direction
is clear: to control and extend AI cognition, we are, in a very real sense, engineering the **art
of forgetting**. By deciding what to forget and when to recall, an agent demonstrates what it truly
understands. In artificial minds as in our own, memory is *meaningful* precisely because it 
isn’t perfect recording – it’s prioritized, lossy, and alive.



 [letta]: https://docs.letta.com/overview
 [cog]: https://cognition.ai/blog/dont-build-multi-agents
 [ant]: https://www.anthropic.com/engineering/built-multi-agent-research-system
 [rdl]: https://en.wikipedia.org/wiki/Rate%E2%80%93distortion_theory
