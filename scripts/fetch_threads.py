#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "sentence-transformers",
#   "numpy",
# ]
# ///
"""
Fetch Bluesky threads and convert them to Jekyll collection files.

Usage:
    ./scripts/fetch_threads.py [--dry-run] [--limit N]
    uv run scripts/fetch_threads.py [--dry-run] [--limit N]

Criteria for archiving:
    - >20 likes on the first post
    - AND (multiple posts OR contains a link in the text)
"""

import argparse
import json
import os
import re
import urllib.request
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

# Configuration
BLUESKY_HANDLE = "timkellogg.me"
API_BASE = "https://public.api.bsky.app/xrpc"
MIN_LIKES = 20
THREADS_DIR = Path(__file__).parent.parent / "_threads"
EMBEDDING_MODEL = "paraphrase-MiniLM-L3-v2"
NUM_SIMILAR = 3

# Lazy-loaded embedding model
_embedding_model = None


def get_embedding_model():
    """Lazy-load the sentence transformer model."""
    global _embedding_model
    if _embedding_model is None:
        from sentence_transformers import SentenceTransformer
        print(f"Loading embedding model: {EMBEDDING_MODEL}...")
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL)
    return _embedding_model


def get_thread_text(posts: list) -> str:
    """Extract all text from a thread for embedding."""
    texts = []
    for post in posts:
        texts.append(post.get("text", ""))
        # Include embed titles/descriptions
        embed = post.get("embed")
        if embed:
            if embed.get("title"):
                texts.append(embed["title"])
            if embed.get("description"):
                texts.append(embed["description"])
    return " ".join(texts)


def compute_similarities(threads_data: list) -> dict:
    """Compute similar threads for each thread using embeddings.

    Args:
        threads_data: List of dicts with 'slug', 'url', 'title', 'text'

    Returns:
        Dict mapping slug -> list of similar thread URLs
    """
    import numpy as np

    if len(threads_data) < 2:
        return {}

    model = get_embedding_model()

    # Compute embeddings
    texts = [t["text"] for t in threads_data]
    print(f"Computing embeddings for {len(texts)} threads...")
    embeddings = model.encode(texts, normalize_embeddings=True)

    # Compute cosine similarity matrix (embeddings are normalized, so dot product = cosine sim)
    similarity_matrix = np.dot(embeddings, embeddings.T)

    # For each thread, find top N similar (excluding self)
    similar_map = {}
    for i, thread in enumerate(threads_data):
        # Get similarities for this thread
        sims = similarity_matrix[i]
        # Get indices sorted by similarity (descending), exclude self
        sorted_indices = np.argsort(sims)[::-1]
        similar_indices = [j for j in sorted_indices if j != i][:NUM_SIMILAR]

        similar_map[thread["slug"]] = [
            {
                "url": threads_data[j]["url"],
                "title": threads_data[j]["title"],
                "score": float(sims[j]),
            }
            for j in similar_indices
        ]

    return similar_map


def api_get(endpoint: str, params: dict = None) -> dict:
    """Make a GET request to the Bluesky API."""
    url = f"{API_BASE}/{endpoint}"
    if params:
        url += "?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(url)
    req.add_header("Accept", "application/json")

    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())


def resolve_handle(handle: str) -> str:
    """Resolve a handle to a DID."""
    data = api_get("com.atproto.identity.resolveHandle", {"handle": handle})
    return data["did"]


def get_author_feed(did: str, limit: int = None, stop_before: datetime = None) -> list:
    """Get posts from an author's feed.

    Args:
        did: Author's DID
        limit: Max posts to fetch (None = unlimited)
        stop_before: Stop fetching when we see posts older than this date
    """
    all_posts = []
    cursor = None

    while True:
        if limit and len(all_posts) >= limit:
            break

        batch_size = 100
        if limit:
            batch_size = min(100, limit - len(all_posts))

        params = {"actor": did, "limit": batch_size}
        if cursor:
            params["cursor"] = cursor

        data = api_get("app.bsky.feed.getAuthorFeed", params)
        posts = data.get("feed", [])

        if not posts:
            break

        all_posts.extend(posts)

        # Check if we've gone past our date filter
        if stop_before and posts:
            last_post = posts[-1].get("post", {}).get("record", {})
            created = last_post.get("createdAt", "")
            try:
                post_date = datetime.fromisoformat(created.replace("Z", "+00:00"))
                if post_date < stop_before:
                    print(f"  Reached posts from {post_date.date()}, stopping fetch")
                    break
            except (ValueError, TypeError):
                pass

        cursor = data.get("cursor")

        if not cursor:
            break

        if len(all_posts) % 500 == 0:
            print(f"  Fetched {len(all_posts)} posts so far...")

    return all_posts


def get_post_thread(uri: str, depth: int = 10) -> dict:
    """Get a full thread starting from a post."""
    return api_get("app.bsky.feed.getPostThread", {"uri": uri, "depth": depth})


def has_link(text: str) -> bool:
    """Check if text contains a URL."""
    url_pattern = r'https?://[^\s]+'
    return bool(re.search(url_pattern, text))


def extract_self_thread(thread: dict, author_did: str) -> list:
    """Extract posts from a thread where the author replies to themselves."""
    posts = []

    def walk(node: dict):
        if node.get("$type") != "app.bsky.feed.defs#threadViewPost":
            return

        post = node.get("post", {})
        author = post.get("author", {})

        if author.get("did") == author_did:
            record = post.get("record", {})
            embed = post.get("embed", {})

            post_data = {
                "text": record.get("text", ""),
                "created_at": record.get("createdAt", ""),
                "uri": post.get("uri", ""),
                "likes": post.get("likeCount", 0),
                "reposts": post.get("repostCount", 0),
                "images": [],
                "embed": None,
                "facets": record.get("facets", []),
            }

            # Extract images
            if embed.get("$type") == "app.bsky.embed.images#view":
                for img in embed.get("images", []):
                    post_data["images"].append({
                        "url": img.get("fullsize", ""),
                        "thumb": img.get("thumb", ""),
                        "alt": img.get("alt", ""),
                    })

            # Extract external embed (link card)
            if embed.get("$type") == "app.bsky.embed.external#view":
                ext = embed.get("external", {})
                post_data["embed"] = {
                    "uri": ext.get("uri", ""),
                    "title": ext.get("title", ""),
                    "description": ext.get("description", ""),
                    "thumb": ext.get("thumb", ""),
                }

            posts.append(post_data)

            # Walk replies to find self-replies
            for reply in node.get("replies", []):
                reply_author = reply.get("post", {}).get("author", {})
                if reply_author.get("did") == author_did:
                    walk(reply)

    walk(thread.get("thread", {}))
    return posts


def is_thread_root(post_item: dict) -> bool:
    """Check if a post is a thread root (not a reply to someone else)."""
    record = post_item.get("post", {}).get("record", {})
    return "reply" not in record


def qualifies_for_archive(posts: list) -> bool:
    """Check if a thread qualifies for archiving.

    Criteria: >20 likes on first post AND (multiple posts OR has a link in text)
    """
    if not posts:
        return False

    first_post = posts[0]
    likes = first_post.get("likes", 0)

    # Must have >20 likes on first post
    if likes <= MIN_LIKES:
        return False

    # Must also have multiple posts OR a link in text
    is_multi_post = len(posts) > 1
    has_link_in_text = has_link(first_post.get("text", ""))

    return is_multi_post or has_link_in_text


def format_time_elapsed(prev_time: datetime, curr_time: datetime) -> str:
    """Format the time elapsed between posts, only if >1 hour."""
    diff = curr_time - prev_time
    hours = diff.total_seconds() / 3600

    if hours < 1:
        return ""

    if hours < 24:
        h = int(hours)
        return f"{h} hour{'s' if h != 1 else ''} later"

    days = hours / 24
    if days < 7:
        d = int(days)
        return f"{d} day{'s' if d != 1 else ''} later"

    weeks = days / 7
    w = int(weeks)
    return f"{w} week{'s' if w != 1 else ''} later"


def apply_facets(text: str, facets: list) -> str:
    """Apply facets (links, mentions) to text using byte indices."""
    if not facets:
        return text

    # Convert text to bytes for proper indexing
    text_bytes = text.encode("utf-8")

    # Sort facets by start index in reverse order (so we can replace from end to start)
    sorted_facets = sorted(facets, key=lambda f: f.get("index", {}).get("byteStart", 0), reverse=True)

    for facet in sorted_facets:
        index = facet.get("index", {})
        byte_start = index.get("byteStart", 0)
        byte_end = index.get("byteEnd", 0)

        for feature in facet.get("features", []):
            feature_type = feature.get("$type", "")

            if feature_type == "app.bsky.richtext.facet#link":
                uri = feature.get("uri", "")
                # Extract the text that should be linked
                link_text = text_bytes[byte_start:byte_end].decode("utf-8")
                # Create the HTML link
                link_html = f'<a href="{uri}" target="_blank" rel="noopener">{link_text}</a>'
                # Replace in the byte string
                text_bytes = text_bytes[:byte_start] + link_html.encode("utf-8") + text_bytes[byte_end:]

            elif feature_type == "app.bsky.richtext.facet#mention":
                did = feature.get("did", "")
                mention_text = text_bytes[byte_start:byte_end].decode("utf-8")
                # Link to Bluesky profile
                link_html = f'<a href="https://bsky.app/profile/{did}" target="_blank" rel="noopener">{mention_text}</a>'
                text_bytes = text_bytes[:byte_start] + link_html.encode("utf-8") + text_bytes[byte_end:]

    return text_bytes.decode("utf-8")


def generate_thread_html(posts: list) -> str:
    """Generate HTML content for a thread."""
    html_parts = []
    prev_time = None

    for i, post in enumerate(posts):
        # Parse timestamp
        created = post.get("created_at", "")
        try:
            curr_time = datetime.fromisoformat(created.replace("Z", "+00:00"))
        except:
            curr_time = None

        html_parts.append('<div class="thread-post">')

        # Time elapsed (only for posts after the first, and only if >1 hour)
        if i > 0 and prev_time and curr_time:
            elapsed = format_time_elapsed(prev_time, curr_time)
            if elapsed:
                html_parts.append(f'<div class="time-elapsed">{elapsed}</div>')

        # Post text with facets (links, mentions) applied
        text = post.get("text", "")
        facets = post.get("facets", [])
        text_html = apply_facets(text, facets).replace("\n", "<br>")
        html_parts.append(f'<div class="post-text">{text_html}</div>')

        # Images
        images = post.get("images", [])
        if images:
            img_class = "single" if len(images) == 1 else "multiple"
            html_parts.append(f'<div class="post-images {img_class}">')
            for img in images:
                alt = img.get("alt", "").replace('"', '&quot;')
                url = img.get("fullsize", img.get("thumb", ""))
                html_parts.append(f'''<div class="post-image-container">
<img src="{url}" alt="{alt}" class="post-image" loading="lazy">
{f'<div class="image-alt">{alt}</div>' if alt else ''}
</div>''')
            html_parts.append('</div>')

        # External embed (link card)
        embed = post.get("embed")
        if embed and embed.get("uri"):
            domain = urllib.parse.urlparse(embed["uri"]).netloc
            html_parts.append(f'''<a href="{embed["uri"]}" class="post-embed" target="_blank" rel="noopener">
<div class="embed-content">
<div class="embed-domain">{domain}</div>
<div class="embed-title">{embed.get("title", "")}</div>
<div class="embed-description">{embed.get("description", "")}</div>
</div>
</a>''')

        # Per-post stats (likes, reposts)
        likes = post.get("likes", 0)
        reposts = post.get("reposts", 0)
        if likes > 0 or reposts > 0:
            html_parts.append('<div class="post-stats">')
            if likes > 0:
                html_parts.append(f'<span class="stat-item"><svg class="stat-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>{likes}</span>')
            if reposts > 0:
                html_parts.append(f'<span class="stat-item"><svg class="stat-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M7 7h10v3l4-4-4-4v3H5v6h2V7zm10 10H7v-3l-4 4 4 4v-3h12v-6h-2v4z"/></svg>{reposts}</span>')
            html_parts.append('</div>')

        html_parts.append('</div>')

        if curr_time:
            prev_time = curr_time

    return "\n".join(html_parts)


def generate_slug(text: str, date: str) -> str:
    """Generate a URL-safe slug from the post text."""
    # Take first ~50 chars of text
    slug = text[:50].lower()
    # Remove special characters
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    # Replace spaces with hyphens
    slug = re.sub(r'\s+', '-', slug)
    # Remove multiple hyphens
    slug = re.sub(r'-+', '-', slug)
    slug = slug.strip('-')

    # Add date prefix for uniqueness
    date_prefix = date[:10] if date else ""

    if slug:
        return f"{date_prefix}-{slug}"
    return date_prefix


def generate_title(text: str) -> str:
    """Generate a title from the first post text."""
    # Take first line or first ~80 chars
    first_line = text.split("\n")[0]
    if len(first_line) > 80:
        first_line = first_line[:77] + "..."
    return first_line


def write_thread_file(posts: list, root_uri: str, similar: list = None, dry_run: bool = False) -> str:
    """Write a thread to a Jekyll collection file.

    Args:
        posts: List of post data dicts
        root_uri: AT Protocol URI of the root post
        similar: List of similar thread dicts with 'url' and 'title'
        dry_run: If True, don't actually write files
    """
    first_post = posts[0]

    # Generate metadata
    created = first_post.get("created_at", "")
    try:
        date = datetime.fromisoformat(created.replace("Z", "+00:00"))
        date_str = date.strftime("%Y-%m-%d %H:%M:%S %z")
    except:
        date_str = created
        date = datetime.now(timezone.utc)

    title = generate_title(first_post.get("text", "Untitled"))
    slug = generate_slug(first_post.get("text", ""), created)

    # Build Bluesky URL from URI
    # at://did:plc:xxx/app.bsky.feed.post/yyy -> https://bsky.app/profile/did:plc:xxx/post/yyy
    uri_parts = root_uri.replace("at://", "").split("/")
    if len(uri_parts) >= 3:
        bluesky_url = f"https://bsky.app/profile/{uri_parts[0]}/post/{uri_parts[2]}"
    else:
        bluesky_url = ""

    # Generate summary (first ~150 chars)
    summary = first_post.get("text", "")[:150]
    if len(first_post.get("text", "")) > 150:
        summary += "..."
    summary = summary.replace("\n", " ").replace('"', '\\"')

    # Generate HTML content
    content = generate_thread_html(posts)

    # Build similar threads YAML
    similar_yaml = ""
    if similar:
        similar_yaml = "similar:\n"
        for s in similar:
            # Escape title for YAML
            # Escape for YAML double-quoted string: backslashes first, then quotes
            escaped_title = s["title"].replace('\\', '\\\\').replace('"', '\\"')
            similar_yaml += f'  - url: "{s["url"]}"\n'
            similar_yaml += f'    title: "{escaped_title}"\n'

    # Build frontmatter
    frontmatter = f"""---
layout: thread
title: "{title.replace('"', '\\"')}"
date: {date_str}
bluesky_url: {bluesky_url}
likes: {first_post.get("likes", 0)}
reposts: {first_post.get("reposts", 0)}
post_count: {len(posts)}
summary: "{summary}"
{similar_yaml}---
"""

    file_content = frontmatter + content
    filename = f"{slug}.html"
    filepath = THREADS_DIR / filename

    if dry_run:
        print(f"\n[DRY RUN] Would create: {filepath}")
        print(f"  Title: {title}")
        print(f"  Date: {date_str}")
        print(f"  Posts: {len(posts)}")
        print(f"  Likes: {first_post.get('likes', 0)}")
        if similar:
            print(f"  Similar: {[s['title'][:30] + '...' for s in similar]}")
    else:
        THREADS_DIR.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(file_content)
        print(f"Created: {filepath}")

    return filename


def parse_date(date_str: str) -> datetime:
    """Parse a date string in various formats."""
    for fmt in ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y/%m/%d"]:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    raise ValueError(f"Could not parse date: {date_str}")


def load_existing_threads() -> list:
    """Load existing thread files and extract text for embedding."""
    threads = []
    if not THREADS_DIR.exists():
        return threads

    for filepath in THREADS_DIR.glob("*.html"):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Parse frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                html_content = parts[2]

                # Extract title
                title = ""
                for line in frontmatter.split("\n"):
                    if line.startswith("title:"):
                        title = line.split(":", 1)[1].strip()
                        # Remove only the outer YAML quotes (not greedy like strip)
                        if title.startswith('"') and title.endswith('"'):
                            title = title[1:-1]
                        # Unescape YAML double-quoted string escapes
                        title = title.replace('\\"', '"').replace('\\\\', '\\')
                        break

                # Extract text from HTML (strip tags)
                text = re.sub(r'<[^>]+>', ' ', html_content)
                text = re.sub(r'\s+', ' ', text).strip()

                threads.append({
                    "slug": filepath.stem,
                    "url": f"/threads/{filepath.stem}/",
                    "title": title,
                    "text": text,
                    "filepath": filepath,
                })

    return threads


def main():
    parser = argparse.ArgumentParser(description="Fetch Bluesky threads for Jekyll")
    parser.add_argument("--dry-run", action="store_true", help="Don't write files")
    parser.add_argument("--limit", type=int, default=None, help="Max posts to fetch (default: 200, or unlimited with --since)")
    parser.add_argument("--since", type=str, help="Only include posts after this date (YYYY-MM-DD)")
    parser.add_argument("--until", type=str, help="Only include posts before this date (YYYY-MM-DD)")
    parser.add_argument("--recompute-similar", action="store_true", help="Recompute similar threads for all existing threads")
    args = parser.parse_args()

    # Parse date filters
    since_date = parse_date(args.since) if args.since else None
    until_date = parse_date(args.until) if args.until else None

    # If no --since, use default limit of 200 (unless explicitly set)
    limit = args.limit
    if limit is None and not since_date:
        limit = 200

    if since_date:
        print(f"Filtering: posts after {since_date.date()}")
    if until_date:
        print(f"Filtering: posts before {until_date.date()}")

    # Load existing threads for similarity computation
    existing_threads = load_existing_threads()
    existing_slugs = {t["slug"] for t in existing_threads}
    print(f"Found {len(existing_threads)} existing threads")

    # Collect new threads to archive
    new_threads = []

    if not args.recompute_similar:
        print(f"Resolving handle: {BLUESKY_HANDLE}")
        did = resolve_handle(BLUESKY_HANDLE)
        print(f"DID: {did}")

        limit_msg = str(limit) if limit else "unlimited (until --since date)"
        print(f"\nFetching author feed (limit: {limit_msg})...")
        feed = get_author_feed(did, limit=limit, stop_before=since_date)
        print(f"Fetched {len(feed)} posts")

        # Find thread roots (posts that aren't replies)
        roots = [item for item in feed if is_thread_root(item)]
        print(f"Found {len(roots)} potential thread roots")

        for item in roots:
            post = item.get("post", {})
            uri = post.get("uri", "")
            record = post.get("record", {})
            text = record.get("text", "")
            likes = post.get("likeCount", 0)

            # Quick check before fetching full thread
            if likes <= MIN_LIKES and not has_link(text):
                continue

            # Fetch full thread
            thread_data = get_post_thread(uri)
            posts = extract_self_thread(thread_data, did)

            if not qualifies_for_archive(posts):
                continue

            # Generate slug to check for duplicates
            created = posts[0].get("created_at", "")
            slug = generate_slug(posts[0].get("text", ""), created)

            # Apply date filters
            try:
                post_date = datetime.fromisoformat(created.replace("Z", "+00:00"))
                if since_date and post_date < since_date:
                    continue
                if until_date and post_date > until_date:
                    continue
            except (ValueError, TypeError):
                pass  # Skip date filtering if we can't parse the date

            if slug in existing_slugs:
                print(f"Skipping (already exists): {slug}")
                continue

            title = generate_title(posts[0].get("text", "Untitled"))
            thread_text = get_thread_text(posts)

            new_threads.append({
                "slug": slug,
                "url": f"/threads/{slug}/",
                "title": title,
                "text": thread_text,
                "posts": posts,
                "uri": uri,
            })

    # Combine existing and new for similarity computation
    all_threads = existing_threads + new_threads
    print(f"\nTotal threads for similarity: {len(all_threads)}")

    # Compute similarities
    similar_map = {}
    if len(all_threads) >= 2:
        similar_map = compute_similarities(all_threads)

    # Write new threads
    archived = 0
    for thread in new_threads:
        similar = similar_map.get(thread["slug"], [])
        write_thread_file(
            thread["posts"],
            thread["uri"],
            similar=similar,
            dry_run=args.dry_run
        )
        archived += 1

    # Update existing threads if --recompute-similar
    if args.recompute_similar and existing_threads:
        print(f"\nUpdating similar threads in {len(existing_threads)} existing files...")
        for thread in existing_threads:
            similar = similar_map.get(thread["slug"], [])
            if not similar:
                continue

            filepath = thread["filepath"]
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # Parse and update frontmatter
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    frontmatter_lines = parts[1].strip().split("\n")
                    html_content = parts[2]

                    # Remove existing similar block
                    new_frontmatter = []
                    skip_similar = False
                    for line in frontmatter_lines:
                        if line.startswith("similar:"):
                            skip_similar = True
                            continue
                        if skip_similar and line.startswith("  -"):
                            continue
                        if skip_similar and not line.startswith(" "):
                            skip_similar = False
                        if not skip_similar:
                            new_frontmatter.append(line)

                    # Add new similar block
                    similar_yaml = "similar:"
                    for s in similar:
                        # Escape for YAML double-quoted string: backslashes first, then quotes
                        escaped_title = s["title"].replace('\\', '\\\\').replace('"', '\\"')
                        similar_yaml += f'\n  - url: "{s["url"]}"'
                        similar_yaml += f'\n    title: "{escaped_title}"'
                    new_frontmatter.append(similar_yaml)

                    new_content = "---\n" + "\n".join(new_frontmatter) + "\n---" + html_content

                    if not args.dry_run:
                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        print(f"Updated: {filepath.name}")
                    else:
                        print(f"[DRY RUN] Would update: {filepath.name}")

    print(f"\n{'Would archive' if args.dry_run else 'Archived'} {archived} new threads")


if __name__ == "__main__":
    main()
