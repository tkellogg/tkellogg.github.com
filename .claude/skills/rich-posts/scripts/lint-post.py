#!/usr/bin/env python3
"""Lint a post for the rich-posts device syntax.

Catches the mistakes that fail SILENTLY in kramdown — the ones you cannot see
by eyeballing the source or the rendered page:

  1. An inline heading attribute list with anything beyond a bare id
     (`### Foo {#bar .baz}`). kramdown's inline header-id extension accepts
     `{#id}` only. Anything more renders the braces as literal text AND
     poisons the auto-generated id. Put the IAL on the next line instead.
  2. A block IAL (`{: ...}`) separated from what it modifies by a blank line.
     The class is dropped with no warning and no visible artifact.
  3. A note link pointing at a key that does not exist — a link that jumps
     nowhere.
  4. Duplicate note keys. kramdown happily emits duplicate ids; notes-1.js
     then refuses to guess and leaves those links as plain anchors.
  5. A note link whose target heading is not under `## Notes {#notes}`, so
     notes-1.js will not upgrade it.
  6. A referenced local image that is not in the repo.
  7. A blockquote that links to one or more notes but has no `{: .prompt}`
     immediately after it — almost always a forgotten prompt card. Renders
     fine as an ordinary blockquote, so nothing looks broken; the annotated-
     prompt kicker and card styling are just silently absent. WARNING.
  8. A markdown link whose target is not a URL, not a `#anchor`, not an
     existing repo path, and not a defined reference-style label — i.e. a
     placeholder that never got filled in, like `[label](click)`. ERROR.
  9. A raw HTML block opened by `<div`/`<svg` at column 0 whose tags never
     balance back to zero by end of file — a missing or mismatched closing
     tag. ERROR.

     NOT checked, after verifying against this repo's own pinned bundle
     (kramdown 2.4.0 + kramdown-parser-gfm 1.1.0): a blank line *inside* a
     `<div>`/`<svg>` block, or missing blank-line padding before/after it.
     These were the original plan (they are a real CommonMark HTML-block
     rule, and were asserted as verified-broken-here going into this task),
     but reproducing them against the actual bundle — an isolated
     div+svg fixture, a bare `<svg>`, one with *multiple* consecutive blank
     lines inside, and inserting a real blank line into this post's own SVG
     and rendering the full 396-line document — kramdown parsed all of them
     as one intact block every time, zero warnings, no visible artifact.
     kramdown's HTML-block parser evidently tracks tag nesting rather than
     stopping at the next blank line the way plain CommonMark type-6/7 HTML
     blocks do. Shipping that check as an ERROR would have flagged several
     genuinely fine posts (mermaid diagrams with a blank line separating
     subgraph sections) as broken. If this repo's kramdown version or
     GFM parser is ever upgraded, this should be re-verified with the
     reproduction recipe in `references/kramdown-attributes.md` before
     being reconsidered.
 10. A note defined under `## Notes` that no link in the post ever points
     to. It still renders as a visible, un-openable endnote — not broken,
     just probably an orphan left behind by an edit. WARNING.

Not attempted: flagging an `<svg>`/raw-HTML block that sits under the
"wrong" note (content-mismatch, as opposed to a syntax problem). Doing this
reliably would need judging semantic overlap between the block's
`<title>`/`<desc>` and the note's heading/prose — and this repo's own
Subagents diagram ("One task, three effort tiers: Codex orchestrates two
subagents" under a heading that just says "Subagents") is a real example
of a correct pairing with almost no shared keywords. A keyword-overlap
heuristic would flag that as often as it caught a real mistake. Skipped;
a false positive here is worse than a miss.

Usage:  lint-post.py _posts/2026-08-02-my-post.md [...]
Exit 1 if any error is found. Warnings alone exit 0.
"""
import os
import re
import sys

FENCE = re.compile(r'^\s*(```|~~~)')
# `### Title {#id}` or the invalid `### Title {#id .cls}`
INLINE_IAL = re.compile(r'^(#{1,6})\s+.*?\{#([^}]*)\}\s*$')
BLOCK_IAL = re.compile(r'^\s*\{:\s*([^}]*)\}\s*$')
ID_IN_IAL = re.compile(r'#([A-Za-z0-9_-]+)')
LINK = re.compile(r'\[[^\]]*\]\(#([A-Za-z0-9_:.-]+)\)')
IMG = re.compile(r'!\[[^\]]*\]\((/[^)\s]+)')
HEADING = re.compile(r'^(#{1,6})\s+(.*?)\s*$')
BLOCKQUOTE = re.compile(r'^\s*>')
CODE_SPAN = re.compile(r'`[^`]*`')
# Any inline markdown link, excluding images (`![...]`).
GENERIC_LINK = re.compile(r'(?<!!)\[[^\]]*\]\(([^)]+)\)')
# `[label]: target` reference definitions.
REF_DEF = re.compile(r'^\s{0,3}\[([^\]]+)\]:\s*(\S+)')
URL_SCHEME = re.compile(r'^[A-Za-z][A-Za-z0-9+.\-]*:')
RAW_HTML_START = re.compile(r'^<(div|svg)\b', re.I)
RAW_HTML_TAG = re.compile(r'<(/?)(div|svg)\b[^>]*?(/?)>', re.I)


def _strip_target(t):
    """Trim a link target down to its path/URL part: drop an optional
    <...> wrapper and an optional trailing "title"."""
    t = t.strip()
    if t.startswith('<'):
        end = t.find('>')
        if end != -1:
            t = t[1:end]
    m = re.match(r'^(\S+)(?:\s+.*)?$', t)
    if m:
        t = m.group(1)
    return t


def _target_ok(t, repo_root, post_dir, ref_labels):
    """True if a link target resolves to something real or is out of scope
    for this check (URL, anchor, reference label, existing path)."""
    if not t:
        return True
    if t.startswith('#'):
        return True  # validated separately, with a more specific message
    if URL_SCHEME.match(t):
        return True  # http:, https:, mailto:, tel:, data:, ...
    if t.lower() in ref_labels:
        return True
    path_part = t.split('#', 1)[0].split('?', 1)[0]
    if not path_part:
        return True
    if t.startswith('/'):
        last_seg = path_part.rstrip('/').rsplit('/', 1)[-1]
        if '.' not in last_seg:
            # No file extension: almost certainly a Jekyll permalink
            # (`/blog/:year/:month/:day/:title`) or a page directory like
            # `/contact`, neither of which exists as a literal repo path.
            # Unverifiable cheaply; accept it.
            return True
        if repo_root is None:
            return True  # can't verify; don't false-positive
        return os.path.exists(os.path.join(repo_root, path_part.lstrip('/')))
    # Relative, schemeless, non-anchor target.
    if post_dir and os.path.exists(os.path.join(post_dir, path_part)):
        return True
    if repo_root and os.path.exists(os.path.join(repo_root, path_part)):
        return True
    return False


def lint(path, repo_root):
    src = open(path, encoding='utf-8').read()
    body = re.sub(r'\A---\n.*?\n---\n', '', src, flags=re.S)
    offset = src[:len(src) - len(body)].count('\n')
    lines = body.split('\n')
    post_dir = os.path.dirname(os.path.abspath(path))

    errors, warnings = [], []
    # id -> (line_no, level, under_notes)
    ids, in_fence, notes_level = {}, False, None

    for i, line in enumerate(lines):
        n = i + offset + 1
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        h = HEADING.match(line)
        if h:
            level = len(h.group(1))
            if notes_level is not None and level <= notes_level:
                notes_level = None       # left the Notes section

        m = INLINE_IAL.match(line)
        if m:
            inner = m.group(2).strip()
            if re.fullmatch(r'[A-Za-z0-9_-]+', inner):
                key, level = inner, len(m.group(1))
                if key in ids:
                    errors.append((n, 'E', f'duplicate note key "#{key}" '
                                           f'(first seen line {ids[key][0]})'))
                ids[key] = (n, level, notes_level is not None)
                if key == 'notes':
                    notes_level = level
            else:
                errors.append((n, 'E', f'inline heading IAL "{{#{inner}}}" has more '
                                       f'than a bare id — kramdown renders the braces '
                                       f'as literal text. Move it to the next line as '
                                       f'"{{: #{inner}}}".'))
            continue

        b = BLOCK_IAL.match(line)
        if b:
            if i == 0 or lines[i - 1].strip() == '':
                errors.append((n, 'E', f'block IAL "{{: {b.group(1).strip()}}}" is '
                                       f'preceded by a blank line — kramdown drops it '
                                       f'silently. It must be on the line immediately '
                                       f'after the element it modifies.'))
            else:
                idm = ID_IN_IAL.search(b.group(1))
                prev = HEADING.match(lines[i - 1]) if i else None
                if idm and prev:
                    key, level = idm.group(1), len(prev.group(1))
                    if key in ids:
                        errors.append((n, 'E', f'duplicate note key "#{key}" '
                                               f'(first seen line {ids[key][0]})'))
                    ids[key] = (n, level, notes_level is not None)
                    if key == 'notes':
                        notes_level = level
            continue

    # Second pass: links and images (headings are all known now).
    ref_labels = set()
    for line in lines:
        rm = REF_DEF.match(line)
        if rm:
            ref_labels.add(rm.group(1).strip().lower())

    linked_keys = set()
    in_fence = False
    for i, line in enumerate(lines):
        n = i + offset + 1
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        for key in LINK.findall(line):
            linked_keys.add(key)
            if key not in ids:
                errors.append((n, 'E', f'link to "#{key}" but no heading defines that '
                                       f'key — this link jumps nowhere'))
            elif 'notes' in ids and not ids[key][2] and key != 'notes':
                warnings.append((n, 'W', f'link to "#{key}" but that heading is not '
                                         f'under "## Notes {{#notes}}" — notes-1.js '
                                         f'will leave it as a plain anchor'))

        if repo_root:
            for src_path in IMG.findall(line):
                if not os.path.exists(os.path.join(repo_root, src_path.lstrip('/'))):
                    errors.append((n, 'E', f'image "{src_path}" not found in the repo'))

        # Check 8: placeholder / dead link targets.
        line_wo_code = CODE_SPAN.sub('', line)
        for target in GENERIC_LINK.findall(line_wo_code):
            clean = _strip_target(target)
            if not _target_ok(clean, repo_root, post_dir, ref_labels):
                errors.append((n, 'E', f'link target "({target})" is neither a URL, '
                                       f'an anchor, an existing repo path, nor a '
                                       f'defined reference label — looks like a '
                                       f'placeholder that was never filled in'))

    # Check 7: a blockquote linking to note(s) with no `{: .prompt}` right after it.
    if 'notes' in ids:
        in_fence = False
        i = 0
        while i < len(lines):
            line = lines[i]
            if FENCE.match(line):
                in_fence = not in_fence
                i += 1
                continue
            if in_fence:
                i += 1
                continue
            if BLOCKQUOTE.match(line):
                start = i
                j = i
                block_text = []
                while j < len(lines) and BLOCKQUOTE.match(lines[j]):
                    block_text.append(lines[j])
                    j += 1
                text = '\n'.join(block_text)
                if LINK.search(CODE_SPAN.sub('', text)):
                    next_line = lines[j] if j < len(lines) else ''
                    nb = BLOCK_IAL.match(next_line)
                    has_prompt = bool(nb and re.search(r'(?:^|\s)\.prompt(?:\s|$)',
                                                        nb.group(1)))
                    if not has_prompt:
                        report_n = j + offset + 1
                        warnings.append((report_n, 'W',
                            f'blockquote starting at line {start + offset + 1} links '
                            f'to note(s) but has no "{{: .prompt}}" on the line '
                            f'immediately after it — likely a forgotten prompt card'))
                i = j
                continue
            i += 1

    # Check 9: raw HTML blocks (`<div`/`<svg` at column 0) whose tags never
    # balance back to zero — a missing/mismatched closing tag. (Blank-line
    # padding and blank lines inside were tested against this repo's pinned
    # kramdown bundle and do NOT break the block — see the module docstring
    # — so they are deliberately not checked here.)
    in_fence = False
    i = 0
    n_lines = len(lines)
    while i < n_lines:
        line = lines[i]
        if FENCE.match(line):
            in_fence = not in_fence
            i += 1
            continue
        if in_fence:
            i += 1
            continue
        sm = RAW_HTML_START.match(line)
        if sm:
            start = i
            tag = sm.group(1).lower()
            depth = 0
            j = start
            end = None
            while j < n_lines:
                for tm in RAW_HTML_TAG.finditer(lines[j]):
                    is_close = tm.group(1) == '/'
                    is_selfclose = tm.group(3) == '/'
                    if is_close:
                        depth -= 1
                    elif not is_selfclose:
                        depth += 1
                if depth <= 0:
                    end = j
                    break
                j += 1
            if end is None:
                errors.append((start + offset + 1, 'E',
                    f'raw HTML block opened by "<{tag}" at line {start + offset + 1} '
                    f'never closes (tag never balances back to zero by end of file) '
                    f'— a missing or mismatched closing tag'))
                i = n_lines
                continue
            i = end + 1
            continue
        i += 1

    # Check 10: orphan notes — defined under `## Notes` but never linked.
    for key, (line_no, level, under_notes) in ids.items():
        if under_notes and key != 'notes' and key not in linked_keys:
            warnings.append((line_no, 'W', f'note "#{key}" is defined under "## Notes" '
                                           f'but no link in the post points to it — it '
                                           f'will only ever appear as a plain endnote'))

    return errors, warnings


def main():
    if len(sys.argv) < 2:
        print((__doc__ or '').strip())
        return 2
    # Walk up to the Jekyll root rather than counting directories — the skill
    # can be moved or symlinked without silently breaking the image check.
    repo_root = os.path.dirname(os.path.abspath(__file__))
    while not os.path.exists(os.path.join(repo_root, '_config.yml')):
        parent = os.path.dirname(repo_root)
        if parent == repo_root:
            print('lint-post: could not find _config.yml above this script; '
                  'image existence checks are disabled', file=sys.stderr)
            repo_root = None
            break
        repo_root = parent
    failed = False
    for path in sys.argv[1:]:
        errors, warnings = lint(path, repo_root)
        for n, kind, msg in sorted(errors + warnings):
            label = 'error' if kind == 'E' else 'warning'
            print(f'{path}:{n}: {label}: {msg}')
        if errors:
            failed = True
        if not errors and not warnings:
            print(f'{path}: ok')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
