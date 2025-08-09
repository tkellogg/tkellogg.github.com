---
layout: post
title: "Do LLMs understand?"
date: 2025-07-18
categories:
 - ai
 - llms
 - engineering
 - philosophy
 - cognition
 - understanding
 - sycophancy
 - embeddings
image: https://cdn.pixabay.com/photo/2025/04/15/05/45/heat-9534673_1280.jpg
# social_image: /images/bash-v-powershell.png
is_draft: false
use_mermaid: true
summary: |
    What does "understand" mean? I didn't know, so I did a bunch of research and this is what I got.
    Spoiler: LLMs do understand things, afaict.
---

I've avoided this question because I'm not sure we understand what "understanding" is. Today I spent
a bit of time, and I think I have a fairly succinct **definition**:

> An entity can understand if it builds a **latent model** of reality. And:
>
> 1. **Can Learn:** When presented with new information, the latent model grows more than the information presented,
>    because it's able to make connections with parts of it's existing model.
> 2. **Can Deviate:** When things don't go according to plan, it can use it's model to find an innovative solution
>    that it didn't already know, based on it's latent model.
> 
> Further, the quality of the latent model can be measured by how **coherent** it is. Meaning that,
> if you probe it in two mostly unrelated areas, it'll give answers that are logically consistent
> with the latent model.

I think there's plenty of evidence that LLMs are currently doing all of this.

But first..

### Latent Model
**Mental model**. That's all I mean. Just trying to avoid anthropomorphizing more than necessary.

This is the most widely accepted part of this. *Latent* just means that you can't directly observe 
it. *Model* just means that it's a system of approximating the real world.

For example, if you saw this:

<img src="/images/understanding-ball.png" style="max-width: 20rem" alt="a dotted 3‑D sphere—the discrete points line up to read unmistakably as a ball while keeping that airy, voxel‑like feel. Let me know if you’d like tweaks!"/>


You probably identify it immediately as a sphere even though it's just a bunch of dots.

A *latent model* is the same thing, just less observable. Like you might hold **a "map"** of your city
in your head. So if you're driving around and a street gets shut down, you're not lost, you just
refer to your *latent model* of your city and plan a detour. 
But it's not exactly a literal image like Google maps. It's just a mental model, a latent model.

### Sycophancy causes incoherence
From 1979 to 2003, Saddam Hussein surrounded himself with hand‑picked yes‑men who, under fear of 
death, fed him only flattering propaganda and concealed dire military or economic realities. 
This closed **echo chamber** drove disastrous miscalculations—most notably the 1990 invasion of Kuwait 
and his 2003 standoff with the U.S.—that ended in his regime’s collapse and his own execution.

Just like with Saddam, sycophancy causes the LLM to diverge from it's true latent model, which
causes incoherence. And so, the amount of **understanding decreases**.

### Embedding models demonstrate latent models
Otherwise they wouldn't work.

The word2vec paper [famously showed][queen] that the embedding of "king - man + woman" is 
close to the embedding for "queen" (in embedding space). In other words, embeddings **model the 
meaning** of the text.

That was in 2015, before LLMs. It wasn't even that good then, and the fidelity of that latent 
model has dramatically increased with the scale of the model.


### In-context learning (ICL) demonstrates they can learn
ICL is when you can teach a model new tricks at runtime simply by offering examples in the prompt,
or by telling it new information.

In the [GPT-3 paper][gpt3] they showed that ICL improved **as they scaled** the model up from 125M to
175B. When the LLM size increases, it can hold a larger and more complex *latent model* of the world.
When presented with new information (ICL), the larger model is more capable of acting correctly on
it.

Makes sense. The smarter you get, the easier it is to get smarter.

### Reasoning guides deviation
When models do Chain of Thought (CoT), they second guess themselves, which probes it's own internal
latent model more deeply. In (2), we said that true understanding requires that the LLM can use it's 
own latent model of the world to find innovative solutions to unplanned circumstances.

A recent [Jan-2025 paper][2025] shows that this is the case.

# Misdirection: Performance != Competance
A large segment of the AI-critical use this argument as evidence. [Paraphrasing:][anti]

> Today’s image-recognition networks can label a photo as “a baby with a stuffed toy,” but the 
> algorithm has no concept of a baby as a living being – it doesn’t **truly know** the baby’s shape, 
> or how that baby interacts with the world.

This was in 2015 so the example seems basic, but the principle is still being applied in 2025.

The example is used to argue that AI isn't understanding, but it merely **cherry-picks** a single
place where the AI's *latent model* of the world is inconsistent with reality.

I can cherry pick examples all day long of human's mental model **diverging** from reality. Like you
take the wrong turn down a street and it takes you across town. Or you thought the charasmatic 
candidate would do good things for you. On and on.

Go the other way, prove that there are areas where AI's *latent model* **matches** reality.

But that's dissatisfying, because [dolphins have a mental model of the sea floor][dolph], and tiny
ML models have areas where they do well, and generally **most** animals have some aspect of the world
that they understand.


# Conclusion
Why are we arguing this? I'm not sure, it comes up a lot. I think a large part of it is human 
exceptionalism. We're really smart, so there must be something different about us. We're not just
animals.

But more generally, AI really is getting smart, to a point that starts to feel more uncomfortable as
it intensifies. We have to do something with that.




 [queen]: https://arxiv.org/abs/1509.01692
 [gpt3]: https://arxiv.org/abs/2005.14165
 [2025]: https://arxiv.org/abs/2506.17088
 [anti]: https://www.edge.org/response-detail/26057#:~:text=The%20learning%20algorithm%20knows%20there,patch%20of%20image%2C%20and%20another
 [dolph]: https://en.wikipedia.org/wiki/Cetacean_intelligence
