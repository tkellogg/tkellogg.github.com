# Cover Image Selection

## Requirements

- **Wide, not tall.** Landscape orientation. Blog layout needs horizontal images.
- **Abstract fit.** The image should evoke the overall point of the blog, not literally depict it. A post about AI agents might use a photo of ants, not a robot.
- **Free with rights.** Only use stock photo sites where Tim has the right to use the image. No attribution-required images unless attribution is trivial.
- **No AI-generated images.** Historically these haven't worked well. Use real photography or illustration from stock sites.

## Sources (in order of preference)

1. **Pixabay** — historically the best source. Free for commercial use, no attribution required.
2. Any other free stock photo site with similar licensing (Unsplash, Pexels, etc.)

## How to Get Pixabay Images

Tim has a Chrome extension at `scripts/pixabay-ext/` that extracts CDN URLs from Pixabay photo pages. The workflow is:

1. Browse Pixabay for a fitting image
2. The extension extracts the `og:image` meta tag URL (the CDN link)
3. Use that CDN URL directly in the front matter `image:` field

**Since Claude can't browse Pixabay** (they block automated access), the workflow for blog drafts is:

- Suggest 2-3 search terms Tim could use on Pixabay
- Describe what kind of image would work (abstract association, not literal)
- Leave the `image:` field as a placeholder for Tim to fill in

## Front Matter Format

```yaml
image: https://cdn.pixabay.com/photo/YYYY/MM/DD/HH/MM/description-NNNNNNN_1280.jpg
```

Or for local images:
```yaml
image: /images/filename.webp
```

## Image Naming (local)

When downloading locally: descriptive, hyphenated names. Example: `satellite-gravity.png`, `strix-architecture.webp`. WebP preferred for newer images.
