---
title: IoT Startups Will Fail Without Standards
layout: post
categories:
 - IoT
---

I was talking to a man at a [Denver IoT meetup group][1] last week about his Internet of Things related startup. He was telling me about his plans to create an innovative new product that interoperates with smart phones, tablets, and arbitrary sensors. I really liked his idea, but then a question occurred to me:

> Are you worried about failing as a hardware startup? I know I've had a lot of ideas for hardware startups, but I always talk myself away from them because it seems like large billion dollar corporations are the only ones with enough resources to execute the idea.

He agreed. Then I continued thinking about it. Silicon valley has perfected the art of software startups. Hardware has the same set of problems, only magnified. For instance, in software you need to get the product into the users hands so you send out a link to your web application via Twitter, Facebook and other social outlets. But in hardware you have to produce 100 prototypes and physically mail them out.

It seems to me that successful software startups have gained traction because they're trivial for new users to start using. Imagine if iTunes didn't recognize MP3 format, or if Github invented their own version control software, or if Tinder made you buy their own specialized device instead of just running on your existing smart phone. No one would fall for that crap. 

We rely on re-using our web browsers and smart phones. If someone sells a smart light bulb, it better work in existing light sockets or else no one is going to use it. If your IoT device is going to talk to my smart phone, I'll be more likely to use it if I don't have to install a new app. This is where standards become important. Big, billion dollar companies have enough resources to force their users to install monolithic and/or incompatible components. Small companies, where the innovation tends to happen, don't have that option. 

Unfortunately, there's far too many competing IoT "standards" today. A standard is utterly useless if it doesn't have a majority of people using it. It doesn't matter how technically superior it is, if it doesn't interoperate with the rest of the world, no one will use it. In fact, there's a [long history][2] of technically inferior technologies taking over simply because they're more broadly accepted. 

I believe that the battle over which IoT standards win out will be decided by chip manufacturers. I've witnessed scores of embedded developers that would rather open a raw UDP or TCP socket and forego security, robustness and interoperability than pull in an MQTT or CoAP library. Chips and embedded operating systems need to have these protocols built in, otherwise developers won't use them and we'll continue down the current path into a rat's nest of incompatible devices.

If you're an embedded engineer, try to influence your hardware suppliers to adopt standards. If you're a user, try to only buy products that interoperate using global Internet standards. It's the only way we'll end up with an innovative and useful Internet of Things.


 [1]: http://www.meetup.com/Denver-Internet-of-Things-Office-Hours/events/219382337/
 [2]: http://ils.unc.edu/callee/gopherpaper.htm
