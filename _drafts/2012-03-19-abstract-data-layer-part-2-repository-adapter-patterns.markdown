---
layout: post
title: "Abstract Data Layer Part 2: Repository & Adapter Patterns"
date: 2012-03-19
comments: false
---

Since I wrote [the first part to this post]({% post_url 2012-03-19-abstract-data-layer-part-1-object-id %}) my
boss agreed that supporting both MongoDB and all relational databases was too complicated to be practical. 
After some thought, I am going to continue this blog series a little further even though I won't be taking the
project further. I'm doing this mainly because, by working through the problem, it became wildly apparent what a 
clean data layer should look like. I know I've worked with relational databases long enough that I started to 
take for granted what was a relational concept and how that could possibly change by going to a document database.

Use the repository pattern
-------------

The [repository pattern](http://devlicio.us/blogs/casey/archive/2009/02/20/ddd-the-repository-pattern.aspx) 
is generally accepted as a good way to abstract an application from the database. The _repository_ is an 
abstraction that, from the business logic side, we can think of as a collection. Which is exactly what you 
want from a data layer - you just want to say "give me some objects that look like _X_" and it gets them
for you.

Add adapters for each target database type
--------------

There 

The repository also isn't supposed to be a data access layer. It's just supposed 

* Maybe cover adapters and how we can leave ourselves open to optimization
* Cover Repository pattern and how we consolidate business logic into it's own layer, separate from the database.
* Probably shout out some mentions of common data layer anti-patterns
