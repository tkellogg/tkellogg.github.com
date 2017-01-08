---
layout: post
title: "SQL is Insecure"
date: 2016-12-24
categories:
 - engineering
 - security
---

_**Note 1:** If this post leaves you confused, go read the discussion at [Lobste.rs][lob], but also
see the [x-post at dev.to][dev.to] as well as the [Reddit discussion][reddit]._

_**Note 2:** Also read [part 2](http://timkellogg.me/blog/2016/12/26/sql-predict-future)_

_**Note 3:** Github Enterprise, a Ruby on Rails application, [has been compromised][github] by a 
SQL injection vulnerability. This places this post in even greater relevance. Despite the
plethora of tools to deal with SQL injection and the excellent engineers that we hire,
we still get SQL injection vulnerabilities_

SQL is insecure, tell everyone. If you use SQL, your website will get hacked. Tell everyone.

I saw the news that the US Elections Agency [was hacked by a SQL injection attack][1] and
I kind of lost it. It's been well over two decades since [prepared statements][1.5] were introduced.
We've [educated and advised][2] developers about how to avoid SQL injection, yet it still
happens. If education failed, all we can do is shame developers into never using SQL.

I actually really like SQL, I've even made [a SQL dialect][3]. SQL's relational algebra is
expressive, probably more so than any other NoSQL database I know of. But developers have 
proven far too often that it's simply too difficult to know when to use prepared statements
or just concatenate strings — it's time we just abandon SQL altogether. It isn't worth it.
It's time we called for all government's to ban use of SQL databases in government contracts
and in healthcare. There must be utter clarity.

Part of the problem is the curse of the junior developer. They're experienced enough to 
realize that their employers will reward rapid development, but inexperienced enough to not 
understand the tremendous cost associated with sloppy code. 

As a senior develper you might note that a relational database provides the flexibility you
need to be successful. You know how to use prepared statements to prevent SQL injection. They
are a little more work than simply concatenating user input with executable SQL code, but not 
much more. The decision seems obvious: use SQL.

But 2 years from now, after you quit this job, a very junior developer picks up your code
with some very tight deadlines and a ton of management pressure. Does he know about 
prepared statements? Maybe, maybe not. Either way, it is a lot easier and faster to slop the 
code together and get shit done, so that's what he does.

It's time we accepted fate and let SQL die. Software runs our world now. When our software
fails, people's lives actually get messed up. Companies will always want software to be made
for cheap, but it's our ethical responsibility as senior developers to prevent future 
mistakes from being made under pressure.

Security is paramount. Your customers are worth it. Abandon SQL.


 [1]: http://www.reuters.com/article/us-election-hack-commission-idUSKBN1442VC
 [1.5]: https://en.wikipedia.org/wiki/Prepared_statement
 [2]: https://ics-cert.us-cert.gov/sites/default/files/recommended_practices/DHS_Common_Cybersecurity_Vulnerabilities_ICS_2010.pdf
 [3]: http://docs.aws.amazon.com/iot/latest/developerguide/iot-sql-reference.html
 [lob]: https://lobste.rs/s/tneut0/sql_is_insecure
 [dev.to]: https://dev.to/kellogh/sql-is-insecure
 [reddit]: https://www.reddit.com/r/programming/comments/5k6p8d/sql_is_insecure/  
 [github]: http://blog.orange.tw/2017/01/bug-bounty-github-enterprise-sql-injection.html
