---
title: MQTT - Another Implementor's Perspective
layout: post
categories:
 - mqtt
 - iot
---

Earlier there was [a blog post by Clemens Vasters][1] that flamed MQTT. My preference is to take these complaints to the standards bodies responsible for MQTT and try to make constructive changes, but it appears that this is a man who prefers flame wars over professional dialog. I've been [challenged to write a rebuttal][2], so here it is.


Goals
-----

Obviously Clemens misunderstands the goals of MQTT. He has an entire section dedicated to extensibility and later even criticizes the lack of custom headers. I've worked with MQTT for about a year and never even realized that extensibility was even a goal of the protocol, so I was mystified why the lack of extensibility was so cornerstone to many of Clemens' arguments. Nowhere in the entire spec does it say anything about extensibility. When I googled for "MQTT extensible", the top relevant hit is Clemens' blog. Where did he get this notion? No one else is talking about it.

MQTT is meant to be "lightweight, open, simple, and designed so as to be easy to implement". Clemens starts off his blog by discussing IBM in depth, as if it was somehow a closed IBM spec. The reality is that IBM has very little to do with the direction of MQTT at the present time. Sure, IBM was the creative force in the beginning, but since it handed it over to OASIS and the Eclipse Foundation, IBM has mostly left it alone. MQTT is truely an open standard driven by open source software. Even I, a simple software engineer at a startup, feel as though I have a voice in the MQTT community. Please don't let Clemens wordy lecture make you believe otherwise.

Most importantly, the goal of the protocol is to be lightweight yet simple and easy to implement clients. If the goal was only to be lightweight, [MQTT-SN][4] would be a much better choice. It also aims to be easy to implement new clients. Evidence of this is easy to see in how it tends to offload complexity to the broker when given the option. Clemens implemented a broker distributed over many machines and tacked onto some other messaging protocol - when he complains that it was a complex task it's because he made it complex, not because the task itself is inherently complex.


Bytes
-----

One complaint that is nearly valid is the variable 1-4 byte remaining length field. All other strings in MQTT are prefixed by a 2-byte length. He rightly points out that the variable 1-4 byte remaining length field is inconsistent with the other strings. However, he neglects to notice that some messages have up to 6 strings, each prefixed by a 2-byte length. If the remaining length was only 2 bytes, this would result in a leaky abstraction (saying each string could be 65535 bytes long but then limiting the sum total of all strings to less than 65536 bytes). What would be the point of introducing a leaky abstraction?

In the CONNCT message there is a protocol identifier that is always "MQTT". The spec explains that it exists only for network analyzers to quickly identify it as MQTT traffic, as is common practice. Clemens criticizes the fact that this string is prefixed by a 2-byte length and suggests that it should be just the raw 4 bytes without the prefixed length. The spec's choice supports the "simple" and "easy to implement" goals of the protocol. In fact, this choice enabled the protocol to switch from the historical IBM-ridden "MQIsdp" to the current "MQTT" representative of it's current open spec. 

The spec's statement that this "will not be changed by future versions of the MQTT specification" means that, while this string has been different in previous versions of the spec, they are committing to the name "MQTT". There's a very clear reason for why it was implemented this way, unfortunately Clemens didn't seem to take time to fully understand before flaming.

When attacking the size of the wire protocol, he adds the length of IPv6, TCP, and TLS headers onto the length of an MQTT message to demonstrate how many bytes are wasted but misses the somewhat obvious point that multiple messages can be sent in a single TCP/IP packet. Given that multiple messages can be sent in the same TCP packet, his point crumbles rather quickly. This embarassing mistake would have been spared had he simply hopped onto the MQTT IRC channel and asked questions in a professional voice.


Content-Type
------------

There has been some discussion in the MQTT community on how to represent the content-type of payloads. Clemens rightly points out the lack of content type as many others have. However, this viewpoint neglects the more traditional usage of MQTT where content-type makes no sense. This usage is best illustrated by the [$SYS topic space][5] used for monitoring the status of the broker. Each topic has UTF-8 numbers published on it. For instance, the broker may periodically publish a message to `$SYS/messages/received` that contains the total number of messages received by the broker since it started.

This strategy can be used in combination with [topic patterns][6] to do realtime queries via SUBSCRIBE requests. It can be very powerful, especially for devices consuming messages in the field. Of course, if he don't know about this strategy I could see how he might be unsatisfied with MQTT. I wish he would learn how to use MQTT correctly before flaming it publically on the Internet.



Choosing The Right Forum
------------------------

When he talks about delivery assurances, data retention, failover and security he mentions a few points that are ambiguous in the spec. Honestly, I think he has some great points. Many of these things could be cleaned up. The 3.1.1 version of the spec has been open for comment for several months - he must have known this since it says so and gives instructions for giving feedback directly inside of the preliminary spec that he was reading (final versions of the spec aren't yet available). I've also insructed him to take his valid concerns to the MQTT-comment mailing list, which he refused. I guess some people are more interested in causing damage than fixing a spec that's intentionally and publically asking for help.



Conclusion
----------

Clemens wrote a damning 21 page blog post on MQTT. I truly doubt that many people took the time to carefully read through all that text. Regardless, Clemens is a respected individual in our community, and this blog received a lot of attention. As a result, hundreds or thousands of people now have the impression that MQTT isn't designed well due to 140 character tweets framing it as such. The trouble is that this argument was made on false pretenses and measured MQTT against goals that it never intended to have. 

Nothing he brought up is beyond fixing, and I have confidence will be fixed soon. The MQTT spec is an open collaboration that depends on individuals to contribute wisdom and experience. I don't understand why Clemens chose to publically destroy the reputation of MQTT rather than simply offering to help fix it. The MQTT Technical Committee has always been very open to hearing and addressing concerns. 



 [1]: http://vasters.com/clemensv/2014/06/02/MQTT+An+Implementers+Perspective.aspx
 [2]: https://twitter.com/kellabyte/status/473472640364331008
 [3]: https://twitter.com/kellogh/statuses/464063809552797697
 [4]: http://mqtt.org/new/wp-content/uploads/2009/06/MQTT-SN_spec_v1.2.pdf
 [5]: https://github.com/mqtt/mqtt.github.io/wiki/SYS-Topics
 [6]: https://github.com/mqtt/mqtt.github.io/wiki/topic_format
