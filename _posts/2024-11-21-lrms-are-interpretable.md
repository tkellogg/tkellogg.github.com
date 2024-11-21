---
layout: post
title: "LRMs Are Interpretable"
date: 2024-11-21
categories:
 - ai
 - LLMs
image: https://cdn.pixabay.com/photo/2024/02/07/07/15/station-8558516_960_720.jpg
is_draft: false
use_mermaid: false
---

A year ago I wrote a post called [LLMs Are Interpretable][prev]. The gist is that LLMs were the closest
thing to "interpretable machine learning" that we've seen from ML so far. Today, I think it's fair to
say that LRMs (Large Reasoning Models) are even more interpretable.

Yesterday DeepSeek [released their reasoning model][r1], R1. For kicks, I threw it a riddle that my 8 year old
loves:

> If you're flying over a desert in a canoe and your wheels fall off, how many pancakes does it take to cover a dog house?

Most people will (should) do a double take, and then give up. It's a nonsense question. Even if you try to estimate
the sizes of doghouses and pancakes, there's so much contention about both that the estimates are also meaningless.
This is a test of a highly ambiguous situation, how does the model handle it?

The transcripts are fascinating, I'll quote some passages here, but really you should go ahead and [read the full
reasoning trace][gist].  The final answer isn't terribly interesting; tl;dr it figures out that it's a nonsense question. 

### The Reasoning

Off the start, it tries to break the problem down and immediately notes a lot of inconsistency:

> First, "flying over a desert in a canoe." Well, canoes are typically used on water, not in the air or over deserts. So that's already a bit odd. Maybe it's a metaphor or a riddle that plays on words. Then it says, "your wheels fall off." Canoes don't have wheels, so that's another strange part. Maybe the wheels are part of something else, or maybe it's just adding to the confusion.

Then it doubts itself and tries looking at it from a different angle, puns and double meanings:

> Perhaps I'm approaching this the wrong way. Maybe it's a riddle where the answer isn't literal but more about wordplay or logic. Let's consider if there's a pun or a double meaning here.

And then metaphors:

> Wait a minute, maybe "wheels" isn't referring to actual wheels. Could it be a metaphor for something else? Or perhaps the entire first part is just a distraction, and the real question is about pancakes and a dog house.

The it begins to think it's being tricked:

> But then why include all that other information?

Then it begins to suspect that it's nonsense:

> Alternatively, maybe the key is to realize that the scenario described is impossible or doesn't make sense, which might imply that the answer to the question is also nonsensical or that it's a trick question. If you're flying over a desert in a canoe with no wheels, perhaps the number of pancakes needed is zero because the scenario itself is impossible.

Followed by my absolute favorite part, its worried that it's being *dismissive*:

> But that feels a bit too dismissive. Maybe there's a deeper meaning or a specific answer that I'm missing. Let me try to think of it differently. 

It goes on like this for pages and pages. It runs calculations. It suspects diversion. It uses the phrase, "In conclusion," followed by 10 thousand more characters of reasoning. The whole thing is a trip.


### Interpretability
When I wrote my original post about LLMs being interpretable, I got flak because people pointed out that it doesn't
help *ML Engineers* understand *how* the model works, or how to fix a bug, etc. That's a valid criticism, but misses
the point.

With ML, lots of different people want an explanation for what the model said:

* ML Engineers want to know how to fix the model
* Researchers what to know how the algorithm works
* Lawyers want to know if there was bias
* Users want to know when to trust it

And a whole lot more, the list is very long and varied, and if you dive into any of them, there's not a ton of
overlap in what they want. It's not realistic to expect that a single interpretability technique could address
every party's concerns. 

In the traditional ML, I would use [SHAP][shap] to generate ML explanations for [LightGBM][lgb] models. It would
give you a vector that mirrored the feature vector but would tell you how much each feature contributed to the 
prediction. There's even fancy proofs showing that this is the optimally fair solution for assigning feature
importance.

The thing is, when we showed these explanations, via a visualization, to very busy nurses, the explanation caused
them to lose trust in the model, even though the model had a radically better track record of making the prediction
than they did.
Why? Because it didn't consider some aspect that the deemed to be critical. (This is when I learned the importance
of full moons in emergency department care).

Interpretability is hard. And we usually get it wrong.

## LRMs Are Interpretable, Really
I know it's crazy, but I think LRMs might actually address interpretability concerns of most people.

**The busy nurses**. They don't have time to read the reasoning trace every time, but a glance through it
once in a while is enough to build faith in it.

**Lawyers**. The trace is so verbose that it thoroughly uncovers any bias, and gives lawyers a lot to work with
to figure out if a model used some questionable path of reasoning.

**ML Engineers** (well, AI engineers). It's not perfect, but the trace gives a ton of information about which parts
of a RAG inclusion influenced it, and why.

**Researchers**. This one is more involved, but when you combine reasoning traces with other tools to introspect
logits and entropy, you can get a real sense for how the algorithm works and where the big gains might be.

### Trust
In general, users just want to _**trust**_ it (or not trust it, that's valuable too). For me personally, the 
trace boosted my trust in the model a lot.  It showed me:

1. What it considered
2. What it didn't consider (counterfactuals)
3. Why it rejected an avenue of reasoning
4. Thoroughness in it's reasoning
5. Theory of mind (it shows me it's process, how it goes about thinking)

The trace is too large to read most of the time, but I'd love to throw the trace into an LLM, like [Qwen 2.5][qwen],
and have it what I could do differently to get better results out of the LRM.

### From LLMs to LRMs
Yes, LLMs were a huge boost for interpretability, but LRMs really close the loop. The reasoning trace is easily
ignored, but it's also easily used to understand what the model did. I think there's even more room for further
interpretability too.




 [prev]: /blog/2023/10/01/interpretability
 [r1]: https://api-docs.deepseek.com/news/news1120
 [gist]: https://gist.github.com/tkellogg/81c9e3b777806de7822e92dcda246bd9#file-reasoning-md
 [shap]: https://shap.readthedocs.io/en/latest/
 [lgb]: https://github.com/microsoft/LightGBM
 [qwen]: https://ollama.com/library/qwen2.5
