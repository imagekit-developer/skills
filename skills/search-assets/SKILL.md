---
name: search-assets
description: "Lucene searchQuery cheatsheet for DAM search_media_library. Use when the user describes assets in everyday language (brand, campaign, region, status, colour, rating, SKU) or when building or debugging a search, filter, or list of ImageKit files and folders."
---

# `search_media_library` `searchQuery`

Call `search_media_library` on DAM with a tight filter. Do not fetch a broad page and filter in code.

## Discover fields before you guess

Accounts define arbitrary custom-metadata fields. The user will type normal words ("Nike", "summer campaign", "EMEA", "approved") that may be a **field name**, a **select option**, a **tag**, or only a **filename**. Never invent `"customMetadata.<name>"`.

For every descriptive word you might put on `name` or `tags`:

1. Call `list_custom_metadata_fields` once. Match the word against each field's `name`, `label`, and `schema.selectOptions` (case-insensitive). Use the field's `name` (not `label`) as `"customMetadata.<name>"`.
2. Call `list_client_tags` with that word as `label`. If tags come back, filter with `tags IN [...]` using the returned tag `name`s verbatim.
3. Only if neither call matches may you fall back to `name HAS "…"`. Literal filenames, extensions, and explicitly "named/called/titled X" go on `name` without this check.

A no-match is cheap: omit that custom-metadata clause rather than guessing a field. Skip filler words ("files", "show me", "assets").

Select types: `SingleSelect` → `=` / `IN`; `MultiSelect` → `IN` / `NOT IN`. Prefer a returned `selectOptions` value over the user's raw spelling. Text → `=` `:` `HAS`; Number/Date → `<` `<=` `>` `>=`; Boolean → `=` with unquoted `true`/`false`.

## Inputs

| Input | Use for |
|-------|---------|
| `searchQuery` | Lucene filter (below). |
| `path` | Folder scope, e.g. `/products`. |
| `type` | `file` / `file-version` / `folder` / `all`. Honored only when `searchQuery` is omitted. |
| `fileType` | `image` / `non-image` / `all`. |
| `sort` | e.g. `DESC_CREATED`. Pair `HAS` with `DESC_RELEVANCE`. |
| `limit` / `skip` | Page size (max 1000) and offset. Default page is 20. |

Put a simple folder scope in `path` and file vs non-image in `fileType`. Whenever `searchQuery` is set, put type in `searchQuery` (`type = "folder"`, or `(name HAS "logo") AND type = "folder"`). The `type` argument is ignored in that case and results default to files.

## Syntax

- **Operators:** `=` `:` `<` `<=` `>` `>=` `IN` `NOT IN` `NOT =` `HAS` `EXISTS` `NOT EXISTS`
- **Combine:** `AND`, `OR`. **Group:** `( ... )`
- **Quoting:** string values in `"double quotes"`; numbers and booleans (`true`/`false`) unquoted; `customMetadata` / `embeddedMetadata` field names must be quoted, e.g. `"customMetadata.brand"`.
- `:` = begins-with / within-subfolders. `=` = exact. `HAS` = case-insensitive full-text (tokenized).

## Fields

| Field | Operators | Value notes |
|-------|-----------|-------------|
| `name` | `=` `:` `IN` `NOT =` `NOT IN` `HAS` | `=` exact (case-sensitive), `:` begins-with, `HAS` case-insensitive full-text |
| `tags` | `IN` `NOT IN` `HAS` `EXISTS` `NOT EXISTS` | Matches both `tags` and `AITags` |
| `type` | `=` `IN` `NOT =` `NOT IN` | `"file"` \| `"file-version"` \| `"folder"` |
| `id` | `=` `IN` `NOT =` `NOT IN` | fileId or folderId |
| `createdAt` / `updatedAt` | `=` `<` `<=` `>` `>=` `IN` `NOT =` `NOT IN` | ISO 8601 or relative (`"1h"` `"2d"` `"3w"` `"4m"` `"1y"`) |
| `width` / `height` | `=` `<` `<=` `>` `>=` `IN` `NOT =` `NOT IN` | Pixels; images only |
| `size` | `=` `<` `<=` `>` `>=` `IN` `NOT =` `NOT IN` | Bytes (`1024`) or `"1mb"` / `"10kb"` |
| `format` | `=` `IN` | `"jpg"` `"png"` `"webp"` `"gif"` `"svg"` `"avif"` `"pdf"` `"mp4"` … |
| `private` / `published` / `transparency` | `=` | Boolean, unquoted |
| `createdBy` | `=` `IN` `NOT =` `NOT IN` | Uploader email |
| `path` | `=` `:` `IN` `NOT =` `NOT IN` | `=` exact folder; `:` folder + subfolders |
| `"customMetadata.<field>"` | type-dependent | Quote the field name. Discover via `list_custom_metadata_fields`. |
| `"embeddedMetadata.<field>"` | type-dependent | From the file, not the DAM schema. `Keywords` uses `IN`/`EXISTS`; `DateTimeOriginal` uses date ops; `LocationTaken` supports geo (`"40,100 5km"`) |

## Examples

```text
name HAS "red dress"
name = "red-dress.jpg"
name : "red-dress"
createdAt > "7d" AND size > "2mb"
tags IN ["sale", "summer"]
tags NOT EXISTS
format IN ["jpg", "webp"]
path : "/sales-banner/"
"customMetadata.brand" = "nike"
"customMetadata.Region" IN ["EMEA"]
"customMetadata.rating" > 4.3
"embeddedMetadata.DateTimeOriginal" > "1y"
(size < "1mb" AND width > 500) OR (tags IN ["summer-sale", "banner"])
```

User says "Nike assets" → `list_custom_metadata_fields` finds `brand` / options including Nike → `"customMetadata.brand" = "Nike"`. Do not search `name HAS "Nike"` if a field or tag matched.

## Gotchas

- `name` `=` / `:` are case-sensitive; use `HAS` for case-insensitive matching.
- `tags` queries search both `tags` and `AITags`.
- `HAS` tokenizes on spaces/punctuation; the last token matches as a prefix. Pair with `sort: DESC_RELEVANCE`.
- Booleans (`private`, `published`, `transparency`) are unquoted; string values are quoted.
- `width` / `height` / `transparency` apply to images only.
- `"customMetadata.<field>"` only matches fields defined on the account. Quote the whole token.
- The `type` tool argument is ignored whenever `searchQuery` is set. Put `type = "folder"` (or `type IN [...]`) in `searchQuery` instead.
