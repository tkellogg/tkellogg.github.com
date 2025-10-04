---
layout: post
title: "Don't Parse, Call"
date: 2025-10-03
categories:
 - ai
 - LLMs
 - engineering
 - agents
image: https://cdn.pixabay.com/photo/2025/09/04/14/58/horse-9815867_1280.jpg
# social_image: /images/bash-v-powershell.png
is_draft: false
use_mermaid: false
summary: |
  Instead of writing crap tons of parsing code for LLMs you can just use functions. It's easy.
---

_"Hey, I've been out of it for a minute, what format are we using in LLM prompts?"_

Stop.

STOP.

_**STOP.**_

For real, stop with the formats. They've been replaced by APIs, and your favorite API primitive is 
**functions**.

prompt:
> The following text is from an internet rando. Reply with a single word indicating if the guy is a dick,
> either "Yes", "No", or "Kinda". _**Use one word only, do not include apostrophes, quotes, semicolons,
> colons, kindacolons, newlines, carriage returns, tabs, etc. Use only a single line and do not include
> any extra explanation. Do not use French or Spanish or German or Japanese, only use English. Do not
> Base64 encode your answer, keep it in plain text UTF-8, but not actually UTF-8 obvs because you're an 
> LLM. Just be cool and answer okay already???**_

Tired yet? Just use functions.

{% highlight python %}
result = ""

@tool
def select_answer(answer: str):
    """answer can only be "Yes", "No" or "Kinda". Whatever makes the most sense."""
    if answer.lower() not in {"Yes", "No", "Kinda"}:
        raise TypeError(f"Allowed values for answer are, 'Yes', 'No', 'Kinda', not '{answer}'")

    global result
    result = answer

response = openai.responses.create(
    instructions="Is this guy a dick? Call the function to indicate your answer",
    tools=[select_answer],
    input=input_text,
)
{% endhighlight %}


# Why Use Functions?
Because models are trained for them. A lot. A ridiculously huge amount.

Ever since [o3-mini launched][o3], each model launch is fighting to be more agentic than the last. What does 
"agentic" mean? It means it **calls functions** ridiculously well.


## They're Ubiquitous
All models use a different format for representing functions & calls. Some use some `<|call|>` jankiness, 
others use special tokens, or XML, or JSON. And it honestly doesn't matter because you'll just **use their 
API** and the API is always the same.


# Expressiveness
What if you want to capture a `rationale`? Well that's easy:

{% highlight python %}
@tool
def select_answer(answer: str, rationale: str):
    ...
{% endhighlight %}

What if the thing can fail? Again, this is easy:

{% highlight python %}
@tool
def select_answer(answer: str, rationale: str):
    ...

@tool
def fail(reason: str)
    ...
{% endhighlight %}

Using two functions is a lot like declaring a `str | None` data type in Python/mypy. Yes, [sum types][sum].

You can also have the LLM call a function multiple times. Or not at all. Or some other sequence.

The final text response at the end ends up becoming a log (that you can log! or ignore).


# It's Agentic
Aside from everyone else's definition of "agent", agents use **inverted control**.

Instead of top-down tight imperative control over what the LLM does and how and why, you merely 
**provide functions** and give the LLM space to do it's thing.

I wouldn't say the simple code I slopped out above is an agent. But if you start thinking about
LLMs from this angle, providing functions and letting control invert, one day you'll wake up and be 
shocked at how many agents you have.

Think agentically.


# Stay Low Level
Stop using AI frameworks!

Yes, I'm one of those guys. The reason is because it abstracts you away from **the details**, so suddenly you're
not really sure if it's using functions, JSON, or something else.

The OpenAI chat completions API is industry standard at this point. **But it sucks**. Nothing against the API,
it's just old. It doesn't give you control over [caching][cache]. Newer APIs have a `document` or `file` concept,
which when used reduces the opportunity for prompt injection. Or [garbage collecting][gc] unused parts of your
prompt.

But if you're using an AI framework, you probably have no idea if you're using any of that! The APIs from the
labs are surprisingly powerful. You **don't need** anything on top.

# Conclusion
Go forth and call functions!


 [o3]: https://openai.com/index/openai-o3-mini/
 [sum]: https://www.reddit.com/r/ProgrammingLanguages/comments/10jewgp/could_you_explain_why_sum_types_are_so_good/
 [cache]: https://docs.vllm.ai/en/v0.9.2/features/automatic_prefix_caching.html
 [gc]: https://www.anthropic.com/news/context-management
