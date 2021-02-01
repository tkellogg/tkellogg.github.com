---
layout: post
title: "Cold Paths: Where Bugs Live"
date: 2021-01-29
categories:
 - engineering
---

*Faced with yet another crisis caused by a bug hidden in a cold path, I found
myself Googling for a quick link to Slack out to the engineering team about cold paths.
Unfortunately, I can't find a focused write-up; and so here I am writing this.*

A **cold path** is a path through the code or situation that rarely happens. By contrast,
**hot paths**
happen frequently. You don't find bugs in hot paths. By nature, bugs are found
in places that you didn't think to look. Bugs are always in cold paths — every bug is
found in a path colder than all the paths you tested.

As an absurd example, here's an `if` statement that happens once every 4 years on leap day:

```python
if datetime.now().strftime("%M/%d") == "02/29":
    drop_database("students")
```

This seems like a mistake. Why do mistakes like this make it into production?

 1. Mocking `strftime` for a unit test seemed too hard at the time. Too much pressure to 
    deliver.
 2. Manual testing didn't catch it because it can't. It doesn't happen often enough.
 3. Code reviewers weren't paying attention because they were tired from an operational
    incident that woke them the night before (or drunk, babies, ADHD, caffeine deficiency, work deadlines or
    any other quite reasonable explanation for not being at peak performance).
 4. Code coverage metrics didn't highlight it because it was only 1 line of missed coverage.
 5. Integration/functional/UAT tests didn't catch it because we can't wait for 4 years 
    between software releases.

Processes like unit testing and code review do indeed catch lots of bugs, but they're not
perfect. They fail for many reasons.

Here are some real world "cold paths" with big consequences:

* [An outage caused by an expired TLS certificate](https://blog.thousandeyes.com/impacts-expired-tls-certificate/)
* [YouTube overflowed a 32-bit `int` "views" counter on Gangnam Style](https://arstechnica.com/information-technology/2014/12/gangnam-style-overflows-int_max-forces-youtube-to-go-64-bit/)
* [Y2K](https://en.wikipedia.org/wiki/Year_2000_problem)
* [Northeast blackout of 2003](https://www.nytimes.com/2003/08/15/nyregion/blackout-2003-overview-power-surge-blacks-northeast-hitting-cities-8-states.html)

Rare events are [hard to predict][blackswan]. That's just the nature of them. As engineers,
I belive it's our responsibility to do our best to try harder and get better at planning for
these rare bugs. But is that it? Try harder? 

I think we can do better. The remainder of this article are strategies I've seen throughout
my career.


# Avoid cold paths
I watched one of Gil Tene's many amazing talks on Azul's C4 garbage collector (not [this talk][giltene],
but similar) where he claimed that normally it takes 10 years to harden a garbage
collector. Azul didn't have 10 years to produce a viable business, so they avoided almost all
cold paths in the collector and they were able to harden it in 4 years (I never tried verifying
this claim).

For a garbage collector, this means things like offering fewer options, or having a simpler
model to avoid cold paths around promoting objects between generations. For your app it will
mean something different.

## Takeaway: Less customization → less testing surface → less bugs
You can **test less** to achieve high quality by **reducing the size** of your application. 
Less edge cases is equivalent to less testing surface area, which implies less testing work
and fewer missed test cases.

{% raw %}
$$effort = \frac{size}{quality}$$
{% endraw %}

# Avoid fallbacks
While I worked at AWS I had this beaten into my skull, but thankfully they've published guidence
an excellent piece titled ["Avoiding fallback in distributed systems"][aws]. The hope is that, 
when system 1 fails you would like to automatically fallback to system 2. 

For example, let's say we have a process that sends logs to another service. For the hot path, we 
send logs directly via an HTTP request. But if the log service fails (e.g. overloaded, maintenence,
etc.) we fallback by writing to a file and have a secondary process send those logs to the service
when it comes back.

* System 1: directly send logs to server
* System 2: send asynchronously via file append

## Takeaway: Always fallback
If system 2 is more reliable than system 1, then why don't we always choose system 2? Always write
to the file and ship logs asynchronously rather than send directly to the server. This is 
surprisingly strong logic that isn't considered often enough.

In cases where fallback can't be avoided they suggest always exercising the fallback. For example,
on every request, randomly decide to use either system 1 or system 2, thereby ensuring that the cold
path isn't cold.


# Know your capacity for testing
In [files are fraught with problems][fraught], Dan Luu demonstrates that it's unexpectedly
difficult to write a file correctly. Juggling issues like handling random power loss or 
strange ext4 behavior becomes a full-time job. It's a lot to keep in your head, just to 
write a file. 

Is it better to:

1. Ignore the cold paths and hope for the best
2. Correctly implement & test each file write event and ship late
3. Use a system that does it correctly for you, like MySQL or SQLite

Choice #3 delegates the testing of all those pesky cold paths to a 3rd party. 
Therefore, #3 is always the best choice, unless your company is in the file writing 
business (e.g. you're AWS and working on DynamoDB or S3).

Alternnate take on the same idea: [Choose boring technology][boring]


# Conclusion
Reducing the size of the application leads to less bugs. The trick is to avoid doing this
at the expense of the user. Find cold paths that don't add business value and kill them.


 [giltene]: https://www.infoq.com/presentations/Java-GC-Azul-C4/
 [blackswan]: https://www.amazon.com/Black-Swan-Improbable-Robustness-Fragility/dp/081297381X
 [aws]: https://aws.amazon.com/builders-library/avoiding-fallback-in-distributed-systems/?did=ba_card&trk=ba_card
 [fraught]: https://danluu.com/deconstruct-files/
 [boring]: https://mcfunley.com/choose-boring-technology
