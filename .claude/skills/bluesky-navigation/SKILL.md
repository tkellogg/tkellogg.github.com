---
name: bluesky-navigation
description: Read-focused navigation of Bluesky for book research — search users and posts, view a user's feed, fetch a specific post and its replies, search within an author's posts. Use whenever you need to look up what someone said on Bluesky, find quotes, gather context on a handle, or understand a thread. Posting section included but requires PDS credentials (not configured in this repo).
version: 1.0.0
---

# Bluesky Navigation

Public-API read access plus a documented write path. No authentication needed for reads.

**Base URL:** `https://public.api.bsky.app`

Bluesky's public AppView serves all read endpoints unauthenticated. URL-encode query strings. Use `jq` to parse responses.

---

## URL ↔ AT URI Conversion

Bluesky has two address forms. App URLs are what humans share; AT URIs are what the API takes.

```
App URL:  https://bsky.app/profile/timkellogg.me/post/3m7v36rwb5k2x
AT URI:   at://timkellogg.me/app.bsky.feed.post/3m7v36rwb5k2x
```

The last path segment of the App URL (`3m7v36rwb5k2x`) is the **rkey**. Handle or DID both work in the URI position.

---

## Search Users

Find profiles by name, handle fragment, or bio keyword.

```bash
curl -s "https://public.api.bsky.app/xrpc/app.bsky.actor.searchActors?q=QUERY&limit=25" \
  | jq '.actors[] | {handle, displayName, description}'
```

Parameters:
- `q` (required): Search query
- `limit`: 1–100 (default 25)
- `cursor`: Pagination

---

## View a User's Profile

Bio, follower counts, post counts:

```bash
curl -s "https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile?actor=HANDLE" \
  | jq '{handle, displayName, description, followersCount, followsCount, postsCount}'
```

`actor` accepts a handle (`timkellogg.me`) or a DID (`did:plc:...`).

---

## View Posts on Someone's Profile (Author Feed)

```bash
curl -s "https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor=HANDLE&limit=30" \
  | jq '.feed[].post | {text: .record.text, createdAt: .record.createdAt, likes: .likeCount, url: ("https://bsky.app/profile/" + .author.handle + "/post/" + (.uri | split("/") | last))}'
```

Parameters:
- `actor` (required): Handle or DID
- `limit`: 1–100 (default 50)
- `cursor`: Pagination
- `filter`: `posts_with_replies` | `posts_no_replies` | `posts_with_media` | `posts_and_author_threads`

Use `posts_no_replies` to see what someone authored top-level (skip the reply chatter). Use `posts_with_media` to find image/video posts.

---

## Search Within an Author's Posts

Bluesky's public API has no per-author search endpoint. Fetch the feed and filter locally:

```bash
curl -s "https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor=HANDLE&limit=100" \
  | jq -r '.feed[].post | "\(.record.createdAt)\t\(.record.text)"' \
  | grep -i "SEARCH_TERM"
```

For older posts, paginate using `cursor` from each response:

```bash
CURSOR=$(curl -s "https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor=HANDLE&limit=100" | jq -r '.cursor')
curl -s "https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor=HANDLE&limit=100&cursor=$CURSOR"
```

---

## Global Post Search

**Requires authentication.** The public AppView returns 403 on `app.bsky.feed.searchPosts` — Bluesky moved it behind auth to mitigate abuse. If you have a session (see Posting section), use:

```bash
curl -s "https://bsky.social/xrpc/app.bsky.feed.searchPosts?q=QUERY&limit=25" \
  -H "Authorization: Bearer $ACCESS_JWT" \
  | jq '.posts[] | {author: .author.handle, text: .record.text, likes: .likeCount, url: ("https://bsky.app/profile/" + .author.handle + "/post/" + (.uri | split("/") | last))}'
```

Parameters:
- `q` (required): Query string. Supports `from:handle`, `since:YYYY-MM-DD`, `until:YYYY-MM-DD`, `lang:en`, quoted phrases
- `sort`: `top` | `latest` (default `latest`)
- `limit`: 1–100 (default 25)

**Unauth fallback for known authors:** pull the author feed (limit 100, paginate via cursor) and grep locally. See "Search Within an Author's Posts" above.

**Unauth fallback for unknown authors:** there isn't a great one. Best workaround is using the bsky.app web UI (`https://bsky.app/search?q=QUERY`) manually, or wiring up auth.

---

## Fetch a Specific Post

Given an App URL `https://bsky.app/profile/HANDLE/post/RKEY`:

```bash
curl -s "https://public.api.bsky.app/xrpc/app.bsky.feed.getPostThread?uri=at://HANDLE/app.bsky.feed.post/RKEY&depth=0" \
  | jq '.thread.post.record.text'
```

`depth=0` returns just the post. Set `depth=6` to pull the reply tree.

---

## Get Replies to a Post

```bash
curl -s "https://public.api.bsky.app/xrpc/app.bsky.feed.getPostThread?uri=at://HANDLE/app.bsky.feed.post/RKEY&depth=6" \
  | jq '.thread.replies[] | {author: .post.author.handle, text: .post.record.text}'
```

Response structure:
- `thread.post` — the requested post
- `thread.replies[]` — direct replies
- `thread.replies[].replies[]` — nested deeper

For full thread context with parent posts:
```bash
curl -s "https://public.api.bsky.app/xrpc/app.bsky.feed.getPostThread?uri=at://HANDLE/app.bsky.feed.post/RKEY&depth=6&parentHeight=10"
```

---

## Get Likes / Reposts / Quote Posts

Who liked a post:
```bash
curl -s "https://public.api.bsky.app/xrpc/app.bsky.feed.getLikes?uri=at://HANDLE/app.bsky.feed.post/RKEY&limit=50" \
  | jq '.likes[] | .actor.handle'
```

Who reposted:
```bash
curl -s "https://public.api.bsky.app/xrpc/app.bsky.feed.getRepostedBy?uri=at://HANDLE/app.bsky.feed.post/RKEY&limit=50" \
  | jq '.repostedBy[] | .handle'
```

Quote posts:
```bash
curl -s "https://public.api.bsky.app/xrpc/app.bsky.feed.getQuotes?uri=at://HANDLE/app.bsky.feed.post/RKEY&limit=50" \
  | jq '.posts[] | {author: .author.handle, text: .record.text}'
```

---

## Follows / Followers

```bash
# Who a user follows
curl -s "https://public.api.bsky.app/xrpc/app.bsky.graph.getFollows?actor=HANDLE&limit=100" \
  | jq '.follows[] | {handle, displayName}'

# Who follows a user
curl -s "https://public.api.bsky.app/xrpc/app.bsky.graph.getFollowers?actor=HANDLE&limit=100" \
  | jq '.followers[] | {handle, displayName}'
```

---

## Response Field Reference

Every post object includes:
- `uri` — AT URI (`at://did/collection/rkey`)
- `cid` — Content ID (immutable hash; needed for likes/reposts/replies if posting)
- `author` — `{ did, handle, displayName, avatar }`
- `record.text` — Post body
- `record.createdAt` — ISO timestamp
- `record.embed` — Images, external links, quoted posts
- `record.reply` — `{ root, parent }` if this is a reply
- `record.facets` — Mentions, links, tags with byte offsets
- `replyCount`, `repostCount`, `likeCount`, `quoteCount`
- `indexedAt` — When the AppView indexed it

---

## Tips

- **URL-encode queries.** Spaces become `%20`, `@` becomes `%40`, `#` becomes `%23`.
- **Pagination:** Every list endpoint returns a `cursor`. Pass it back as `&cursor=...` to get the next page.
- **Rate limits:** Public AppView is generous but not infinite. Throttle to ~1 req/sec for bulk work.
- **DIDs vs handles:** Both work in `actor` and AT URI positions. Handles can change; DIDs are permanent. If you cache results, store DIDs.
- **Search quirks:** `searchPosts` is approximate and recency-biased. For exhaustive search of one author's posts, paginate the author feed and grep locally.

---

## Posting (Requires Auth)

**Not configured in this repo.** This section documents the API for when credentials are wired up.

Bluesky uses AT Protocol. Posting requires a session token from the user's Personal Data Server (PDS — usually `https://bsky.social` for default accounts).

### 1. Create a session

```bash
curl -s -X POST "https://bsky.social/xrpc/com.atproto.server.createSession" \
  -H "Content-Type: application/json" \
  -d '{"identifier": "HANDLE_OR_EMAIL", "password": "APP_PASSWORD"}'
```

Returns `accessJwt`, `refreshJwt`, `did`, `handle`. Use an **app password** (generated in Bluesky settings), never the account password.

### 2. Create a post

```bash
curl -s -X POST "https://bsky.social/xrpc/com.atproto.repo.createRecord" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_JWT" \
  -d '{
    "repo": "DID",
    "collection": "app.bsky.feed.post",
    "record": {
      "$type": "app.bsky.feed.post",
      "text": "Post body here",
      "createdAt": "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'"
    }
  }'
```

### 3. Reply to a post

Add a `reply` field to the record with `root` and `parent` (each an object with `uri` and `cid`):

```json
"reply": {
  "root":   {"uri": "at://...", "cid": "bafyrei..."},
  "parent": {"uri": "at://...", "cid": "bafyrei..."}
}
```

For top-level replies, `root` and `parent` are identical. For threaded replies, `parent` is the post you're directly replying to and `root` is the thread origin.

### 4. Character limit

300 chars per post. Threads = chained replies, each post a separate `createRecord` call referencing the previous via `parent` and the original via `root`.

### 5. Facets (mentions, links, hashtags)

The API does NOT auto-linkify. To make `@handle` clickable or URLs tappable, supply byte-offset `facets`:

```json
"facets": [
  {
    "index": {"byteStart": 0, "byteEnd": 13},
    "features": [{"$type": "app.bsky.richtext.facet#mention", "did": "did:plc:..."}]
  }
]
```

Most users handle this via a client library (`atproto` Python package, `@atproto/api` for JS) rather than building facets by hand.

### Setting up auth in this repo

When ready: create an app password at https://bsky.app/settings/app-passwords, store `BSKY_HANDLE` and `BSKY_APP_PASSWORD` in a `.env` file (gitignored), and source it before posting. The `atproto` Python package (`uv add atproto`) wraps all of the above cleanly.
