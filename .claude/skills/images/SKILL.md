---
name: images
description: This skill should be used when the user asks to "generate an image", "create a diagram", "make a chart", "visualize data", "create a cover image", or when a blog post needs visual content like mermaid diagrams, matplotlib/seaborn charts, or AI-generated images via Google Gemini.
version: 1.0.0
---

# Image Generation & Visualization

This skill handles all visual content creation for the blog. Four tools available:

## 1. Mermaid Diagrams

For structural/relational visuals embedded directly in blog posts. See the writing-style skill's `references/mermaid-diagrams.md` for full syntax and philosophy.

Quick reference:
- Use `<div class="mermaid">` wrapper (not backtick fences)
- Add `use_mermaid: true` to front matter
- Keep it simple: 3-8 nodes, one idea per diagram
- Mermaid's complexity limits are a feature — they force clarity

## 2. Matplotlib / Seaborn Charts

For data visualization. Generate Python scripts that produce chart images.

```bash
uv run python3 -c "
import matplotlib.pyplot as plt
import seaborn as sns
# ... generate chart ...
plt.savefig('/Users/tim/code/tkellogg.github.com/images/chart-name.png', dpi=150, bbox_inches='tight')
"
```

Guidelines:
- Save to `/images/` with a descriptive hyphenated name
- Use `dpi=150` for web-appropriate resolution
- Prefer clean, minimal styling — no chartjunk
- Reference in posts as `/images/chart-name.png`

## 3. Pixabay Cover Images (durable CDN link)

For blog cover photos, Tim shares a Pixabay page URL like:

```
https://pixabay.com/photos/ant-aphid-lice-macro-insect-3716248/
```

The post's `image:` front-matter needs the **durable CDN URL** instead:

```
https://cdn.pixabay.com/photo/YYYY/MM/DD/HH/MM/{slug}-{id}_1280.jpg
```

The date/time path is the photo's upload timestamp and **cannot be guessed** — it must be read from the Pixabay page's `og:image` meta tag.

### The problem: Cloudflare blocks plain curl

Pixabay sits behind Cloudflare which TLS-fingerprints the client (JA3/JA4). Plain `curl` — even with a Firefox `User-Agent` — gets a 5KB "Just a moment..." challenge page, never the real HTML. Don't waste time on header permutations.

### Use `curl-cffi` via `uv run`

`curl-cffi` is a Python wrapper that ships real browser TLS fingerprints. No homebrew install needed, just `uv` (already required for everything else):

```bash
PAGE_URL="https://pixabay.com/photos/ant-aphid-lice-macro-insect-3716248/"

uv run --with curl-cffi python3 -c "
from curl_cffi import requests
import re, sys
url = sys.argv[1]
r = requests.get(url, impersonate='firefox133')
m = re.search(r'<meta property=\"og:image\" content=\"([^\"]+)\"', r.text)
print(m.group(1) if m else 'NOT FOUND', file=sys.stderr)
" "$PAGE_URL"
```

The `og:image` will be the `_640.jpg` variant. **Swap `_640` → `_1280`** to match Tim's existing covers (sharper at retina resolutions):

```
og:image:  https://cdn.pixabay.com/photo/2018/10/01/13/31/ant-3716248_640.jpg
use this:  https://cdn.pixabay.com/photo/2018/10/01/13/31/ant-3716248_1280.jpg
```

Verify the 1280 variant exists before using:

```bash
curl -sI "https://cdn.pixabay.com/photo/.../slug-ID_1280.jpg" | head -1
# Want HTTP/2 200
```

### Fallback

If `curl-cffi` ever stops bypassing Cloudflare (impersonation arms race), ask Tim to right-click the photo in his browser → "Copy image address" → paste. That gives the exact CDN URL.

---

## 4. Gemini Image Generation

For AI-generated images when stock photos won't work. Uses `gemini-3-pro-image-preview`.

**Important:** This is a reasoning model. Prompt it with:
- **Less instruction, more values.** Describe what you want the image to *feel* like, not pixel-level details.
- **Data over directives.** Give it context and let it reason about the visual.
- **Wide aspect ratio.** Blog layout needs landscape images — use `"16:9"` or `"3:2"`.

### How to Generate

Load the API key from `.env` and call the REST API:

```bash
source /Users/tim/code/tkellogg.github.com/.env

RESPONSE=$(curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [
        {"text": "YOUR PROMPT HERE"}
      ]
    }],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"],
      "imageConfig": {
        "aspectRatio": "16:9",
        "imageSize": "2K"
      }
    }
  }')

# Extract and save the image
echo "$RESPONSE" | uv run python3 -c "
import sys, json, base64
r = json.load(sys.stdin)
for part in r['candidates'][0]['content']['parts']:
    if 'inlineData' in part:
        data = base64.b64decode(part['inlineData']['data'])
        with open('/Users/tim/code/tkellogg.github.com/images/OUTPUT_NAME.png', 'wb') as f:
            f.write(data)
        print('Saved image')
        break
"
```

### Prompting Philosophy

Since this is a reasoning model, don't over-specify. Good prompt:
> "A wide landscape photograph evoking the feeling of information flowing through interconnected systems. Warm tones. Abstract but grounded in nature."

Bad prompt:
> "Generate a 16:9 image with exactly 5 nodes connected by blue lines on a white background with the title 'Systems Architecture' in 24pt Arial at the top."

### When to Use Gemini vs Stock Photos

- **Prefer stock photos** (Pixabay etc.) for most cover images. They look natural and Tim has rights.
- **Use Gemini** when the concept is too specific/abstract for stock, or when generating diagrams that mermaid can't handle.
- **Never use Gemini without telling Tim.** Always flag that an image was AI-generated.

### Available Aspect Ratios

Wide (preferred for blog): `"16:9"`, `"3:2"`, `"4:3"`, `"21:9"`
Square: `"1:1"`
Tall (rarely needed): `"9:16"`, `"2:3"`

### Available Sizes

`"1K"` (default), `"2K"`, `"4K"`
