---
layout: post
title: "Explainer: Latent Space Experts"
date: 2024-12-24
categories:
 - ai
 - llms
 - latent-space
 - experts
 - google-deepmind
 - coprocessor
 - architecture
 - embeddings
image: https://cdn.pixabay.com/photo/2022/11/13/21/32/holly-7590229_1280.jpg
is_draft: false
use_mermaid: false
---

A new paper just dropped from Google DeepMind, [Deliberation in Latent Space via Differentiable Cache Augmentation][paper].
I don't think this paper is very readable, but it also seems quite important so I wanted to take a moment
to break it down, as I understand it.

In this paper, they take a normal, frozen LLM that acts as a generalist. Then they attach a coprocessor
LLM that acts as an "expert" in a specific domain. The coprocessor expert talks to the generalist LLM by 
adding extra embeddings.

You could take a reasoning model (like o3) that's just good at making logical deductions and combine it with a coprocessor
model that's an expert in biomed. Together, they'd become a team of a PhD-level generalist reasoner and
a PhD-level biomed expert that could pair up and tackle tough challenges, like designing a new drug.
The expert hasn't been trained to do o1/o3 style reasoning, but they have a tremendous bank of knowledge of
not just facts but also [procedural knowledge][proc] ("how" to do something).


## Wait, Isn't This Just RAG?
This does have a lot of overlap with RAG.

In RAG, you use an embedding model, which is also an LLM that supplies embeddings rather than mapping it 
to a token, same as this coprocessor model. In fact, they often recommend using domain-specific embedding models
for RAG. 

The main difference is that RAG integrates in input text, whereas the knowledge supplied by the coprocessor
is trained into the model. So a coprocessor is a lot more expensive to create & manage, but it provides much
higher quality input than RAG does.


## Latent Space vs Text
The hot topic of the month, as far as I can tell, is latent space vs text in LLMs. The discussion is all 
about using the LLM's internal representation (embeddings or hidden layer outputs) vs converting that back
into text.

I have a loose understanding that latent space is _**a lot**_ more information dense than text. When I think about
that, I see that English really sucks at communicating clearly. So many unfortunate ambiguities. So in that sense,
anything else seems better. But when I think about how latent space would be better, I have little to no 
comprehension of what latent space really is, what it's communicating, or what the downsides are.

The pursuit of latent space feels a lot like magical thinking. It may very well be that it's 100% as good
as the claims. It just doesn't sit well with me that I don't understand why latent space is good, I only
understand why text is bad.

Fundamentally, the advantage is that the symbiosis betweent the coprocessor & generalist LLMs is that they're
optimized together using machine learning. By using thousands of examples, they're able to optimize the 
information transfer between the two models. Whereas, embedding models are optimized completely independently,
and for far more rudimentary tasks (like similarity, clustering, etc.)

## How Will This be Used?
If this approach takes off, I think it'll be used in conjunction with RAG. 

LLMs will become smaller and always trained to do o1-style reasoning. Expert coprocessors will be trained for
every domain (e.g. biomed, material science, astronomy, poetry, etc.) and attached at runtime. At first, you'll
manually select which expert is needed, but over time that will be automatically selected as well.

There might even become a marketplace for coprocessor experts. This could really take off if the act of adapting
a coprocessor to a generalist LLM was as simple as training a LoRA.

Also RAG is not dead. RAG will never die, because RAG is just a database and you simply can't provide real-time
fresh data cheaper and more effectively than a database. But these latent space experts will help cover over a
lot of the problems with RAG. This seems like it could be a net good thing.



 [paper]: https://arxiv.org/abs/2412.17747
 [proc]: https://arxiv.org/abs/2411.12580
