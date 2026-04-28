---
layout: post
title: "Agent Memory Patterns"
date: 2026-04-27
categories:
 - ai
 - LLMs
 - engineering
 - agents
image: https://upload.wikimedia.org/wikipedia/commons/5/5d/Inside_a_card_catalog_at_the_Indiana_State_Library_-_ask_the_librarian.jpg
is_draft: false
use_mermaid: false
summary: "A short HOW TO guide for agent memory systems. Especially the difference between blocks, files and skills."
---

Say you get asked to "add memory" to an agent. What does that mean? How do you do it? 

There's three common kinds of mutable memory:

1. Files
2. [Memory blocks][letta]
3. [Skills][skills]

If you don't need the agent **to learn**, then you're looking in the wrong place. You don't need memory.
But this post might also be useful if you're just using agents, like a coding agent.


## Files are for data & knowledge
Everything in this post needs to satisfy the following functions:

1. **Explore** to find items — `ls`, `find`, `grep`, or equivalent tools
2. **Read** an item — `cat`, or some ReadFile tool
3. **Write** an item — pipe, `sed`, or some WriteFile tool

For files, all that seems fairly obvious. Files can be complicated, but those are the parts that are
important for files to work as agent memory.
Files don't have to be literal files. If they are, you can provide a `Bash` tool (or `Powershell`) that
gives you cool Linux utilities for navigating the filesystem, reading parts of files, etc. 

But also, you can absolutely use database records or S3 blobs. As long as:

1. Each file has a **hierarchical path**, to enable exploring, but also so that files are a key-value store
2. **Long text** content. We don't care too much about file structure or validation, but please do give the
  agent space to work.


## Memory blocks are a learnable system prompt
Memory blocks are just a flat key-value store. Except the key isn't used for looking things up, it's just
used for writing. All memory blocks are **included inline** in the system prompt, or user prompt.

Where to put it?

* **System prompt** — this one's easier in a lot of systems. But can cause [cache invalidation][cache] (higher token cost)
  when the agent calls WriteBlock.
* **User prompt** (prepend) — This also works, it's still highly visible to the LLM, and it causes less prompt cache 
  invalidation issues.

Either is fine. User prompt is slightly better, I guess.

Required tools:

* `WriteBlock(key, value [, sort_order])` — I like including a sort_order, because we know order does matter,
  so let the agent control it too. Not a huge deal though.

Optional tools:

* `ListBlocks()`
* `ReadBlock(key)`

Theoretically you don't need these because they're in the prompt already, but I've noticed that coding agents
will always try to insert them and agent agents will always call them, every time. So, whatever that means..

### What goes into blocks?
Blocks are a learnable system prompt. Put stuff in there that tends to go into the system prompt — behavior,
preferences, identity, character, etc.

Since it's in the prompt, the agent can't look away or ignore. So you may want to promote from file to block
if you want to **guarantee visibility**, like you don't want to risk the agent forgetting to read a file.


## Skills are indexed files
Skills are a combination of files & memory blocks. They're files, literally, but they also are represented in 
the system prompt.

It's just a directory with a `SKILL.md` file:

```
the-skill/
  SKILL.md
  important-concept-1.md
  helper-script.py
  worksheet.csv
```

The `SKILL.md` is generally just a plain markdown file, but it has a special top few lines at the start of the file:

```
---
name: the-skill
description: what it does and when to use it
---
```

The `description` is the critial part. Both `name` and `description` go into the system prompt, but the 
`description` is the trigger. It encourages the agent to use the skill in the right circumstance.

### Do you need a Skill tool?
Not really. [Claude Code][cc] has a `Skill(name)` tool, but functionally it's the same as the agent
reading `the-skill/SKILL.md` with a regular Read tool. The benefits are harness-side: lazy-loading
the SKILL.md content (so it only enters the context window when invoked), telemetry, and permission
scoping.

If you skip the dedicated tool, just tell the agent in the system prompt: _"When a skill matches,
read its SKILL.md before doing the thing."_ Works fine.

### What goes into skills?
Data or instructions that are only needed in certain circumstances. Honestly "skill" is actually a really 
good name for them.

The key phrase is **progressive disclosure** — skills unfold as needed. The agent reads files as it deems
necessary. Typically you'll include file references in the `SKILL.md` file, like _"Read important-concept-1.md
when you need to..."_. There's nothing special, no notation, it's just hints for the agent.

Scripts and data are nice too. Obviously scripts are only useful if you enable a Bash tool, but scripts especially
can act like a **agent optimizer**. Like, sure, the agent can probably figure out how to string together all the
headers to authenticate to your weird API, or you can just make a script for it and skip the LLM.

### Editable skills
Most people think of skills as being immutable programs of English. Sure, they're useful when used like that,
but they're even more useful when you allow your agent to change them.

A great way to use skills is as an **experience cache**. At the end of a long investigation or research, have the
agent record the experience in a skill. Next time, it just reads the skill!
Could you use files for this? Yes, but the `description` field in the system prompt makes it more likely to be 
used at the right time.


## Observability
How do you know when the agent is using memory well?

For files & skills, you can start at the entry point and construct a graph of which files reference which other
files:

1. For each file
2. Search for the file name
3. Pair "file referenced from" -> file

Then compare against reality. Find all the times those files were accessed in that order versus not. If they're
referenced randomly, that means the agent needs to use Search or ListFiles tools to navigate. That might mean
your files or skills are becoming too unwieldy.

Also, you should monitor memory block size & count. Definitely keep them under 5000, probably under 500 characters.
When the blocks get too big, they tend to confuse the agent.

Unfortunately, given the nature of agents, there's not that much you can do for observability. But these two 
things do tend to be useful to monitor.


## Search index
Is a search index a good idea? Yes absolutely. It's just annoying.

Seriously, it adds a data asset that needs to be maintained. Most of the time that's not a huge deal, but when
it is, it is. Your call.


## Git is an agent database
I highly recommend versioning files & ideally also skills & memory blocks. In open-strix I store memory blocks
in yaml so they version and diff cleanly.

Versioning gives you checkpoints and lets you see evolution. It also lets you rollback or let the agent discover
when a bad change was made. I've tried to use branching and merging, but not successfully.


## Bad ideas
**Knowledge graphs** and other writable **data models**, e.g. backend by SQL, tend to not work very well because the
LLM's weights doesn't know about their schemas. Most people talk themselves into knowledge graphs because they
have structure and historically structure has been good. But the only structure LLMs need is tokens. They reason
just fine in token space.


## Good (but weirder) ideas
I've discovered that some types of generic data structures can be very useful for agents, for special purposes.

**Issue trackers** are oddly useful. I've been using [chainlink][cl], which is an issue tracker specifically
for agents, but I've heard [Asana][as] also works fine. Probably any issue tracker would work. An issue tracker
gives you a searchable work queue.

I've added an *interest backlog* to all of my agents now. Any time they come across something weird, interesting,
or annoying they can create an issue and tag it `interest`. Then, during the night while I sleep they work 
through the backlog. This has led to multiple agents making connections between ideas & things I hadn't discovered
yet, and generally coming up with fresh ideas that feel honestly novel.

Also, an **append-only log** is super useful. I have an `events.jsonl` file that goes into all of my agents. The
agent harness writes every single event that happens, like tool calls and messages, and appends a JSON object 
minified to the `events.jsonl` file. It's not writable memory in the normal sense, but the agent can read it
to give grounded answers about what it actually did.


# Conclusion
Editable memory is extremely powerful. I highly recommend trying it out. Hopefully this helped.


 [cl]: https://github.com/dollspace-gay/chainlink
 [as]: https://asana.com/
 [letta]: https://docs.letta.com/overview
 [skills]: https://simonwillison.net/2025/Oct/16/claude-skills/
 [cache]: https://www.anthropic.com/news/prompt-caching
 [cc]: https://www.claude.com/product/claude-code
