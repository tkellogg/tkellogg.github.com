---
layout: post
title: "I Taught My 8yo Subduction Zones With NotebookLM"
date: 2024-09-29
categories:
 - ai
 - LLMs
image: https://cdn.pixabay.com/photo/2024/03/09/16/59/typewriter-8622984_960_720.jpg
is_draft: false
use_mermaid: false
---

I'm blown away by [NotebookLM][link]. It seems there's nothing too hard to learn when you 
can get a podcast-style overview and then ask any question in an interactive learning session. 
So let's think big; why can't my 8 year old child learn about cutting edge PhD research? How 
far can we get?

## Finding An Article
First, I needed a topic, so I went to [phys.org][phys]. I've spent a lot of
time browsing articles there in the past. A lot of it is open access, so the full article is
available, and it's got a huge variety of topics.

[![screenshot of phys.org home page](/images/phys-org.png){: .backdrop}][phys]

I clicked on an article at random, ["Mesozoic intraoceanic subduction shaped the lower mantle beneath the East Pacific Rise"][article].
That title sounds very complicated, I have no idea what it means but it seems like geology.
I wonder how much my daughter will understand 🤔. Only one way to find out...

[![screenshot of the article, from ScienceAdvances, the title and the first part of the abstract](/images/science-mesozoic.png){: .backdrop}][article]


## The Podcast
In [NotebookLM][link], I created a new notebook and added the link to the article as a source.
Immediately there is a text sumamry available. It's still fairly terse, even for me, so I
generated an "audio summary". This is the "podcast" that's been all the rage across the internet.
It creates a podcast, where the two hosts banter back and forth to break down the concepts.

I have to say, I've never been a fan of podcasts, but I'm sold. They take the complicated
concepts and defuse your "fear instinct" by asking the dumb questions for you, and providing
answers that an 8 year old can understand.

Well, kinda, let's discuss.

Here's the podcast:

<audio controls>
    <source src="/images/subduction-podcast.mp3" type="audio/mpeg">
    Your browser does not support the audio element.
</audio>

## Following Up

The kid was completely engaged for the entire 9 minute audio clip. Y'all don't know her, so
I'll say that this sort of attention only happens when her brain is fully engaged. It's honestly
quite rare, she often gets scared off by big ideas and loses attention.

They described the _MTZ (Mantle Transition Zone)_ as feeling cooler on the surface
when the tectonic plates are thicker and hotter when the plates are thinner.

My girl instantly responded:

> Yeah! It got hotter when I dug a really deep hole in the back yard!

😂 Okay that's funny. She's probably missing some things, but clearly she's mentally engaged and
has some level of understanding of what's going on. Their style of bantering back and forth is 
simple enough to keep even an eight year old glued while also not shying away from more 
complex topics.

She stayed engaged the entire time. After it was over, she told me she was afraid. Why? Because
she's worried that we're floating and constantly in motion, where before the podcast she thought
ground was solid.

🤯 She gets it. Well, maybe not the core of the research, but she really learned things.


## Asking Questions
NotebookLM lets you ask questions, and it'll answer based on the sources. Her burning question was,
_"does that mean dinosaurs could have been flying overhead millions of years ago?"_

To which it responded with a rejection, as it only answers from the provided sources:

> The sources primarily discuss geological research about the Earth's mantle and do not contain information about dinosaurs. Whether or not dinosaurs could fly depends on whether they existed during a time when flight was possible, and what kind of animal qualifies as a "dinosaur."  You may want to consult resources on paleontology and the history of flight to research this question.
> 
> It is worth noting that the Mesozoic Era, which lasted from about 252 to 66 million years ago, is the era when dinosaurs lived . The sources mention this era several times, as they are examining evidence of geological activity during that time, particularly a period of intraoceanic subduction they believe began between 250 and 240 million years ago.

This is a great feature, but obviosly a bit annoying. I'd love for it to help me find new sources
about paleontology to satiate my curiosity.

I don't think this is a contrived 8yo-specific example. My brain wanders a lot, and I could see
myself getting mildly annoyed with a rejection rather than helping me find new sources to answer
my burning curiosity.


# Conclusion
I'm still blown away, maybe even more so. It has it's limits, I don't think my eight year old child
is getting a PhD in geology anytime soon. On the other hand, this was only 9 minutes. I could see her
spending more time on this and producing a science fair project that demonstrates an understanding
that goes deeper than just subduction zones, actually understanding the core research on some level.

But NotebookLM wasn't designed for kids. This is absolutely revolutionary technology for adults.
My wife commented about how easy college would have been with something like this, that can read
30 papers and distill the concepts for you.

Her take was, _"kids have it too easy these days"_. But my take is more, _"why can't an 8 or 9 year old
keep track of current PhD-level research?"_ It seems absurd, but maybe it's not. Maybe it's all about
how we approach education. It seems that AI is creating a lot of unexpected opportunities.

Regardless, I'll definitely be using NotebookLM to keep track of new research in my own field.


<style>
.backdrop {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    border-radius: 4px; /* Optional: rounds the corners */
    }
</style>

 [link]: https://notebooklm.google/
 [article]: https://www.science.org/doi/10.1126/sciadv.ado1219
 [phys]: https://phys.org/
