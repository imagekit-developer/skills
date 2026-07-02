---
name: search-docs
description: "Guidance for searching ImageKit documentation with the search_docs tool — how to craft effective queries, select the right sources, and handle results. Use before calling search_docs to look up ImageKit features, APIs, configuration, pricing, or SDK examples."
---

# Documentation Search Skill

Prepare your query and source selection using the guidelines below, then call `search_docs` and present the results following the rules here.

## When to use
- User asks about ImageKit features, capabilities, or services
- Transformation builder fails and you need parameter/limit info
- User asks about APIs, configuration, pricing, or DAM features
- Need to verify if ImageKit supports a specific feature
- Need to find SDK usage examples or API reference details

## Tool Parameters

**Required**: `query` - Clear, specific question about ImageKit (see Query Crafting below)

**Optional**: `sources` array (default: `["imagekit_guides", "imagekit_community"]`)
- `imagekit_guides`: Official guides and tutorials
- `imagekit_community`: User-generated content, practical solutions. Great for troubleshooting and real-world use cases.
- `imagekit_api_references`: Technical API details
- `imagekit_sdk`: SDK implementation examples

## Query Crafting

**Rule: Always rewrite vague user questions into specific, searchable queries before calling the tool.**

| User Says | Bad Query (don't pass this) | Good Query |
|---|---|---|
| "Tell me about ImageKit" | "tell me about ImageKit" | "ImageKit features overview image optimization CDN" |
| "How do I upload?" | "upload" | "How to upload files using ImageKit upload API" |
| "Pricing info" | "pricing" | "ImageKit pricing plans and extension unit costs" |
| "Can it do background removal?" | "background removal" | "How to apply background removal using ImageKit AI transformation" |

## Source Selection

| Use Case | Sources |
|----------|---------|
| General features | `["imagekit_guides", "imagekit_community"]` |
| API details | `["imagekit_guides", "imagekit_api_references"]` |
| SDK examples | `["imagekit_sdk", "imagekit_guides", "imagekit_community"]` |
| Troubleshooting | `["imagekit_community", "imagekit_guides"]` |

## Imagekit Community 
- Valuable for real-world solutions, troubleshooting, and user experiences
- May contain practical tips not found in official guides
- Always include community sources. They often provide insights and solutions that official documentation may not cover, especially for troubleshooting and real-world use cases.

## Handling Results

Always cite sources:
```
References:
1. [Title]: [URL]
```

If results don't answer the question, acknowledge the limitation and suggest contacting ImageKit support.

## Gotchas

- Specific queries yield better results ("How to apply background removal using API" not "tell me about ImageKit")
- Multiple searches may be needed; refine query if first search is insufficient
- Community sources provide real-world solutions; official guides are authoritative
