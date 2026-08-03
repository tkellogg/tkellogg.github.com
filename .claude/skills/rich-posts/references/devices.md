# Device catalog

Each device: what it is for, when **not** to use it, exactly what to type, what
it renders to, and what it costs.

---

## 1. The fold

**For:** inline depth. The second, third, and fourth analogy stacked to support
one point. Implementation detail. A long worked example. A tangent you would
otherwise cut entirely.

**Not for:** the argument's spine. If the reader must open it to follow along,
it is not a fold — restructure instead. Also know the SEO cost: collapsed
content is indexed but carries less ranking weight than visible text, so never
fold the passage a post should rank for.

**Type:**

```markdown
<details markdown="1">
<summary>The queueing-theory version of the same point</summary>

Markdown works in here — **bold**, lists, `code`, links.

</details>
```

The blank lines above and below the body are required by kramdown's documented
behavior. (This repo's bundle happens to render correctly without them; do not
rely on that.) `markdown="1"` is what makes the interior parse as markdown
rather than raw HTML.

**Renders:** a native `<details>` / `<summary>`. Baseline for years.

**Summary text matters more than the device.** A good summary tells the reader
what they are choosing to skip — "The queueing-theory version of the same
point," not "More details." A vague summary makes everyone open it, which
defeats the purpose.

**Cost:** zero JavaScript, ~15 lines of CSS already in `notes-1.css`.

---

## 2. The prompt card

**For:** a verbatim artifact quoted at length — a prompt, a model response, a
log line, an error. Signals "this is a specimen, not my prose."

**Not for:** ordinary quotation of a person or a source. That is a normal
blockquote, and diluting the distinction costs you the signal.

**Type:**

```markdown
> Given the photographs, the dimensional measurements, and the fact that the
> hotend rotates freely but cannot translate downward, identify the actual
> retention mechanism before recommending additional force.
{: .prompt}
```

**The `{: .prompt}` line must be the line immediately after the blockquote.** A
blank line between them drops the class silently — no error, no warning, just a
normal-looking blockquote that quietly is not a prompt card. This is lint
check #2.

**Renders:** `<blockquote class="prompt">`, styled monospace with a gold rule.

**Cost:** zero JavaScript. Pure CSS, works forever.

---

## 3. The tap-note

**For:** lateral depth attached to a *phrase*. Why a particular word is there.
A term of art the general reader will not know. Annotating a prompt span by
span — which is the case this was built for, and a genuine gap in the prior art:
there is no general-purpose annotated-prompt viewer on the web.

**Not for:** anything load-bearing. A note is by definition skippable. If the
reader must know it, it goes in the prose. Ration them to about five per post —
a paragraph where everything is highlighted is a new kind of wall.

**Type:**

```markdown
The hotend [rotates freely but cannot drop](#spin) — which is the whole puzzle.

## Notes {#notes}

### The paradox
{: #spin}

A recessed set screw whose tip still catches an internal groove even when it is
loose enough to let the shaft spin. **Free rotation is not proof.**
```

The trigger is a plain markdown link. There is no new syntax to remember. The
convention "links targeting a heading under `## Notes` are notes" is what makes
it a note, and `lint-post.py` enforces it.

**Renders:** without JavaScript, an ordinary anchor to a visible endnotes
section. With `notes-1.js`, the link becomes a `<button>` that opens a note
card — a bottom sheet on phones, a centered card with a backdrop on wider
screens, and the endnote copy is hidden so there is no duplicate appendix.

**The Notes section does not have to be last.** The collector reads `<h3 id>`
siblings after the Notes heading and stops at the next heading of the *same or
higher rank* — so a `# Why Codex?` (h1) or another `## Section` (h2) after the
notes correctly ends the block and renders normally. This was a real bug once:
the walk was hardcoded to stop only at `H2`, so an `<h1>` after the notes got
swallowed into the last note's body and then hidden along with it. If you touch
that loop, compare heading *rank*, never a specific tag name.

**Note bodies must read acceptably as endnotes**, because in RSS, Reader Mode,
and no-JS that is exactly what they are. Write them as short standalone
paragraphs, 40–80 words. That is the real cost of this device: a four-note post
is 200–300 words of new prose. It is payable because it is the material
otherwise crammed into italic parentheticals — and for research-driven posts,
draft the note bodies from the source files and let Tim edit them into voice.

**No ARIA by hand.** `popovertarget` gives the button an implicit
`aria-details`/`aria-expanded` relationship to the card it opens. Setting
`aria-details` manually overrides that correct implicit link with a worse one
(a bare heading id).

**Cost:** `notes-1.js` (~4KB, deferred, exits immediately on pages with no
`#notes` heading) plus the note prose.

---

## 4. The stepper

**For:** a revealed sequence where the reader should see one step at a time — a
5-Whys, a debugging trail, a chain of deductions. Tim has hand-faked this before
with a literal "..." in `_posts/2026-04-14-forgetting.md`.

**Not for:** items the reader should compare side by side. Comparison wants a
table or a list, not a device that hides all but one.

**Type:**

```markdown
<details name="whys" markdown="1">
<summary>1. Why won't the hotend come out?</summary>

Because something is still retaining it.

</details>
<details name="whys" markdown="1">
<summary>2. Why is it still retained if the screw is loose?</summary>

Because "loose" and "clear" are different states.

</details>
```

The shared `name` is what makes opening one close the others — no JavaScript.
Baseline September 2025; older browsers degrade to independently-openable
sections, which is a perfectly fine fallback.

**Cost:** CSS only. Build when a post wants it.

---

## 5. The standalone page, embedded

**For:** anything that is an application — real state, simulation, WebGL, a
canvas. The 3D printer repair guide with its set-screw simulator is the type
specimen.

**Not for:** anything a fold or a note can carry. Reach for this only when the
thing genuinely needs to be a program.

**Building it:** use the `add-jsx` skill for a React component, or the existing
`lab/` + `boredom/` + `nitinol-tools.html` pattern — a self-contained directory
at the repo root, which Jekyll copies through untouched (an `index.html` with no
front matter is treated as a static file, not a template). For a Vite app set
`base: "./"` so the bundle uses relative asset paths and the same `dist/` works
at any URL without a rebuild. Drop the sourcemap; it is often several times the
size of the app itself and is a debug artifact.

**Opening it:**

```markdown
<a class="embed-app" href="/printer-rescue/" data-title="Finder 3 rescue guide">Open Report</a>
```

Renders as a button, opens the app in a 90vw × 90vh modal dialog with the title,
an "Open in new tab ↗" link, and a close button. Full-bleed under 640px, because
a 90% box wastes what little room a phone has.

**It must be an `<a>`, never a `<button>`.** Cmd-click, Ctrl-click, Shift-click,
middle-click, and the right-click "Open in new tab" menu all work with zero code,
because the browser already knows what an `href` means. The script only
intercepts an unmodified left click. With JavaScript off it is a plain link to
the app — the un-enhanced state was already correct, so there is nothing to
build a fallback for.

**The iframe unloads on close.** An embedded app with a render loop keeps
burning CPU and battery behind a closed dialog otherwise. Cleanup watches the
dialog's `open` attribute with a MutationObserver rather than listening for the
`close` event — Chrome was observed here never firing `close` at all, while
`dlg.open` flipped correctly. Watching state also catches every close path at
once: the button, the backdrop, our Escape handler, and the browser's native
Escape. If you extend this device, do not reintroduce a dependence on `close`.

**Knowing this boundary is part of the job.** When a device wants state, it is a
page, not a device. Embed or link to it; do not try to inline it.

---

## Inventing a one-off device

A single post can carry its own `<style>` and `<script>` at the bottom, keyed to
a class no other post uses. Unknown classes are inert everywhere else on the
site, so the blast radius is exactly one post.

```markdown
Tap [this passage](#thing){: .my-experiment} to try it.

<style>
.note-link.my-experiment { border-bottom-style: solid; }
</style>
```

This is the medium-exploration loop. Try a device in one post. If you reach for
it a second time, graduate it into `notes-1.js` and `notes-1.css`. Nothing
accumulates in the shared files until it has earned its place — which is what
keeps the shared files small enough to stay understandable.
