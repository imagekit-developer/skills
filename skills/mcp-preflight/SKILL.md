---
name: mcp-preflight
description: "Routing guide for ImageKit's two MCP servers (imagekit_api and imagekit_devtools) — maps each capability to the correct server and tool, and covers the routing rules (e.g. never upload local files via execute). Use before calling any ImageKit MCP tool. Covers file management, folder ops, cache purge, metadata, docs search, transformation building, and upload routing."
---

# MCP Preflight

## Read This Before Any ImageKit MCP Call

You have access to two ImageKit MCP servers. Each serves a different purpose. Calling the wrong server or the wrong tool wastes tokens and produces errors. This skill is your routing table.

## Server Map

### `imagekit_api` — Authenticated API Server

Prefix: `mcp_imagekit_api_*`

Two tools only:

| Tool | Purpose |
|------|----------|
| `search_doc` | Local search that only searches TypeScript SDK code — use to find method signatures and types |
| `execute` | Executes TypeScript code against the ImageKit SDK to perform CRUD operations |

All CRUD operations are performed by writing TypeScript code that runs via `execute`:

- List, search, get details of files
- Delete, move, copy, rename files
- Create, delete, move, copy folders
- Bulk tag/untag operations
- File versions (list, restore, delete)
- Custom metadata fields (CRUD)
- Cache invalidation (purge)
- URL endpoints and origins management
- Account usage stats

### `imagekit_devtools` — Public Tools Server

Prefix: `mcp_imagekit_devtools_*`

Two tools only — no auth required:

| Tool | Purpose |
|------|---------|
| `search_docs` | RAG-powered search across ImageKit docs, guides, API refs, SDKs, community posts |
| `transformation_builder` | Builds transformation URLs from natural language descriptions |

## Routing Table

| Need | Route To |
|------|----------|
| List, delete, move, copy files | `mcp_imagekit_api_execute` (write TS code) |
| Folder operations | `mcp_imagekit_api_execute` (write TS code) |
| File metadata, tags, custom fields | `mcp_imagekit_api_execute` (write TS code) |
| Bulk operations | `mcp_imagekit_api_execute` (write TS code) |
| Cache purge | `mcp_imagekit_api_execute` (write TS code) |
| URL endpoints, origins | `mcp_imagekit_api_execute` (write TS code) |
| Find SDK method signatures/types | `mcp_imagekit_api_search_doc` |
| **Upload files** | Use `mcp_imagekit_api_execute` with `client.files.upload()` — **only URL-based uploads work; local files cannot be passed**. Read the `upload-files` skill first. |
| How to do something in ImageKit | `mcp_imagekit_devtools_search_docs` |
| Build a transformation URL | `mcp_imagekit_devtools_transformation_builder` |
| Find SDK usage or API parameters | `mcp_imagekit_devtools_search_docs` |
| Verify feature exists or find limits | `mcp_imagekit_devtools_search_docs` |
| Search / filter / list assets | `mcp_imagekit_api_execute` (write TS code) — read `search-assets` skill first |
| Integrate ImageKit into a framework/SDK/CMS | read `imagekit-integrations` skill first |

## Searching / Filtering Assets

When listing assets with `client.assets.list`, **filter on the server** instead of fetching everything and filtering in code. **Read the `search-assets` skill first** — it is the canonical reference for the Lucene-like `searchQuery` syntax, when to use top-level params vs a `searchQuery`, and how to narrow the returned `File`/`Folder` results.

## Integration Use Cases

When the task is to integrate ImageKit into a specific technology (front-end, back-end, mobile, CMS, external storage, upload widgets, URL generation, etc.), **read the `imagekit-integrations` skill** to find the right SDK/plugin and what it covers before writing code.

## Before Calling imagekit_api

**Use the `imagekit-sdk-reference` skill** before constructing any TypeScript code that calls `mcp_imagekit_api_*` tools. That skill provides complete SDK method signatures, parameters, return types, error handling patterns, and examples to ensure correct API calls and proper data handling.

## Critical Rules

1. **Uploads are URL-only** — `client.files.upload()` via `mcp_imagekit_api_execute` only accepts a public URL string. **Local files cannot be uploaded** (no file bytes, streams, or Buffers). Read the `upload-files` skill first.
2. **ALWAYS call `search_docs` before writing any ImageKit SDK code** — do not rely on training data for method signatures or parameters.
3. **Do NOT read library source code to figure out usage** — `search_docs` returns official docs and working examples. Only read source code as a last resort when docs fail.
4. **Use `transformation_builder` instead of hand-crafting transformation URLs** — it knows correct parameter syntax and ordering.
5. **Filter `client.assets.list` server-side, not in code** — read the `search-assets` skill for how to choose between top-level params and a `searchQuery`.
