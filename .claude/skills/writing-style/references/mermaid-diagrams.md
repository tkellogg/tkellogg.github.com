# Mermaid Diagrams

## When to Use

Mermaid diagrams are a visual tool, like the bold text anchors but for relationships and flows. Use them when a concept has structure that's easier to see than read — data flows, feedback loops, architecture layers, decision trees.

## Syntax

Use HTML `<div>` tags, **not** markdown backtick fences:

```html
<div class="mermaid">
graph TD
  A-->B-->C
</div>
```

## Front Matter

Posts with mermaid diagrams **must** include in front matter:

```yaml
use_mermaid: true
```

This triggers conditional loading of the mermaid JS library in the post layout.

## Diagram Types Used

- `graph TD` — top-down (most common for hierarchies, architectures)
- `graph LR` — left-right (good for flows, pipelines, sequences)
- `flowchart TD` / `flowchart LR` — same but with flowchart syntax (supports more features)

## Complexity Philosophy

**Mermaid's limitations are an asset.** It forces simplicity. If a diagram is getting complex in mermaid, the concept probably needs to be broken into multiple diagrams or simplified.

Keep diagrams:
- **3-8 nodes** typically. Rarely more than 10.
- **One main idea per diagram.** Don't cram an entire architecture into one.
- **Labels short.** 1-3 words per node. Use HTML `<br/>` for line breaks if needed.

## Common Patterns

### Simple cycle:
```html
<div class="mermaid">
graph LR
  Problem((Problem))-->Solution((Solution))-->Growth((Growth))-->Problem
</div>
```

### Flow with subgraphs:
```html
<div class="mermaid">
flowchart LR
  subgraph agent
    LLM
    mem
  end
  information --> LLM -->|store| mem[(state)] -->|recall| LLM
  LLM -->|filtered <br/>through state| response
</div>
```

### Simple hierarchy:
```html
<div class="mermaid">
graph TD
  sys[system prompt]
  user[user data]
  sys-->model
  user-->model-->output
</div>
```

### Architecture with styling:
```html
<div class="mermaid">
flowchart TD
    subgraph CORE["Core (Always Loaded)"]
        persona["persona"]
        values["bot_values"]
    end
    subgraph FILES["Files (On Demand)"]
        insight_files["state/insights/*.md"]
    end
    style CORE fill:#e8f5e9,stroke:#4caf50
    style FILES fill:#fff3e0,stroke:#ff9800
</div>
```

## Node Shape Reference

- `A` or `A[text]` — rectangle
- `A([text])` — rounded rectangle (stadium)
- `A((text))` — circle
- `A[(text)]` — cylinder (database)
- `A{text}` or `A{???}` — diamond (decision)

## Edge Labels

```
A-->|label text|B
A-->|"label with <br/> linebreak"|B
```
