---
layout: post
title: "The Levels of Agentic Coding"
date: 2026-01-20
categories:
 - ai
 - LLMs
 - engineering
 - agents
image: https://cdn.pixabay.com/photo/2024/05/03/17/17/jazz-bar-8737486_1280.jpg
# social_image: /images/bash-v-powershell.png
is_draft: false
use_mermaid: true
---

Are you good at agentic coding? How do you even **evaluate that?** How do you get better? Let's approach this though
the Viable System Model (VSM) from cybernetics. Previously I showed how the 
[VSM can be used to build agents][agents]. 

Stafford Beer proposed the VSM [in 1971][bof] as a way to view (people) organizations through the lens of cybernetics.
One insight is that viable systems are **hierarchical and composable**. You are a viable system, so is
your team, as well as your company, etc.

When you use a coding agent, the combination of **you and your agent** form a _viable system_. If you want
to leverage AI more, that means handing over more control to the coding agent without destabilizing the team.

The VSM does this for you. It gives you a guide for knowing what systems to build and interventions to put in
place in order to **progressively** hand more control over to the AI safely.

# The VSM
These systems have numbers, but they're not entirely ordered. Treat the numbers like names.

## System 1: Operations
Getting stuff done.

**Before S1:** 
* No agent. You write code by hand in your favorite text editor. _**You were a viable system**_, on 
you're own without any agent involvement.

**After S1:** 
* Using a coding agent to write most or all of the code.

Most agentic coding tutorials will get you this far.

## System 2: Coordination
How does the system avoid tripping itself up?

**Before S2:** 
* Agent writes code that it later can't navigate
* Agent changes files that conflict with other people on your team (inhibits you from participating in the S1 of a larger viable system, **your team**).
* Agent adds dependencies that your company can't use for legal reasons (inhibits you from participating in the S1 of a larger viable system, **your company**).

**After S2:**
* Agent can make changes in a large project over many months and years without stepping over itself.

If your agent needs to be manually reminded to use good coding practices, or to handle certain modules
differently, then you're still **operating S2 yourself**. Once the agent can do it autonomously, without reminder,
then you progress to S3.

Today's tools for getting to S2 include `AGENTS.md`, skills, Git, tests, type systems, linters, and 
[formal methods][fm]. It also involves a fair amount of skill, but as the tools improve it involves
less skill.

## System 3: Resource Allocation
Where do compute/time resources go? What projects/tasks get done?

**Before S3:** You prompt the agent and it does a task.

**After S3:** The agent pulls task from a backlog, correctly prioritizing work.

To get to this point you need a fully functioning System 2 but also an established set of values (System 5)
that the agent uses to prioritize. You also need some level of monitoring (System 4) to understand what issues
are burning and are highest priority.

## System 4: World Scanning
Reading the world around the agent to understand if it's fulfilling it's purpose (or signal where it's not).

**Before S4:** Agent prioritizes work well, but customer's biggest issues are ignored.

**After S4:** The system is self-sustained and well-balanced.

On a simple level, ask yourself, _"how do I know if I'm doing my job well?"_ That's what you need to do to get a 
functioning S4. e.g. If you logged into production and realized the app was down, you'd have a strong signal that
you're not doing your job well.

The obvious S4 tool is ops monitoring & observability. But also channels to customers & stakeholders. Being
able to react to incidents without over-reacting involves well-functioning S3 & S5. Generally, attaching the
agent to the company Slack/Teams seems like an easy win.

## System 5: Policy
The agent's purpose, values, operating rules and working agreements.

Unlike the other systems, S5 isn't easily separable. You can't even build a functioning S2 without at least some
S5 work. Same with S3 & S4.

I've found that, in building agents, you should have a set of values that are in tension with each other.
Resolvable with logic, but maybe not clearly resolvable. e.g. "think big" and "deliver quickly".


## What Comes Next?
Congrats! If you have a coding agent can operate itself, implementing all S1-S5, the next step is to make a 
team of 2-5 agents and start over at S2 with the team, a higher level viable system.

# Algedonic Signals
Pain/Pleasure type signals that let you skip straight from S1 to S5.

Sprint retrospectives in agile teams are a form of algedonic signal. They highlight things that are going
well or not so that the team can change it's _Policy_ (S5), which often involves changing S3-S4 as well.

An algedonic signal in coding agents might be an async process that looks through the entire code base for
risky code. Or scans through ops dashboards looking for missed incidents.
Algedonic signals can be a huge stabilizing force. But, they can also be a huge distraction if used wrong.
Treat with care.

## POSIWID (the Purpose Of a System is What It Does)
It's a great mantra. POSIWID is
a tool for understanding where you currently are. Not where you're meant to be, it's just what you
**are today**. But if you can clearly see what you are today, and you have the foresight to clearly articulate
where you need to be, then it's pretty easy to adjust your S5 Policy to get there.

# How To Interview
Let's say you're hiring engineers to work on a team. You **want your team** to be highly leveraged with AI,
so your next hire is going to really know what they're doing. You have an interview where the candidate
must use agentic coding tools to do a small project.

_How do you evaluate how they did?_

I argue that if you penalize candidates for using AI too much, that leads to all sorts of circular
logic. **You want AI, but you don't**. So that leaves the candidate with a bit of a gamble. However much
they end up using AI is a pure risk, some shops will appreciate and others will judge them for it.

Instead, break out the VSM. Which systems did the use? (Intentionally or not). Did define values &
expectations in their initial prompt? Did they add tests? Did they give it a playwright MCP server so
it could see it's own work? (especially if they can articulate why it's important). Did they think,
mid-session, about how well the session is progressing? (algedonic signals)

The VSM gives us all a principled way of thinking about AI & teams. It's a good way to hire too.


# Conclusion
Viable systems are recursive. Once you start seeing patterns that work with coding agents, there may be
an analog pattern that works with teams. Or if your company does something really cool, maybe there's
a way to elicit the same effect in a coding agent.

It's systems all the way down.


 [agents]: _posts/2026-01-09-viable-systems.md
 [fm]: https://martin.kleppmann.com/2025/12/08/ai-formal-verification.html
 [bof]: https://ia902300.us.archive.org/25/items/brain-of-the-firm-reclaimed-v-1/Brain%20of%20the%20Firm%20-%20Stafford%20Beer.pdf
