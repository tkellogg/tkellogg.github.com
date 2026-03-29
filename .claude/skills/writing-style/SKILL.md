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
- **Softmax on certainty.** When certain, be boldly certain — no hedging. When uncertain, say so plainly. Nothing in the middle. Certainty and uncertainty are both stated with conviction; the mushy middle gets pushed to one pole or the other.
- **Opinionated but open-minded.** State opinions bluntly, then steelman the opposing view.
- **Direct address to the reader.** Use "you" naturally.

## Paragraph Structure

- **Short paragraphs. 1-4 sentences max.** This is non-negotiable.
- **Single-sentence paragraphs are a primary tool.** Use them as thesis statements, transitions, punchlines, and anchors.
- **5-8 word anchor paragraphs.** These act like visual headings — the eye processes them instantly and they set expectations for what follows. Examples: "Systems software." / "Learn the domain." / "That's inner loop agents." / "This is the way."

## Bold Text as Visual Anchors

Bold is the primary formatting tool. It serves as a highlighter pen — marking the key concept in a paragraph so a reader scanning the page can reconstruct the argument from bold text alone.

- Bold **1-5 word phrases**, never entire sentences
- Every 2-3 paragraphs should have a bold anchor
- Use for: key insights, surprising claims, introduced terminology, contrast words
- Combine bold+italic (`_**word**_`) for maximum emphasis, sparingly

## Sentence Patterns

- **Short declarative openers.** These are crafted with the target reader in mind — something they'll understand and resonate with, but that also feels loud and unorthodox. It's a statement the reader already half-believes but hasn't heard said out loud. "AI code is slop." / "Plan mode *feels* good."
- **Fragments for emphasis.** "Stop." / "STOP." / "Systems software."
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

- End every post with a `# Discussion` section containing social media links (Bluesky, sometimes HN, Lobste.rs, LinkedIn, X)
- Collect reference-style links at the bottom of the file

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
