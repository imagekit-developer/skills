---
name: upload-files
description: "Upload files to the ImageKit media library via DAM MCP. Use upload_file (interactive picker) for local files; create_upload_signature for a public URL or CLI upload. Never inline file bytes into the conversation."
---

# Upload files

Uploads go through DAM (`https://imagekit.io/mcp/dam`).

**Never put file bytes in the conversation or a tool argument.** No base64, data URIs, Buffers, or streams. That burns tokens and fails for large files.

## Which tool

| Situation | Call |
|-----------|------|
| User wants to pick a file on their computer, or the client can show MCP Apps | `upload_file` with **no parameters**. Opens a picker (filename, folder, tags, custom metadata). |
| User has a **public URL**, or the client has no picker | `create_upload_signature`, then POST from the **user's environment** using the returned `formFields` and `curlExample`. |

If they asked you to write upload code for their app, use `search_docs` — do not upload to their library unless they asked for that.

## `create_upload_signature`

This tool never receives file contents. The response includes `formFields` (send these exactly) and `curlExample`.

POST multipart/form-data from the user's environment:

- `file=@<LOCAL_FILE_PATH>` for a file on disk, or
- `file=<PUBLIC_URL>` to have ImageKit fetch that URL

plus every `formFields` entry as returned. Do not add, remove, or re-serialize fields. One signature is one file; call again for each file.

## Procedure

1. Confirm folder, filename, tags, and custom metadata. Fields must already exist (`list_custom_metadata_fields`).
2. Call `upload_file` or `create_upload_signature` as above.
3. Confirm the file landed with `search_media_library` or the upload response.

## Notes

- Folder is a media-library path starting with `/`, not a local path. Nested folders are created as needed.
- Filenames allow `a-z`, `A-Z`, `0-9`, `.`, `-`. Other characters become `_`.
- Free plan limits: 25MB images, 100MB videos. Max 100 versions per file.
