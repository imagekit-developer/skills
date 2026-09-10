---
name: mcp-preflight
description: "Routing guide for ImageKit's MCP servers (imagekit_dam, imagekit_admin, and imagekit_devtools) — maps each capability to the correct server and tool. Use before calling any ImageKit MCP tool. Covers media library ops, access control, origins, URL endpoints, usage, docs search, transformation building, and upload routing."
---

# MCP Preflight

## Read This Before Any ImageKit MCP Call

You have access to three ImageKit MCP servers. Each serves a different purpose. Calling the wrong server or the wrong tool wastes tokens and produces errors. This skill is your routing table.

DAM and Admin require the user to sign in to ImageKit. Their tokens are isolated: a DAM token cannot call Admin tools, and vice versa. DevTools needs no authentication.

## Server Map

### `imagekit_dam` — Authenticated DAM server

Prefix: `mcp_imagekit_dam_*` (exact prefix may vary by client)

URL: `https://imagekit.io/mcp/dam`

Manages the user's media library with the same access as their ImageKit user account (OAuth scopes intersected with their role and folder ACLs). Do not write TypeScript SDK code to perform these operations — call the DAM tools directly.

Representative tools (not exhaustive — prefer the tool whose title matches the task):

| Area | Tools |
|------|-------|
| Search / browse | `search_media_library`, `get_file_details`, `list_client_tags`, `list_custom_metadata_fields` |
| Upload | `upload_file` (interactive picker), `create_upload_signature` (signed URL/CLI upload) |
| Download | `download_file`, `create_archive`, `list_downloads` |
| Files | `update_file_details`, `copy_file`, `move_file`, `rename_file`, `delete_files_batch`, `add_tags_bulk`, `remove_tags_bulk`, `publish_files_bulk` |
| Folders | `create_folder`, `delete_folder`, `copy_folder`, `move_folder`, `rename_folder` |
| Versions | `list_file_versions`, `get_file_version_details`, `restore_file_version`, `delete_file_version` |
| Metadata schema | `create_custom_metadata_field`, `update_custom_metadata_field`, `delete_custom_metadata_field`, `update_metadata_bulk` |
| Path policies | `list_path_policies`, `create_path_policy`, `get_path_policy`, `update_path_policy`, `delete_path_policy` |
| Media collections | `list_media_collections`, `create_media_collection`, `add_assets_to_media_collection`, `remove_assets_from_media_collection` |
| Access control | `build_access_list`, `update_asset_acl`, `get_collection_access_list`, `list_associated_media_collections` — read the `asset-access-control` skill first |
| Public links | `list_all_public_links`, `create_public_link_for_asset`, `update_public_link_details`, `delete_specific_public_link_for_asset` |
| Extensions / AI | `list_saved_extensions`, `create_saved_extension`, `apply_extension_bulk` |
| Cache | `purge_cache`, `get_purge_status` |

In clients that support MCP Apps, `search_media_library`, `upload_file`, and `get_file_details` can open an interactive UI.

### `imagekit_admin` — Authenticated Admin server

Prefix: `mcp_imagekit_admin_*`

URL: `https://imagekit.io/mcp/admin`

Account-level delivery settings and usage. No media-library tools.

| Tool | Purpose |
|------|---------|
| `list_origins` / `create_origin` / `get_origin` / `update_origin` / `delete_origin` | External storage (origins) |
| `list_url_endpoints` / `create_url_endpoint` / `get_url_endpoint` / `update_url_endpoint` / `delete_url_endpoint` | URL endpoints |
| `get_account_usage` | Usage totals |
| `get_account_usage_analytics` | Usage analytics |

### `imagekit_devtools` — Public tools server

Prefix: `mcp_imagekit_devtools_*`

URL: `https://devtools-mcp.imagekit.io/mcp`

Two tools only — no auth required:

| Tool | Purpose |
|------|---------|
| `search_docs` | RAG-powered search across ImageKit docs, guides, API refs, SDKs, community posts |
| `transformation_builder` | Builds transformation URLs from natural language descriptions |

## Routing Table

| Need | Route To |
|------|----------|
| Search / filter / list assets | `search_media_library` on DAM — read the `search-assets` skill first |
| Upload files | DAM `upload_file` or `create_upload_signature` — read the `upload-files` skill first |
| Download files or ZIP archives | DAM `download_file` / `create_archive` |
| File or folder CRUD, tags, metadata, versions | matching DAM tool |
| Share / revoke access on files, folders, collections | DAM ACL tools — read the `asset-access-control` skill first |
| Path policies, public links, saved extensions, media collections | matching DAM tool |
| Cache purge | DAM `purge_cache` |
| Origins (external storage) | Admin origin tools |
| URL endpoints | Admin URL-endpoint tools |
| Account usage / analytics | Admin `get_account_usage` / `get_account_usage_analytics` |
| How to do something in ImageKit | `search_docs` on DevTools |
| Build a transformation URL | `transformation_builder` on DevTools |
| Find SDK usage or API parameters | `search_docs` on DevTools |
| Write application code with `@imagekit/nodejs` | read the `imagekit-sdk-reference` skill — do **not** use DAM/Admin tools to generate app code |
| Integrate ImageKit into a framework/SDK/CMS | read the `imagekit-integrations` skill first |

## Searching / Filtering Assets

When listing assets, **filter on the server** with `search_media_library` instead of fetching everything and filtering in code. **Read the `search-assets` skill first** — it is the canonical reference for the Lucene-like `searchQuery` syntax. Discover custom metadata fields (`list_custom_metadata_fields`) and tags (`list_client_tags`) before guessing field names.

## Integration Use Cases

When the task is to integrate ImageKit into a specific technology (front-end, back-end, mobile, CMS, external storage, upload widgets, URL generation, etc.), **read the `imagekit-integrations` skill** to find the right SDK/plugin and what it covers before writing code. Use DAM/Admin MCP only when the user wants you to **act on their live account**, not when they want integration code.

## Critical Rules

1. **Call the DAM/Admin tool that matches the task.** Do not write TypeScript against `@imagekit/nodejs` and expect an MCP `execute` tool — that server no longer exists.
2. **Never put file bytes in the conversation.** For local uploads, call `upload_file` (MCP App) or `create_upload_signature` and POST from the user's environment. Read the `upload-files` skill first.
3. **ALWAYS call `search_docs` before writing ImageKit SDK or integration code** — do not rely on training data for method signatures or parameters.
4. **Do NOT read library source code to figure out usage** — `search_docs` returns official docs and working examples. Only read source code as a last resort when docs fail.
5. **Use `transformation_builder` instead of hand-crafting transformation URLs** — it knows correct parameter syntax and ordering.
6. **Filter `search_media_library` server-side, not in code** — read the `search-assets` skill.
7. **DAM and Admin tokens cannot call each other's tools.** If a tool is missing, the user needs to connect that server and grant the matching scope.
