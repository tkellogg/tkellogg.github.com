---
layout: post
title: "How Emotional is Trump?"
date: 2024-06-26
categories:
 - ai
 - LLMs
 - embeddings
 - psychology
 - politics
 - emopoint
image: /images/emotion/woman-angry.jpg
is_draft: true
use_mermaid: false
summary: 
    Join us as we analyze the emotional ebb and flow of Trump's social media posts
---

What if you could measure emotions? What would you do with that?

You absolutely can measure emotion using AI, or at least in a sense. I built
[emopoint][gh], a tool for analyzing emotions in text. If you want to technical details, I wrote about it in [part 1][part1].

The short story: The AI model encodes everything it sees into it's own "language" (all numbers, obviously), 
from which emopoint extracts just the emotion part so we can make cool graphs and charts.


# Trump: Something everyone can disagree about
Who is the most known person that evokes the biggest emotional response? Everyone I ask agrees it's Donald Trump (well,
my brother said Taylor Swift, but I fear that might be too controversial to analyze).

I [downloaded][dataset] all of Trump's Truth Social posts from 2022 and plotted the emotional intensity. To get a feel for
what that actually means, I compared it against the [most boring Wikipedia articles][boring] I could find. 

![a histogram showing the distribution of emotional intensity between anger and fear in two different datasets: Trump’s Truth Social posts and Wikipedia articles. The x-axis represents the intensity scale, ranging from anger on the left (-0.4) to fear on the right (0.4). The y-axis on the left represents the percentage of sample paragraphs from Wikipedia, while the y-axis on the right represents the percentage of Truth Social posts from Trump. The histogram uses two colors: red for Trump's posts and blue for Wikipedia articles, with an overlap area shown in purple. The title of the graph is "anger<-->fear," and a legend in the top left corner identifies the colors used for each dataset.](/images/emotion/trump-anger-fear.png)

**How to read this:** The middle is the least emotional, the right and left extremes are most. 

I see an obvious slant toward anger. The Wikipedia articles are a thin spike, and the bulk of Trump's 
posts sit to the left (the anger side). That seems right to me; I do see a lot of angry content from him.

Are anger and fear opposites? That's how I plotted them. In [Plutchik's wheel of emotions][wheel], he 
regards them as opposites because anger often leads to confrontation, while fear leads to avoidance. That makes a lot of
sense to me, but there are other ways to plot these as well.

Here's the same graph, but for joy vs sadness, and disgust vs surprise (categories from [Eckman's primary emotions][eckman]):

![a histogram showing the distribution of emotional intensity between joy and sadness in two different datasets: Trump’s Truth Social posts and Wikipedia articles. The x-axis represents the intensity scale, ranging from joy on the left (-0.4) to sadness on the right (0.4). The y-axis on the left represents the percentage of sample paragraphs from Wikipedia, while the y-axis on the right represents the percentage of Truth Social posts from Trump. The histogram uses two colors: red for Trump's posts and blue for Wikipedia articles, with an overlap area shown in purple. The title of the graph is "joy<-->sadness," and a legend in the top left corner identifies the colors used for each dataset.](/images/emotion/trump-joy-sadness.png)

It's a smooth curve, but leans toward the joy side. That means he frequently uses joy, and less often sadness. I
found this surprising, I didn't realize how often he uses joy. However, looking through his posts, I see it
strongly on display. In hindsight, I don't know why that's surprising. You can't build a movement using no
positive emotions at all.

![a histogram showing the distribution of emotional intensity between surprise and disgust in two different datasets: Trump’s Truth Social posts and Wikipedia articles. The x-axis represents the intensity scale, ranging from surprise on the left (-0.4) to disgust on the right (0.4). The y-axis on the left represents the percentage of sample paragraphs from Wikipedia, while the y-axis on the right represents the percentage of Truth Social posts from Trump. The histogram uses two colors: red for Trump's posts and blue for Wikipedia articles, with an overlap area shown in purple. The title of the graph is "surprise<-->disgust," and a legend in the top left corner identifies the colors used for each dataset.](/images/emotion/trump-surprise-disgust.png)


The bump in the _disgust_ side is interesting. It implies that Trump tends to dish out an extra helping of disgust
whenever he goes that direction.


# Can an AI really understand emotion?

Short answer: Yes, if it's in text.

Large language models (LLMs) are extremely good at picking up on language artifacts like word choice
or formal vs informal tone. In fact, they're trained expicitly to find subtle nuances.

Think about people. Some people are better than others at identifying emotion from pure text.
Other people are better at picking up on body language or tone of voice. Others are sensitive to highly 
contextual clues, like inside jokes or reading the subtext.

Most people can become better through practice and being exposed to it more. That's what these AI models
are doing during training, they're being exposed to a gargantuan number of situations and learn to see
patterns that might not be apparent to others. That's what all machine learning is: pattern matching.


![](/images/emotion/emotion-sources.png)

But that's just language. When two people talk, there's a whole lot going on:

* Language, word choice, etc.
* Body language and intonation
* Context, like the listener's state of mind, or current events (e.g. subtext, inside jokes, etc.)


## Aphasia

Oliver Sacks, a neurologist, wrote a chapter called [The President's Speech](https://plantainclan.com/wp-content/uploads/2021/09/Oliver-Sacks-The-PresidentS-Speech.pdf)
in his book. It's fascinating; if you have time for a 5-page read, do it. 

He talks about patients who have a condition called _**aphasia**_, where they truly _cannot understand
language_. Receptive aphasiacs can speak but don't understand words spoken to them. Yet they responded
dramatically with laughter and yelling to a speech by the then president of the United States. 
They apparently understood what was going on, yet they definitely (clinically) did not understand the words.

_Body language, intonation, context, current events..._

Many of the aphasia patients' friends and family
insisted that they couldn't have aphasia because they seem to follow conversations just fine.
Oddly, a lot of the conversations we have, day-to-day, don't involve facts that can't be derived from
the context. Language is only a part of what's communicated. 

LLMs are the reverse. They understand only the words, not everything else.


# What did we measure?
The emotion in the text alone.

Or, more precisely, the words intended to trigger emotion in the text. Words don't contain emotion,
they're just signals intended to trigger emotion in other people.

Trump in particular is good at creating key phrases and attaching emotion to them. Phrases like 
**_"Let's go Brandon"_** sound like _Joy_ but registers as _Disgust_ to people who know what it means.


## A Tour of 2022

Let's look at all of his [ posts throughout the year of 2022][data], individual posts instead of rolled
up into a histogram.

![](/images/emotion/trump-timeline-anger-fear.png)

_Note: 90th & 10th percentile show the posts that are more extreme, but not the most._

I see a general downward trend for use of fear. On the other hand, initially there was a sharp increase
(to the negative side) in anger, but then it settled in at a rough baseline throughout the remainder of 
the year

Those first few posts seem to slant hard away from anger and toward fear. Here's what the first one says:

> We have until SEPT 3rd until federal protections lift and the 2020 election can be DELETED FOREVER. Cast vote records PROVE fraud by machines. We need your help, SHARE THIS EVERYWHERE! https://frankspeech.com/article/save-your-county


## What are the Numbers?

In short, the numbers are label-less quantities. Don't pay too much attention to the exact number. Focus
on the general trends. 

* `-0.15` is angry
* `0.15` is fearful
* `-0.15` is more angry than `-0.1`
* `0.15` is more fearful than `0.1`

They follow the principles of ordering, bigger numbers are more intense.

It's extracted from AI embeddings. Each model uses this "secret language" that it uses to think about
concepts and how they interact. With emopoint, I found a way to extract specific concepts that are
normally difficult to measure and display them in graphable quantities. 

Each model learns it's own representation. And yes, using bigger and more capable models seems to result
in more "emotional information" being captured, at least in my experiments.


# What next?
**Voice!** I experimented with [CLAP][clap], a multi-modal model that understands both audio & text. The hope was
that I could also incorporate vocal intonation and other aspects of a live speaker. My hypothosis is that we'll
be able to capture even more emotion from Trump. Unfortunately, it got a bit complicated, so I bailed on it for
this post. I'll follow up!

**Debates!** Yes, the presidentail debates are this week, Trump v. Biden. I want to do an analysis between the
two speakers. I'm particularly interested in what topics evoke the most emotion, textually.

**Use cases.** There's a lot of business use cases for this sort of analysis. Even with it's shortcomings,
there's a lot of potential for scaling up or doing more objective analysis. For example, I want to integrate
it into [fossil][fossil], a social media algorithm optimized for the reader, to analyze an account's emotional
trend, or to block angry or fear-evoking content on particular topics.

Also, I did this for emotions, but you can do this for anything with oposites. The process is useful for
anything that we have an intuitive notion of, but where computers have traditionally failed. I've wanted
to build a sarcasm detector, a program that can identify if the speaker might be sarcastic (although, this
would be a lot more complex than just text analysis).

Be sure to checkout [emopoint on github][gh] or read [the technical details][part1] of how it works.

## So...is he?
Is he emotional? Maybe, what do you think? You can try looking at the data for yourself. Or maybe you have
something more interesting? Let me know, I'd love to hear about it.



 [gh]: https://github.com/tkellogg/emopoint/
 [part1]: /blog/2024/06/07/emotions
 [dataset]: https://zenodo.org/records/7531625
 [boring]: https://github.com/tkellogg/emopoint/blob/1d47df75886788546baabc7d2c6f239e587a3af7/lab/politics.py#L60-L92
 [wheel]: https://en.wikipedia.org/wiki/Robert_Plutchik#Plutchik's_wheel_of_emotions
 [eckman]: https://www.paulekman.com/universal-emotions/
 [data]: https://zenodo.org/records/7531625
 [clap]: https://github.com/LAION-AI/CLAP
 [fossil]: https://www.fossil-social.com/
