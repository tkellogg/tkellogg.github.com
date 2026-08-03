---
name: rich-posts
description: This skill should be used when a post is a wall of text, when detail needs to be kept but hidden away, when the user asks to "clean this up visually", "make this more interactive", "shorten this post", "hide the details", "add a tap-to-explain", "annotate this prompt", or when adding any structural/interactive device to a post. Covers folds, tap-notes, prompt cards, and steppers.
version: 1.0.0
---

# Rich Posts — structural devices for the blog

This skill owns the **structural and interactive layer** of a post: how detail is
hidden, revealed, and annotated. It does not own voice or images.

| Need | Skill |
|---|---|
| Voice, paragraph shape, bold anchors | `writing-style` |
| Mermaid, charts, cover images, AI images | `images` |
| A React app as its own page | `add-jsx` |
| Folds, tap-notes, prompt cards, steppers | **this one** |

## The problem these devices solve

Tim writes for two audiences at once: readers who need it **short**, and
detail-seekers who want everything. `writing-style` already handles this in
prose — the "intentionally skippable paragraph," where the wall-of-text *shape*
signals "skip me." These devices are the structural version of the same move.

The rule that makes or breaks it: **the short version must be genuinely complete
on its own.** If a reader has to open a fold to follow the argument, the post is
a wall of text with extra clicks, and both audiences are worse off. Draft the
short version first. Treat every fold as material you **cut**, not material you
hid. If you find yourself folding the argument's spine, the post needs
restructuring, not a device.

Interactivity is not the cure for walls of text. Structure is the cure;
interactivity is what makes structure affordable without flattening the voice.

## Before using any JavaScript device — check the install

The tap-note needs two files that **may not be installed yet**. Check:

```bash
ls css/notes-1.css public/notes-1.js 2>/dev/null
grep -c notes-1 _layouts/default.html
```

If either is missing, install them (this is a one-time, ~2 minute job):

1. `cp .claude/skills/rich-posts/assets/notes-1.css css/`
2. `cp .claude/skills/rich-posts/assets/notes-1.js public/`
3. Add to the `<head>` of `_layouts/default.html`, unconditionally — **no
   front-matter flag.** The script exits immediately unless the page has a
   `#notes` heading, and a flag only creates a class of silent
   forgot-the-flag failures:
   ```html
   <link rel="stylesheet" href="/css/notes-1.css">
   <script defer src="/public/notes-1.js"></script>
   ```

Filenames are version-pinned (`notes-1`), matching the existing
`mermaid-11.14.0-min.js` convention. If a v2 ever exists, old posts keep loading
v1 and published pages never reflow. **Never edit `notes-1.*` in place** once
posts depend on it — copy to `notes-2.*` and migrate deliberately.

Folds and prompt cards are CSS-only and work the moment `notes-1.css` is
installed, with or without the JavaScript.

## The devices

Full syntax, when-not-to-use, and rendered output: `references/devices.md`.
Quick version, in the order you should reach for them:

**1. The fold** — inline depth. The workhorse, and the one that most directly
shortens a post. Use it for the second, third, and fourth analogy stacked to
support one point; for implementation detail; for the long worked example. Pure
CSS, no JavaScript, degrades to a plain block everywhere.

```markdown
<details markdown="1">
<summary>The queueing-theory version of the same point</summary>

Markdown here — blank lines above and below are required.

</details>
```

**2. The prompt card** — a blockquote styled as a verbatim artifact (a prompt,
a log line, a model response). Pure CSS.

```markdown
> Given the photographs and the dimensional measurements, identify the
> retention mechanism before recommending additional force.
{: .prompt}
```

**3. The tap-note** — lateral depth, attached to a phrase. For "why is this
word here," terms of art, and annotating a prompt span by span. Needs
`notes-1.js`.

```markdown
The hotend [rotates freely but cannot drop](#spin) — which is the whole puzzle.

## Notes {#notes}

### The paradox
{: #spin}

A recessed set screw whose tip still catches an internal groove even when it is
loose enough to let the shaft spin. **Free rotation is not proof.**
```

**4. The stepper** — a revealed sequence (a 5-Whys, a debugging trail).
Consecutive `<details name="steps">` blocks; the shared name makes opening one
close the others. CSS-only, Baseline since September 2025.

**5. The standalone page, embedded** — when a device wants real state or
simulation, it is a page, not a device. Build it with the `add-jsx` skill or the
`lab/` + `boredom/` pattern, drop it in a top-level directory that Jekyll copies
through untouched, then open it in a near-fullscreen modal from the post:

```markdown
<a class="embed-app" href="/printer-rescue/" data-title="Finder 3 rescue guide">Open Report</a>
```

It is an anchor, not a button, and that is the whole design: Cmd-click,
Ctrl-click, middle-click and "open in new tab" all work for free because the
browser already knows what to do with an `href`, and without JavaScript it is
just a link to the app. A `<button>` would need every one of those
reimplemented, badly. `data-title` is optional and defaults to the link text.
Vite apps need `base: "./"` so the build works at any path.

## Parameterizing: classes and data attributes

Classes and `data-*` on both the trigger and the note body ride through kramdown
and are carried onto the rendered elements by `notes-1.js`:

```markdown
Tap [this phrase](#spin){: .popup} to see.

### The paradox
{: #spin .wide data-kind="aside"}
```
→ `<button class="note-link popup">` and `<div class="note-pop wide" data-kind="aside">`

**Name the device, not the presentation.** A class should mean "this is a
lateral aside"; it should never mean "put this on the left" or "make this
yellow". The CSS decides that a card is a bottom sheet on a phone and a centered
card on a laptop — Tim never picks. Every knob is a decision at writing time,
and decisions at writing time are exactly the tax this system exists to delete.
Reserve `data-*` for genuine per-instance values only you can know: a
coordinate, an image path, a step number.

**Inventing a one-off device is cheap and safe.** A single post can carry its own
`<style>` and `<script>` at the bottom keyed to a class nobody else uses —
unknown classes are inert everywhere else on the site. That is the medium-
exploration loop: try it in one post, and if you reach for it a second time,
graduate it into `notes-1.js`. Nothing accumulates until it has earned its place.

## Rules that must not be broken

**Content first, JavaScript second.** Every device's content exists in the served
HTML, visible by default. JavaScript only *moves* it. This is what keeps RSS,
Reader Mode, Googlebot, and no-JS readers whole — the note body is a real
`<h3>` with real prose in a real endnotes section. Never write a device where JS
*creates* the content.

**Ration the tap-notes.** Roughly five per post. Genius.com is the cautionary
tale: a paragraph where everything is highlighted is a new kind of wall. A note
is by definition skippable — if the reader must know it, it belongs in the
prose. If a note outgrows a short paragraph, it is a section.

**Keys unique per post.** kramdown will happily emit duplicate ids;
`notes-1.js` then refuses to guess and leaves those links as plain anchors.

**No mermaid inside a note body** in v1. Cloning a rendered mermaid SVG
duplicates its internal ids. `notes-1.js` detects this and safely skips those
links, leaving them as plain anchors.

## Ways to break a post silently — always lint

The first two produce no error, no warning, and no visible artifact:

1. `### Title {#key .popup}` — kramdown's inline header-id extension accepts a
   **bare id only**. With a class added, the braces render as literal text and
   the auto-generated id is poisoned. Put the attribute list on the next line:
   `{: #key .popup}`.
2. A blank line before a `{: ...}` line drops the class **silently** — a
   normal-looking blockquote that quietly is not a prompt card.
3. Forgetting the `{: .prompt}` line entirely after a blockquote that links to
   note(s) — same symptom as #2 (a normal-looking, un-styled blockquote), just
   a different way to arrive at it: the annotated-prompt card was never added
   in the first place rather than dropped by a stray blank line. `lint-post.py`
   flags this as a warning, since an ordinary requoted fragment with no note
   links is a legitimate plain blockquote and shouldn't be forced into a card.
4. A typo'd note key is a link that jumps nowhere.
5. A placeholder link target that was never filled in — `[label](click)`
   instead of a real path. Renders as a real, clickable, wrong link; nothing
   in the build complains. `lint-post.py` treats this as an error unless the
   target is a URL, a `#anchor`, an existing repo path, or a defined
   reference-style label.

```bash
python3 .claude/skills/rich-posts/scripts/lint-post.py _posts/2026-08-02-my-post.md
```

Run it before every push on any post using these devices. Exit 1 on error.

`lint-post.py` also warns on a note defined under `## Notes` that nothing
links to (a harmless orphan, but usually leftover from an edit), and errors on
a `<div>`/`<svg>` raw HTML block at column 0 whose tags never balance back to
zero (a missing or mismatched closing tag). It deliberately does **not** flag
a blank line inside a raw HTML block, or missing blank-line padding around
one — that looked like it should be a silent-failure case too, but
reproducing it against this repo's actual pinned bundle (kramdown 2.4.0 +
kramdown-parser-gfm 1.1.0, several fixtures plus the full text of this post
with a live blank line inserted into its own SVG) showed kramdown parses the
raw block as one intact element regardless; see the checks' docstring in
`scripts/lint-post.py` for the reproduction. Re-verify before ever adding
that check back.

## What is verified, and what is not

Verified by running it: the kramdown behavior above against this repo's own
bundle (kramdown 2.4.0 + GFM); the full tap-note interaction driven in Chrome at
a 390×844 phone viewport — the trigger becomes a `<button>`, the bottom sheet
opens within the viewport, author classes ride across from both the link and the
heading, the close button dismisses, "Read in the endnotes" closes the card and
jumps, and the console is clean; and every check in `lint-post.py` against
deliberately broken fixtures.

**Not verified: real iOS Safari.** Every mobile result above is Chrome emulating
a phone. Tap-outside light-dismiss is a documented open WebKit bug on iOS, which
is why the card has a visible 44px close button rather than relying on it. On
iOS 16 and earlier there is no Popover API at all, so triggers stay ordinary
anchors that jump to the endnotes. Write the surrounding prose ("tap the
highlighted passages") so it still reads fine if nothing pops.
