---
layout: post
title: NuGet Should Have OSS License Reporting
---

Producing comercial applications today has changed quite a bit in the past
decade. If you want to produce a decent modern application you'll be using
a large amount of open source software. Logging, database drivers, ORMs,
unit testing, mocking, IoC containers, and the list goes on. 

A lot of this software is released under permissive licenses like Apache, 
MSPL, MIT, or BSD. However, a lot of older engineers still have aches in the
back of their minds of times when they got burned by using copy-left
licenses. The truth is, most OSS these days is released under a permissive
license, but getting burned by a copyleft license like GPL could mean 
releasing all your proprietary code. That could crush a small tech company.

One of the great things about NuGet is how it keeps metadata about all OSS
tools and their dependencies locally. 
