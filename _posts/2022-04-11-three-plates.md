---
layout: post
title: "Three Plates"
date: 2022-04-11
categories:
 - engineering
---

"Why don't you have to test your tests?", someone asked me. Well, it's like the three plates method.
You grind one test against some code until the two are perfect. That's unit testing.

The [three plates method](https://ericweinhoffer.com/blog/2017/7/30/the-whitworth-three-plates-method)
is a process that creates the flattest plates, with the highest precision. The goal is to create the 
flattest surface possible. It doesn't use any power tools, just 3 granite plates. 

1. Take plates `a` and `b`, grind them together for a while
2. Grind `b` and `c` together for a while
3. Grind `c` and `a` together for a while
4. Repeat

This process takes a while, but eventually you find yourself with three of the flattest, smoothest 
surfaces. At first, they're very rough with bumps, scars and points. But through this process the 
blemishes break off iteratively to reveal a flat, smooth, beautiful surface.

Unit testing is a lot like this. I like to think TDD means that you write the tests first, but it's
not actually important what came first. It's the process of rubbing two chunks of code together to
smooth out the bumps. It's not like I spit out perfect test code on my first try, it takes iteration,
and a lot of back-and-forth between fixing test code and fixing prod code. But eventually, I'm left
with two pieces of code that complement each other, prove each other.

Unit testing is a good technique for honing "surfaces". But that's the thing, you can't rub two
buildings together to create better buildings. Unit testing is an excellent tool for what it does,
but it needs to be complemented by a larger toolbox. Unit testing creates fine-tuned individual
units, but you need integration & functional tests to make sure those units are arranged together
correctly. Prior to all that, formal methods can be a great way to prove out a design.

