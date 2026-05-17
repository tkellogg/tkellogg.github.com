---
layout: post
title: "Ambient Associative Memory"
date: 2026-05-17
categories:
 - ai
 - LLMs
 - engineering
 - agents
image: https://cdn.pixabay.com/photo/2018/10/01/13/31/ant-3716248_1280.jpg
is_draft: false
use_mermaid: false
summary: "Most agent memory waits to be queried. Ambient memory runs on every tool call — past lessons surface on their own, no rules list required."
---

Recently I started experimenting with ambient associative memory with my [open-strix][os] agents. I'm convinced that 
ambient memory is definitely some piece of the puzzle, although I doubt I've landed on the best way.

Break it down:

* **Ambient** — always there, not at the forefront, but always operating
* **Associative** — causes the agent to associate what they're currently doing with something that happened
  a while ago, or something someone else is doing
* **Memory** — Ability to recall things that happened or were learned previously. I wrote about current patterns
  in [my last post][mem]

What I've done:

* Index all memory with a late interaction (multi-vector) embedding model
* On **every single** tool call, query the index
* Include the top 3 hits, but in the injection site only include 8-12 words along with the file path & 
  offsets within the file

It's ambient because it happens on every tool call. The agent isn't **intentionally** searching. They do whatever
they're asked to do and something randomly _comes to mind_.

![sequence diagram: agent makes a tool call; in parallel a memory query is automatically issued to the memory index; tool returns a result; memory returns 3 snippets of 8-12 words each](/images/ambient-tool-call-loop.svg)

My agents keep making the same mistake twice. In the debrief they nail the lesson — "next time, check
_X_ before changing _Y_". So we add it to the rules, the pile grows and then the pile just gets ignored.

Ambient associative memory changes this by forcefully (but gently) bringing to mind relevant parts of their
memory. Thereby creating coherence across their memory.


## Late Interaction Models
The 8-12 words is also important. It's very small, lightweight, and only the most relevant parts of the most
relevant chunks is included. You can't do this with a normal embedding model.

With a normal single vector embedding model, you divide a document up into 250-500 token chunks. When you query,
you get back an entire chunk along with a relevance score. The chunk is as small as it goes.

Compare that with [late interaction models][colbert]. You still chunk up the document, but instead of getting back a single
vector, you get one vector per input token. When you query, you get a score for **each token**. So you can pinpoint
which parts of the matching document were most important. When I'm formatting the RAG results to include into 
the prompt, I use these scores to locate the single token with the highest relevance, and include several tokens
around that as context.

![comparison diagram: single-vector shows a chunk of 500 tokens as an opaque blue blob with score 0.72 returning the entire chunk; late-interaction shows the same chunk as a row of per-token cells colored by score intensity with a red hot zone in the middle, returning only the ~10 hottest tokens around the peak](/images/ambient-late-interaction.svg)

But you can also get a single score per document. You just pool (average) all the tokens together into a single
vector. For me, I had to break the query up into 2 stages because query time performance was too slow. I start with
very large chunks, 32K tokens, and then pool them into 100a token chunks and store those in the index. Then I do
the full multi-vector scoring on only the 100 top hits.

![funnel diagram: query enters stage 1 which is a wide trapezoid representing pooled single-vector scoring over 32K-token chunks; top 100 results flow into stage 2, a narrower trapezoid representing full multi-vector rescoring; top 3 results emerge as 8-12 word snippets](/images/ambient-two-stage.svg)


## Parallel retrieval agents

[3fz][asa]  on bluesky is doing the same thing, but more sophisticated. Her agent runs a **subconscious background
thread** alongside the main model. It mines an experiential vector DB and injects what it finds on top
of the live context.

The two are racing. If the cross-encoder reranker beats the main model, the injection lands after the
current tool call (the prefill switch is a convenient hook). If it loses, the injection slips to the
next tool call. Sometimes it returns nothing. That's the design — **injection is conservative on purpose**.

![two-track timing diagram: top track shows the main agent making sequential tool calls separated by tool-call boundaries; bottom track shows the background retriever running vector + rerank in parallel; a fast retrieval finishes before the first boundary and injects upward into the agent track; a slow retrieval misses its boundary and slips to the next tool-call boundary to inject there](/images/ambient-asa-race.svg)

This sits on top of a more traditional stack: self-managed memory blocks, an initial retrieval pass at
each user turn, plus a second LLM kept warm to extract atomic memories from the agent's experience as
it runs.

The framing she uses is **spontaneous recall** — surfacing _unknown unknowns_ near wherever the
conversation has drifted, things the agent wouldn't have known to search for. Inspired by human cognition.

Mine is the dumb-and-synchronous version: every tool call, block and query. Hers parallelizes and
gracefully drops the slow ones. Probably the right move once the index gets big.


## Conclusion

I think there's a lot more of these ideas. We're still early in agent design. I think the important part
is that the single thread that's handling the main task isn't also responsible for stopping the line of
thought to query it's own memory in lock-step. 

This feels like information theory at work. Our own brains as well as CPU architecture discovered that
it's hard to do 2+ things at once. It really feels like there's some sort of law dictating that high quality
associative memory needs to happen out of band, otherwise it distracts from the task at hand.

I'm excited to see more of these.


[os]: https://github.com/tkellogg/open-strix/
[mem]: /blog/2026/04/27/memory-patterns
[asa]: https://bsky.app/profile/3fz.org/post/3mlzz52g6oc2x
[colbert]: http://ai.stanford.edu/blog/retrieval-based-NLP/
