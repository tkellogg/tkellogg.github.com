---
layout: post
title: "LLMs Are Not Security Mitigations"
date: 2025-04-01
categories:
 - ai
 - LLMs
 - engineering
 - security
image: https://cdn.pixabay.com/photo/2025/03/26/17/03/pasque-flower-9494841_1280.jpg
# social_image: /images/bash-v-powershell.png
is_draft: false
use_mermaid: true
---

LLMs are great code reviewers. They can even spot security mistakes that open us up to vulnerabilities.
But no, they're not an adequate mitigation. You can't use them to ensure security.

To be clear, I'm referring to this:

1. User sends a request to app
2. App generates SQL code
3. **App asks LLM to do a security review**, and then iterates with step 2 if it fails the review
4. App executes generated code
5. App uses results to prompt LLM
6. App returns LLM response to user

This might be confusing at first. LLMs **are** good at identifying security issues, why can't they be
used in this context?


# Bad Security
The naive way to do security is to know everything about all exploits and simply not do bad things.
Quickly, your naive self gets tired and realizes you'll never know about all exploits, so anything
that I can do that might prevent a vulnerability from being exploited is a good thing.

This is where LLM-review-as-mitigation seems to make sense. LLM code reviews will uncover vulnerabilities
that I probably didn't know about.

That's not how security works.


# Good Security
The right approach to security is to:

1. Identify what's important
2. Identify **attack surfaces**
3. Reduce or remove attack surfaces

This is threat modeling. Instead of fighting all vulnerabilities ever, focus first on **ones that matter**,
and then list out dangers the app actually might experience.

Focus on what matters

One simple framework to help guide this process is the CIA framework:

* **C — Confidentiality** — Info is only accessible to authorized users
* **I — Integrity** — Info is complete, accurate, and there is no unauthorized modification or deletion
* **A — Availability** — Authorized users have timely and reliable access to information & resources when they need it

[STRIDE][stride] is a much better and more complete framework, but the same message applies.

## What does LLM-review address?
LLM-review clearly doesn't prevent information leaks, and it doesn't improve the availability of the service,
so by elimination it must improve the **integrity**.

But does it?

LLM-review does identify dangerous coding issues, but it **doesn't prevent** anything. Anything that
can be surfaced by an LLM-review can be circumvented by [prompt injection][inj]. 

It's not your goal, as an engineer or architect, to come up with the exploit, only to understand if 
an exploit **might be possible**. The attacker can inject code or comments into the input to
the LLM check instructing the LLM to say there are no issues. If the attacker isn't directly writing the 
code, they're still influencing the prompt that writes the code, so they can conceivably instruct the
code writer LLM to write a specific exploit. And if there's another layer of indirection? Same. And another?
Same, it keeps going forever. A _competant_ attacker will always be able to exploit it.

In the presence of a _competant_ attacker, the LLM-review check will **always be thwarted**.
Therefore, it holds no value.

There is no attack surface that it removes. None at all.


## Availability
But surely it has value anyway, right? It doesn't prevent attacks, but something is better than 
nothing, right?

The clearest argument against this line of thinking is that, no, it actually hurts availability. For
example:

* **Resource exhaustion** — LLM-review checks consume LLM resources (e.g. token buckets), and therefore there's
    less resources to be used by the primary application. One possible outcome is an outage.
* **False positives** — LLMs are predisposed to completing their task. If they're told to find security
    vulnerabilities, they're biased toward finding issues even if there are none. That causes another kind of
    outage, where perfectly fine code is randomly rejected. If code is regenerated in a loop, this causes
    further resource exhaustion, that triggers global outages.

So no, "something" is not better than nothing. LLM security checks carry the risk of taking down production
but without any possible upside.

Hopefully it's clear. Don't do it.

## Error Cascades (The Spiral of Doom)
In distributed systems, this problem is typically expressed in regards to retries.

Suppose we have an app:

<div class="mermaid">
graph TD
Frontend--3 retries-->Microserice--3 retries-->db[(Database)]
</div>

Suppose the app is running near the point of database exhaustion and the traffic momentarily blips up
into exhaustion. You'd expect only a few requests to fail, but it's much worse than that.

1. When the DB fails, Microservice retries causing more traffic
2. Frontend retries, causing even more retry traffic
3. User gets angry and contributes further by also retrying

A small blip in traffic causes an inexcapable global outage.

The LLM security check is similar mainly because failed checks reduce availability, and if that check
is performed in a retry loop it can lead to real cascading problems.


## But Content Filters Are Good!
Yes, it's frequently listed as a best practice to include content filters. For example, check LLM input and
output for policy violations like child pornography or violence. This is often done by using an LLM-check,
very similar to the security vulnerabilities we've been discussing.

Content filters **aren't security**.
They don't address any component of CIA (confidentiality, integrity or availability), nor of STRIDE. 

You can argue that bad outputs can damage the company's **public image**. From that perspecive, any filtering
at all reduces the risk exposure surface, because we've reduced the real number of incidents of damaging
outputs.

The difference is content filters defend against **accidental** invocation, whereas threat mitigations
defend against intentional hostile attacks.


# What You Should Do Instead
Lock it down, with traditional controls. Containerize, sandbox, permissions, etc.

* SQL — Use a special locked-down user, set timeouts, and consider running on a copy of production instead 
    of directly on production.
* Python — Run it in Docker, whitelist modules (blacklist by default), use containers to isolate users (e.g.
    new container for every user)

_Note: VMs are certainly better than Docker containers. But if wiring up firecracker sounds too hard, then
just stick with Docker. It's better than not doing any containerization._

All these directly reduce attack surface. For example, creating a read-only SQL user guarantees that the
attacker can't damage the data. Reducing the user's scope to just tables and views ensures they can't
execute stored procedures.

Start with a threat model, and let that be your guide.


## Passive Monitoring
Another good option is to still include LLM-driven security code review, but passively monitor instead of
actively block.

This is good because it lets you be aware and quantify the size of a problem. But at the same time it 
doesn't carry the error cascade problem that can cause production outages. More upside and less downside.


# Use LLMs In Your Dev Process!
Using LLMs to review code is good, for security or for general bugs.

The big difference is that in the development phase, your threat model generally doesn't include employees
intentionally trying to harm the company. Therefore, prompt injection isn't something you need to be
concerned about.

Again, and I can't stress this enough, build a threat model and reference it constantly.

# Closing
The astute reader should realize that this post has nothing to do with LLMs. The problem isn't that LLMs
make mistakes, it's that they can be **forced to make mistakes**. And that's a security problem, but
only if it exposes you to real risk.

If there's one thing you should take away, it should be to **make a threat model** as the first step in your
development process and reference it constantly in all your design decisions. Even if it's not a complete
threat model, you'll gain a lot by simply being clear about what matters.


# Discussion
* [Hacker News](https://news.ycombinator.com/item?id=43545816)
* [Bluesky](https://bsky.app/profile/timkellogg.me/post/3llqtstcf7c2p)

 [stride]: https://www.practical-devsecops.com/what-is-stride-threat-model/
 [inj]: https://docs.aws.amazon.com/prescriptive-guidance/latest/llm-prompt-engineering-best-practices/common-attacks.html
