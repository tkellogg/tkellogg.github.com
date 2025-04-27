---
layout: post
title: "MCP is Unnecessary"
date: 2025-04-27
categories:
 - ai
 - LLMs
 - engineering
 - MCP
image: https://cdn.pixabay.com/photo/2013/07/12/14/30/ants-148326_1280.png
# social_image: /images/bash-v-powershell.png
is_draft: false
use_mermaid: true
---

I can't think of any strong technological reasons for [MCP][mcp] to exist. There's a lot
of weak technological reasons, and there's strong sociological reasons. I still strongly
feel that, ironically, it is necessary. I'm writing this post to force myself to clarify
my own thoughts, and to get opinions from everyone else.

## Misconception: MCP Doesn't Go Into The Prompt
You absolutely *can* directly paste the JSON from an MCP tool declaration into a prompt.
It'll work, and it's arguably better than doing the same with OpenAPI. But it's JSON,
extremely **parseable, structured** information, and most LLMs are trained to do function calling with some 
XML-like variant anyway.

An LLM tool declaration can look like:

* Raw MCP/OpenAPI JSON
* Formatted as XML
* Use the tool calling APIs (e.g. [OpenAI][oai], [Ollama][oll])
* Formatted as Python code (e.g. [smolagents][smol])

MCP is not concerned with what your prompt looks like. That is not a function of MCP.

## Tool Libraries
MCP has two primary functions:

1. Advertising tools
2. Calling tools

It does a lot of other things (logging, sampling, etc.), but tool calling is the part 
that's most **frequently** implemented and used.

You could accomplish the same thing with OpenAPI:

1. Advertising tools: Always post the `openapi.json` file in the same place
2. Calling tools: OpenAPI standardizes this part

This is even easier than you think. OpenAPI operations have an `operationId`
that is usually set to the function name of the server API anyway.


## Steelman: OpenAPI APIs Are Too Granular
This is a good argument, at least on the surface. Here's an example of a typical API 
representing an async task:

<div class="mermaid">
graph TD

c((client))-->start_job
c-->poll_status
c-->get_result
</div>

You can wrap all that into one single MCP operation. One operation is better than 3 because
it removes the possibility that the LLM can behave wrong.

<div class="mermaid">
graph TD

subgraph MCP
    c
end
client((client))-->c
c[do_job]-->start_job
c-->poll_status
c-->get_result
</div>


Okay, but why does this have to be MCP? Why can't you do the same thing with OpenAPI?


## Steelman: MCP Is Optimized For LLMs
Yes, most APIs don't work well directly in LLM prompts because they're not designed or 
documented well. 

There's [great tooling][fastmcp] in the MCP ecosystem for composing servers
and operations, enhancing documentation, etc. So on the surface, it seems like MCP is an
advancement in API design and documentation.

But again, why can't OpenAPI also be that advancement? There's no technological reason.

## Steelman: MCP Is A Sociological Advancement
Here's the thing. Everything you can do with MCP you can do with OpenAPI. But..

1. It's not being done
2. There's too many ways to do it

Why isn't it being done? In the example of the async API, the operation might take a
very long time, hence why it's an async API. There's no technical reason why APIs can't
take a long time. In fact, MCP implements tool calls via [Server Sent Events (SSE)][sse].
OpenAPI can represent SSE.

The reason we don't do OpenAPI that way is because engineering teams have been conditioned
to keep close watch on operation latency. If an API operation **takes longer** than a few hundred
milliseconds, someone should be spotting that on a graph and diagnosing the cause.
There's a lot of reasons for this, but it's fundamentally sociological.

SSE is a newer technology. When we measure latency with SSE operations, we measure time-to-first-byte.
So it's 100% solveable, but async APIs are more familiar so we just do that.

## Steelman: One Way To Do Things
The absolute strongest argument for MCP is that there's mostly only a single way to do
things.

If you want to waste an entire day of an engineering team's time, go find an arbitrary API `POST`
operation and ask, "but shouldn't this be a `PUT`?" You'll quickly discover that HTTP has a
lot of ambiguity. Even when things are clear, they don't always map well to how we normally 
think, so it gets implemented inconsistently.

| MCP | OpenAPI |
|-----|---------|
|function call| resources, `PUT`/`POST`/`DELETE`|
|function parameters| query args, path args, body, headers|
|return value| SSE, JSON, web sockets, etc.|


## Conclusion: Standardization Is Valuable
Standards are mostly sociological advancements. Yes, they concern technology, but they govern
how society interacts with them. The biggest reason for MCP is simply that everyone else is doing
it. Sure, you can be a purist and demand that OpenAPI is adequate, but how many clients support it?

The reason everyone is agreeing on MCP is because it's far smaller than OpenAPI. Everything in the tools
part of an MCP server is directly isomorphic to something else in OpenAPI. In fact, I can easily
generate an MCP server from an `openapi.json` file, and vice versa. But MCP is far smaller
and purpose-focused than OpenAPI is.


 [mcp]: https://modelcontextprotocol.io/introduction
 [oai]: https://platform.openai.com/docs/guides/function-calling?api-mode=responses
 [oll]: https://ollama.com/blog/functions-as-tools
 [smol]: https://huggingface.co/docs/smolagents/en/tutorials/secure_code_execution
 [sse]: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events
 [fastmcp]: https://github.com/jlowin/fastmcp?tab=readme-ov-file#composing-mcp-servers
