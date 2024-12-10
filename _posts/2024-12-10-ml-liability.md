---
layout: post
title: "Is ML Experience A Liability For AI Engineering?"
date: 2024-12-10
categories:
 - ai
 - LLMs
 - engineering
image: https://cdn.pixabay.com/photo/2014/09/22/10/22/leap-456100_1280.jpg
is_draft: false
use_mermaid: false
---

[Yesterday I posted here][here] about becoming an AI Engineer and made a statement that _prior ML experience 
is often a liability_ for transitioning into AI engineering. That turned out to be quite the hot take! In this 
post I'll incorporate feedback and try
to expand that into a more balanced take. I'll expand on the perspective of it being an asset, as well as where 
it's a liability.

First of all, the responses were very polarized, either enthusiastic agreement or disagreement (no in between, 
so you know it was extra spicy). That seems like a strong indicator that it's a difference between archetypes.

My hunch is that those who disagreed with my statement tend to align with the "researcher" archetype.

* Data pipeline archetype — *"the data is most important, improve the data/indexes/storage/etc."*
* UX archetype — *"the user & AI collaborate to create intelligence, improve the fluency that they can collaborate"*
* **Researcher archetype — _"the model/algorithms are most important, improve the model"_**

The researcher arechetype is probably poorly named, although I'm not sure what a better name is. They're 
model-centric.


## Why it's a liability

I originally formed that opinion back in 2022 about a week or two after trying to build on top of 
LLMs for the first time. I was talking to a data scientist (who I'm close with both
personally and professionally) about how to incorporate LLMs. I recall there being a ton of friction
in those initial conversations, which led me to state something overly dramatic like, "I think data science 
is going to be dead post-LLM".

Since then, I've had a lot of people independently validate that opinion. One take I've heard went
something like this:

> ML people think their job is to produce a model, whereas (pure) engineering folk 
> do not, which leads engineers to view fine-tuning as an optimization that's often premature.

I've also used the argument that ML folk view Occam's Razor to mean that they should produce the
simplest (smallest) possible model first and increase the model complexity as needed, whereas
engineers tend think Occam's Razor means they should start with the approach that's most likely
to work easily (the biggest, baddest LLM available) and work downward toward more efficient models
to optimize costs.

I've talked to hiring managers who explicitly seek "Please No ML Experience". In their words, they've
seen ML people push their org into spending tens or hundreds of thousands of dollars fine tuning models.
Those projects fail at an unfortunately high rate and deliver slowly. Whereas simply 
prompting better will often get you close enough to launch (and therefore mitigate project risk).


## Why it's an asset
Rahul Dave [posted on Bluesky][rahul] that it's sometimes difficult to know _**when**_ you need to
fine tune, and he found that his prior ML experience was critical in identifying that situation.

That's a very good point. Organizationally, the act of identifying that a threshold has been crossed
is very difficult. Historically in my engineering experience it'll show up as 

> We built component _X_
> to solve problem _Y_. But 3 months ago problem _Y_ disappeared due to a change in management/customers/business
> and now component _X_ only causes people friction. We're stuck with it forever because nobody
> realized that the original problem it solved is now gone.

One of the big ways a [staff+ engineer][sp] contributes is to identify and explain change. With LLM apps, it often takes
ML intuition to be able to correctly identify the situation where performance isn't good enough (and therefore
a huge architectural change is needed).

[Vicki Boykis took another tack][vicky], arguing that the non-determinism of LLMs is unfamiliar to 
software engineers:

> I think software engineering in general favors things like: unit tests where you get 
> the same input and same output, a `for` loop `n` times will only loop through `n` times, type 
> checking (in most languages 😅) confer correctness etc. LLMs are none of that, and 
> lossy compression to boot.

Her experience is that, for this reason, ML people have an easier time transitioning into AI engineering.
I personally think some engineers, e.g. distributed systems background, are already adept at dealing with 
non-determinism, so this isn't much of a hurdle for them. But she's correct, this is a huge hurdle for
a lot of engineers. If you're a hiring manager, you should probably **address non-determinism in the interview**.

## Conclusion
If you have too much ML experience, your organization will definitely fine tune models and it will cost a lot
of money. If you have too little, you won't fine tune any models and you'll be leaving performance
on the table.

Fine tuning historically has a much riskier track record, which leads a lot of people to recommend against
fine tuning. However, it might be wise to include a staff+ engineer with ML experience on your team so they
can identify when your team needs to transition into the researcher archetype.


 [here]: /blog/2024/12/09/ai-engineer
 [rahul]: https://bsky.app/profile/rahuldave.bsky.social/post/3lcxhsyltek2w
 [vicky]: https://bsky.app/profile/vickiboykis.com/post/3lcw4bl4ej22n
 [sp]: https://leaddev.com/career-development/what-do-we-mean-staff
