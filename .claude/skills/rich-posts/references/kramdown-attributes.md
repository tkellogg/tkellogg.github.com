# kramdown attribute lists — what actually works

All results below were produced by running the source through **this repo's own
bundle** (`bundle exec`, kramdown 2.4.0 with the GFM parser), not from memory or
documentation. Re-run the commands at the bottom if you doubt any of it.

## Why this file exists

Attribute lists are what make a personal device vocabulary possible without a
custom format or a build step. `{: #key .popup data-x="y"}` has the same
expressive power as `<note id="key" kind="popup" x="y">` — id, type, arbitrary
parameters — while staying markdown, riding the stock GitHub Pages build, and
degrading to plain HTML.

This repo builds on **GitHub Pages' default builder** (the `github-pages` gem,
no `.github/workflows`), which runs Jekyll in safe mode. Custom Ruby plugins and
custom Liquid tags are impossible without moving to a GitHub Actions build.
Attribute lists are the ceiling, and they are a high one.

## The matrix

| Source | Result |
|---|---|
| `[x](#k)` | `<a href="#k">x</a>` |
| `[x](#k){: .popup}` | `<a href="#k" class="popup">x</a>` |
| `[x](#k){: .a .b data-side="right"}` | `<a href="#k" class="a b" data-side="right">x</a>` |
| `### T {#k}` | `<h3 id="k">T</h3>` |
| `### T {#k .popup}` | **BROKEN** — see below |
| `### T`<br>`{: #k .popup}` | `<h3 id="k" class="popup">T</h3>` |
| `### T`<br>`{: #k .a data-kind="aside"}` | `<h3 id="k" class="a" data-kind="aside">T</h3>` |
| `> quote`<br>`{: .prompt}` | `<blockquote class="prompt">…</blockquote>` |
| `> quote`<br><br>`{: .prompt}` | **BROKEN, SILENTLY** — see below |

Span IALs work inside blockquotes, so a link inside a `{: .prompt}` card keeps
its own classes. Verified.

## The two failures

### Inline heading IAL with anything beyond a bare id

kramdown's inline header-id extension accepts `{#id}` and nothing else. Adding a
class does not error — it falls through to literal text **and** poisons the
auto-generated id:

```
### Inline form {#spin .popup}
```
```html
<h3 id="inline-form-spin-popup">Inline form {#spin .popup}</h3>
```

Visible on the page, so at least it is loud. Note also that the literal text
gets smart-quoted: `data-kind="aside"` became `data-kind=”aside”` with curly
quotes. **Fix:** put the attribute list on the next line as `{: #spin .popup}`.

Because of this, prefer the next-line form **always**, even when you only need
an id. One rule instead of two, and no chance of hitting the cliff later when
you add a class.

### A block IAL separated by a blank line

```
> a prompt

{: .prompt}
```

The class is dropped with **no warning, no error, and no visible artifact** — a
normal-looking blockquote that quietly is not a prompt card. This is the nastiest
failure in the system because nothing on the page or in the build tells you.
It is lint check #2 for exactly that reason.

## What is not possible here

- Custom Liquid tags or `_plugins/` — GitHub Pages safe mode.
- Attributes on arbitrary inline spans of text that are not already an element.
  A link is the trigger because a link is a real element; a bare phrase is not.
- `kramdown-math-katex` is in the Gemfile but is **not** on GitHub Pages'
  supported-plugins list, so this repo already has one local-vs-production
  divergence. Do not assume blanket parity; smoke-test the deployed URL after
  any change to these components.

## Reproducing

```bash
cd /Users/tim/code/tkellogg.github.com
bundle exec ruby -e '
require "kramdown"; require "kramdown-parser-gfm"
src = File.read("/path/to/test.md")
d = Kramdown::Document.new(src, input: "GFM", auto_ids: true)
puts d.to_html
STDERR.puts "WARNINGS: #{d.warnings.inspect}"'
```

`d.warnings` was empty for every case above, including both silent failures —
kramdown does not consider them errors. That is why the lint exists.
