---
title: Can HTTP/2 Replace MQTT?
layout: post
categories:
 - IoT
 - MQTT
---

Yesterday I got an [interesting question][1]:

> Would you agree that HTTP/2 with HPACK would certainly rule out any reason for using MQTT?

Well, I never thought about that possibility before, so I went and read through the specs
for [HPACK][2] and [HTTP/2][2.1]. What follows is my analysis to the best of my understanding. If I get something wrong,
feel free to leave a well-intentioned comment.

If you're not familiar, MQTT is a publish/subscribe protocol that is typically associated with
the Internet of Things because of it's compact header size. It uses a long-lasting TCP connection
to send messages with (minimum) 2-byte headers. The main verbs are `CONNECT`, `DISCONNECT`,
`PUBLISH`, `SUBSCRIBE` and `UNSUBSCRIBE` (the others are different forms of acknoledgements used to implement
higher delivery guarantees than TCP).


Implementing HTTP/2 Pub/Sub
===========================

Of course, the reason this question is even being asked is because HTTP/2 supports
multiplexing of requests. This means that a single HTTP connection can be reused by the server 
to send many requests and responses. Even better, a single request can receive multiple 
responses -- so the server can effectively push more messages to the client than they requested.

If you were to implement the rough equivalent of MQTT using HTTP/2 you could:

* `PUBLISH` to `foo/bar` by sending a `POST` request to `http://example.com/topic/foo/bar` with
	the message in the body of the request.
* `SUBSCRIBE` to `foo/bar` by sending a `GET` request to `http://example.com/topic/foo/bar`.
* `UNSUBSCRIBE` from `foo/bar` by sending a `DELETE` request to `http://example.com/topic/foo/bar`.

All information normally transmitted in the MQTT `CONNECT` would happen naturally through 
headers on requests and `DISCONNECT` would be a matter of severing the HTTP connection. To deliver
a published message to a subscribing client, the server could simply open another stream and push 
the message to the client. This is called _server push_.

Streams are a new concept in HTTP/2. They're somewhat equivalent to an HTTP/1.1 connection, 
except that a server can initiate a stream in order to do a server push. If a 
client makes a GET request and, while responding to the request, the server decides that the
client will also want another complimentary item (image, stylesheet, etc) the server 
can send a `PUSH_PROMISE` message then immediately open a new stream and send the additional 
item without the client having to request it.

In our miniature MQTT look-alike, when the client makes a `GET` request to subscribe to a topic,
the server would send response headers but leave the stream open. Whenever a new message comes
in on that subscription, the server would send a `PUSH_PROMISE` and then open a new stream to
transmit the actual message.

I'm sure someone could develop a much better pub/sub framework than I did in 2 minutes, but 
you get the idea. HTTP/2 lends itself surprisingly well to the pub/sub pattern, despite being
designed for request/response.


A Little About HPACK & Huffman Coding
=====================================

HPACK is part of HTTP/2 for header compression. One of the causes for hesitation on using HTTP/1.1 
for Internet of Things applications is the massive header size. If HTTP were ever to be viable,
some sort of header compression like HPACK would be a necessary part of this.

Internally, HPACK uses an old compression algorithm called [Huffman coding][3] to find the minimum
number of bits to encode strings based on their frequency. The encoded version of strings are variable length - a 
common string could be 2 bits and another less common string could be 17 bits (just examples, of course).
If you've never heard of Huffman coding before or just want a reasonable programming challenge, 
I highly recommend walking through the [Wikipedia page][4] and trying to implement it in your 
favorite programming language.

Huffman coding finds the optimal number of bits to encode symbols, but there's still much better
compression algorithms. In fact, many popular compression formats including PKZIP, JPEG and MP3
have used Huffman coding in addition to other steps. So why didn't the IETF choose the _optimal_
compression format for compressing headers? Well, frankly, compression takes compute power 
and memory space. Huffman coding does fairly well with both of these constraints.

It takes 2 passes to encode data with Huffman. The first pass you build a tree
out of occurrences of bit strings and track the frequency of the bit string. This is
also where the optimization happens. On the second pass, bit strings are looked up in the tree
and replaced with the corresponding optimially sized short codes.

Normally, the entire tree/table of codes is transimitted or stored preceding the fully encoded 
message. HPACK has two "tables" - a static table and a dynamic table (you could call them trees, 
like we talked about previously with Huffman coding). The static table is known by the HTTP/2 client
_a priori_ because it's part of the spec. This static table was decided on based on samples of 
actual web traffic on the Internet.

The dynamic table is calculated by the encoder or decoder based on live data for just the current HTTP/2 connection and,
unlike the static table, is transmitted at the start of each message. A single HTTP/2 connection 
can be used to service many HTTP requests and responses. The dynamic table is refined
with each message so compression gets better the longer the connection stays open (or so I assume).


MQTT Patterns
=============

To better understand the question, we need to talk about ways people actually use MQTT.


As A Funnel Protocol
--------------------

The most common (and arguably the best) usage for MQTT is to have embedded devices publish data to 
a multi-protocol broker over MQTT and re-distribut the data via another protocol that's more
suitable for server-to-server traffic such as HTTP, Apache Kafka, AMQP or Amazon Kinesis. I 
gave a [presentation][5] on using MQTT to funnel into Kafka at ApacheCon 2014. From there the 
data is typically funneled into a storage or analytics system like Hadoop, Cassandra, a timeseries 
database or some sort of web API.  

At [2lemetry][6] we quickly ran into issues scaling what we call the _firehose subscription_ (`#`),
which basically means that a single MQTT client wants to consume all the traffic (or just a lot of it) 
that passes through the broker. The biggest problem with this is that a subscription can only be 
serviced by a single connection on a single computer. At some point you're going to find the memory
or I/O limits of the NIC. On the other hand, Kafka and Kinesis both offer consumer groups, 
which are essentially a [consistent hash ring][7] of clients that cooperatively process a single
subscription. This effectively fixes the firehose subscription problem by spreading the load over
several cleints.

Some embedded devices have extremely limited resources (8-16 KB of memory, slow 8 bit CPUs, 
expensive data transfer rates), so they generally want to transmit that telemetry data with as
little effort as possible and consuming the least amount of bandwidth. This is one of the 
greatest strengths of MQTT and is primarily where HPACK will come into play. The Huffman coding 
that we discussed earlier is relatively gentle on the CPU, but encoding/decoding messages requires 
roughly 2x the memory than the actual data frame (I believe). However, a message can be split over 
several data frames to control memory usage, so this may not be as big of an issue as I'm making it.

From what I can tell, as the client re-uses the HTTP connection for PUBLISH after PUBLISH, the 
headers would continue to be compressed better and better (I'm not sure this is actually true
since the dynamic table also drops entries over the life of the connection). In comparison, MQTT
is certainly smaller on the wire (and easier to parse) but time will tell if the difference is
big enough to make people use it over HTTP/2 (people seem to generally avoid using too many
protocols/technologies).


To Ignore Faulty Networks
-------------------------

MQTT provides three quality of service (QoS) levels that govern delivery guarantees. The lowest 
(and most common) has the same guarantees as TCP. _At Least Once_ (QoS=1) uses the unique client
identifier to re-deliver messages that the client may have missed while offline. The highest level,
_Exactly Once_ (QoS=2) [isn't actually possible][8] according to some basic distributed systems 
principles.

The ability to have missed messages delivered while offline is extremely helpful for some 
embedded systems. I would wager that any protocol targeted for the Internet of Things absolutely
must have the ability to give _At Least Once_ guarantees. As far as I can tell, HTTP/2 doesn't 
support this level of delivery guarantee, but I believe it would be trivial to implement it on
top of HTTP/2.


Scaling HTTP/2 On The Server
============================

When discussing IoT protocols, scaling is rarely a topic we discuss. But, working for [2lemetry][6],
this is a topic I deal with frequently so I'll briefly address it.

HTTP/1.1 is easy to scale. Just throw a load balancer in front of a cluster of servers and voila!
It scales!. This is true with HTTP/2 for single use connections, but if multiplexing is heavily 
used, load balancing could become difficult. Think about it, if the connection stays open for minutes
or hours, how does the server tell the client "connect to another server, I'm getting bogged down".
This is a problem we run into frequently when scaling MQTT, as connections are frequently left open
for days on end. I'm sure we'll solve this problem with HTTP/2, but I'm not quite sure what that 
will look like.


Obligatory Notes About CoAP
===========================

CoAP ([RFC 7252][9]) is a proposed standard (**Correction:** it is finalized) to implement 
a RESTful architecture (like HTTP) for constrained devices. It's a very compact, trivial to 
parse, binary protocol that runs over UDP and has support for optional guaranteed delivery. CoAP
also supports server push in mostly the same way that HTTP/2 does.

CoAP maps very well to HTTP/1.1. In fact, there's a section of the specification dedicated to
proxying between HTTP and CoAP. Two CoAP features (server push and multicast) aren't supported
natively by HTTP/1.1, so having HTTP/2 support server push only narrows the gap and makes these 
two protocols a great match. Use CoAP in constrained environments and use HTTP/2 everywhere else.
After all, CoAP can almost always be proxied neatly to HTTP/2.


Conclusion
==========

MQTT definitely has a smaller size on the wire. It's also simpler to parse
(let's face it, Huffman isn't _that_ easy to implement) and provides guaranteed delivery to cater
to shaky wireless networks. On the other hand, it's also not terribly extensible. There aren't a 
whole lot of headers and options available, and there's no way to make custom ones without touching 
the payload of the message.

It seems that HTTP/2 could definitely serve as a reasonable replacement for MQTT. It's reasonably
small, supports multiple paradigms (pub/sub & request/response) and is extensible. Its also supported
by the IETF (whereas MQTT is hosted by OASIS). From conversations I've had with industry leaders
in the embedded software and chip manufacturing, they only want to support standards from the IETF.
Many of them are still planning to support MQTT, but they're not happy about it.

I think MQTT is better at many of the things it was designed for, but I'm interested to see over 
time if those advantages are enough to outweigh the benefits of HTTP. Regardless, MQTT has been 
gaining a lot of traction in the past year or two, so you may be forced into using it while HTTP/2 
catches up.  


 [1]: https://twitter.com/errordeveloper/status/568410467493908480
 [2]: http://http2.github.io/http2-spec/compression.html
 [2.1]: https://http2.github.io/http2-spec/
 [3]: https://www.cs.auckland.ac.nz/software/AlgAnim/huffman.html
 [4]: http://en.wikipedia.org/wiki/Huffman_coding
 [5]: http://www.slideshare.net/kellogh/mqtt-kafka-33100776
 [6]: http://2lemetry.com/
 [7]: http://www.paperplanes.de/2011/12/9/the-magic-of-consistent-hashing.html
 [8]: https://lobste.rs/s/ecjfcm/why_is_exactly-once_messaging_not_possible_in_a_distributed_queue
 [9]: https://tools.ietf.org/html/rfc7252
