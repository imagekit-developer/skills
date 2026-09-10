---
name: upload-files
description: "Upload files to the ImageKit media library. Use when uploading images, videos, or files; specifying folder paths, tags, or metadata. Prefer the DAM upload_file tool (interactive picker) for local files; use create_upload_signature for URL or CLI uploads. Never inline file bytes into the conversation."
---

# Upload Files to ImageKit

Uploads go through the **DAM MCP server** (`https://imagekit.io/mcp/dam`). Do not look for an `execute` tool or `client.files.upload()` over MCP.

**NEVER convert a local file to a base64 (data URI) string and try to upload it.** Reading a file into the model context burns a huge number of tokens and still fails for large files. Never pass file bytes, Buffers, or streams as tool arguments.

## Choose a path

| Situation | What to call |
|-----------|----------------|
| User wants to pick a local file, or the client supports MCP Apps | `upload_file` — **no parameters**. Opens an interactive picker (filename, folder, tags, custom metadata). |
| User has a **public URL**, or the client has no MCP Apps | `create_upload_signature`, then POST multipart from the **user's environment** using the returned `formFields` and `curlExample`. |
| User is writing **application code** (Node, browser, etc.) | Read the `imagekit-sdk-reference` skill and `search_docs`. Do not upload via MCP unless they asked you to put the file in their live library. |

`upload_file` injects `clientNumber` from the OAuth token. Folder suggestions use `search_media_library` with `searchQuery: type = "folder"`. Tag suggestions use `list_client_tags`. Metadata fields come from `list_custom_metadata_fields` for that folder (path-policy overlays apply).

## `create_upload_signature` (URL or CLI)

This tool never receives or returns file contents. The response contains:

- `token`
- `formFields` — the exact multipart fields the signature is bound to
- `curlExample` — a ready-to-run command with a file-path placeholder

To upload, POST multipart/form-data from the user's environment:

- `file=@<LOCAL_FILE_PATH>` for a file on disk, or
- `file=<PUBLIC_URL>` to have ImageKit fetch a publicly accessible URL

plus **every** `formFields` entry exactly as returned. Do not add, remove, or re-serialize fields. One signature covers one file; call again for each file.

Scope: `mcp_media_library:write`.

## Procedure

1. **Confirm destination.** Folder path, filename, tags, and any custom metadata. Custom metadata fields must already exist in the DAM (`list_custom_metadata_fields`).
2. **Pick the upload path** from the table above.
3. **If using `upload_file`:** call it with no arguments and let the user complete the picker.
4. **If using `create_upload_signature`:** call it, then run the returned upload command in the user's environment. Never paste file contents into chat.
5. **Verify:** the library should show a new file (`search_media_library` or the upload response). Check `fileId` / URL when returned.

## Notes

- `folder` is the ImageKit media library path (not a local path). Starts with `/`; nested folders are created as needed. Do not put the filename in the folder path.
- Filenames allow `a-z`, `A-Z`, `0-9`, `.`, `-`. Other characters become `_`.
- File size limits: Free plan 25MB images / 100MB videos. Paid plans are higher.
- Version limit: max 100 versions per file.

## Error Prevention

- **No file bytes in tool arguments or chat.** Use `upload_file` or a shell POST with `file=@...` / `file=<URL>`.
- **Never base64-encode a file to upload it.**
- **Do not skip `formFields`.** The signature is bound to those fields; changing them makes the upload fail.
- **Write scope required.** If the tool returns `insufficient_scope`, the user must grant `mcp_media_library:write` on the DAM consent screen.
