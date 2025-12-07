---
layout: post
title: "Agents Need Responsibility"
date: 2025-05-25
categories:
 - ai
 - LLMs
 - agents
 - engineering
image: https://cdn.pixabay.com/photo/2022/01/14/04/11/laptop-6936428_1280.jpg
# social_image: /images/bash-v-powershell.png
is_draft: false
use_mermaid: false
---

Someone must take responsibility, **always**. AI agents are no different, yet we're seeing seeing agents
hit the market where nothing is taking responsibility for their actions. These won't work, they're
simply bubbles waiting to be popped. And there is a better way.

The Github Copilot agent [launched last week][ghcp] solves this by clearly stating both:

1. The agent that performed the work
2. The human that verified the work ("On Behalf Of")

This is the way.

![screenshot showing Copilot started work on behalf of soapoperadiva](/images/ai-responsibility/gh-copilot-assignment.png)

Historically in automation, the software development team **took ownership**. When things broke, you
could dial up the team lead or product manager, complain, and things get fixed. 

In organizations of people, there must always be someone to talk to or some way to resolve problems. 
Anything else is insanity. It would be out of control.

In traditional software, the solutions being automated were narrow. The developer understood the problem 
being solved as well as what went wrong. They could do something about it because they could understand
the nature.

Agents are different. They're general solutions. They're only specialized insofar as they use a
special set of tools. The entire point of having an agent is that you don't need to explicitly
"program" it. The implication is that users are going to dream up far more use cases than the development
team could ever have planned for. 

As a result, the development team often doesn't have enough context to proactively monitor for problems.
They don't know what they're looking for, and even if they did, the data is too unstructured to effectively
spot misbehavior.

It's already been a problem with GenAI. There's stories [of lawyers][law] using ChatGPT to submit court 
filings with hallucinated case law.

Your reaction to those stories is critical. If you blame the lawyer, then it sends a message to all lawyers 
to either learn how to spot hallucinations or stop using AI in that context. If you blame AI, then nobody
can ever use AI in any context.

There is no third option. You can't blame nobody and ignore the issue. 


 [ghcp]: https://github.com/features/copilot
 [law]: https://www.reuters.com/technology/artificial-intelligence/ai-hallucinations-court-papers-spell-trouble-lawyers-2025-02-18/
