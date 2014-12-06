---
layout: post
title: "ThingMonk 2014: Toward a more intelligent IoT"
categories:
 - iot
 - standards
---

This week I was fortunate enough to attend ThingMonk in London. RedMonk were excellent hosts and managed to put together a tremendous lineup of speakers and talks that I hadn't anticipated. There were only 150 attendees, but each one of them brought something unique. Here I attempt to summarize some of the day, I know I've missed several truly great talks, but I just wanted to  keep it short.

[Boris Adryan][3], a geneticist, gave a thought provoking perspective on how he believes the Internet of Things needs to have some form of directory or database. In his field of study, academic papers are mapped ontologically so that similar papers can be quickly found. He believes that this sort of knowledge and information mapping needs to be applied to sensors and open data to force valuable epiphanies out into the open.

Boris' talk was just the start of an overarching theme that emerged over the course of the day. We've already fought over protocols like MQTT versus CoAP versus DDS, etc. Now it's time to go beyond simple wire protocols and talk about what these giant mounds of data actually mean. As [Nick O'Leary][1] [eloquently put it][2]:

> What (mostly) everyone agrees on is the need for more than just efficient protocols for the Things to communicate by. A protocol is like a telephone line. It’s great that you and I have agreed on the same standards so when I dial this number, you answer. But what do we say to each other once we’re connected? A common protocol does not mean I understand what you’re trying to say to me.
>
> And thus began the IoT meta-model war.

[Yodit Stanton][4], founder of [OpenSensors.io][5] talked about the need for more than simply gathering sensor data. Her general message was that we're starting to get the hang of the wire protocols, but how do we make sense of all this data? Data structures  such as the Bloom filter and hyper log log are becoming available that let us estimate useful information, like presence or cardinality, without consuming a gargantuan amount of computer resources.

[Andy Stanford-Clark][10], the inventor of MQTT, had everyone's eyes glued to the front during his talk. The first couple minutes of his presentation were spent explaining how the machine worked that he ran his slide show from. It was a Raspberri Pi powered by hydrogen. While that seems like it could have been the thesis of his talk, that was simply to kill time until the machine booted. Once started, he talked about different aspects of his home that he's redesigned with sensors and devices. It is clear that Andy's vision for the Internet of Things does not require much human interaction - it just quietly augments our lives without inducing noticeable burden.

[Andiamo][11] presented an inspirational story about a young girl that he was able to help by 3D printing a back brace. While the traditional methods would have required 25 weeks, this back brace was produced in only 48 hours. They knew they had succeeded in producing something beautiful for this girl when a woman mistook the device for some sort of kinky clothing style - a far cry from the ugly status quo that would have labeled the girl as an invalid.

I gave a talk toward the end of the day about some problems in the MQTT specification, originally [identified by Clemens Vasters][6]. Much of my talk revolved around how exactly-once delivery (QoS 2) simply isn't possible to guarantee in a horizontally scaled broker. I took some time to explain the CAP theorem and how it is relevant to the Internet of Things. Overall, I think my talk was well recieved, however much I felt woefully antiquated in my choice of topic.

[Ian Skerret][7] wrapped up the day with an overview of the current state of standards organizations. I highly recommend skipping on over to [his slides that have been posted on SlideShare][8]. He carefully reviewed several standards bodies and assigned high school style letter grades for qualities such as openness and adoption levels. Again, his slides do a pretty good job of standing on their own. I'd like to see his talk manifested into a website analogous to [TL;DR Legal][9] but for IoT standards orgianizations.

Overall I was blown away by the quality and personal conviction of all the speakers. Even after dinner, when the talks were finished, I engaged Boris in a fascinating conversation about how distributed systems concepts arise in cellular conscription; something I certainly hadn't planned on hearing about. My recommendation is that, if you go to one conference next year, let ThingMonk be the one.



 [1]: https://twitter.com/knolleary
 [2]: http://knolleary.net/2014/12/04/a-conversational-internet-of-things-thingmonk-talk/
 [3]: https://twitter.com/borisadryan
 [4]: https://twitter.com/yoditstanton
 [5]: http://www.slideshare.net/kellogh/thing-monk-improvemqtt
 [6]: http://vasters.com/clemensv/2014/06/02/MQTT+An+Implementers+Perspective.aspx
 [7]: https://twitter.com/ianskerrett
 [8]: http://www.slideshare.net/IanSkerrett/abc-of-iot-consortium
 [9]: https://tldrlegal.com/
 [10]: https://twitter.com/andysc
 [11]: https://twitter.com/andiamohq