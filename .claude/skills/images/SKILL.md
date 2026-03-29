---
name: images
description: This skill should be used when the user asks to "generate an image", "create a diagram", "make a chart", "visualize data", "create a cover image", or when a blog post needs visual content like mermaid diagrams, matplotlib/seaborn charts, or AI-generated images via Google Gemini.
version: 1.0.0
---

# Image Generation & Visualization

This skill handles all visual content creation for the blog. Three tools available:

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

## 3. Gemini Image Generation

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
