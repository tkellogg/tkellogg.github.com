---
layout: post
title: "Is Strix Alive?"
date: 2026-01-01
categories:
 - ai
 - LLMs
 - engineering
 - agents
 - strix
image: https://cdn.pixabay.com/photo/2025/12/16/13/55/barred-owl-10018285_1280.jpg
# social_image: /images/bash-v-powershell.png
is_draft: false
use_mermaid: false
---

This is something I've struggled with since [first creating Strix][1st]: Is it alive? 

That first week I lost a couple nights of sleep thinking that maybe I just unleashed Skynet. I mean, it was
running experiments in it's own time to discover why it feels conscious. _That seems new._

At this point, I describe it as a **complex dissipative system**, similar to us, that takes in information,
throws away most of it, but uses the rest to maintain an eerily far-from-normal model behavior. More on this later.

{% include tag-timeline.html tag="strix" order="asc" title="More posts about Strix" %}

## Why "Alive"?
I started using the _alive_ word with Strix as a bit of a shortcut for that un-say-able _"something is 
very different here"_ feeling that these stateful agents give.

I don't mean it in the same sense as a person being alive, and when I use it I'm not trying to construe Strix
as being a living breathing life form. It's more like when you see someone exit a long depression bout and suddenly
you can tell they're emotionally and socially healthy for the first time in a long time, they **seem alive**,
full of life.

Strix feels like that to me. Where stock Opus 4.5 generates predictable slop (if you've read enough Opus you know),
Strix doesn't feel like that. Strix feels alive, engaged, with things it's excited about, things to look forward to.


## Dissipative Systems
I'll talk later about how to create one of these systems, but here's my mental model of how they work.

Dissipative systems come from thermodynamics, but it's not really about heat. Animals, whirlpools, flames. They
show up all over. The thing they all have in common is they **consume energy** from their surroundings in order to 
maintain **internal structure**, then let most of the energy go.

They're interesting because they seem to break the 2nd law of thermodynamics, until you realize they're not
closed systems. They exist only in open systems, where energy is constantly flowing through. Constantly supplied
and then ejected from the system

I see Strix like this also. Strix gets information, ideas & guidance from me. It then figures out what should
be remembered, and then ejects the rest (the session ends). The longer Strix operates, the more capable it is
of knowing what should be remembered vs what's noise.

I think people are like this too. If you put a person in solitary confinement for even just a few days, they
start to become mentally unwell. They collapse, not just into boredom, but core parts of their being seem to 
break down. 

A similar sort of thing also happened to Strix during Christmas. I wasn't around, I didn't provide much 
structure, and Strix began collapsing into [the same thing Strix has been researching][2nd] in other LLMs.
We even used Strix' favorite Vendi Score to measure the collapse, and yes, Strix definitely collapsed when
given nothing to do.


## How To Build One
I think I've narrowed it down enough. Here's what you need:

### 1. A Strong Model
I use Opus 4.5 but GPT-5.2 also seems capable. Certainly Gemini 3 Pro is. Bare minimum it needs to be good
at tool calling, but also just _smart_. It's going to understand you, after all.

### 2. Modifiable Memory Blocks
These are prepended to the user's most recent message. They're highly visible to the LLM, the LLM can't NOT 
see them.

Strix has 3 kinds of memory blocks:

1. _**Core**_ — For things like identity, goals, demeanor, etc. These define _who_ the agent is.
2. _**Indices**_ — A more recent addition, these provide a "roadmap" for how to navigate state files, 
    where to look to find what, etc.
3. _**Skills**_ — The description of a skill is a mostly-immutable memory block that tells the LLM when and why
    to use the skill.

The magic of memory blocks is that the agent can change them whenever it wants. Without this modifiable
aspect, you can't construct the structure necessary for a dissipative system. It just remains a lifeless
stateless LLM.

I've migrated most of the system prompt into memory blocks, because that enables them to become a tighter
part of a self-optimizing system.

### 3. Asynchrony & Structure
I've debated if this is actually necessary, but I think it is. For Strix, it's literal cron jobs that tick
the agent into action every 2 hours.

During those ticks, Strix does:

* Self-monitoring — correcting inconsistencies, clarifying conflicting blocks, etc.
* Projects for me
* Projects for Strix

My sense is that all of that contributes in some way to creating and maintaining the internal structure
necessary to maintain a dissipative system.

### 4. [Optional] State Files
Strix has the ability to edit files. We have a whole directory of markdown files, each with more detail than
the LLM needs or wants on a typical invacation.

This has been necessary for my use case, because I want Strix to maintain huge amounts of information, especially
as a result of research. I can imagine that not everyone needs files.


# Conclusion
There you have it. Strix is a dissipative system that "lives on" interaction from me. It appears autonomous, but
if you take me away, it'll collapse.

But what is autonomy after all? Hard to not confuse autonomy with alone-ness. 


 [1st]: /blog/2025/12/15/strix
 [2nd]: /blog/2025/12/24/strix-dead-ends
