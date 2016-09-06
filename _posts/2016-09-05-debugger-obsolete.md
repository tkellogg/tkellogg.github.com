---
layout: post
title: "Your Debugger Is Obsolete"
date: 2016-09-06
categories:
 - engineering
---

Debuggers used to be super useful, but today they are usually a sign that you don't 
know what you are doing.

Debuggers are still good at debugging serial code, but these days my code is asynchronous and
distributed over many hosts. There is no concept of "stepping through code" in asynchronous
systems - stepping implies that you are on a single thread, running on a single machine.

Today we use metrics. With metrics, I can observe failures on hundreds of hosts 
simultaneously. I can witness a starvation event begin and end over an entire fleet,
and have visual graphs to explain what happened. I can look at a period of high latency
and correlate it to a new profile of traffic that I had not considered before.

Things I put metrics on:

* **Latency.** Obviously request latency, but also usually 6-10 different sub-sections of the
request to help troubleshoot slowness.
* **Failures.** Not only should you record all failures in order to calculate availability, but also put
counters on different classes of failures. Where there is an assert statement, there should
be a counter.
* **Dependencies.** They are like children; you have great hopes and dreams for them, but in
the end they disappoint you. Record their latency and availability for yourself.
* **Features.** What do customers actually use? Where do they get stuck most often?
* **Traffic Profile.** Record how big the request and response were or how many elements
were in "that array". This is great for understanding where load is coming from and what sorts
of mitigations are appropriate.
* **System Health.** Record CPU, memory, disk and network usage. I find that, on the JVM,
a high number of garbage collections is a more reliable indicator of an unhealthy host than
high CPU or memory usage.

Alarms are the first step toward a service that can manage itself. Alarms are just events. 
They can notify me that something went wrong, or, better yet, fix the problem automatically. 
The AWS [Autoscaling][1] API is killer, spin up a few instances if you notice a traffic spike
or an unhealthy host, then decommission them automatically when the event is over.

There are some great upsides to this new world where metrics are my debugger. When things
go wrong, I find out first from my servers instead of my customers. Back when debuggers 
were relevant, I found out about issues through support tickets. This is much more proactive.

Tests also helped make the debugger obsolete. I find that when I need to replicate an 
issue, I can do it in a high component-level or functional-level test. In the process of
figuring out what went wrong I usually write a few unit-level tests. In the meantime,
I use metrics and log lines to understand the internal state and figure out where things
are going wrong. Unlike an IDE debugger, this debugging session is recorded and re-run
forever. If you still need a debugger, there is a chance that the code is simply too
complex and needs major refactoring.

You should absolutely write unit tests against metrics. If they don't work, you'll be
blind in production. They are a part of the application just as much as the request handler.
Once you start doing this, you might notice that the debugger is less useful.

If systems aren't asynchronous enough for you, we're in the process of launching the
Internet of Things where we make it extremely difficult to launch a debugger on the devices
where your software runs. Not only do they not have screens, but your fleet
has 100K or 1M devices. Whole classes of problems are about to happen that you never heard
of. So learn how to debug an application through metrics. It will be the only way
to be successful in the future.

 [1]: https://aws.amazon.com/autoscaling/
