---
layout: post
title: "Why Open Source May Not Work For IoT"
categories:
 - iot
 - open-source
---

On Friday, [Matt Asay][2] wrote an [article on readwrite][1] about *why the Internet of Things has to be open sourced* that triggered a lot positive responses in [my Twitter feed][8]. I generally agree with what Matt had to say, but I found it unsettling that he conflates open source software with open specification. This distinction is important! There is a place for both open source and proprietary in the IoT and I believe that ignoring these differences will cause more harm than good.

First of all, I think Matt's intentions are right on target. The sub-title of his article is "developers aren't going to go for proprietary standards". While this is a great statement to make, it isn't even close to the same statement as "IoT has to be open sourced". Let's look at the best success story we have available: HTTP.

HTTP is the core of the old web. It's simple, small and does one thing very well - it implements a request/response pattern and makes very few assumptions about the underlying technology. This is huge. Remember how those expensive monolithic Unix servers fell out of favor and were replaced by cheap Linux servers? No one had to go to the IETF to revise the HTTP specification to account for Linux because HTTP wasn't tied up with Unix concerns. They were entirely seperate. This is a trait that we need in the IoT.

Open standards usually need to be small to be successful. If they're small, there's less to disagree on. Several years ago I worked for a large corporation and I remember it being nearly impossible to get stakeholders across the company to agree on standards. Internet standards are magnitudes more difficult to arrive at because you have so many participating corporations, each with wildly different intentions and company (and geographic) cultures. 

Worse, we frequently [make bad decisions][3] the first few times around. If our standards are small and componetized, it's not too difficult to roll back the ones that didn't pan out and replace them with another idea. When SOAP didn't work as well as promised [^4], we didn't have to throw out our web servers, we just stopped using SOAP. Cryptographic algorithms are an even better example, we've upgraded our algorithms every few years and most developers and sysadmins never needed to care much because the upgrade path was so seemless. *The IoT needs small componentized open standards.*


Are we talking about open source?
---------------------------

No, this isn't the same thing as open source. Open source is about making a free implementation with an open process. Unfortunately, implementations don't always get it right. Even when the process is open and adaptive. Sometimes they do get it right, but organizations have wildly different worldviews and can't agree on an implementation [^5]. 

Just look at the Apache web server. Was it successful? Absolutely! But lately it's market share has trended toward being replaced by Nginx due to the simplicity of Nginx. Even still, a significant portion of market share is owned by proprietary web servers from Google, Microsoft and others - yet none of this has caused problems because they all standardized on an open specification.

Recently it seems like open source has become the new generally accepted correct way to do things. The trouble is open source software takes time to create yet money must still be made. We still have to feed our families, so where does the money come from? Matt Asay is a VP at MongoDB. The MongoDB database is open source but the company earns a profit by charging for support. Amazon EC2 is fully closed source and non-free but many of their services have [open source clients][6].

There is no such thing as a free lunch. The money always comes from somewhere, and [sometimes it's more ethical][7] to have the money-flow stated explicitly up-front. With that said, I still think Matt is correct. Capturing money later in the development process does wonders for accelerating innovation.

Overall, I think Matt's analysis was spot-on. Open source is going to have a critical role in the Internet of Things. However, open specification is non-negotiable. Some organizations may need proprietary solutions - and that's fine as long as we're standardized behind a set of small componentized open specifications.




 [1]: http://readwrite.com/2014/10/17/internet-of-things-open-source-iot-developers
 [2]: http://readwrite.com/author/matt-asay
 [3]: http://quod.lib.umich.edu/j/jep/3336451.0014.103?view=text;rgn=main
 [^4]: Okay, I'm still kind of young and don't really have a lot of great examples of failed Internet technologies. If you can't contain yourself, feel free to post your own examples in the comments.
 [^5]: I'll go out on a limb and say that no implementation (open source or otherwise) has ever become universally accepted. However, I think standards have a much better track record for full acceptance.
 [6]: https://github.com/aws
 [7]: http://www.usatoday.com/story/news/nation/2014/03/08/data-online-behavior-research/5781447/
 [8]: https://twitter.com/kellogh 