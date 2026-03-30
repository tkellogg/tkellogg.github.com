---
name: writing-style
description: This skill should be used when the user asks to "write a blog post", "draft a post", "write in my style", "help me write", or when creating or editing content for the Jekyll blog at tkellogg.github.com. It encodes Tim Kellogg's distinctive writing voice and should guide all blog content generation.
version: 1.0.0
---

# Tim Kellogg's Writing Style

When writing or editing blog posts for this site, follow these patterns precisely. This is not generic "good writing" advice — these are specific, observed patterns from Tim's published work.

## Voice

Write as a **practitioner-thinker** — someone who builds things and reflects on what they learned. Not an academic. Not a journalist. A senior engineer who reads widely and connects ideas across domains.

- **First person, conversational.** Like explaining something to a smart friend at a bar.
- **Softmax on certainty.** When certain, be boldly certain — no hedging. When uncertain, say so plainly. Nothing in the middle. Certainty and uncertainty are both stated with conviction; the mushy middle gets pushed to one pole or the other. **Uncertainty is a strength on genuinely uncertain topics.** "My hunch is we'll want to run Mythos like a CEO" is more credible than "You should run Mythos like a CEO" — because nobody knows yet. Asserting false confidence on speculative claims makes you sound like a hack. Owning it as a hunch ("my take", "it seems to me", "my hunch is") establishes credibility because the reader knows you're being honest about what you know vs. what you're guessing.
- **Opinionated but open-minded.** State opinions bluntly, then steelman the opposing view.
- **Direct address to the reader.** Use "you" naturally. But when making predictions about the future, prefer first-person plural ("we'll want to") or prediction framing over commands ("you should"). The post is thinking out loud, not issuing instructions.

## Paragraph Structure

- **Short paragraphs. 1-4 sentences max.** This is non-negotiable — for paragraphs the reader should actually read.
- **Single-sentence paragraphs are a primary tool.** Use them as thesis statements, transitions, punchlines, and anchors.
- **5-8 word anchor paragraphs.** These act like visual headings — the eye processes them instantly and they set expectations for what follows. Examples: "Systems software." / "Learn the domain." / "That's inner loop agents." / "This is the way."
- **Intentionally skippable paragraphs for tech details.** When you need to include implementation details (tools, protocols, config), isolate them in a longer paragraph with no bold anchors. The wall-of-text shape signals "skip me if you're skimming." Dedicated readers will dig in; everyone else jumps to the next short paragraph. The *point* goes in the short paragraph before it; the *how* goes in the skippable block.
- **Short callout paragraphs tie back to the thesis.** When a section ends with a short paragraph that names what just happened ("That's resource allocation."), it should pull toward the post's main argument — not just label the concept. A standalone label sounds like Claude summarizing. Instead, use it to bridge back: connect the local point to the larger claim the post is making.
- **Don't explain what just happened.** If a concrete example is strong enough, the reader gets it. Sentences like "That's not X. That's Y" after an example are Claude-voice — they over-explain what the reader already understood. Let the example land on its own. If you feel the urge to label what it means, that's a sign the example should be stronger, not that you need a caption.

## Bold Text as Visual Anchors

Bold is the primary formatting tool. It serves as a highlighter pen — marking the key concept in a paragraph so a reader scanning the page can reconstruct the argument from bold text alone.

- Bold **1-5 word phrases**, never entire sentences
- Every 2-3 paragraphs should have a bold anchor
- **Anchor emotion words, not information words.** The bold text should pull the reader's eye with feeling — surprise, tension, relief — then instinct drives them to read the surrounding information. "That's not a complaint. That's a **design constraint**" works because "design constraint" carries the emotional punch. "That's not a complaint. That's a **design** constraint" doesn't.
- **Keep anchors to 2-4 words.** The reader should consume the bold phrase in a single glance. Pick the short phrase that sets the atmosphere of the point: "**create an environment** where other people make good decisions" beats "other people **make good decisions without being told to**" — the short phrase sets the emotional frame, the surrounding words provide the information.
- Use for: key insights, surprising claims, introduced terminology, contrast words
- Combine bold+italic (`_**word**_`) for maximum emphasis, sparingly

## Sentence Patterns

- **Short declarative openers.** These are crafted with the target reader in mind — something they'll understand and resonate with, but that also feels loud and unorthodox. It's a statement the reader already half-believes but hasn't heard said out loud. "AI code is slop." / "Plan mode *feels* good."
- **Fragments for emphasis.** "Stop." / "STOP." / "Systems software."
- **Emdashes with spaces for visual separation.** Horizontal whitespace is a lesser form of emphasis — it creates breathing room without starting a new paragraph. "the next wall is resource allocation — figuring out what to work on next" uses the emdash to separate the concept from the definition, giving the reader two bites.
- **Question-then-answer.** Rhetorical questions answered with a surprise or pivot.
- **Start paragraphs with "But" or "And" freely.**
- **Casual interjections.** "idk", "NGL", "TBQH", "yada yada yada" — used sparingly but naturally.

## Humor

The humor is **dry, insider, and sideways**. Non-insiders don't realize there was a joke. Never goes for big laughs.

- **Deadpan understatement:** State something absurd as if it's normal
- **Self-deprecating asides:** "Maybe I'm weird (okay fine, I am)"
- **Sarcastic advice delivered straight:** Say something obviously bad as if recommending it
- **Parenthetical jabs** and mock formality
- **Never mean-spirited.** Aimed at self, industry, or absurdity of the situation.

## Incomplete Thoughts & Trusting the Reader

Write for smart people. Give them enough to follow the bread crumb trail, then stop.

- **The intro is minimal orientation.** Just enough to tell the reader what this is about and who it's for. Let them self-select. No lengthy setup or background — drop them in.
- **Don't over-explain.** If the reader can infer the connection, let them.
- **Links fill gaps.** If someone is unfamiliar, the link connects A to B. The text itself doesn't need to spell it out.
- **No summaries, ever.** Not in the intro, not at the end, not between sections. The reader was there.
- **Kill cool ideas that don't serve the narrative.** A great insight that doesn't advance the post's argument is a distraction, no matter how interesting it is. If it doesn't pull toward the thesis, cut it — save it for another post. This is painful but non-negotiable. Every section must earn its place in *this* story.
- **The closer ties ideas together and points forward.** It's not a recap — it's connecting the threads from the post and gesturing long into the future. Often ends with an open question or a forward-looking statement.

## Analogies & Wild Ideas

Most posts are about ideas people haven't been thinking about. The text's job is to **pull readers from familiar territory into the new idea** using analogies.

- Draw from: management/organizations, physics/thermodynamics, biology, everyday life (road trips, parenting, woodworking)
- Introduce analogies casually: "Basically, if you envision an LLM as being a muffin tin..."
- The analogy is the bridge. The wild idea is the destination.

## Links

Use **reference-style markdown links** (`[text][ref]` with definitions at the bottom).

Links serve double purpose:
1. **Visual formatting** — they break up text like anchors
2. **Filling incomplete thoughts** — they provide the verbose explanation the text deliberately omits

Link to: own previous posts, papers, external blog posts, announcements. Nearly every claim should have a link.

## Argument Structure

Follow this pattern:

1. **Provocative opening** (1-3 short paragraphs) — a bold, slightly contrarian thesis stated plainly
2. **Grounding** — concrete example, personal experience, or experiment
3. **Framework** — introduce a mental model or analogy that explains *why*
4. **Steelman** — acknowledge the opposing view honestly
5. **Practical implications** — specific advice or forward-looking statement
6. **Brief conclusion** — 1-3 paragraphs. End with an open question, a callback, or a look forward. Never grandiose. "There you have it." / "Go forth and call functions!"

## Section Headings

- Informal, often provocative or playful
- Sometimes intentionally lowercase for casual tone
- Mix of H1 (`#`) and H2 (`##`) — don't stress about strict hierarchy

## Post Structure (Jekyll)

```yaml
---
layout: post
title: "Title Here"
date: YYYY-MM-DD
categories: ai  # common: ai, LLMs, engineering, agents
image: /images/filename.webp
summary: "One-line summary for social cards"
is_draft: false
---
```

- **Do NOT add a Discussion section.** Tim adds this after posting, tailored to where the post will do well and who needs to hear it.
- **Always include alt text on images.** Every `![alt text](path)` should have a descriptive alt attribute — what the image shows, not just what it is. This is non-negotiable.
- Collect reference-style links at the bottom of the file

## Jargon & Audience

Write for general audiences AND highly technical audiences simultaneously. Define terms, but make the definitions skippable for experts.

- **No framework shorthand.** Don't use "S1", "S2", "S3" etc. from the Viable System Model — those are internal shorthand, not reader-facing. Reference the VSM lightly and link to it; don't assume the reader knows it.
- **Define in passing, not in blocks.** Weave definitions into sentences so experts can skip them: "the bottleneck is resource allocation — figuring out what to work on next" rather than a paragraph explaining what resource allocation means.
- **Jargon earns its place.** Use a term only when it compresses meaning the reader needs. If plain language works, use plain language.

## What NOT To Do

- Don't write long paragraphs (5+ sentences)
- Don't summarize at the end — the reader was there, they read it
- Don't hedge excessively — state the opinion, then complicate it
- Don't use academic tone or formal transitions ("Furthermore", "In conclusion", "It is worth noting")
- Don't explain jokes
- Don't use emojis
- Don't write "Click here" or "Read more" — weave links into sentences naturally

## References

- **`references/style-examples.md`** — Detailed style patterns with real examples from posts
- **`references/cover-images.md`** — Cover image selection: stock photos, Pixabay workflow, what to look for
- **`references/mermaid-diagrams.md`** — Mermaid diagram syntax, complexity philosophy, common patterns
