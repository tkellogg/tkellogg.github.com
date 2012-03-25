---
layout: post
title: "Discriminated Unions in C# Mono Compiler"
date: 2012-03-10
comments: false
categories:
 - functional programming
 - fsharp
 - csharp
 - workflow
 - discriminated unions
 - language
---

Recently I've been using F# a bit. F# is .NET's functional language (the syntax of F# 1.0 was backward compatible with OCaml, but 2.0 has diverged enough to make it more distinct). Learning F# was a huge mind-shift from the C-family of languages. Of all the features of F#, like implicit typing, tail recursion, and monads, many people list discriminated unions as their favorite.  

Discriminated unions feel like C# enums on the surface. For instance, a union that can represent states of a light switch:

{% highlight ocaml %}
type LightSwitch =
| On
| Off

// And to use it, we use pattern matching:

let lightSwitch = getLightSwitchState()
match lightSwitch with
| On ->
    turnOnLight()
| Off -> 
    turnOffLight()
{% endhighlight %}


This example is really no different from C# enums. Discriminated unions, however, can hold data. For instance, consider when our light switch needs to also be a dimmer:

{% highlight ocaml %}
type LightSwith = 
| On
| Dimmed of int
| Off

// And to use it, we use pattern matching:

let lightSwitch = getLightSwitchState()
match lightSwitch with
| On ->
    turnOnLight()
| Dimmed intensity -> dimLightToIntensity intensity
| Off -> 
    turnOffLight()
{% endhighlight %}

In C# we would have had to rewrite this whole program to handle the new dimmer requirement. Instead, we can just tack on a new state that holds data.

When you're deep in the F# mindset, this structure makes perfect sense. But try implementing a discriminated union in C#. There's the enum-like part, but there's also the part that holds different sizes of data. There's [a great stackoverflow answer](http://stackoverflow.com/a/2321922/503826) that explains how the F# compiler handles discriminated unions internally. It requires 1 enum, 1 abstract class and _n_ concrete implementations of the abstract class. It's quite over-complicated to use in every-day C#.

Nevertheless, I really want to use discriminated unions in my C# code because of how easy they make state machines &amp; workflows. I've been brainstorming how to do this. There are several implementations as C# 3.5 libraries, but they're cumbersome to use. I've been looking at the source code for the mono C# compiler, and I think I want to go the route of forking the compiler for a proof-of-concept.

I'm debating what the syntax should be. I figure that the change would be easier if I re-used existing constructs and just tweaked them to work with the new concepts.

{% highlight csharp %}
public enum LightSwith
{
    On,
    Dimmed(int intensity),
    Off
}

// And to use

var value = GetLightSwitchValue();
switch(value)
{
case On:
    TurnOnLight();
    break;
case Dimmed(intensity):
    DimLightToIntensity(intensity);
    break;
case Off:
    TurnOffLight();
    break;
}
{% endhighlight %}

I've been debating if the Dimmed case should retain the regular case syntax or get a lambda-like syntax:

{% highlight csharp %}
var value = GetLightSwitchValue();
switch(value)
{
case On:
    TurnOnLight();
    break;
case Dimmed(intensity) => 
    {
        DimLightToIntensity(intensity)
    }
case Off:
    TurnOffLight();
    break;
}
{% endhighlight %}

I'm leaning toward the lambda syntax due to how C# usually handles variable scope. I've barely just cloned the mono repository and started reading the design documents to orient myself with the compiler. This could be a huge project, so I'm not sure how far I'll actually get. But this is a very interesting idea that I want to try hashing out.
