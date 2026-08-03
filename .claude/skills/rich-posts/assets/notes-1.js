/* notes-1.js — tap-to-explain notes, v1.

   Upgrades in-post links that target an <h3 id> under "## Notes {#notes}"
   into buttons that open a note card (native Popover API). Without JS, or on
   browsers without the Popover API (iOS 16 and earlier), the links stay
   ordinary anchor jumps to the visible endnotes section. The note text always
   exists in the served HTML — this script only MOVES it. That is what keeps
   RSS, Reader Mode, Googlebot and no-JS readers whole. Never change that.

   Endnotes are for the no-JS case ONLY. When this script runs and successfully
   upgrades a note, it HIDES that note's endnote copy — the experience is
   purely click-based, and a reader with JS never sees a duplicate appendix. A
   note that could not be upgraded (duplicate key, contains mermaid, defined but
   never linked) stays visible, so its plain anchor link still lands somewhere
   real. If every note was upgraded, the "Notes" heading itself is hidden too.

   Author-supplied classes and data-* attributes are carried through:
     [the phrase](#key){: .popup}   -> <button class="note-link popup">
     ### Title
     {: #key .wide data-x="y"}      -> <div class="note-pop wide" data-x="y">
   So a single post can define its own device with an inline <style> block and
   a class nobody else uses, with no risk to any other post.

   Deliberate v1 limitations:
   - No CSS anchor positioning. Cards are centered on wide screens and a bottom
     sheet on phones. (The anchored variant was tested and overlapped the very
     prompt it annotated; centered is calmer and all-Baseline.)
   - Note bodies containing a .mermaid diagram are NOT upgraded — cloning a
     rendered mermaid SVG duplicates its internal ids, which is invalid HTML
     and can corrupt url(#id) references. Those links stay plain anchors.
   - Duplicate {#key} headings fail loud: a console warning, and every link to
     that key stays a plain anchor rather than guessing which body wins.       */
(function () {
  'use strict';
  if (!HTMLElement.prototype.hasOwnProperty('popover')) return;
  var notesHeading = document.getElementById('notes');
  if (!notesHeading) return;

  // Collect note bodies: each <h3 id> after the Notes heading, stopping at the
  // next heading of the SAME OR HIGHER rank — that heading starts a new section
  // of the post, not another note.
  //
  // This must not be hardcoded to H2. The Notes heading is an <h2>, but a post
  // can perfectly well have an <h1> section after it ("# Why Codex?"), and a
  // walk that only stops at H2 sails straight past it, swallows the rest of the
  // post into the last note's body, and then hides it. That is a real bug this
  // code shipped with.
  var notesRank = +notesHeading.tagName.charAt(1);
  var sections = Object.create(null);
  var notesEnd = null;   // the heading that terminated the Notes block, if any
  var el = notesHeading.nextElementSibling, cur = null;
  while (el) {
    var rank = /^H[1-6]$/.test(el.tagName) ? +el.tagName.charAt(1) : 0;
    if (rank && rank <= notesRank) { notesEnd = el; break; }
    if (el.tagName === 'H3' && el.id) {
      if (sections[el.id]) {
        console.warn('notes-1: duplicate note key "#' + el.id +
          '" — links to it are left as plain anchor links');
        sections[el.id].dup = true;
        cur = null;
      } else {
        cur = sections[el.id] = { title: el.textContent, heading: el, nodes: [], dup: false };
      }
    } else if (cur) {
      cur.nodes.push(el);
    }
    el = el.nextElementSibling;
  }

  /* Note bodies are CLONED into their card, so any id inside one would then
     exist twice in the document — invalid HTML, and actively breaking for SVG,
     where url(#id), aria-labelledby and <use href="#id"> all resolve to the
     FIRST match. A figure cloned into a card would silently borrow the
     original's gradients, masks and labels.
     So: rewrite every id in the clone to a unique name, and repoint everything
     that referenced it. */
  function namespaceIds(root, prefix) {
    var owned = root.querySelectorAll('[id]');
    if (!owned.length) return;
    var map = Object.create(null);
    owned.forEach(function (el) {
      var old = el.id;
      map[old] = prefix + old;
      el.id = map[old];
    });
    var keys = Object.keys(map);
    // Attributes that can hold an id reference, by url(#x), #x, or an id list.
    var REFS = ['aria-labelledby', 'aria-describedby', 'aria-details', 'aria-owns',
      'aria-controls', 'for', 'headers', 'href', 'xlink:href', 'fill', 'stroke',
      'clip-path', 'mask', 'filter', 'style', 'marker-start', 'marker-mid',
      'marker-end', 'use'];
    root.querySelectorAll('*').forEach(function (el) {
      REFS.forEach(function (attr) {
        var v = el.getAttribute && el.getAttribute(attr);
        if (!v || v.indexOf('#') === -1) return;
        keys.forEach(function (old) {
          v = v.split('#' + old + ')').join('#' + map[old] + ')')   // url(#old)
               .split('#' + old + '"').join('#' + map[old] + '"');
          if (v === '#' + old) v = '#' + map[old];                   // href="#old"
        });
        el.setAttribute(attr, v);
      });
      // space-separated idref lists (aria-labelledby="a b")
      ['aria-labelledby', 'aria-describedby', 'headers'].forEach(function (attr) {
        var v = el.getAttribute && el.getAttribute(attr);
        if (!v) return;
        el.setAttribute(attr, v.split(/\s+/).map(function (t) { return map[t] || t; }).join(' '));
      });
    });
    // <style> inside an SVG can select by id too.
    root.querySelectorAll('style').forEach(function (s) {
      var t = s.textContent;
      keys.forEach(function (old) { t = t.split('#' + old).join('#' + map[old]); });
      s.textContent = t;
    });
  }

  var n = 0;
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    var id = a.getAttribute('href').slice(1);
    var sec = sections[id];
    if (!sec || sec.dup) return;
    // Leave alone only the links that sit INSIDE the Notes block — i.e. after
    // the Notes heading and before whatever heading ended it. Testing merely
    // "comes after the Notes heading" is wrong and was a real bug: when the
    // Notes section sits mid-post, every link in every later section got
    // skipped and silently stayed a plain anchor.
    var after = !!(notesHeading.compareDocumentPosition(a) & Node.DOCUMENT_POSITION_FOLLOWING);
    var beforeEnd = !notesEnd ||
      !!(notesEnd.compareDocumentPosition(a) & Node.DOCUMENT_POSITION_PRECEDING);
    if (after && beforeEnd) return;
    // v1 limitation: notes containing mermaid stay plain anchor links.
    var hasMermaid = sec.nodes.some(function (node) {
      return node.matches('.mermaid') || node.querySelector('.mermaid');
    });
    if (hasMermaid) return;

    n += 1;
    var pop = document.createElement('div');
    pop.id = 'note-pop-' + n;
    pop.className = 'note-pop';
    pop.setAttribute('popover', ''); // "auto": Esc + light-dismiss where the browser provides them

    // Carry the author's heading IAL onto the card, so `{: #key .wide}` can be
    // styled per-post. The id is NOT copied — it belongs to the endnote, and
    // duplicating it would break the "read in the endnotes" jump.
    sec.heading.classList.forEach(function (c) { pop.classList.add(c); });
    Object.keys(sec.heading.dataset).forEach(function (k) { pop.dataset[k] = sec.heading.dataset[k]; });

    var head = document.createElement('div');
    head.className = 'note-pop-head';
    var title = document.createElement('p');
    title.className = 'note-pop-title';
    title.textContent = sec.title;
    var close = document.createElement('button');
    close.type = 'button';
    close.className = 'note-pop-close';
    close.setAttribute('popovertarget', pop.id);
    close.setAttribute('popovertargetaction', 'hide');
    close.setAttribute('aria-label', 'Close note');
    close.textContent = '×';
    head.appendChild(title);
    head.appendChild(close);
    pop.appendChild(head);

    // Echo the passage the reader actually clicked, so the card stands on its
    // own — by the time it is open on a phone it may be covering the sentence
    // it explains, and "which words did I tap?" should never be a question.
    var quote = document.createElement('blockquote');
    quote.className = 'note-pop-quote';
    quote.textContent = a.textContent;
    pop.appendChild(quote);

    sec.nodes.forEach(function (node) {
      var clone = node.cloneNode(true);
      namespaceIds(clone, 'np' + n + '-');
      pop.appendChild(clone);
    });

    document.body.appendChild(pop);
    sec.converted = true;

    // Swap the link for a real button: this is disclosure, not navigation.
    // No manual ARIA here on purpose — popovertarget gives the button an
    // implicit aria-details/aria-expanded relationship to the popover it
    // opens, and setting aria-details by hand would override that correct
    // implicit link with a worse one (a bare heading id).
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'note-link';
    // Preserve the author's link IAL: [x](#k){: .popup} keeps .popup.
    a.classList.forEach(function (c) { btn.classList.add(c); });
    Object.keys(a.dataset).forEach(function (k) { btn.dataset[k] = a.dataset[k]; });
    btn.innerHTML = a.innerHTML;
    btn.setAttribute('popovertarget', pop.id);
    a.replaceWith(btn);

    // Move focus into the card when it opens and hand it back to the trigger
    // when it closes. Without this a keyboard or screen-reader user tabs on
    // from where they were and never reaches the note they just opened.
    pop.addEventListener('toggle', function (e) {
      if (e.newState === 'open') {
        pop.setAttribute('tabindex', '-1');
        pop.focus();
      } else if (document.activeElement === pop || pop.contains(document.activeElement)) {
        btn.focus();
      }
    });
  });

  // Endnotes exist for readers without JavaScript. This reader has it, so hide
  // every note that became a card. Anything NOT upgraded stays visible, because
  // its link is still a plain anchor that has to land somewhere.
  var anyLeftVisible = false;
  Object.keys(sections).forEach(function (id) {
    var sec = sections[id];
    if (sec.converted) {
      sec.heading.hidden = true;
      sec.nodes.forEach(function (node) { node.hidden = true; });
    } else {
      anyLeftVisible = true;
    }
  });
  if (!anyLeftVisible) notesHeading.hidden = true;

  function closeAll(except) {
    document.querySelectorAll('.note-pop').forEach(function (p) {
      if (p !== except && p.matches(':popover-open')) p.hidePopover();
    });
  }

  // Tap/click outside to close. popover="auto" already light-dismisses in
  // Chrome and desktop Safari, but it is a documented open WebKit bug on iOS,
  // and closing by tapping away is the gesture people expect on a phone. This
  // is belt-and-braces: harmless where the platform already does it.
  document.addEventListener('click', function (e) {
    // The click that OPENS a card also bubbles here — don't immediately close it.
    if (e.target.closest && e.target.closest('.note-link')) return;
    document.querySelectorAll('.note-pop').forEach(function (p) {
      if (p.matches(':popover-open') && !p.contains(e.target)) p.hidePopover();
    });
  });

  // Escape closes. popover="auto" is supposed to give this for free, but it was
  // observed NOT firing in a real Chrome page, so it is handled explicitly
  // rather than trusted. Capture phase, so it wins regardless of focus.
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' || e.key === 'Esc') closeAll(null);
  }, true);
})();

/* ---------------------------------------------------------------- embed-app
   <a class="embed-app" href="/some-app/">Open Report</a>
   opens that URL in a near-fullscreen modal iframe instead of navigating away.

   It is an ANCHOR, not a button, and that is the whole design:
   - Cmd-click, Ctrl-click, middle-click and "open in new tab" all work for free,
     because the browser already knows what to do with a real href. A <button>
     would need every one of those reimplemented, badly.
   - Without JavaScript it is simply a link to the app. Nothing to fall back to,
     because the un-enhanced state was already correct.
   The iframe src is set on open and CLEARED on close — the embedded app runs a
   Three.js render loop, and leaving it mounted burns CPU and battery behind a
   closed dialog.                                                             */
(function () {
  'use strict';
  var links = document.querySelectorAll('a.embed-app');
  if (!links.length || !window.HTMLDialogElement) return;

  var dlg, frame, titleEl, newTab;

  function build() {
    dlg = document.createElement('dialog');
    dlg.className = 'embed-modal';
    var head = document.createElement('div');
    head.className = 'embed-modal-head';
    titleEl = document.createElement('p');
    titleEl.className = 'embed-modal-title';
    newTab = document.createElement('a');
    newTab.className = 'embed-modal-newtab';
    newTab.target = '_blank';
    newTab.rel = 'noopener';
    newTab.textContent = 'Open in new tab ↗';
    var close = document.createElement('button');
    close.type = 'button';
    close.className = 'embed-modal-close';
    close.setAttribute('aria-label', 'Close');
    close.textContent = '×';
    close.addEventListener('click', function () { dlg.close(); });
    head.appendChild(titleEl);
    head.appendChild(newTab);
    head.appendChild(close);
    frame = document.createElement('iframe');
    frame.className = 'embed-modal-frame';
    frame.setAttribute('loading', 'lazy');
    dlg.appendChild(head);
    dlg.appendChild(frame);
    // Clicking the backdrop targets the dialog itself, not its children.
    dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
    // Unload the app whenever the dialog stops being open, so its Three.js
    // render loop stops burning CPU behind a closed dialog.
    //
    // This watches the `open` ATTRIBUTE rather than listening for the 'close'
    // event, because Chrome was observed here NOT firing 'close' at all —
    // dlg.open flipped true to false correctly, but no event was ever
    // dispatched. Attribute state is the thing that is actually reliable, and
    // it also catches every close path for free: the button, the backdrop,
    // our Escape handler, and the browser's own native Escape.
    new MutationObserver(function () {
      if (!dlg.open && frame.hasAttribute('src')) frame.removeAttribute('src');
    }).observe(dlg, { attributes: true, attributeFilter: ['open'] });
    document.body.appendChild(dlg);
  }

  links.forEach(function (a) {
    a.addEventListener('click', function (e) {
      // Let the browser own every gesture that means "somewhere else":
      // Cmd/Ctrl (new tab), Shift (new window), Alt (download), middle-click.
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
      e.preventDefault();
      if (!dlg) build();
      titleEl.textContent = a.getAttribute('data-title') || a.textContent.trim();
      newTab.href = a.href;
      frame.setAttribute('title', titleEl.textContent);
      frame.src = a.href;
      dlg.showModal();
    });
  });

  // Belt-and-braces Escape, for the same reason the note cards have one.
  document.addEventListener('keydown', function (e) {
    if ((e.key === 'Escape' || e.key === 'Esc') && dlg && dlg.open) dlg.close();
  }, true);
})();
