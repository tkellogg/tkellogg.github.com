---
layout: post
title: "Entrapix: You Should Have A ConfusedAgentError"
date: 2024-12-08
categories:
 - ai
 - LLMs
image: https://cdn.pixabay.com/photo/2017/09/27/12/07/green-2791849_1280.jpg
is_draft: false
use_mermaid: false
---

I just released [entrapix][entrapix], which is a fork of [Ollama][ollama] that raises
a `ConfusedAgentError`, so to speak, when the LLM becomes unsure of itself.

Entrapix is a riff off of [entropix][entropix], which is an experiment with dynamic 
samplers. Basically, you shouldn't have to set `top_p`, `top_k`, `temperature`, etc. 
manually, entropix streamlines the whole process by watching the internal state of
the model and reacting accordingly. I [wrote about it][blog] a while back.

Entrapix is much simpler. It doesn't do the dynamic sampler stuff, it just detects the
case when the LLM is high entropy / high varentropy and exits immediately, setting
`done_reason = "trap"` in the API.

<table>
    <thead>
        <tr>
        <td></td>
        <td><b>Low Entropy</b></td>
        <td><b>High Entropy</b></td>
        </tr>
    </thead>
    <tbody>
        <tr>
        <td><b>Low Varentropy</b></td>
        <td style="background-color: #76D07A; /* Amber color */
    border: 1px solid #76D07A; /* Border color for contrast */
    color: black;
    padding: 5px 10px;
    display: inline-block;
    margin-bottom: 10px;">Easy, churn out tokens</td>
        <td></td>
        </tr>
        <tr>
        <td><b>High Varentropy</b></td>
        <td></td>
        <td style="background-color: #ffcc66; /* Amber color */
    border: 1px solid #f0a541; /* Border color for contrast */
    color: black;
    padding: 5px 10px;
    display: inline-block;
    margin-bottom: 10px;">Uncertainty! <pre>raise ConfusedAgentError()</pre></td>
        </tr>
    </tbody>
</table>


The CLI tool is wired up. At minimum, the `--entrapix true` flag is needed to
enable it.

```shell
❯ ./ollama run llama3.1 "How much energy is required for the information contained in 
a bowling ball to escape a black hole?" --entrapix true --entrapix-threshold 1 --entrapix-varent 1
A fun and imaginative question!

In theory, if we were to place a bowling ball near the event horizon of a black hole, its information would indeed be 
affected by the strong gravitational field.

However,

Error: agent is confused and has stopped
```

I haven't tried it yet, but I imagine most would want to set the thresholds in the modelfile.


### Use Cases
I built the concept to try out in [dentropy][dentropy]. Dentropy is an app
that helps overactive people keep track of their lives. The thing obout our users is they often
write notes and have no idea what they meant a few hours later. Naturally, the LLM also has no
idea what you meant, and it exhibits in the entropy/varentropy. We handle a confused agent by asking
the user clarifying followup questions.

However, I imagine it's going to be more common to just do a different query and RAG from a
different angle.


### Inner Loop vs Outer Loop
The philosophical difference between entropix and entrapix is the original bets on the information
encoded inside the model, whereas my entrapix bets on things found outside the model.

The agent-building crowd is similarly split. Some folk think you should build agents out of *systems*
of LLMs & other components (e.g. the [DSPy][dspy] crowd). Like my entrapix, they think they can guide
models via information found in databases, setting up judge LLMs or planning LLMs, etc.

In an agent, a systems approach is going to start with a loop outside the LLM and call 
the LLM (& other resources) from within it:

```python
while True:
    convo = plan(convo)
    convo = act(convo)
    convo = measure(convo)
```

Whereas the other approach is to embed the loop inside the LLM itself. Recall that an LLM is
just predicting the next token over and over in a loop, right? Well, when does it stop? LLMs are 
fine-tuned to stop relatively soon, but realistically, there's no reason they can't keep going
until their context window fills up (and then, if you're good at forgetting, maybe keep going 
forever). 

This is called an *inner loop*.

In that world, the original entropix helps continually nudge the LLM back into line, after every
token. In a sense, it's implementing a generic version of the `measure` step. Rather than building
a control loop for every new agent and problem, you just have a single "AgentGPT" app that takes
any problem and brings it to completion.


# Conclusion
I don't know which approach will win out in the end. I have a hunch that the inner loop might,
but I build for technology that exists today. And today LLMs & LRMs are quite hard to wrangle
in real world applications. I hope entrapix gives more hooks that you can use to keep outer loop
apps functional, today.


# Discussion
* [Hacker News](https://news.ycombinator.com/item?id=42362582)


 [entropix]: https://github.com/xjdr-alt/entropix
 [entrapix]: https://github.com/tkellogg/ollama-entrapix
 [ollama]: https://ollama.com/
 [dentropy]: https://www.getdentropy.com/
 [blog]: /blog/2024/10/10/entropix
 [dspy]: https://dspy.ai/
