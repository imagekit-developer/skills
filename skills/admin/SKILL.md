---
name: admin
description: "ImageKit Admin MCP — origins (external storage), URL endpoints, account usage, and usage analytics. Use when the user asks to connect S3/GCS/Azure/a web server, add or change a URL endpoint, or view bandwidth/storage usage."
---

# Admin MCP

Connect `https://imagekit.io/mcp/admin` (separate from DAM). These tools are not on DAM.

## Origins (external storage)

Create and manage where ImageKit fetches original files: S3, GCS, Azure, web server, and similar.

| Tool | When |
|------|------|
| `list_origins` | See what is already connected |
| `create_origin` | Add a new origin |
| `get_origin` | Inspect one origin |
| `update_origin` | Change credentials, bucket, or host |
| `delete_origin` | Remove an origin |

An origin does not serve traffic by itself. Attach it to a URL endpoint.

## URL endpoints

Delivery hostnames (`https://ik.imagekit.io/…` or a custom domain mapping). Origins are attached here, in preference order.

| Tool | When |
|------|------|
| `list_url_endpoints` | See existing endpoints |
| `create_url_endpoint` | Add an endpoint and attach origins |
| `get_url_endpoint` | Inspect one endpoint |
| `update_url_endpoint` | Change attached origins or settings |
| `delete_url_endpoint` | Remove an endpoint |

Typical order: `create_origin` (if needed) → `create_url_endpoint` or `update_url_endpoint` to attach it.

For provider-specific setup (IAM, bucket policy), use `search_docs` after picking the storage type from `imagekit-integrations`.

## Usage

| Tool | When |
|------|------|
| `get_account_usage` | Totals (bandwidth, storage, and similar) between two dates |
| `get_account_usage_analytics` | Breakdowns — countries, referrers, devices, and similar |

Do not look for usage tools on DAM.
