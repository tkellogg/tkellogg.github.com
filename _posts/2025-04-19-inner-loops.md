---
layout: post
title: "Inner Loop Agents"
date: 2025-04-19
categories:
 - ai
 - LLMs
 - engineering
 - agents
image: https://cdn.pixabay.com/photo/2022/03/12/17/40/pink-flower-7064566_1280.jpg
# social_image: /images/bash-v-powershell.png
is_draft: false
use_mermaid: true
summary: |
    What if an LLM could use tools directly? In this post I discuss a potentially
    divergent view of agents, where agents are less like systems and more like LLMs
    specially trained to solve problems with a specific set of tools.
---

What if an LLM could use tools directly? As in, what if LLMs executed tool calls
without going back to the client. That's the idea behind inner loop agents. It's
a conceptual shift. Instead of thinking of agents as being a system involving
client & server, you just have a single entity, the LLM. I hope it will help
clarify how [o3 and o4-mini][o3] work.

_(note: this post isn't as long as it looks, there's a lot of diagrams and examples)_

To illustrate, regular LLMs rely on the client to parse and execute tools, like this:

<div class="mermaid">
graph TD
subgraph inn["LLM (Inner Loop)"]
    Tokenizer-->nn[Neural Net]-->samp[Select Next Token]-->Tokenizer
end
text((Input))-->Tokenizer
parse--->out((Output))
samp-->parse[Parse Tool Calls]-->exec[Run Tools]-->parse
parse--"tool<br/>result"-->Tokenizer
</div>

On the other hand, with inner loop agents, the LLM can parse and execute tools
on it's own, like this:

<div class="mermaid">
graph TD
  subgraph inn["Inner Loop Agent"]
    direction TB

    Tokenizer
    nn[Neural Net]
    samp[Select Next Token]
    parse[Parse Tool Calls]
    exec[Run Tools]
  end

  text((Input)) --> Tokenizer
  Tokenizer --> nn --> samp --> parse
  parse --> exec -->parse

  parse -----> Tokenizer
  parse ---> out((Output))                  
</div>

## The LLM Operating Software (Ollama, vLLM, etc)
In these diagrams, the LLM is emitting text that looks like this:

```
System: You are an agent with access to the following tools:

<tool name="google_maps" description="Look up directions between two places on Google Maps">
    <param name="begin" description="The starting point of the trip"/>
    <param name="end" description="The ending point of the trip"/>
</tool>


User: How do you drive from Raleigh, NC to Greene, NY?


Assistant: To do this, I will use my Google Maps tool.

<tool name="google_maps">
    <param name="begin">Raleigh, NC</param>
    <param name="end">Greene, NY</param>
</tool>
<|eot|>
```

The LLM only generates the text after `"Assistant:"`

That `<|eot|>` is a special token that the LLM is **trained to emit** as
a way to signal that it's done.

The software you're using to run your LLM, e.g. [Ollama][ollama], [vLLM][vllm],
OpenAI, Anthropic, etc., is responsible for running this loop. It parses the
LLM output and stops the loop when it runs into a `<|eot|>` token.

If you use the tool calling APIs ([Ollama][oll-tools], [OpenAI][oai-tools]),
Ollama will parse out the tool call and return it as JSON in the **API response**.

Ollama and vLLM are special in that they support _a lot_ of different models.
Some models are trained to represent tool calls with XML, others are JSON,
others something else entirely. Ollama and vLLM abstract that away by allowing the model to configure
how it wants to represent tool calls. It doesn't much matter
what the format is, only you're **consistent** with how the model was trained.


# Why Are Inner Loop Agents Good?
Okay, so inner loop agents still do all that parsing. The only difference
is that they handle the tool calling themselves instead of letting the client
handle the tool call and making another API response.

But why?

The most compelling reason to do this is so that the LLM can call tools concurrently
with it's thinking process.

If you've gotten a chance to use an agent, like [Deep Research][dr] or [o3][o3],
you'll notice that it's thought process isn't just inner dialog, it's also tool
calls like _web searches_. That's **the future** of agents.

![](/images/o3-thought-trace.png)

### Trained With Tools

`o3` and `o4-mini` are special because they're trained to be **agentic models**.

In [reinforcement learning][rlhf], the model is given a problem to solve and
rewarded for good behavior, like getting the right answer or at least getting
the format right. For example the [R1 paper][r1] discussed rewarding the model 
for staying in English if the question was given in English.

Here's a diagram of reinforcement learning:

<div class="mermaid">
graph TD
input((Problem))
subgraph LLM
tok[Tokenizer]-->nn[Neural Net]-->samp[Select Next Token]-->tok
end
input-->tok
samp-->out[Output]-->reward[Calculate Reward]-->update[Update Model Weights]-->next((Next Problem))
update----->nn
</div>

With inner loop agents, you would change the above diagram to include tools in the
yellow box, in the inner loop. The model is still
rewarded for the same things, like getting the right result, but since tools are
included you're simultaneously reinforcing the model's **ability to use** it's
tools well.

It's clear to me that `o3` was trained to use it's web search tool. I believe
they even said that, although I might be remembering wrong. It's certainly the
generally accepted view.

Today LLMs can do all this, if they're trained for tool use. What changes, is that
the model become good at using the tools. Tool use isn't just possible, tools
are used at the **optimal time** in order to solve the problem in the best 
possible way.

Optimal tool use. Hmm... Almost sounds like art.

## Emergent Tool Use
The agentic models today (`o3`, `o4-mini`, [Claude Sonnet][sonnet]) are only trained
to use a **small set** of specific tools. 

Web search & bash usage are cool and all, but what would be truly powerful is
if one of these inner loop agents were trained to use tools that regular people use.
Like, what if it could submit a purchase order, or analyze a contract to understand
if I can make the supplier cover the tariffs? Or to use a tool to navigate an org 
chart and guess who I need to talk to.

[Model Context Protocol (MCP)][mcp] was designed to support **diverse** tool use. All you have to
do to get an LLM to use your API is build an MCP server. Anyone can then use your
API from their own AI apps. Cool.

But the LLM wasn't trained to use **your tool**. It was only trained to use tools, generically.
It just follows the tool call format, but it hasn't been optimized for using those tools
to solve a problem.

Emergent tool use would mean that an LLM could pick up any MCP description and use
the tool effectively to solve a problem. 

This isn't _planning_. 

Let's say you're doing wood working and you get a new chisel.
You can read all you want on when and how you're supposed to the chisel, but ultimately
it takes experience to know what kind of results you can expect from it. And once you
fully understand the tool, _then_ you can include it in your planning.

Emergent tool use hasn't happened yet, as 
far as I know. I hope it'll happen, but it seems unlikely that an LLM can discover
the finer points of how to use a tool just from reading the manual, without any training.


## Trained Tool Use
Until emergent tool use happens, we have two options:

1. Use MCP description fields to carefully explain how the tool is used and _hope for the best_.
2. Inner loop agents. Train a model with your tool.

Right now, those options are our future.

If you want an agent, you can prototype by prompting it to use tools well. But ultimately,
to build a high-quality agent as a product, you'll likely need to train a model to use
your tools effectively.


## Agent To Agent
Google recently released [Agent 2 Agent (A2A)][a2a]. A protocol that facilitates interactions between agents.

My hunch is that this level of protocol will become critical. If people take inner loop
agents seriously, it'll be difficult to always use the state of the art models. Instead,
each agent will be using it's own LLM, because training is expensive and slow.

A protocol like A2A allows each of these fine tuned LLM agents to communicate without
forcing yourself into LLM dependency hell.


# Conclusion
That's inner loop agents. 

One big note, is that even if you're training an LLM with tools, the tools don't _actually_
have to be executed on the same host that's running the LLM. In fact, that's unlikely to 
be the case. So, inner loop vs not inner loop is not really the part that matters. It's
all about whether or not the LLM was trained to use tools.


# Discussion
- [Hacker News](https://news.ycombinator.com/item?id=43752627)
- [Bluesky](https://bsky.app/profile/did:plc:ckaz32jwl6t2cno6fmuw2nhn/post/3ln6g2fh5r326)


 [o3]: https://openai.com/index/introducing-o3-and-o4-mini/
 [ollama]: https://ollama.com/
 [vllm]: https://vllm.ai
 [oll-tools]: https://ollama.com/blog/tool-support
 [oai-tools]: https://platform.openai.com/docs/guides/function-calling?api-mode=responses
 [dr]: https://openai.com/index/introducing-deep-research/
 [claude]: https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview
 [rlhf]: https://rlhfbook.com/
 [r1]: https://arxiv.org/abs/2501.12948
 [sonnet]: https://www.anthropic.com/claude/sonnet
 [mcp]: https://modelcontextprotocol.io/introduction
 [a2a]: https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/
