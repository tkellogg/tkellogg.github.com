---
title: Why Open Source Is Worth Your Time
layout: post
categories: 
 - engineering
 - philosophy
 - open source
---

One of my math professors said that our beliefs are shaped by our life experiences. Two people can logically come
to two very different lifestyle choices based on how they were raised, taught and friends that impacted them. The
lecture was meant to apply to religious and moral beliefs, but I think it also applies to how we grow professionally.

I have a coworker that keeps asking me how I know so much about software engineering techniques. Part of the answer
is that I had excellent teachers. I went to a great college, but also in my internships I had highly skilled
engineers teach me how to write unit tests
and design maintainable code. But after school and internships, I was responsible to teach myself. I've read tech 
magazines, programming books, blogs and answered stack overflow questions, but the best thing I ever did was
contribute to open source.

Learn By Imitating Good Work
----------------------------

It's like Pavlov's dog. We all get conditioned, many of us get conditioned to commit [acts of code treason][1] by 
surrounding ourselves with bad work. A lot of great coders surround themselves with  people who don't care about
quality, they let their skills slip. The best way to get better at your job is to watch a job well done. It's the 
same idea behind mentorships. When you get a chance to see things done well, it's easier to see how 
you could also do excellent work.

I got started learning Behavior Driven Design first by perusing through the [objectflow][2] code. I later followed
up the learning by reading books & blogs about BDD to get a better understanding of the intent. I also humbly 
learned why the service locator design pattern is actually an anti-pattern from working on [moq-contrib][3]. On
other projects I learned about safe deployment cycles, organizing people and support, and responding professionally 
to criticism, and much more.

Just to be clear, inventing your own open source project that no one ever uses doesn't count. This argument only
applies if your working on a relatively mainstream project. Writing code in your spare time is great and all, but
if you're trying to sharpen your skills I think it's not the most efficient way to do so. 

If you're not someone who lives in a tech hub like New York City or Silicon Valley, it's even easier to get stuck
in a job where seniority is valued over skill, and watch your motivation crumble. Sometimes it's hard to find a job
where you can surround yourself with people smarter and more motivated than yourself. But with open source, you can
pick your project and choose who you work with. Furthermore, when choosing teams, open source has a far richer
pool of coworkers.

It Grows Your Professional Network
----------------------------------

A lot of open source projects are driven by consultants and book authors. Normally you would have to pay them 
thousands of dollars to teach you how to write good code. But if you're contributing to one of their projects
they'll be happy to give you free code reviews and show you a better way to do what you've always been doing. Most
people who maintain highly used projets have a large professional network, especially if they're consultants or
speakers. By working closely with them on a project, you can often times utilize their professional contacts if
you ever need a job. 

It Makes Your Resume Shine
--------------------------

I haven't heard of any employers who would look at a resume and scoff, "whoops another one of those open source
duds got through our recruiter again". The fact is, most employers realize that working on open source projects
is doubling your experience. You get experience during your work day, and then work with an entirely different
team outside of work, sometimes on totally different technologies. Even if they don't understand that, they can
still see that you're a self-starter, driven, and are probably intelligent. 

Recently, people are actually beginning to use their open source work _as_ their resume. How better to vet a new
recruit than to see what they're actually producing? You can see how they design code, structure tests,
observe their source control habits and how they interact with other people. On open source projects _everything_
is public.

You Get To Give Back
------------------------

I've seen a number of open source projects that are used by thousands of people and developed by one. [VsVim][4]
is a great example. Jared Parsons has been working for years on the project in his spare time - many hours a week.
There are 10-20 regular bug reporters who report bugs and plead for new features. Sometimes they even get upset
when a VsVim upgrade breaks previous functionality. But very few people actually contribute pull requests back to
the project.

In order to stay relavent in our industry you'll probably use 5-15 open source projects in order to get a web 
application published (probably similar numbers for other types of applications). You save hundreds of hours a year
by using open source software. Often, the open source alternatives are superior to the COTS products.
Hundreds of thousands of developers use open source software, but there's probably only a couple thousand that 
actually give back. The .NET ecosystem is especially disproportionate. 

The Hard Part Is Knowing Where To Start
---------------------------------------

I know from talking to people that many developers want to contribute to open source projects. We're a good hearted
people - we all want to share and give back. But most don't know where to start. They'll make a resolution to go
home and read through some code over the weekend. But either it doesn't happen or it's so ungodly boring that they
never do it again. I really believe that most developers, if given a good place to start, would have little trouble
committing to a project for a significant period of time (years).

The problem is having an easy place to start and people to motivate you. The easiest way to get into a project is
to go through their issue tracker and find a bug that looks easy and fix it. Write tests, fix it, test it out and
send a pull request. It'll seem hard at first, but the more times you practice the easier it'll get.

Time To Get Involved
---------------------

If you're a developer who uses open source libraries and other software but have never contributed back, now is
as good a time as any to look around. I find it easiest if you find a project that you already are familiar with.
Look through the issue tracker and find some easy issues. Try writing an email to the maintainers of a project.
Ask them for a good place to start and some pointers. Keep in mind that you're pull request probably won't get 
accepted unless it's high quality code complete with tests, so take your time.

Since I'm a .NET developer, I've run into several .NET projects that are in high demand for help. I 
[put together a list of a few][5] moderately high profile projects that are high quality but need help. If you're
not a .NET developer, there's no end of projects that could use help. Just look at the software you use and think
about what you think is interesting. If you know of other .NET projects that are in need of help, [contact me][6]
so I can add them to the list also.

Contributing to open source grows your skill set, professional network and makes your resume shine. So
look our for yourself first - contribute to open source!


 [1]: /blog/2011/12/30/can-bad-code-ruin-your-career/
 [2]: http://objectflow.codeplex.com/
 [3]: http://moqcontrib.codeplex.com/
 [4]: https://github.com/jaredpar/VsVim
 [5]: /projects/open-source.html
 [6]: /contact/
