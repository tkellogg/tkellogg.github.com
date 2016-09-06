---
title: Was C For Hipsters?
layout: post
categories:
 - programming
 - history
---


Last week I came across [this tweet][1]:

<blockquote class="twitter-tweet" lang="en"><p>When C went viral was it crapped on as much as JavaScript is now?</p>&mdash; deech (@deech) <a href="https://twitter.com/deech/status/564178220908417024">February 7, 2015</a></blockquote>
<script src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

It's true, JavaScript gets a lot of hate these days for various reasons. Some of those reasons are definitely legitimate 
concerns, but a lot of it is just noise. Still, this could be an interesting case study into computer programmer's 
history of hating languages, so I shot a quick email off to my dad.

> Hey dad,
>
> I saw this tweet and I want to know the answer. Since you were around when C came out, did it have a bad reputation 
> for making things too easy? Like too much abstraction or whatever? Like the crap JavaScript gets today
> 
> Tim

One of the benefits of having a dad that's been an realtime embedded C developer for most of his career is that I 
can ask him questions like this and I get really interesting replies. Sure enough, he delivered (minimal editing by me):

> Well, back then there was no Internet, so it was harder to assess reputation.
> 
> C did not have a bad reputation about being too easy.  There was, however, a lot of concern about "tight code" and 
> efficiency (of the code), and how the compiler measured up to a competent assembly programmer. 
> 
> When I switched from assembly to C in 1981, there was never any question about programmer efficiency 
> improvements.  The rough rule "10 lines per hour, regardless of the language" was true for both.  But a line of C could do the 
> work of two to eight lines of assembly.
>
> By programming at a higher level of abstraction with C, there were entire classes of bugs in assembly that went 
> away.  For instance, using a 'branch less than' vs a 'branch less than or equal' vs 'branch greater than' vs ...
>  
> In assembly, it took *much* more effort to clearly document the intent, because there were so many more saplings in 
> the forest to clutter the view. There were labels that were truly part of the logical structure (loops, etc), and 
> then a lot of distracting labels just to jump around the linear execution of the assembly code.
>  
> The early C compilers did tend to be buggy, and it was not uncommon to 'code around a compiler bug' (hopefully with 
> a comment explaining the rational). 
>  
> The optimizations tended to be poor, too.  I once created a bunch of commotion on the GCC list, when I compared 
> the size of the generated code to a commercial compiler.  I must have hit a nerve somewhere, because within a couple of 
> days the GCC code size was reduced by about a third.
>  
> In the early days of C, debugging was almost always done at assembly level.  In a way, this was good because the 
> engineer was always 'peer reviewing' the compiler's code generation.  But efficiency again increased when symbolic 
> C source level debuggers became widely available. 
>  
> Early Windows programming in C was painful, because the engineer needed to set up everything manually.  Typically, 
> this would take a couple pages of C code, with arcane incantations and rituals.  When Microsoft introduced Visual Studio 
> to automatically hide and abstract most of the setup, then I think the concern "too easy" perhaps became more 
> prevalent.
>  
> The other part of "too easy" came from not needing to debug at the assembly level -- programmers lost a feel for the 
> implementation of the C code.  I saw this happen a lot, and it was a significant handicap for some of our guys.
>  
> +++++++++++
>  
> For a time, there was the thought "real men program in assembly".  But the economic advantages of higher abstraction, 
> the arrival of (mostly) bug-free compilers, and source-level debuggers pretty much killed that mindset.
> 
> IMO, a good systems-level/embedded software engineer should at least once walk through and understand the assembly 
> implementation of interrupt vectors, a task context switch, multi-precision math, pointer indirection, subroutine 
> register calling convention, implementation of high-level data structures, etc.


 [1]: https://twitter.com/deech/status/564178220908417024
