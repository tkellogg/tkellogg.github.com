---
layout: post
title: "Software Engineering"
date: 2025-06-21
categories:
 - ai
 - LLMs
 - agents
 - engineering
image: https://cdn.pixabay.com/photo/2022/04/08/11/48/fern-7119343_1280.jpg
# social_image: /images/bash-v-powershell.png
is_draft: false
use_mermaid: false
---

Earlier I got caught in an online debate about the topic of the year: can AI do 
the work of a software engineer?

It led to statements like, "Dropbox is not complex", and more. I think a lot
of this can be cleared up fast with a short discussion on what Software Engineering
actually is, and what we do.

Quick baseline: I've been a software engineer for about 18 years doing a very broad
range of work. Startups, big tech, non-profits, stale corporations. Web dev, QA, backend,
distributed systems, AR/VR, and now AI. I've done a lot.

# Complexity
That sums it up. Almost everything software engineers do has to do with managing 
**complexity** one way or another.

You'd be forgiven for thinking it was about code. It's not. But there's lots of professions
that **aren't** software engineers but write lots of code. Off the top of my head, I've worked 
with game artists, linguists, and data scientists; all of which
wrote a lot of code but couldn't pass for a software engineer.

The biggest **lie** about complexity is rarely spoken: _that it's one thing._

Lots of conversations go in circles because each person is thinking different things in
regards to complexity:

* Difficult algorithms
* Algorithms with high runtime complexity
* Spaghetti code
* No comments
* Too many comments
* Fully-automated build process
* No automation
* Unfamiliar programming language
* Unfamiliar tools
* Unfamiliar libraries
* New naming scheme
* New code style

A lot of these are contradictory. 

My dad worked on forklift truck drive systems. He used only C and never `malloc()` (stack 
& global allocations only). One time a new engineer used `malloc()` and he was upset 
because it was complex — it made it **difficult to reason** about timings.

_(The runtime complexity of `malloc` depends on how much memory is being used. Realtime
systems like drive controllers rely on strict deadlines, otherwise things quickly fall
apart and fail. Every time code executes, it has a fixed time it has to finish. Late
is an error. They wouldn't ever use algorithms that didn't have a constant run time 
complexity.)_

If you wrote a web app like my dad writes embedded C, that would generally be considered 
**too complex**. _Simple in one context, complex in another._


## Moving Complexity Around
A lot of times, good software engineering involves **adding** complexity.

A CI/CD pipeline is definitely more complex than not having one. But it's often the first
thing we add, because without it, managing changes between members of a team gets to be
complex, and it's hard to track deployments.

Microservices are for scaling. They help you decouple teams so they can each move at
their own pace without coordination. Microservices add complexity so you can scale up
to larger **team sizes**.

We end up adding complexity in one place in order to lower it somewhere else. To make
the business run more smoothly.


## AI And Complexity
_"AI can't handle complex code"_

Statements like this make my head spin. Where to start...

First of all, if such a statement makes sense for you, that's a problem with your code base.
It's too complex. I guarantee you that you also have trouble onboarding engineers.

Armin Ronacher recently wrote a post titled [Agentic Coding Recommendations][armin] where
he described making some fairly wild changes to be more productive with AI coding tools.
For example, he started using Go (he's well-known for Python & Rust) because he thinks
it works better with LLMs. 

Major changes like programming choice might feel like excessive complexity. But what if it
makes the difference between AI trashing your code base vs 5x productivity boost? If so,
it's just moving complexity around.


# Are We Still Engineers?
If we stop writing code, do we also stop being engineers?



 [armin]: https://lucumr.pocoo.org/2025/6/12/agentic-coding/
