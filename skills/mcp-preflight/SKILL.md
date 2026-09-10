---
name: mcp-preflight
description: "Routing guide for ImageKit's MCP servers (DAM, Admin, DevTools). Use before any ImageKit MCP call. DAM: media library search, upload, organize, share. Admin: origins, external storage, URL endpoints, account usage, usage analytics. DevTools: docs search and transformation URLs."
---

# MCP Preflight

ImageKit has three hosted MCP servers. Call the one that matches the job. Do not write SDK code to operate the user's account.

| Job | Server | Then |
|-----|--------|------|
| Search, upload, organize, tag, share, metadata, collections, path policies, public links, cache purge | DAM (`https://imagekit.io/mcp/dam`) | See skills below when the task is search, upload, sharing, or AI tasks |
| Origins / external storage (S3, GCS, Azure, web server, …) | Admin (`https://imagekit.io/mcp/admin`) | `list_origins`, `create_origin`, `get_origin`, `update_origin`, `delete_origin` |
| URL endpoints | Admin | `list_url_endpoints`, `create_url_endpoint`, `get_url_endpoint`, `update_url_endpoint`, `delete_url_endpoint` |
| Account usage totals or usage analytics | Admin | `get_account_usage`, `get_account_usage_analytics` |
| "How do I…", API/SDK details, whether a feature exists | DevTools `search_docs` | Read the `search-docs` skill first |
| Build a transformation URL | DevTools `transformation_builder` | Read the `transformation-builder` skill first |
| Integrate ImageKit into an app, CMS, or framework | — | Read `imagekit-integrations` to pick the SDK/plugin, then `search_docs` for details |

DAM and Admin each need a separate connection and ImageKit sign-in. DevTools does not. If a tool you need is missing, the user has not connected that server (or has not granted that permission).

## When a skill actually helps

Most DAM and Admin tools are self-explanatory. Read a companion skill only for the cases below — they have calling conventions that the tool schema does not make obvious.

| Task | Skill |
|------|--------|
| Search / filter / list assets | `search-assets` — Lucene `searchQuery`, and you must discover custom metadata fields and tags before guessing |
| Upload a file | `upload-files` — picker vs signed upload; never put file bytes in chat |
| Who can access a file, folder, or collection; grant or revoke access | `asset-access-control` — file/folder ACL tools are not the same as collection ACL tools |
| Create or apply AI tagging / metadata / QC workflows | `ai-tasks` — payload shape, vocabularies, and how they attach to saved extensions |
| Which SDK, plugin, or widget to use for a stack | `imagekit-integrations` — then `search_docs` for implementation details |

## Rules

1. **DAM for the media library. Admin for origins, URL endpoints, usage, and usage analytics.** Do not search DAM for origins or usage, and do not look for file tools on Admin.
2. **Never inline file bytes** (no base64, no paths as file contents). See `upload-files`.
3. **Filter search on the server** with `search_media_library`. See `search-assets`.
4. **Use `transformation_builder`** instead of hand-crafting transformation URLs.
5. **Use `search_docs`** before writing ImageKit integration code. Do not rely on training data for method names or parameters. If you need to pick an SDK or plugin first, read `imagekit-integrations`.
