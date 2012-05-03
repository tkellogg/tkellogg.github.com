---
layout: post
title: Why don't more developers contribute to open source?
categories:
 - open source
 - philosophy
---

One night last weekend I couldn't sleep because I couldn't stop thinking about open source projects like
[StructureMap][1] where the maintainers are burnt out from giving all their time and energy. I recently
took over the responsibility of merging pull requests and fielding issues for StructureMap so Jeremy can
focus on life issues and his work with [FubuMVC][2]. Regardless, it remains one of the most highly used
IoC containers for C#.

I had a lot of thoughts rushing through my head about how StructureMap is not alone. There's way too many
projects that die simply because the maintainer is spread too thin. If each one of us contributed just a 
little bit of time to the open source software that we love, we could prevent hundreds of valuable projects
from going stale or dying. 

I ended up giving up on sleep and [wrote a blog post][3] that stayed on the front page of hacker news for 
a while. It turns out that there's a lot of people that would love to give back to these projects but are
intimidated in one way or another. I'm not a big fan of speculation, so I decided to throw together a [quick
survey][4] and sent it out to some peers and coworkers.

<div id="chart1"><!-- first chart goes here --></div>

The inexperienced are intimidated
---------------------------------

It's a bit of a chicken-and-the-egg problem. For people who either infrequently or never contribute
to open source, the one of the largest reasons is that they're scared that their code won't be good enough. Many
of the friends and coworkers that mentioned this issue to me also realized that the best way for them to get to a
level of comfort with their own code is probably to actually work on open source projects. But without working
on open source projects, their code isn't getting better.

The largest response for infrequent contributors was that the code base is too large or intimidating to 
navigate and learn. The most useful projects out there are large and complex, so this probably won't change.
However, people who often contribute to open source projects tend to have an inclination toward soaking in
large code bases. It's a learned skill that is obtained either by changing jobs every month or by working on
open source projects.

The experienced love contributing
---------------------------------

Of the people who gave frequently (more than a few times a month) one of the overwhelmingly biggest reasons 
for continuing to contribute was that they just plain enjoy it. For myself, I know I get a sense of
satisfaction, maybe even excitement, when a pull request is accepted. One respondant said that they like
making things that their friends and coworkers find useful. I can echo that! 

<div id="chart2"><!-- second chart goes here --></div>

The experienced also don't mind digging into code
---------------------------------------------

The next biggest reason to contribute was that, when something isn't working, they crack open the code to
see what's going wrong. A lot of times they fix the problem and end up sending a pull request if they fix it.
I think this is the biggest advantages to open source software. 

In the past I've gotten bit by closed source software (I'm looking at you,
Microsoft) where there's something really simple that's not working, but I can't change it because I can't
recompile the source code. Other times I really just want to see what's going wrong but I can't look at the 
code because it's proprietary.

What if we worked together?
---------------------------

While talking to lots of people about open source, it became abundantly clear that a lot of people simply
don't know where to start. What would happen if we started a [meetup group][5] to pair up and work through
code together? It could be a convenient place where the inexperienced could learn from the experienced,
and where ideas could spread organically.

I'm in the planning stages of starting [such a group][7] where I live in Boulder. If you or someone you know
lives or works in Boulder, you should definitely [get in contact][6] with me. I'm open to suggestions and
advice. I'm also looking for people to help out and companies to sponsor.


 [1]: http://stackoverflow.com/a/8785437/503826
 [2]: http://mvc.fubu-project.org/
 [3]: /blog/2012/04/22/why-open-source-is-worth-your-time/
 [4]: http://www.zoomerang.com/Survey/WEB22FJY9L3RZ3
 [5]: http://lists.openhatch.org/pipermail/events/2012-April/000304.html
 [6]: /contact/
 [7]: http://www.meetup.com/OpenHatch-X-Boulder/

<script type="text/javascript" src="/public/raphael-min.js"> </script>
<script type="text/javascript" src="/public/g.raphael-min.js"> </script>
<script type="text/javascript" src="/public/g.bar-min.js"> </script>
<script type="text/javascript" src="/public/backbone-min.js"> </script>
<script type="text/javascript" src="/blog/open-source-charts.js"> </script>
<script type="text/javascript" src="/blog/open-source-results.json"> </script>
