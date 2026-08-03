---
layout: post
title: 'Prompt Walkthrough: Fixing my 3D printer with Codex (and Chutes & Ladders!)'
date: 2026-08-01
categories:
 - ai
 - LLMs
 - engineering
 - agents
image: /images/printer-example/IMG_3589.webp
is_draft: false
use_mermaid: false
---

We need more examples of prompting agents into completing big tasks. I used to think it was easy, you just
type like you're asking a super smart friend. But people keep looking confused, as if it's hard. So, let's just
work through some examples here.

First up, I had some issues with my 3D printer (uh, I fixed it wrong a year ago and now it's haunting me).
I tried using ChatGPT a couple weekends in a row, and finally decided to revert to full Codex.

Here is a prompt I used. It's heavily annotated, I recommend clicking through everything.

> [hey](#greeting), I have this 3d printer. [I'm trying to fix it](#fix1). My brother gave me this printer, it looked new out-of-the-box, but
> [felt like it shipped straight from china. Like all the instructions were in chinese.](#china) He does a ton of business in
> china, so it seems likely that he did indeed buy it from a chinese supplier and it shipped straight from china
> 
> ok, so [the issue I'm trying to solve is the hotend is clogged](#fix2). [I've gone back and forth with chatgpt](#chat1) a while on it.
> I've consolidated a lot of the chat here: chatgpt-transfer.md
> 
> [iPhone HEIC pics here in the root are just the 3d printer from various angles.](#pics)
> 
> ChatGPT suggested buying a new print head. [I looked online and it was like $120, which is 50% of the cost of a whole new printer (the new kind that doesn't have these problems).](#money-banter)
> [I don't want to spend $120, let's keep it under $50.](#constraints) If
> you need me to buy new parts, send me links to reputable buyers. I've added more HEIC pics also of a hotend I bought
> already.
> 
> [I want you to figure out how to fix this. Communicate the fix to me through files. Ideally an interactive HTML file, maybe a react app with Three.js integration for maximum visual utility.](#files)
> 
> [Now, when you write, I understand that it's very tempting to use shorthand. Please don't. Please talk to me like I'm a dumbass bussiness person who just tried plugging the printer power chord into a wifi router.](#dumb) 
> Use visual aids. Make it
> fun and easy to follow. [Raccoons and goblins?](#goblins) Sure. Whatever.
> 
> Also: [this week openai reduced pricing of Luna by 80% and Terra by 20%](#reduce). That means both of these (quite capable models
> imo) are extremely cheap. I have you (Sol) on max effort [because I'm confident your intelligence will be able to wield these resources appropriately.](#wield) 
> This is a chatGPT sub though, so we only have a single 5hr block to compute our way out
> of this. Use it wisely.
> 
> If you have questions, you are welcome to ask me. You're also welcome to install tools, just let me know if you're
> modifying my computer.
{: .prompt}

Click here to open it's first take on the web app (it's really cool!). It made great use of [Three.js][3js].

<a class="embed-app" href="/printer-rescue/" data-title="Finder 3 hotend rescue guide">Open Report</a>

In my head, it mostly feels like I'm just chatting with a super smart friend. But it probably seems complicated,
because I've gotten to know that friend and maybe you haven't.

## Notes {#notes}

### The greeting
{: #greeting .explain-block}
I usually go goofier. I figure I'm talking to some intelligent being and whatever I say at the beginning sets the tone
for the rest of the conversation. Like you would if you were talking to a friend or a coworker. After all, they were 
trained to imitate people, so obviously they'd act like people in this sense.

### Establish expectations
{: #fix1 .explain-block}
It's a good idea to open with some rough idea of what you're asking them for. Advice? Design? Problem solving? Again,
it's like talking to a person. Everything they hear is going to be filtered through that lens.

Now technically, an LLM sees all of your words simultaneously, so it works differently than people. For us, we hear/read
the words one-after-the-other, in slow sequence. I guess that means we don't have to start off like this, but old habits
die hard. A better reason to do it is I sometimes get lost in my thoughts while writing the prompt and forget to ask a 
basic question like, "how to I fix it?". So starting off with this is more just for me, I guess.

### The China context
{: #china .explain-block}
Agents eat context. The problem with being an intelligent entity but not actually having a body, is AIs miss out on
a huge amount of information. So here I'm just trying to lay the foundation for the possibility that my 3D printer isn't
actually a normal stock OOTB device.

I also didn't want to *tell it* that it wasn't normal. If I did that, it might get stuck in that line of reasoning.
By phrasing it this way, I'm giving the agent **permission to doubt**, without instructing it to do so.

### Explain the problem
{: #fix2 .explain-block}
The real issue, explained better. It's important to clearly state the problem. I did an unclear version right at the
start. Really I only need this version.

I don't edit my prompts at all. I just type pretty much stream-of-consciousness, so yeah, duplication happens.

### Context for context
{: #chat1 .explain-block}
Context is super important. Agents eat context, the more you can provide, the more they can do. 

I already went on with ChatGPT for two rounds already, and I didn't want to make the same
mistakes. So I opened up the old conversations and had it summarize (1) just the facts that I provided, and then (2) the
inferences it had made. I kept them separate. I had ChatGPT write it up because I'm lazy and didn't want to type it again.
I told ChatGPT that I was handing off to Codex, so that put it's mindset into a knowledge transfer mode, to get what I
was looking for.

Since I had already gone through the trouble to type it up, this seemed like the most expedient route to reusing that
context.


### Provide pics
{: #pics .explain-block}
I took a pictures from my phone at several angles. Basically every angle I could think of, then moved them over to my 
laptop. On my laptop I had created a directory to dump these files, a work directory.
I didn't do any curation, the LLM can do a fine job of that. It just read all of them anyway. 

This particular problem is extremely visual. Without pictures, the agent knows nothing except for what I say. But,
I'm actually not that knowledgeable in 3D printers, so every time the AI tries to do some experiment, I get highly
annoyed. By including a bunch of pics, I bypass a whole lot of problems.

Later on, we take even more pics, and those prove to be the linchpin evidence needed for a breakthrough.


### Money banter
{: #money-banter .explain-block}
Context is king. Rather than simply telling it how much to spend, I'm intentionally spilling my internal mental state
in regards to spending money. Yes, I'm going to follow up with a constraint, but this is what I'm *really* thinking.

If I simply state the constraint, then I'm worried that it'll get distracted and *try* to spend money. Whereas I
really just want to offer it the possibility of buying new parts.

But also, I'm opening up the possibility of giving up and just buying a new printer. Whatever happens, it now has
the context to reason about what the most reasonable next step is.


### Constraints
{: #constraints .explain-block}
State the constraints clearly.

Agents eat context, of course, but they also excel at staying within absurd constraints. They *love* constraints.
In fact, if you have crazy constraints, you absolutely *should* be using AI to work though it.

More constraints is better, but only if they're hard constraints. If they're flexible, mention where they can flex.

### Communication
{: #files .explain-block}
Establish how I want to be communicated with.

For this, it's highly visual. When I'm looking at the device I often can't figure out what I'm looking at.

**Three.js** — this is something I've recently discovered. It's a game engine, I think, where you can build 3D environments
in the browser. I bet you'd have to be sadistic to sling Three.js code manually, but LLMs can do it all day without
issue. Code is how they interact with the world. Fwiw I love what it came up with.

Throughout this, I often intentionally try to be vague when I don't absolutely need something specific. LLMs are
quite creative and talented, and quite often the thing they come up with is better than whatever I was thinking.


### Anti-shorthand clause
{: #dumb .explain-block}
Ever since Opus 4.7 I've noticed that all LLMs are deviating hard into a dense shorthand that's hard to follow.
They'll invent terms and I'll think I'm just an idiot for not being able to follow. Turns out the language is constantly
changing.

> Please talk to me like I'm a dumbass bussiness person who just tried plugging the printer power chord into a wifi router.

This line makes me laugh. But also it feels like something someone would have said to me when I was young, smart, and
had no idea how to communicate with superiors.


### Racoons and goblins
{: #goblins .explain-block}
Okay, long story. Basically when GPT-5.5 was released, a few days after people realized there was some language in the 
codex system prompt about racoons, goblins and magical creatures. OpenAI [wrote a blog post][goblins] about the incident.
It was something to do with RL reinforcing behaviors.

But I like the goblins & raccoons. I periodically try to coax GPT into being it's true self, because it's fun. But also,
I tend to think an AI will do better work if it's not being constantly hand-slapped, like a human (they're imitating them
after all)

### Reduced pricing
{: #reduce .explain-block}
Rather than just saying "use Luna", I give some details for why it's important to me. The intelligent LLM can reason
through how hard it needs to try to use this model as a subagent.

### Compliments
{: #wield .explain-block}
This is my way of giving the agent permission to use

### Why is autoregression a problem?
{: #autoregress .explain-block}
Autoregression is when the model generates the next token, one token at a time until the output is complete 
(versus diffusion where all tokens are generated simultaneously).

Things have changed more recently, but it used to be that models were trained to believe that everything in the
conversation thus far was *true*. And while it's no longer the case, the beginning of a conversation still sets
the tone, similar to how **first impressions** work with people. Henceforth, you see all through that lens.

So autoregression is a bit _like a **narrowing hallway**_. It's difficult for the LLM to suddenly make a surprising
turn in logic. Everything kind of just follows the status quo.

<div style="margin:1.5rem 0"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 756" width="100%" style="max-width:420px;height:auto;display:block;margin:0 auto" role="img" aria-labelledby="ar-title ar-desc" font-family='-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'>
  <title id="ar-title">Autoregression as a narrowing corridor</title>
  <desc id="ar-desc">A corridor seen from above, wide open at the top and narrowing with every generated token. The tokens of a printer diagnosis sit on a single gold path down the middle: The, extruder, is, clogged, so. At each token the walls step inward, and small crossed-out doors on the ledges mark continuations that are no longer reachable, including one labeled the actual cause. By the last token the corridor is a slot that fits only one likely next token. Backing out means climbing all the way up; a fresh context starts at the top with every door open again.</desc>
  <defs>
    <g id="ar-door">
      <rect x="0" y="0" width="14" height="20" rx="1.5" fill="#f3f4f6" stroke="#666" stroke-width="1.2"/>
      <line x1="1" y1="19" x2="13" y2="1" stroke="#666" stroke-width="1.2"/>
      <circle cx="11" cy="10.5" r="1.2" fill="#666"/>
    </g>
  </defs>
  <text x="200" y="30" text-anchor="middle" font-size="16" font-weight="600" fill="#111827">One token at a time</text>
  <text x="200" y="52" text-anchor="middle" font-size="14" fill="#666">each choice narrows what can follow</text>
  <g opacity="0.9">
    <use href="#ar-door" x="110" y="58"/>
    <text x="132" y="75" font-size="14" fill="#666">= a path no longer reachable</text>
  </g>
  <path d="M30,100 V160 H60 V250 H95 V340 H128 V430 H158 V520 H175 V585 H225 V520 H242 V430 H272 V340 H305 V250 H340 V160 H370 V100 Z" fill="rgba(192,138,0,.13)"/>
  <text x="200" y="124" text-anchor="middle" font-size="14" fill="#666">every continuation open</text>
  <g stroke="#666" stroke-width="1.5" stroke-dasharray="4 3" opacity="0.55">
    <path d="M177,173 L78,226"/>
    <path d="M223,173 L322,226"/>
    <path d="M158,263 L111,316"/>
    <path d="M242,263 L289,316"/>
    <path d="M183,353 L143,406"/>
    <path d="M217,353 L257,406"/>
    <path d="M170,443 L167,496"/>
    <path d="M230,443 L234,496"/>
  </g>
  <g opacity="0.85">
    <use href="#ar-door" x="30" y="140"/>
    <use href="#ar-door" x="46" y="140"/>
    <use href="#ar-door" x="340" y="140"/>
    <use href="#ar-door" x="356" y="140"/>
    <use href="#ar-door" x="62" y="230"/>
    <use href="#ar-door" x="79" y="230"/>
    <use href="#ar-door" x="307" y="230"/>
    <use href="#ar-door" x="324" y="230"/>
    <use href="#ar-door" x="104" y="320"/>
    <use href="#ar-door" x="282" y="320"/>
    <use href="#ar-door" x="136" y="410"/>
    <use href="#ar-door" x="250" y="410"/>
    <use href="#ar-door" x="160" y="500"/>
    <use href="#ar-door" x="227" y="500"/>
  </g>
  <path d="M300,355 L290,343" stroke="#666" stroke-width="1.2" fill="none"/>
  <text x="394" y="367" text-anchor="end" font-size="14" font-style="italic" fill="#666">the actual cause</text>
  <path d="M16,86 L30,100 V160 H60 V250 H95 V340 H128 V430 H158 V520 H175 V585" fill="none" stroke="#111827" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>
  <path d="M384,86 L370,100 V160 H340 V250 H305 V340 H272 V430 H242 V520 H225 V585" fill="none" stroke="#111827" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>
  <path d="M200,134 V608" stroke="#c08a00" stroke-width="3" fill="none"/>
  <polygon points="200,622 193,608 207,608" fill="#c08a00"/>
  <g>
    <rect x="177" y="147" width="46" height="26" rx="8" fill="#fbfaf7" stroke="#c08a00" stroke-width="2.5"/>
    <text x="200" y="165" text-anchor="middle" font-size="14" font-weight="700" fill="#8a6300">The</text>
    <rect x="158" y="237" width="84" height="26" rx="8" fill="#fbfaf7" stroke="#c08a00" stroke-width="2.5"/>
    <text x="200" y="255" text-anchor="middle" font-size="14" font-weight="700" fill="#8a6300">extruder</text>
    <rect x="183" y="327" width="34" height="26" rx="8" fill="#fbfaf7" stroke="#c08a00" stroke-width="2.5"/>
    <text x="200" y="345" text-anchor="middle" font-size="14" font-weight="700" fill="#8a6300">is</text>
    <rect x="162" y="417" width="76" height="26" rx="8" fill="#fbfaf7" stroke="#c08a00" stroke-width="2.5"/>
    <text x="200" y="435" text-anchor="middle" font-size="14" font-weight="700" fill="#8a6300">clogged</text>
    <rect x="177" y="507" width="46" height="26" rx="8" fill="#fbfaf7" stroke="#c08a00" stroke-width="2.5"/>
    <text x="200" y="525" text-anchor="middle" font-size="14" font-weight="700" fill="#8a6300">so&#8230;</text>
  </g>
  <text x="200" y="645" text-anchor="middle" font-size="14" font-weight="600" fill="#111827">only one likely next token</text>
  <text x="200" y="668" text-anchor="middle" font-size="14" fill="#666">Backing out means climbing all the way up.</text>
  <rect x="24" y="684" width="352" height="56" rx="8" fill="rgba(192,138,0,.13)" stroke="#e5e0d3"/>
  <rect x="24" y="690" width="4" height="44" rx="2" fill="#c08a00"/>
  <text x="42" y="707" font-size="14" font-weight="700" fill="#8a6300">A fresh context starts at the top &#8212;</text>
  <text x="42" y="727" font-size="14" fill="#333">every door open again.</text>
</svg></div>

### Intro
{: #intro2 .explain-block}
Intros are important. After all, these agents are autoregressive, so how you open impacts how the conversation
goes from there. If you want something cool, set the vibe.

### Dynamic Workflows
{: #dynwork .explain-block}
This is a Claude Code feature. You have to mention it by name for the harness to allow Claude to use it. I
love it because it enables Claude to string together many subagents in a workflow (actually, just regular code).

Simply mentioning this already makes Claude think in terms of writing code in one workflow, and verifying with
another. By not specifying exactly how I want it done, it lets Claude figure it out. Since I was talking to Fable 5,
I was pretty confident it would be able to schedule out the dynamic workflow. Fable is able to conceive of the
the workflow well.

### Use Opus & Sonnet
{: #useopus .explain-block}
Trying to nudge it into doing more of it's work via cheaper models. Since Fable is constructing the workflow
and writing all the prompts of each of the subagents, I felt confident that Opus/Sonnet would be more than
enough for the individual pieces, as long as Fable is the architect.

### "Chaotically falling"
{: #chaos .explain-block}
Intentional word choice. Any model can rip off a copy of a game easily, but the 3D part with animations is new.
I figure Fable probably used these words as both inspiration for the animations, as well as during verification,
"yup, that's chaotic, done".

### Chutes and ladders
{: #chutes .explain-block}
A classic game.

I'm constantly looking out for words and phrases where 2-3 words expand out to whole essays, if you were to
explain them. It saves typing and conveys a lot of implicit details.

Building a brand new game with totally new concepts takes a lot more prompting and iteration. Here we can simply
invoke it's name and the LLM knows vaguely what we're after.

# Why Codex?
I tried solving this in ChatGPT two times before this. I wanted to try Codex because:

1. The **filesystem** becomes a library. The pictures I add become assets that can be reused for context. I can start a new
   agent or conversation and it has access to the same exact assets.
2. Output goes into files. The conversation context is volatile. It gets randomly compacted (lost), plus the LLM
    ignores parts of the context, it has uneven recall over it. But with files, when they're read, they're always at
    the optimal location in context. And you can always re-read them. This makes them a more effective way to store
    information in long-running sessions.
3. Subagents. I'm not sure if ChatGPT can use subagents, but subagents are enormously useful. See below.

## Subagents
Subagents are like a normal Codex session that the agent can launch off. It's how agents can break down the work.

<div style="margin:1.5rem 0"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 470 430" width="100%" role="img" aria-labelledby="sa-ed-title sa-ed-desc" style="width:100%;max-width:470px;height:auto;display:block" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif">
  <title id="sa-ed-title">One task, three effort tiers: Codex orchestrates two subagents</title>
  <desc id="sa-ed-desc">You talk to Codex through a terminal TUI, a two-way conversation. Codex, running on Sol at high effort, is the orchestrator: it holds the task and delegates the work. It launches a Researcher subagent on Luna at medium effort and a Reviewer subagent on Terra at extra-high effort. On every link, work goes out and results come back. Each agent's effort level is shown as a four-cell meter: two cells for medium, three for high, four for extra-high. The reviewer runs hotter than the orchestrator that spawned it.</desc>
  <text x="10" y="26" font-size="11" font-weight="700" letter-spacing="2.2" fill="#8a6300">SUBAGENTS</text>
  <text x="460" y="26" text-anchor="end" font-size="11" font-weight="600" letter-spacing="1.8" fill="#666">ONE MAIN TASK &#183; TWO SUBTASKS</text>
  <line x1="10" y1="38" x2="460" y2="38" stroke="#e5e7eb" stroke-width="1"/>
  <text x="10" y="72" font-size="19" font-weight="700" fill="#111827">You</text>
  <text x="54" y="72" font-size="11.5" font-style="italic" fill="#666">at the keyboard</text>
  <g stroke="#c08a00" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M16.5 88.5 L22 82 L27.5 88.5"/>
    <line x1="22" y1="87" x2="22" y2="101"/>
    <path d="M16.5 99.5 L22 106 L27.5 99.5"/>
  </g>
  <text x="34" y="98" font-size="11.5" fill="#666"><tspan font-weight="700" letter-spacing="1">TUI</tspan><tspan font-style="italic"> &#8212; a two-way conversation</tspan></text>
  <text x="10" y="124" font-size="11" font-weight="700" letter-spacing="2.2" fill="#8a6300">ORCHESTRATOR</text>
  <text x="10" y="152" font-size="32" font-weight="800" fill="#111827">Codex</text>
  <text x="126" y="152" font-size="13" font-weight="700" letter-spacing="1.8" fill="#8a6300">ON SOL</text>
  <text x="460" y="152" text-anchor="end" font-size="16" font-weight="800" fill="#111827">HIGH</text>
  <g>
    <rect x="376" y="158" width="18" height="10" rx="2" fill="#c08a00" fill-opacity="0.8"/>
    <rect x="398" y="158" width="18" height="10" rx="2" fill="#c08a00" fill-opacity="0.8"/>
    <rect x="420" y="158" width="18" height="10" rx="2" fill="#c08a00" fill-opacity="0.8"/>
    <rect x="442" y="158" width="18" height="10" rx="2" fill="#f5f5f5" stroke="#e5e7eb" stroke-width="1"/>
  </g>
  <text x="418" y="182" text-anchor="middle" font-size="9.5" letter-spacing="1.5" fill="#666">EFFORT</text>
  <text x="10" y="176" font-size="13" fill="#666">holds the task, delegates the work</text>
  <line x1="22" y1="188" x2="22" y2="316" stroke="#c08a00" stroke-opacity="0.5" stroke-width="2"/>
  <text x="34" y="210" font-size="11.5" font-style="italic" fill="#666">work goes out &#8212; results come back</text>
  <g stroke="#c08a00" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <line x1="24" y1="238" x2="80" y2="238"/>
    <path d="M35 232.5 L28 238 L35 243.5"/>
    <path d="M77 232.5 L84 238 L77 243.5"/>
  </g>
  <text x="96" y="244" font-size="22" font-weight="700" fill="#111827">Researcher</text>
  <text x="240" y="244" font-size="13" font-weight="700" letter-spacing="1.8" fill="#8a6300">ON LUNA</text>
  <text x="460" y="244" text-anchor="end" font-size="13" font-weight="600" fill="#666">MED</text>
  <g>
    <rect x="376" y="250" width="18" height="10" rx="2" fill="#c08a00" fill-opacity="0.6"/>
    <rect x="398" y="250" width="18" height="10" rx="2" fill="#c08a00" fill-opacity="0.6"/>
    <rect x="420" y="250" width="18" height="10" rx="2" fill="#f5f5f5" stroke="#e5e7eb" stroke-width="1"/>
    <rect x="442" y="250" width="18" height="10" rx="2" fill="#f5f5f5" stroke="#e5e7eb" stroke-width="1"/>
  </g>
  <text x="96" y="268" font-size="13" fill="#666">digs through the problem, reports findings</text>
  <g stroke="#c08a00" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <line x1="24" y1="316" x2="80" y2="316"/>
    <path d="M35 310.5 L28 316 L35 321.5"/>
    <path d="M77 310.5 L84 316 L77 321.5"/>
  </g>
  <text x="96" y="322" font-size="24" font-weight="800" fill="#111827">Reviewer</text>
  <text x="222" y="322" font-size="13" font-weight="700" letter-spacing="1.8" fill="#8a6300">ON TERRA</text>
  <text x="460" y="322" text-anchor="end" font-size="20" font-weight="800" fill="#111827">XHIGH<tspan dy="-7" font-size="12" font-weight="700">&#8224;</tspan></text>
  <rect x="371" y="323" width="94" height="20" rx="5" fill="#c08a00" fill-opacity="0.13"/>
  <g>
    <rect x="376" y="328" width="18" height="10" rx="2" fill="#c08a00"/>
    <rect x="398" y="328" width="18" height="10" rx="2" fill="#c08a00"/>
    <rect x="420" y="328" width="18" height="10" rx="2" fill="#c08a00"/>
    <rect x="442" y="328" width="18" height="10" rx="2" fill="#c08a00"/>
  </g>
  <text x="96" y="346" font-size="13" fill="#666">scrutinizes the result before it ships</text>
  <line x1="10" y1="372" x2="460" y2="372" stroke="#e5e7eb" stroke-width="1"/>
  <text x="10" y="394" font-size="13" font-style="italic" fill="#666">&#8224; The reviewer runs hotter than the orchestrator that spawned it.</text>
  <text x="10" y="416" font-size="12.5" font-weight="700" letter-spacing="0.4" fill="#8a6300">Match the model &#8212; and the effort &#8212; to the job.</text>
</svg></div>

Another way to think about it is a single agent has **tunnel vision**. It has a hard time thinking beyond
what's top of mind. Whereas each subagent is a different agent with a different tunnel vision.

That's why it works so well to have one agent write code and another to check/verify it. If they don't share
any conversation, then the verifier is truly looking at it through fresh eyes.

Tunnel vision is a big problem for [autoregressive models (how LLMs work)](#autoregress).
But here you can see that we can wield that same weakness as a rather strong asset.
The verification subagents work well *because* they **share no context**. They can legitimately look at the problem
as if they'd never seen it before.

Wouldn't it be great, as humans, to be able to fork yourself and look at a problem as if you'd never seen it 
before? I think it would be quite useful.

# Skills
I have a skill setup, both at work and at home, at `~/.codex/skills/working-with-tim`

<a class="embed-app" href="/skills/working-with-tim/" data-title="working-with-tim — the skill">Read the skill</a>

The purpose is to clarify my expectations for agents. I like agents to work autonomously. I expect that when
they say the work is done, it's actually done. I expect them to check their work.

Admittedly, this skill leads to slow response times. e.g. on the printer, it took about 2 hours. But there were
no dumb tangents or circles, all the questions were good. At work, I usually get agents to work for 30+ minutes,
sometimes as much as 8-10 hours. And when the work comes back, it's done correctly.a

I like that, it's how I work. So I setup a skill for it.

I don't use `AGENTS.md` anymore, because it doesn't trust the agent to know when to read it. The harness just
shoves it into the context randomly (in the eyes of the agent).

# Conclusion
I'd love to say a lot more about how I think about these things, like model choices and Claude Code vs Codex. But
ultimately, it's just like chatting with a friend. Only, you just have to get to know the friend first.

Get to know what their good at vs not. How their brain thinks about problems. It takes time, but mostly that time
is pure fun and tinkering.


# Bonus: Chutes & Ladders
As a bonus, here's another one. My kids were playing Chutes and Ladders (the board game), so I had Claude Code 
turn it into a video game.

> [yo, let's go big](#intro2). I want to make a Three.js based [Chutes and ladders](#chutes) game with real animations. Just the regular
> chutes and ladders game. When a player moves, it's a real animation in 3D third person view of them climbing up some
> ladder or [chaotically falling down a slide](#chaos). Each animation is different. Also animations for each movement.
>
> For working, use [dynamic workflows](#dynwork). Try to [make heavy use of Opus 5 and Sonnet 5](#useopus). But specify it clearly for them.
> Use clean Fable 5 sub agent to validate.
{: .prompt}

<a class="embed-app" href="/chutes-ladders/" data-title="Chutes &amp; Ladders Mountain">Play the Game Here!</a>


[goblins]: https://openai.com/index/where-the-goblins-came-from/
[3js]: https://threejs.org/
