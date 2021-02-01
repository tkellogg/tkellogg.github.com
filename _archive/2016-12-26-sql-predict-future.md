---
layout: post
title: "SQL is Insecure Part 2: Protect us from the idiots"
date: 2016-12-26
categories:
 - engineering
 - security
---

On Christmas Eve I wrote a post titled [SQL is Insecure][1] in which I asserted that, because
SQL has been systematically used incorrectly, that no one should use it. In this post I want
to discuss why a complete ban of SQL is actually a good idea: while you personally are smart
enough to stay away from the traps, it's still you're responsibility to prevent others from
falling into those same traps.

**Idiots**

In the original post, I referred to "junior developers" as a person who wants to "get shit done"
in order to please management, sometimes introducing things like SQL injection vulnerabilities.
The truth is tenure or experience have little to do with it. These developers are just idiots.

What makes an idiot developer? I know I've been an idiot developer in the past. I like to think 
I'm too experienced to make those mistakes these days, but honestly, I bet I would still make those 
same mistakes if you put enough pressure on me. So yeah, crazy amounts of management pressure
to deliver results can also produce idiotic engineering decisions. If you're a manager, I want
to encourage you to create a culture of good work/life balance. 

It's not just current culture. At a previous company, I worked for a manager that 
actively helped me grow professionally. He was one of the few managers that I've had in my career
that actually had my best interest in mind. It was a great environment. And then upper management fired him
and replaced him with a VP willing to hire idiot developers to get shit done.

So, lesson learned: companies change, and they're incentivized to change for the worse.
Always assume that an idiot will be working on your code in a few years.

Other people point out that [government contractors aren't encouraged to spend time on quality][3].
The spark that caused me to write the original post was caused by a [poorly done government contract][4].
Sure, there's a lot of broken things about how government contracts are conducted, these need to be
fixed, but the consequences of SQL injection are hurting real people, right now. Today [governments
are being manipulated][5.1], [money is being stolen][5.2], [identities are being compromised][5.3].
We could make laws and require certifications and licenses to make software. All this would
probably work, but not soon enough.

I'm a software engineer, not a congressman or a manager. I might not be able to make laws or mold
company culture, but there are still things I can do to make the world around me a safer and
better place. 

**Idiot Proof**

What does the world look like through an idiot developer's eyes? I know I've been there — exhausted,
looking for the quickest and fastest way to get things done and deliver results. Of course I plan
to come back and pay the technical debt, but if I'm completely honest with myself, that's never 
going to happen.

It's right there:

> looking for the quickest and fastest way to get things done

To write idiot-proof code, make sure the quickest and fastest way to get things done is safe
and secure. You might introduce an ORM to wrap your SQL database, but what happens when it
doesn't work? Remember, the idiot is looking for the quickest and fastest way to get things done.
The go-to tool is `mysql_query('SELECT * FROM users WHERE id = ' + user_id + ')'`. Maybe the ORM isn't
even broken, it could be that the idiot developer just doesn't want to take the time to understand
how it works.

It's not that SQL **can't** be used securely, it's that the most obvious way to use it is inherently
insecure. Most of the literature teaching SQL demonstrates it being used in a way that's vulnerable
to SQL injection. Your cool ORM framework might be idiot-proof, but a true idiot will bypass the
ORM.

**Other Ways to Idiot-Proof**

It doesn't stop at SQL or security, here's some other ways to isulate yourself from the damage
caused by an idiot:

* Don't manually allocate memory — don't use C, use a garbage collected langauge. It's too easy to 
make a fatal mistake. You might be smart enough, but don't trust that the next guy is.
* Don't roll your own crypto/web framework/database/etc. You might be smart enough to understand
the complexity, but the next idiot is going to screw it up and cost your users.
* Avoid synchronizing code for thead safety. You're probably smart enough to deal with concurrency bugs
and avoid leaked data, but the next exhausted engineer will mess it up. Use [actors][6] instead.

How else can you idiot-proof your code? What else can to do, as a software engineer, to make the
world a safer and better place?


 [1]: http://timkellogg.me/blog/2016/12/24/sql-is-insecure
 [3]: https://lobste.rs/s/tneut0/sql_is_insecure/comments/hnpck2#c_hnpck2
 [4]: http://www.reuters.com/article/us-election-hack-commission-idUSKBN1442VC
 [5.1]: https://www.wired.com/2016/08/hack-brief-fbi-warns-election-sites-got-hacked-eyes-russia/
 [5.2]: http://siliconangle.com/blog/2016/03/07/bangladesh-bank-claims-100m-stolen-via-hack-of-its-us-federal-reserve-account/
 [5.3]: http://www.denverpost.com/2016/12/14/yahoo-hackers-stole-information-accounts/
 [6]: https://www.destroyallsoftware.com/talks/boundaries
