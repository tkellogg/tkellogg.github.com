---
title: Websockets Are Not Magical
layout: post
categories:
 - websockets
 - iot
---


A couple months ago I was talking to a high-ranking engineer from an embedded RTOS 
vendor. He was insisting that websockets are going to be one of the most important
standards for the Internet of Things. Unfortunately, the conversation was cut short
too soon for me to get a better understanding of his reasons.

Since then I've seen an endless stream of tweets and blogs indicating that there might be 
a lot of misconceptions about websockets and the Internet of Things. Every time I
see someone list "websockets" along side MQTT and CoAP my inner voice screams
**"People! Websockets are just rich TCP sockets"**. 

I hope to dispell some myths here and hopefully stir up excitement about websockets 
for _the right reasons_.


Myth: There's No Extra Overhead
-------------------------------

I've heard intelligent and respected people say that websockets have no per-message 
overhead after the initial negotiation request. This is simply not true. Two things 
should tip you off: (1) its message-oriented instead of stream-oriented and (2) the 
existence of text frames and data frames. These things don't come for free.

Each websocket message is divided up into frames (normally 1 frame per message). 
Each frame has a minimum overhead of:

* 2 bytes for short messages (<126 bytes) going from server to client
* 6 bytes for short messages going from client to server (4 bytes for the mask)

Maximum overhead is 14 bytes (or unlimited if [websocket extensions][0] are used). Still,
this still isn't much overhead compared to HTTP and seems to be consistent with the 
spec's goals:

> The WebSocket Protocol is designed on the principle that there should be minimal framing


Myth: Websockets Are Just TCP
-----------------------------

I'm guilty of spreading this myth. It seems intuitive that a technology called 
"websockets" that runs on TCP would also be stream-oriented. But in [section 1.5][1]
of the spec says:

> Conceptually, WebSocket is really just a layer on top of TCP that [...] layers a 
> _framing mechanism_ on top of TCP to get back to the IP packet mechanism that TCP is 
> built on, but without length limits.

So websockets are message-oriented like UDP without the maximum length constraints 
but with TCP's delivery guarantees and congestion control. It turns out that TCP's
stream orientation isn't all that useful (think about how many protocols build some
sort of "message" concept on top of TCP). In fact [SCTP (RFC 4960)][2] provides many
of the same benefits of messages-on-top-of-TCP but removes the TCP part to reduce 
the overhead. Unfortunately, SCTP is yet to gain widespread adoption.

Since websocket connections are made from streams instead of messages, some 
stream-oriented protocols could be difficult to implement in websockets. But most 
protocols should fit easily into websocket frames.


Negotiation
-----------

The single best thing about websockets (in my opinion) is that they start off with an 
HTTP request that can negotiate terms for the connection. The request could 
contain an `Authorization` header in order to authenticate the client before creating 
the session. This means that OAuth could become less complex for protocols like MQTT.

The server can respond with any response code, so it's completely legitimate to 
respond with `307 Temporary Redirect` to force the client to connect to a different
(less stressed) server. For TCP protocols like MQTT that suffer from being difficult 
to load balance, this could be an answer.

A lot of the problems I run into with trying to create a better client experience with
MQTT could be solved easily with a single negotiation request. Many kinds of metadata
could be coordinated by setting request and response headers. 

For instance, I often want to communicate errors to the client (i.e. _You don't have 
access to publish to `foo/bar/baz`, try `foo/bar/biz` insead_). The only reasonable 
way I've seen to communicate these errors is to have the client subscribe to a certain 
topic that only they have access to (usually something like `$SYS/errors/<client_id>`). 
Of course, there's no standard place to look for errors and each broker does it 
different (if at all). Sending a header like `Client-Errors: $SYS/errors/ww1922` in
the response could solve this problem smoothly. This strategy could also work for other 
things like topic schemas, provenance conventions, and the list goes on.


Conclusion
----------

The initial negotiation request is a powerful addition to TCP-based binary protocols.
If the client is strong enough to handle some HTTP communication, websockets can add
a lot of value. At the same time, I keep seeing the term _websockets_ thrown around
alongside protocols like MQTT and CoAP. Websockets are in no way a replacement for
many of these traditional IoT protocols. At best, it offers a mechanism to enhance
these protocols and communicate conventions. However, I wonder if it's not better to
simply fix the broken protocols rather than to throw in another abstraction (we're actually
talking about making packets out of a stream which was formed from packets, and 
everyone seems to be keeping their poker faces).

However, I find it worrisome that websockets are being recommended so highly for Internet of
Things applications when it was so obvioulsy designed for web browsers. For instance,
each server-bound frame is masked. This seems like a frivolous use of CPU cycles 
and memory buffers when we've worked so hard to minimize CPU and memory usage in
other areas. Also, the Origin-based security is apparently a useless gesture for 
non-HTML based applications. If the Internet of Things is going to be [so important][3],
then why doesn't it deserve it's own set of protocols instead of poorly repurposing
highly specialized web browser technology?


 [0]: https://tools.ietf.org/html/draft-ietf-hybi-permessage-compression-19
 [1]: https://tools.ietf.org/html/rfc6455#section-1.5
 [2]: https://tools.ietf.org/html/rfc4960
 [3]: http://www.gartner.com/newsroom/id/2636073

