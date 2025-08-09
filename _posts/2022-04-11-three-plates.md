---
layout: post
title: "Three Plates"
date: 2022-04-11
categories:
 - engineering
 - testing
 - practices
 - tdd
 - methodology
 - mentoring
---

"Why don't we test our tests?". It's like the three plates method. Take test code and
prod code and grind them against each other until the blemishes are ground smooth. That's unit testing.

The [three plates method](https://ericweinhoffer.com/blog/2017/7/30/the-whitworth-three-plates-method)
is a process that creates the flattest plates, with the highest precision. No power tools needed, 
just 3 granite plates. 

It goes like this:

1. Take plates `A` and `B`, grind them together for a while
2. Grind `B` and `C` together
3. Grind `C` and `A` together
4. Repeat until smooth enough

The process takes a while, but there's no upper bound to the precision. All it takes is time and skill.
Before you start, the plates are rough cut with bumps, scars and points. But 
after a few iterations, the blemishes break off iteratively to reveal a flat, smooth, beautiful surface.

Unit testing is a lot like this. I like to think [TDD][tdd] means that we write the test first, but it's
not important what comes first. It's not like I spit out perfect test code or prod code on my first try, 
and yet, after several iterations of fixing code on both sides, the code converges to a well-functioning
unit. 

The three plates method is also a great analogy for understanding TDD and where it fits. 

* _**Two Plates?**_ — Naively, I would have thought it only takes two plates to create a smooth surface,
    but the third plate important. In TDD, a single test will get you a long way toward functioning prod
    code, but you need more tests to hash out all the edge cases. The more, the better.
* _**Units**_ — For a granite countertop, the three plates method is all you need. But
    usually you'll want to install it somewhere useful, like in a kitchen. To do that, you'll need other
    quality tools, like a level to make sure it was installed correctly. TDD is useful for what it does, 
    but it would be a shame to have a giant unit test suite with no functional tests. Maybe go crazy and 
    [try formal methods][fm].
* _**Dedication**_ — The three plates method requires a lot of experience and skill. It also takes a lot of
    practice to be able to leverage unit tests effectively. If your organization has trouble hiring
    high caliber engineers, you may find that large unit test suites cause projects to be late or fail.
    It's hard to be internally honest about things like this, but if you can, shift some of your
    controls to quality processes that require less skill, or hire QA engineers.

I hope you find the three plates method to be a useful analogy for unit testing. The idea of "rough 
smoothing rough" comes up in a lot of contexts, e.g. [mentoring][m] and [machine learning][gan]. 
Broadly speaking, it's great whenever the ideal isn't tangible, or when you're pushing past known limits.

 [tdd]: https://www.agilealliance.org/glossary/tdd/#q=~(infinite~false~filters~(postType~(~'page~'post~'aa_book~'aa_event_session~'aa_experience_report~'aa_glossary~'aa_research_paper~'aa_video)~tags~(~'tdd))~searchTerm~'~sort~false~sortDirection~'asc~page~1)
 [fm]: https://learntla.com/introduction/
 [gan]: https://machinelearningmastery.com/what-are-generative-adversarial-networks-gans/
 [m]: https://www.evidencebasedmentoring.org/four-ways-mentoring-benefits-mentor/
