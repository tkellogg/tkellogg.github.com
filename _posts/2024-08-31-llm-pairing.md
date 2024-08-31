---
layout: post
title: "Who Wins With Cursor & Copilot?"
date: 2024-08-31
categories:
 - engineering
 - testing
 - ai
 - LLMs
 - consulting
image: https://cdn.pixabay.com/photo/2018/01/31/07/42/running-3120507_960_720.jpg
is_draft: false
use_mermaid: false
---

Nobody writes code correctly on the first pass 100% of the time. Not even the best programmers.
It's wild that unit tests even work. You test buggy code by writing more buggy code. And yet it works.
But why? 

I wrote about this [a couple years ago][orig]. I compared it to a process my dad told me about,
where you can make a plate that's precision smooth by taking three rough plates and carefully
grinding them together. Crazy, huh. You can make a perfect thing out of imperfect things.

LLM coding assistants, like [Github Copilot][gh] or the radical new [Cursor][cur] IDE, have a lot of
similarities to unit testing, the three plates, as well as pair programming. After looking at
the similarities, it should be obvious who is going to benefit most from these tools.


## You're Not Perfect
Let's get this out of the way. It's popular these days to idolize the work of human programmers, but take
a moment and be radically honest with yourself. You make mistakes. It's fine, we have processes
to make sure that doesn't matter.

LLMs make mistakes too. A lot of them are really dumb mistakes. Then again, if you're being radically honest
with yourself, you make dumb mistakes too.


## Sum of Strengths
There's something in common between all these things. They all take two or more imperfect things 
in a way that **combines the best features** of each and removes the imperfections.

In pair programming, who do you pair with? In one of my internships years ago, they loved [Extreme
Programming][xp]. In XP you pair program 100% of the time. Their guidance was to pair very different
people together. Have a junior dev? Put them with a senior. Or maybe one dev knows an extraordinary amount
about a particular component, then let them rotate across the rest of the team. In a sense, it's the 
rougher the better. 

Don't look at the weaknesses, look at the strengths that stand to be shared.


## AIs Think Very Different
Let's look at LLMs:

* Good: They know an absurd number of programming languages, libraries, tools, etc.
* Good: They think a lot faster than me
* Good: They're great at brainstorming and coming up with ideas
* Good: They're not clever (boring code is good code!)
* Bad: They make mistakes, sometimes really dumb mistakes
* Bad: They're still not great at design
* Bad: They don't innovate

Let's pair you up with a coding AI, will you do well? Yes, if you're **strong in the areas where the AI is weak**.

* **Mistakes** — If you're experienced, you'll be able to spot the LLMs' mistakes. If you're not experienced,
    then consider using a strongly typed language, use static analysis, and make heavy use of unit tests.
* **Design** — Similarly, experienced programmers have an advantage. But design isn't terribly important when the
    project is small, so inexperienced programmers still have a path to being productive with AI.
* **Innovate** — In my experience, innovation is 99% having a good problem and 1% having a good solution.
    LLMs don't offer anything here, it's our domain.

## Accountants Should Code
That last point, on innovation, is critical. The people with the best problems have the most to offer an AI.
I wrote a post recently called [Accountants Should Do Hackathons][acct]. The idea is that companies are 
filled with people who don't code but have good problems that cost companies gobs of money and time.

Give them Cursor. Show them how to use it. Show them how to help themselves. Problems will be solved.


## Who Wins?
If you're strong in one or more places that the AI is weak, you'll do well.

I don't think there's a lot of correlation to being good or bad as a programmer. In my experience, good 
programmers will declare that AI will benefit good programmers, and bad programmers will declare that AI
will benefit bad programmers. 

Realistically, it comes down more to personality traits. You'll do great if you have the persistence to
push it to the limits. That kind of person will get the most out of the AI's ability to brainstorm. 
Or if you have the skepticism to doubt and double check the AI's outputs, you'll protect yourself from
the LLM's weaknesses.


 [orig]: /blog/2022/04/11/three-plates
 [gh]: https://github.com/features/copilot
 [cur]: https://www.cursor.com/
 [xp]: https://asana.com/resources/extreme-programming-xp
 [acct]: https://timkellogg.me/blog/2024/07/26/hackathons
