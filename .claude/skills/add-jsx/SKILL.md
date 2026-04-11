---
name: add-jsx
description: Use when the user wants to add a React/JSX component to the Jekyll site as a page. Triggers on "add jsx", "put this jsx on the site", "render this react component", or when given a .jsx file to integrate.
version: 1.0.0
---

# Adding React JSX Components to the Jekyll Site

This site is a static Jekyll blog with no Node.js build pipeline. React components run 100% client-side using CDN scripts and Babel standalone for in-browser JSX transformation.

## Quick Start Script

Run the wrapper script to scaffold a new page from a JSX file:

```bash
.claude/skills/add-jsx/scripts/wrap-jsx.sh ~/Downloads/my-component.jsx my-page-slug
```

This handles the mechanical conversion (stripping imports/exports, adding CDN scripts, wrapping in `{% raw %}`). You still need to review and adjust the output — see the checklist below.

## How It Works

Three CDN scripts, no build step:

| Script | Size (gzip) | Purpose |
|--------|------------|---------|
| `react@18` UMD | ~6KB | React core |
| `react-dom@18` UMD | ~40KB | DOM rendering |
| `@babel/standalone` | ~300KB | Client-side JSX → JS transformation |

The JSX lives in a `<script type="text/babel">` tag. Babel compiles it in the browser on first load. Everything is cached by the CDN after that.

## Conversion Checklist

After running the script (or doing it manually), verify these:

### 1. React Imports → Globals

```diff
- import { useState, useEffect } from "react";
+ const { useState, useEffect } = React;
```

The script adds a broad destructure at the top: `const { useState, useEffect, useRef, useMemo, useCallback, useReducer } = React;` — unused ones are harmless.

### 2. Export → Mount Call

```diff
- export default function MyComponent() {
+ function MyComponent() {
```

Add at the bottom:
```jsx
ReactDOM.createRoot(document.getElementById('react-root')).render(<MyComponent />);
```

### 3. Liquid Escaping

Jekyll's Liquid engine interprets `{{` as template variables. The entire `<script type="text/babel">` block **must** be wrapped:

```
{% raw %}
<script type="text/babel">
...
</script>
{% endraw %}
```

This is the #1 gotcha. If the Jekyll build fails with a "Liquid syntax error" about `Variable ... was not properly terminated`, you forgot this.

### 4. CSS Scoping

If the component has a global CSS reset like `* { box-sizing: border-box; margin: 0; padding: 0; }`, scope it to the mount container:

```css
#react-root, #react-root * { box-sizing: border-box; margin: 0; padding: 0; }
```

Otherwise it breaks the site header and footer.

### 5. Fixed Header Offset

The site has a fixed header at 60px height, z-index 1000. If the component uses `position: sticky`:

```diff
- top: 0,
- zIndex: 100,
+ top: "60px",
+ zIndex: 999,
```

### 6. Full-Bleed Dark Components

The site body has `max-width: 1200px` and `background: #f5f5f5`. For dark full-bleed components, add these overrides in a `<style>` tag before the mount div:

```html
<style>
  body { background-color: #0a0a0a !important; }
  .site-content { padding-left: 0 !important; padding-right: 0 !important; padding-bottom: 0 !important; max-width: none !important; }
  .site-content main { padding-top: 0 !important; }
  .site-footer { background: #111 !important; border-top: 1px solid #222; }
  .site-footer p, .site-footer p a { color: #555 !important; }
  .footer-social a { color: #444 !important; }
</style>
```

If the component has a light background or shouldn't be full-bleed, skip most of these.

### 7. Third-Party React Libraries

If the JSX imports other npm packages (e.g., `framer-motion`, `recharts`), find their UMD/CDN builds:

```html
<script src="https://unpkg.com/framer-motion@11/dist/framer-motion.js" crossorigin></script>
```

Check the package's docs for CDN availability. Not all packages have UMD builds — if one doesn't, you may need to inline or rewrite that dependency.

## File Placement

- Standalone interactive pages: site root (e.g., `/hormuz-factcheck.html` → `/hormuz-factcheck`)
- Sub-pages or experiments: `/lab/<slug>/index.html`
- If it's a blog post with embedded React: use `layout: post` instead of `layout: default`

## Verify

Always rebuild after adding:
```bash
bundle exec jekyll build
```

Check for Liquid errors. Then `bundle exec jekyll serve` to preview.

## Reference Implementation

See `/hormuz-factcheck.html` for a working example of a full-page React component integrated into the Jekyll site.
