#!/bin/bash
# Converts a standalone React JSX file into a Jekyll-compatible HTML page.
#
# Usage: wrap-jsx.sh <input.jsx> <output-slug>
# Example: wrap-jsx.sh ~/Downloads/my-component.jsx my-cool-page
#
# Produces: /Users/tim/code/tkellogg.github.com/<output-slug>.html
#
# What it does:
# 1. Strips `import ... from "react"` and `export default`
# 2. Detects the default-exported component name
# 3. Wraps everything in a Jekyll page with React/ReactDOM/Babel CDN
# 4. Adds {% raw %} / {% endraw %} so Liquid ignores {{ }}
# 5. Adds ReactDOM.createRoot(...).render(<Component />) mount call

set -euo pipefail

SITE_ROOT="/Users/tim/code/tkellogg.github.com"

if [ $# -lt 2 ]; then
  echo "Usage: $0 <input.jsx> <output-slug>"
  echo "Example: $0 ~/Downloads/hormuz-factcheck.jsx hormuz-factcheck"
  exit 1
fi

INPUT="$1"
SLUG="$2"
OUTPUT="${SITE_ROOT}/${SLUG}.html"

if [ ! -f "$INPUT" ]; then
  echo "Error: $INPUT not found"
  exit 1
fi

# Detect the default-exported component name
COMPONENT=$(grep -E 'export default function\s+(\w+)' "$INPUT" | sed -E 's/.*export default function\s+(\w+).*/\1/' | head -1)
if [ -z "$COMPONENT" ]; then
  # Try: export default ComponentName  (separate line)
  COMPONENT=$(grep -E '^export default \w+' "$INPUT" | sed -E 's/export default (\w+).*/\1/' | head -1)
fi
if [ -z "$COMPONENT" ]; then
  echo "Error: Could not detect default-exported component name."
  echo "Expected 'export default function MyComponent' or 'export default MyComponent'"
  exit 1
fi

echo "Detected component: $COMPONENT"
echo "Output: $OUTPUT"

# Transform the JSX:
# - Remove import lines from "react"
# - Remove "export default " prefix from function declaration
# - Remove standalone "export default ComponentName" lines
TRANSFORMED=$(cat "$INPUT" \
  | sed -E '/^import .* from ["\x27]react["\x27];?$/d' \
  | sed -E 's/^export default function /function /' \
  | sed -E '/^export default \w+;?$/d'
)

cat > "$OUTPUT" << 'FRONTMATTER'
---
layout: default
title: "TITLE"
summary: "SUMMARY"
---

<style>
  /* Full-bleed overrides for dark/custom components */
  body { background-color: #0a0a0a !important; }
  .site-content { padding-left: 0 !important; padding-right: 0 !important; padding-bottom: 0 !important; max-width: none !important; }
  .site-content main { padding-top: 0 !important; }
  .site-footer { background: #111 !important; border-top: 1px solid #222; }
  .site-footer p, .site-footer p a { color: #555 !important; }
  .footer-social a { color: #444 !important; }
</style>

<div id="react-root"></div>

<script src="https://unpkg.com/react@18/umd/react.production.min.js" crossorigin></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js" crossorigin></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>

{% raw %}
<script type="text/babel">
const { useState, useEffect, useRef, useMemo, useCallback, useReducer } = React;

FRONTMATTER

# Append the transformed JSX
echo "$TRANSFORMED" >> "$OUTPUT"

# Append the mount call and closing tags
cat >> "$OUTPUT" << MOUNT

ReactDOM.createRoot(document.getElementById('react-root')).render(<${COMPONENT} />);
</script>
{% endraw %}
MOUNT

echo "Done! Created $OUTPUT"
echo ""
echo "Next steps:"
echo "  1. Edit the title/summary in the front matter"
echo "  2. Adjust the <style> overrides if the component isn't dark/full-bleed"
echo "  3. If the component uses sticky positioning, set top: 60px (fixed header height)"
echo "  4. Run: bundle exec jekyll build"
