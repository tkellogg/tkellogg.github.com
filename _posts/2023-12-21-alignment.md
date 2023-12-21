---
layout: post
title: "Are They Actually Afraid of AI?"
date: 2023-12-21
categories:
 - llm
 - opensource
image: https://gist.github.com/assets/437044/e79213c9-e26d-47ef-9fb5-ac45ebd24696
is_draft: false
---

Yesterday I talked to a longtime friend of mine. He works about as far away from tech as you can imagine.
He does maintenance for summer camps, so basically a lot of plumbing and odd jobs fixing houses and buildings.
He's always been vehemently opposed to AI, which has always added a flare of excitement to our conversations
given that I, ya know, work in AI.

I told him about [the mastodon client I made][fossil] that uses AI to automatically categorize and group
posts together, so that I can spend less time on social media. His immediate response was, "oh, can you set
me up with that?".

> I hate things I don't understand (that aren't aligned to me)

We, as a society, are getting fairly comfortable with working with technology that we don't understand.
How many of us hop into a car or a bus without any concept for how it actually works? Heck, most people don't
realize that [ammonia is more important to the world than silicon][amonia]. We're fine with not understanding 
how things work, the issue is when those things aren't aligned to us.

![a close-up of a Middle-Eastern descent farmer's hand, gently releasing a handful of dark, nutrient-rich soil. The soil, infused with fine granules of ammonia-based fertilizer, streams between the fingers against a softly blurred background. This backdrop features a sunlit, lush green farm field, bathed in warm, golden sunlight. The image evokes a strong sense of agriculture and the nurturing connection between the farmer and the earth.](https://gist.github.com/assets/437044/63412740-d5ec-4ab5-8aa1-f176d0feb8dd# inline)

A few weeks ago, Bruce Schneier wrote a post called [AI and Trust][schnier] in which he talked about how companies 
are aligned to sustaining themselves, but since we occasionally benefit from that alignment we get tricked 
into believing that they're aligned to us, that they're our friends. He argued (persusasively), that AI will
be aligned to the companies that create it, although it might appear they're aligned to us at times. Cory Doctorow's 
[enshittification][enshittification] is the same idea, in principle.

To fix it, it seems clear that the organizations making AI and applications of AI should be aligned to us, 
regular people.
Bruce Schneier says that only governments are aligned to us. Although, I suspect that if you subsitute
"governments" with select autocracies that perform atrocities, like "North Korea" or "Myanmar", then it might not
sound great to blindly trust all governments to always act in the best wishes of it's people. I think open source
provides a model that might be a little closer to what we need.

By nature, open source serves the people who create it. That's true of all software, but there aren't any
gatekeepers for open source. Anyone can start a project or contribute to one. Participating in open source
is exercising the power to control your own destiny. Your contributions don't have to be aligned with some company,
they just have to be aligned to the project, and if you can't find such a project, you simply create your own
project.

For fossil, my [mastodon client][github], I had a theory that social media is good at it's heart. The bad aspects
that we talk about are artifacts of enshittification, companies designing social media algorithms to keep you
on their site, viewing ads. The thing is, I don't actually want to be engrossed in social media, I just want
to see the good stuff in 10 minutes, post my own content, and then get out. I want social media that works for me.

![...](https://gist.github.com/assets/437044/1de5c3d1-149f-4bcc-a4d3-b72530f4400a# inline)

Prior to Large Language Models (LLMs), building something like this would be quite difficult. Only the largest social
media companies could do it, and they wouldn't, of course, because it doesn't help their bottom line. But now
we have this commodity AI where we can reduce the meaning of a chunk of text to numbers and 
[do math on it][embeddings]; compute similarity between two posts, or cluster similar posts together in my 
timeline. The options are wide open, and we're just beginning to explore it all.

Open source is a powerful force for correcting corporate misalignment. I think of open source like "capitalism
without the money". If a project needs a small alignment adjustment, contributions work. If it needs a big
adjustment, then you fork it and start a new project. The cool part about forking is you don't have to start
from scratch, you can take the entire old project and just replace the parts that don't work for you.

For fossil, I anticipate that it's not going to work for a lot of people. That's fine. They can contribute back,
or fork it, or rewrite it in a totally different direction. Whatever suits them. It's an application of AI that's
fully aligned to "the people", rather than some corporate entity, hence why my friend who's terrified of AI
has absolutely no fear of this. He trusts that it's aligned to what he wants.

I'm not sure open source has all the answers, but it does seem like a good option for checking the balance of
power between the public and corporations. I'm old enough to recall how Firefox did this to Internet Explorer, or
how Linux did this to corporate Unix flavors. In all cases, it forced the corporate option to better serve their
users. Open source isn't perfect, but it certainly is a powerful tool for societal alignment. I wish goverments 
leveraged open source more readily.


# Conversation

* [Mastodon](https://hachyderm.io/@kellogh/111618404480295496)
* [LinkedIn](https://www.linkedin.com/posts/tim-kellogg-69802913_are-they-actually-afraid-of-ai-activity-7143578361078902785-TX4v?utm_source=share&utm_medium=member_desktop)



 [fossil]: https://timkellogg.me/blog/2023/12/19/fossil
 [github]: https://github.com/tkellogg/fossil/
 [amonia]: https://www.economist.com/christmas-specials/2022/12/20/deadly-dirty-indispensable-the-nitrogen-industry-has-changed-the-world
 [schnier]: https://www.schneier.com/blog/archives/2023/12/ai-and-trust.html
 [enshittification]: https://www.eff.org/deeplinks/2023/04/platforms-decay-lets-put-users-first
 [embeddings]: https://simonwillison.net/2023/Oct/23/embeddings/
