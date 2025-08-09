---
layout: post
title: "Target Practice: Resumes, But Better"
date: 2025-02-20
categories:
 - ai
 - career-advice
 - job-search
 - open-source
 - productivity
 - automation
image: https://cdn.pixabay.com/photo/2017/04/14/17/36/archery-2230855_1280.png
# social_image: /images/bash-v-powershell.png
is_draft: false
use_mermaid: false
---

I recently got a job, but it was a bear going through rejections on repeat. It almost felt
like nobody was even **looking** at my resume. Which made me think 🤔 that might be the case.

It turns out that [hiring managers are swamped][research] with **stacks of resumes**. Surprisingly (to me),
they're not really using AI to auto-reject, they just aren't reading carefully. 

If you're a hiring manager with a stack of 200 resumes on your desk, how do you process them?
I think I'd probably:

 1. Scan for the most critical info (e.g. years of experience, industry focus, tech stack, etc.)
 2. Read the remaining ones more carefully.

So you have to **spoon feed** the hiring manager. Sounds easy.

Except it's not. One single resume won't work, because it's basically impossible to satisfy all
potential job postings and also have it be **succinct enough** to properly spoon feed. 

It seems you need to generate a different resume for every job opening. But that's a ton of work.
So I made a tool for myself, and I'm **open sourcing** it today. [Here it is][gh].

This breaks it down into 2 steps:

1. A huge verbose "resume", that's more of a knowledge bank
2. A targeted resume, generated to be tailored to each job posting

## Step 1: The Big Resume
The flow is:

1. Start with your existing resume
2. For each job:
    1. Open a **chat** dialog
    2. AI offers some icebreaker **questions**, like _"what challenges did you run into while developing Miopter Pengonals for Project Orion?"_
    3. **Answer** the question. Well, just type anything really. The point isn't to interview, it's to get everything in your head down on paper.
    4. AI asks **followup** questions
    5. Repeat 3-4 for a few turns
    6. Review/edit **summarized** version & save
3. Have the AI suggest **skills and accomplishments** based on these AI interviews

I'm not gonna lie, this is the most fun I've ever had writing a resume. Most of the time I want to 
tear my hair out from searching fruitlessly for something I did that can sound cool. But with this,
you just kick back, relax, and brain dump like you're talking with a friend over drinks. 

And while all that is great, the most electrifying part was when it suggested accomplishments, 
and it struck me that, "dang, I've done some cool stuff, I never thought about _that project_ that way".

All of that, the summaries, the full conversations, all of it is stored alongside the normal resume 
items. For each job, I have like 30-40 skills and 8-12 accomplishments, mostly generated with some
light editing.


## Step 2: The Small Resume
The flow is:

1. **Upload** a job posting
2. **Analyze** the job posting for explicit and implied requirements. Again, this is an AI collaboration,
    where an AI can go off and do recon on the company.
3. **Generate** resume. 
4. **Review** and edit
5. **Export** to PDF

The strategy is to use as much as possible verbatim text from the big resume. So generally you put **effort**
into the big resume, not the small one.

When generating, very little generation is happening. It's mostly just selecting content from the 
big resume that's pertinent to the specific job posting based on analyzed needs.


## Side Effects
Outside of generating the small resume, I also had a huge amount of success throwing the entire Big Resume
into NotebookLM and having it generate a podcast to help prep me for **interviews** (😍 they are so nice 🥰😘).
I've also done the same thing with ChatGPT in search mode to run recon on interviewers to prep.

The big resume is an XML document. So you really can just throw it into any AI tool **verbatim**. I could
probably make some export functionality, but this actually works very well.

# Status
I'm open sourcing this because I got a job with it. It's not done, it actually kinda sucks, but the
approach to **managing information** is novel. Some people urged me to get VC funding and turn it into
a product, but I'm tired and that just makes me feel even more tired. Idk, it can work, but something
that excites me a lot is enabling others to thrive and not charging a dime.

The kinds of people who want to use it are also the kinds of people who might be motivated to 
bring it over the finish line. Right now, there's a ton of tech people out of work, and thus a
lot of people who are willing, able, and actually have enough time to contribute back. This could
work.

**Why use it?** Because, at bare minimum you'll end up recalling a lot of cool stuff you did.

**Why contribute?** Because, if you're an engineer, you can put that on your resume too.


Again, if you missed it: [Github Repo Here][gh]


 [gh]: https://github.com/tkellogg/target-practice
 [research]: https://bsky.app/profile/timkellogg.me/post/3lfmtvn4f422g
