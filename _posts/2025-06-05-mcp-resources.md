---
layout: post
title: "MCP Resources Are For Caching"
date: 2025-06-05
categories:
 - ai
 - LLMs
 - agents
 - engineering
 - MCP
image: https://cdn.pixabay.com/photo/2015/12/29/14/51/mountains-1112911_1280.jpg
# social_image: /images/bash-v-powershell.png
is_draft: false
use_mermaid: false
summary: This is a quick tour of what MCP resources actually are. And more to the point, what MCP is supposed to do (and not supposed to do).
---

If your MCP client doesn't support resources, it is **not a good client**.

There! I said it!

It's because [MCP resources][resources] are for improved prompt utilization, namely cache invalidation. 
Without resources, you eat through your context and token budget faster than Elon at a drug store. And
so if your client doesn't support it, you basically can't do **RAG with MCP**. At least not
in a way that anyone would consider _production worthy_.


# RAG documents are BIG

You don't want to duplicate files. See this here:

<p>
<div style="background-color: #aaaaee; text-align: center; margin: 0.25rem">
system prompt
</div>
<div style="background-color: #aaeeaa; text-align: center; margin: 0.25rem">
user message with tool definitions
</div>
<div style="background-color: #eeaaaa; text-align: center; margin: 0.25rem">
agent message with tool calls
</div>
<div style="background-color: #aaeeaa; text-align: center; margin: 0.25rem">
user message with tool call results
    <div style="">
    <div style="border-radius: 2px; border: 1px solid black; margin: 0.25rem">giant file 1</div>
    <div style="border-radius: 2px; border: 1px solid black; margin: 0.25rem">giant file 2</div>
    </div>
</div>
<div style="background-color: #eeaaaa; text-align: center; margin: 0.25rem">
another agent message with tool calls
</div>
<div style="background-color: #aaeeaa; text-align: center; margin: 0.25rem">
user message with tool call results
    <div style="">
    <div style="border-radius: 2px; border: 1px solid black; margin: 0.25rem"><b><i>giant file 2</i></b></div>
    <div style="border-radius: 2px; border: 1px solid black; margin: 0.25rem">giant file 3</div>
    </div>
</div>
<div style="background-color: #eeaaaa; text-align: center; margin: 0.25rem">
...
</div>
</p>

That's 2 tool calls. The second one contains a duplicate file.

Is this bad? If your answer is "no" then this blog post isn't going to resonate with you.


## Separate results from whole files
The core of it: A well-implemented app, MCP or not, will keep track of the documents
returned from a RAG query and avoid duplicating them in the prompt. To do this, you
keep a list of resource IDs that you've seen before (sure, call it a "cache").

Format the RAG tool response in the prompt like so:

```
<result uri="rag://polar-bears/74.md" />
<result uri="rag://chickens/23.md" />

<full-text uri="rag://chickens/23">
Chickens are...
</full-text>
```

In other words:
1. The return value of the function, to the LLM, is an **array of resources**
2. The full text is included elsewhere, for reference

URIs are useful as a cache key.

btw I'm just spitballing what the prompt format should be for returning results. You 
can play around with it, you might already have strong opinions. The point is,
**mapping must be done**.

## MCP is not LLM-readable
There's been a lot of discussion about if LLMs can interpret OpenAPI fine, and
if so, why use MCP. That misses the entire point. MCP isn't **supposed to be**
interpreted directly by an LLM.

When you implement an MCP client, you should be mapping MCP concepts to whatever
works for that LLM. This is called _implementing the protocol_. If you throw
vanilla MCP objects into a prompt, it could actually work. But a good client
is going to map the results to phrases & formats that particular LLM has gone
through extraordinarily expensive **training** to understand.


## MCP is a protocol
MCP standardizes how tools should **return** their results. 
MCP resources exist so that tools (e.g. RAG search) can return files, and
client can de-duplicate those files across many calls. 

Yes, it's cool that you can list a directory, but that's not the primary 
purpose of resources. Without resources, your LLMs just **eat more tokens**
unnecessarily. 

_(Side note: did you notice that neither [Anthropic][ant] nor [OpenAI][oai] supports 
resources in their APIs? It's a conspiracy..)_


# Resources are table stakes MCP support
If a client doesn't support MCP resources, it's because they don't care enough
to implement a proper client. Period.

While I'm at it, prompts are just functions with special handling of the results.
Might as well support those too.


# Discussion
* [Bluesky](https://bsky.app/profile/timkellogg.me/post/3lqvtthat622m)


 [resources]: https://modelcontextprotocol.io/docs/concepts/resources
 [ant]: https://docs.anthropic.com/en/docs/agents-and-tools/mcp-connector
 [oai]: https://gofastmcp.com/integrations/openai


