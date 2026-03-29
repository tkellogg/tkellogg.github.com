# Tim Kellogg Writing Style — Detailed Examples

This reference contains real examples from Tim's blog posts organized by technique. Use these as calibration when writing in his voice.

## Anchor Paragraphs (5-8 words, standalone)

These are single-sentence paragraphs that act like visual speed bumps. The reader's eye catches them instantly and they anchor expectations.

- "Systems software."
- "Learn the domain."
- "That's inner loop agents."
- "This is the way."
- "Slop. Good code should be slop."
- "It's systems all the way down."
- "A paradox!!!"
- "It collapses."
- "Claude Code is software."
- "Focus on what matters."
- "There is no third option."

**When to use:** After explaining a concept (as a landing pad), before diving deeper (as a thesis), or as a pivot between sections.

## Bold Text Patterns

Bold marks the skeleton of the argument. A reader scanning only bold text should get the gist.

### Key insight of a passage:
- "The more time spent planning, the longer and more complex the implementation phase was."
- "code should be slop"
- "don't do things that don't work"

### Surprising claims or contrasts:
- "the agent doesn't"
- "they're mostly a lie"
- "not both"

### Introduced terminology:
- "untrusted content (red)"
- "Critical Actions (blue)"
- "synthetic dopamine"
- "the **Agent Attention Economy**"
- "**context engineering**"

### Double emphasis (bold+italic):
- "_**Clearly stated:**_"
- "_**ALL**_"
- "_**didn't use tools**_"

## Opening Patterns

Openers are crafted with the target reader in mind. They say something the reader already half-believes but hasn't heard said out loud — it resonates but also feels loud and unorthodox. The intro is minimal orientation: just enough to tell the reader what this is and who it's for, then drop them in.

### Provocative thesis:
> Plan mode *feels* good. It's like taking a bath in rich sophistication.

> AI code is slop.

> I can't think of any strong technological reasons for MCP to exist.

### Direct challenge:
> Are you good at agentic coding? How do you even **evaluate that?**

### Question:
> We always give AI **something** to do. [...] What happens when we give an AI **nothing** to do?

### "I was wrong" opener:
> I was wrong. Or at least overly ambitious.

## Closing Patterns

Closings tie together the threads from the post and point long into the future. They are NOT recaps or summaries — the reader was there, they don't need a restatement. The closer connects ideas and gestures forward.

### Open question pointing forward:
> Where did you end up? Is there life beneath? Or just plain mechanics?

### Simple declarative:
> Go forth and call functions!
> There you have it.

### Forward-looking:
> Watch this space. Keep an open mind.
> What will happen in the second half of '25? Not sure, but I can't wait to find out.

### Tying threads together:
> Our job as software engineers **isn't to write code**.

### Personal reflection pointing forward:
> I'm not 100% sure how I feel about this stuff.

## Humor Examples

### Deadpan understatement:
> They expected AGI, the **AI god**, but instead got merely the best model in the world. _v disapointng_

### Self-deprecating:
> Maybe I'm weird (okay fine, I am)
> I don't even know anymore. This used to be clear.

### Sarcastic advice delivered straight:
> tell your boss that you're not going to use AI tools because you believe your objective does not include quickly delivering value. Just try it. I'm sure it'll go well.

### Mock formality:
> "Obviously we'll develop in Docker, as one does when they're *as sophisticated as you*"

### Parenthetical jabs:
> (I made Strix for my own ADHD, but sometimes I think it has ADHD)

### Breaking the fourth wall:
> I mean, you have one of these tabs open too, right? riiiight????

### Internet-native casualisms:
> "lol n00b"
> "yada yada yada..."
> "NGL this freaks me out."
> "idk sometimes you just have to look at the code to be sure"

## Analogy Patterns

Analogies bridge from the familiar to the wild idea. Introduced casually, never with "This is like..."

### Management/organizations:
- AI agent autonomy compared to employee handbooks and management styles
- Viable System Model applied to coding agents

### Physics/thermodynamics:
- Dissipative systems, entropy, attractor basins
- "Basically, if you envision an LLM as being a muffin tin..."

### Everyday life:
- Road trips with kids
- Woodworking and chisels for tool familiarity
- Parenting dynamics

### Biology:
- Barred owls, tiger migration
- Evolution and natural selection

## Argument Progression Example

From "Plan Mode" post — follows the exact pattern:

1. **Provocative opening:** "Plan mode *feels* good. It's like taking a bath in rich sophistication."
2. **Caricature as grounding:** Fake dialog showing plan mode being sycophantic
3. **Framework:** Introduces "bliss attractor" concept — the planning feels productive but delays real work
4. **Evidence:** Links to research showing planning correlates with longer, more complex implementations
5. **Steelman:** "That's a caricature, but it scratches at something real."
6. **Practical advice:** When to actually use plan mode
7. **Brief close:** "Plan Mode is a trap. Well no, it's not inherently a problem..."

## Structural Conventions

### Discussion section (end of every post):
```markdown
# Discussion

[Bluesky][bsky] &#124; [Hacker News][hn] &#124; [Lobste.rs][lob]
```

### Reference-style links (bottom of file):
```markdown
[bsky]: https://bsky.app/profile/...
[hn]: https://news.ycombinator.com/item?id=...
[paper]: https://arxiv.org/abs/...
```

### Blockquote attribution:
```markdown
> Quoted text here

-- Source Name
```

### Series cross-references:
```markdown
{% include tag-timeline.html %}
```

## Sentence-Level Patterns

### Starting with conjunctions:
> But this paper..
> And that's the _lens_ I saw GPT-5 through.
> But does it?

### Trailing double dots (not ellipsis):
> "But this paper.."
> "But first.."
> "Okay, but why..."

### Characteristic hedges:
> "I tend to think"
> "Feels like"
> "The thing is"

### Characteristic emphasis words:
> "Wild" — "The wild part?" / "This whole thing has been wild."
> "Honestly" as an opener
> "The thing is" as a transition

## Vocabulary Notes

- Uses "it's" for possessive "its" consistently (a quirk — preserve it)
- Uses internet abbreviations naturally: "idk", "NGL", "TBQH", "AFAICT", "tl;dr", "BTW"
- "Slop" / "slopped out" for low-quality generated content
- "Wild" as an adjective of wonder
- "Feels like" for subjective technology impressions
