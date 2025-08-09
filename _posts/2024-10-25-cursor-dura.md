---
layout: post
title: "Cursor: How I rollback multi-file changes"
date: 2024-10-25
categories:
 - ai
 - cursor
 - git
 - dura
 - tooling
 - backup
 - version-control
image: https://cdn.pixabay.com/photo/2020/10/02/13/38/sea-5621150_960_720.jpg
is_draft: false
use_mermaid: true
---

Yay! [Cursor][cursor] is fun. All the way up until you accept some large multi-file change only to
realize it was a mistake, but there's no simple way to rollback. 

But there is. You can rollback! Use dura!

After New Years 2022 I spent a couple days building [dura][gh]. The tool is real simple,
it just makes Git commits in a background thread to a branch you never see unless you go
looking for it. Every time a file changes, it'll make a commit.

So now, when I find myself wallowing in a Cursor-inflicted hell hole, I just pop open my
git log ([`tig --all`][tig] for those that partake), and roll back to the change just prior
to my idiocy.

Back when I made it, tools like Cursor or Github Copilot didn't exist. It was worth it to
me simply just for that once-or-twice a year mistake where I royally mess up my repo. For
example, last week I was writing a script and made changes a bit too fast and ended up
deleting my whole working directory, including the script I was executing.

The beauty of dura is that you forget its there. It just silently does it's thing until one
day you desperately need it. It would be a terrible startup idea, so I released it open source.


## Using Dura
The [readme][gh] has good enough install instructions. It works very well on MacOS. The
[homebrew installer][brew] installs it as a service so you can truly forget about it.
It also works great on Windows and Linux, I just took special care with the homebrew installer.

Don't forget to watch a directory:

```bash
dura watch ~/code
```

It doesn't watch your entire computer, so you have to give it some clues as to where
you write code.

## Sharp Edges
For the most part, it works great. But I've gotten bitten when I try to revert to a dura
commit and it includes a dura commit. Once I tried pushing 1.5 GB of Git changes to Github.
Oops.

_**Don't push dura commits**_

The thing about dura commits is that it makes the commit before you update your `.gitignore`.
So dura commits end up including things like database files, passwords, etc. I just added
a git pre-push hook to check commit messages for it.


## Conclusion
Enjoy!

Well, actually, I hope you ignore it and forget it exists. But definitely go install it.



 [gh]: https://github.com/tkellogg/dura
 [brew]: https://github.com/Homebrew/homebrew-core/blob/master/Formula/d/dura.rb
 [cursor]: https://www.cursor.com/
 [tig]: https://jonas.github.io/tig/ 
