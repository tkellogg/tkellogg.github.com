---
title: Why I'm Not Going To Stop Posting Go Links
layout: post
categories:
 - haskell
 - functional-programming
---

On Friday, shortly after [posting a link][1] about learning Go to Lobste.rs I got this tweet:

<blockquote class="twitter-tweet" lang="en"><p><a href="https://twitter.com/kellogh">@kellogh</a> Since we&#39;re on the topic of link quality, may I ask you not to post Golang stuff to lobste.rs?</p>&mdash; Chris Allen (@bitemyapp) <a href="https://twitter.com/bitemyapp/statuses/424289998167212032">January 17, 2014</a></blockquote>
<script async="true" src="//platform.twitter.com/widgets.js" charset="utf-8"> </script>

We continued the conversation [via Twitter][2] and then a personal email. The short story is that Chris believes that Go's type system and core language is seriously flawed and that we should be promoting pure and complete languages like Haskell instead of broken languages like Go. I completely agree that Haskell is a beautiful language, and that Go pales in comparison. The thing is, I believe Go (and impure languages like it) are very powerful and we should be excited about them.

Somewhere down the line the conversation lead to this tweet:

<blockquote class="twitter-tweet" lang="en"><p><a href="https://twitter.com/kellogh">@kellogh</a> That doesn&#39;t sound like something somebody that understands Haskell would say. Are you sure? What did you build?</p>&mdash; Chris Allen (@bitemyapp) <a href="https://twitter.com/bitemyapp/statuses/424291827508727809">January 17, 2014</a></blockquote>
<script async="true" src="//platform.twitter.com/widgets.js" charset="utf-8"> </script>

I mean no harm against Chris or anyone else. He's very passionate and I understand the point he's trying to make, I just don't agree with it. There's a lot of people who share his view, but I haven't heard a lot of people who agree with mine. To clarify my position and respond to his question, I moved the conversation to email:

> Hi Chris,
>
> I tried making a MQTT client in Haskell. I was a beginner, it felt impossible to read I/O and hold the state that MQTT requires. I'm sure that someone who really knows Haskell wouldn't have any trouble writing an MQTT client. I tried for a while then gave up.
>
>That seems to be a common story though. Man tries Haskell, realizes he's not smart enough and gives up to pursue simple things like distributed systems. OK, that last part is a little snarky but it seems like a developer can only pursue a very limited number of hard things. I thought about becoming an expert in Haskell and writing networking apps, but it doesn't pay well. I can make my company much happier by working hard on distributed systems, embedded systems, organizing meetups, writing blogs, etc.
>
> Its all about a point that I've been honing in on over the last few years. Programming isn't an end goal. Even within computer science it isn't an end goal. Its always a means to an end. Its a way to have a computer achieve your goals for you. So I need to focus my effort on what gets me to the end goal.
>
> Its really easy to accomplish hard goals when you're working on a team. The trouble is, its really hard to find a team that writes exclusively in Haskell (or any pure functional language for that matter). Its probably because some idiot a long time ago decided that imperative programming is easier; it doesn't really matter though.
>
> People learn to program imperatively and the rest of their career needs to be spent unlearning. Sure it would be nice if it wasn't that way. I like languages like C#, Go, Scala and Rust because they introduce the learner to functional concepts at they're own pace without forcing it on them.
>
> Imagine if there was an activist group that wanted to get all American people to use chopsticks. They even have proof that if eliminates obesity and diabetes, so they swiftly conquer congress and pass a law stating that all dinnertime place settings must have the option of both chopsticks and fork and spoon. Do you think that most people are going to start using chopsticks after using fork and spoon all their lives? Probably not. But they might start using them incrementally as their friends start catching on.
>
> Obviously the analogy isn't perfect but it does have its merits. People will continue using what they know. With programming this has an even bigger effect since the entire team has to agree on the same technology stack.
>
> So the short story is that I think we should get excited about the impure languages like C#, Scala, Go and Rust. They're mainstream enough that it gives us hope that one day we can use a more pure language. Until that day I'm choosing to use whatever tools let me get stuff done.
>
> I hope this makes sense.
>
> Regards, <br/>
> Tim

I really don't want to start a flame war, but I can't stand how much hate is flying around the developer community. Everything has a purpose. There is no silver bullet, and there is no paradigm, process or technology that is always the best choice. Rather than flaming each other, lets spend time teaching each other about the caveats so we can all achieve our end goals.

 [1]: https://lobste.rs/s/qt8zcq/go_by_example
 [2]: https://twitter.com/bitemyapp/statuses/424289998167212032
