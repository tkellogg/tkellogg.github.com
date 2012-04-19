---
layout: post
---
Occasionally I get emails about 
[objectflow](https://github.com/tkellogg/objectflow). Questions range from
documentation to examples to the status of objectflow. I haven't worked on
objectflow for several months. I don't want it to float out in OSS space
with a cloud of uncertainty hanging over it, so this post is to clear up
the status of objectflow (or at least the _stateful_ fork of it).

History of Objectflow
=====================

I first came into contact with Objectflow when we needed a workflow 
framework. We didn't like Windows Workflow Foundation because it offered
a heavy overhead for what we saw as a simple task. WWF uses XAML to make
a beautiful designer experience with perfect drag-n-drop bliss. However,
we are programmers, we like keyboards.

Objectflow seemed like the only good alternative to WWF. It's concept of
unique constraints seemed very promising. I quickly dove into the code,
only to realize it's biggest fault - it was originally intended for managing
complex algorithms, not workflows oriented around people. 

I still liked how Objectflow was laid out, with it's 
