---
layout: post
title: "Jump-Location: autojump for Windows"
categories:
 - jumplocation
 - powershell
---

A while ago I discovered [autojump][1] and quickly realized that it could 
change how I use a console. Autojump listens when you change directories
and keeps an index of the directories where you spend the most time. The `j`
command lets you search the index and `cd` to the most relevant search 
result. It's best if you just watch this video:

<iframe width="420" height="315" src="http://www.youtube.com/embed/tnNyoMGnbKg" frameborder="0" allowfullscreen></iframe>


Introducing Autojump for Windows (via Powershell)
-------------------------------------------------

[Jump-Location][2] is a Powershell implementation of autojump that I've
been working on. It does most everything that autojump does, but better.

For instance, after using the `j` Powershell cmdlet for a while, I 
quickly realized that I wanted to use it for more than a `cd` command.
I like using `pushd` and `popd`, so I made a `pushj` alias that uses
`pushd` (`Push-Location`) instead of `cd` (`Set-Location`).

I also realized that as a Windows user, you inevitably have to use Windows
Explorer for things like TortoiseSVN checkins. But mousing through the 
folder tree is a pain, so I made the `xj` alias to query `Jump-Location` 
and open up `explorer` to the result.

You can now use `Jump-Location` in conjunction with any command.  I can 
use the `getj` alias to open a file in notepad:

```
PS> notepad "$(getj ju)\Readme.md"
```

Enhancements to jumpstat
------------------------

Autojump provides a `jumpstat` command to display the index (and debug
why you didn't get the directory you expected). `Jump-Location` also
provides this command (as the `Get-JumpStatus` cmdlet alias).

Since Powershell deals in actual objects instead of text, the design of
`jumpstat` is a lot different from the original. This really comes out 
when changing the weights in the index. The documentation for the 
original instructs you to edit `~/autojump.txt`. While we still store
the index in a text file, you can just set the weight and save from
within Powershell.

For instance, setting a weight to a negative number will remove it from
search results:

```
PS> $record = jumpstat je bin
PS> $record.weight = -1
PS> jumpstat -Save
```

Go Try It!
----------

I highly recommend installing `Jump-Location`. Head on over to the 
[downloads area][3] and grab the latest zip file. Running `Install.ps1` will
register `Jump-Location` in all future Powershell sessions.


 [1]: https://github.com/joelthelion/autojump/wiki/
 [2]: https://github.com/tkellogg/Jump-Location
 [3]: https://github.com/tkellogg/Jump-Location/downloads

