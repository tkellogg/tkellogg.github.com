---
layout: default
title: Projects
---


# Hire Me

I work with companies to navigate AI. See my [consulting](/projects/consulting) page for more information.

# Open Source Projects

Over time I've contributed to a number of open source projects. I've become aware of several projects that do 
excellent work and solve great problems, but are in need of help. I started [a list](/projects/open-source.html) of
several of such projects. I encourage everyone to 
[contribute to open source](/blog/2012/04/22/why-open-source-is-worth-your-time/), so please look over the list and
suggest any that I might be missing.


## [dura](https://github.com/tkellogg/dura)
You shouldn't lose work if you're using Git. I wrote more about it [here](https://timkellogg.me/blog/2022/10/04/dura).
It's a daemon that automatically makes commits, but not to your current branch. In practice, it's nearly
invisible until you seriously mess up, and, in a moment of panic suddenly realize you're find because you've
been running dura in the backround all along.

## [fossil](https://github.com/tkellogg/fossil/)
An AI-driven mastodon client that works for me. It groups posts by similar content, so I can spend less time
in social media while still retaining all the benefits I get from it. I wrote about it [here](https://timkellogg.me/blog/2023/12/19/fossil) and [here](https://timkellogg.me/blog/2023/12/21/alignment).

## [Jump-Location](https://github.com/tkellogg/Jump-Location)
A Windows PowerShell take on [autojump](https://github.com/wting/autojump). I haven't used it in years, but
[Scott Hanselman](https://www.hanselman.com/blog/jumplocation-a-change-directory-cd-powershell-command-that-reads-your-mind)
promoted it on his blog. It's been largely replaced by Z-Location (which I appreciate, since I don't actually
have time to maintain Jump-Location).

## [Moq.AutoMocker](https://github.com/moq/Moq.AutoMocker)
I started this and handed it off to the Moq organization. It's an inversion of control container that generates
mocks for dependencies. So you can say, `mocker.Get<UserFetchService>()` and it'll return an instance of a
concrete `UserFetchService`, but with all it's dependencies mocked out. I don't maintain this anymore, but it
is well-maintained by a few guys in Washington state.

