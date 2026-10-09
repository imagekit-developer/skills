---
name: upload-files
description: "Upload files to the ImageKit media library via DAM MCP. With a shell, use create_upload_signatures_in_bulk for any number of local files or URLs; without one, upload_file (interactive picker); create_upload_signature only when the user runs the upload elsewhere. Never inline file bytes into the conversation."
---

# Upload files

Uploads go through DAM (`https://imagekit.io/mcp/dam`).

**Never put file bytes in the conversation or a tool argument.** No base64, data URIs, Buffers, or streams. That burns tokens and fails for large files.

## How an upload works

An upload is a multipart/form-data POST to ImageKit's upload endpoint, authorized by a short-lived, single-use signature. The DAM server only signs. The file goes straight from where it lives to ImageKit: from the user's machine for a local file, or fetched by ImageKit for a public URL. Your job is to get a signature for each file and make sure the POST runs where the file is.

## Which tool

| Situation | Call |
|-----------|------|
| You can run shell commands in the user's environment (one file or many, local paths or public URLs) | `create_upload_signatures_in_bulk`, then run the returned `uploadCommand`. |
| No shell, and the user wants to pick a file on their computer (the client can show MCP Apps) | `upload_file` with **no parameters**. Opens a picker (filename, folder, tags, custom metadata). |
| The user will run the upload themselves elsewhere and needs the signed form fields | `create_upload_signature`; they POST each file with its `formFields`. |

Prefer `create_upload_signatures_in_bulk` whenever there is a shell, even for a single file: the signed tokens never enter the conversation, and one command uploads everything and reports a status line per file.

If they asked you to write upload code for their app, use `search_docs` — do not upload to their library unless they asked for that.

## `create_upload_signatures_in_bulk`

- Signs 1 to 1,000 entries in one call. Each entry is either a file directly inside one local directory or a public URL, with its own `fileName`, `folder`, and upload fields.
- The tokens are not returned. They stay on the server behind `manifestUrl` until `expire` (60 to 3,600 seconds, default 600). Pass `localDirectory` so the command knows where the local files are.
- Run the returned `uploadCommand` in the user's shell. It changes into the local directory, fetches the manifest, and uploads up to 16 files at a time.
- It prints one line per file: `<status> <name>`. `200` means uploaded. `SKIP <name>` means the name was refused locally (empty, contains `/` or `"`, or starts with `.`).
- Before expiry, re-running the same command retries failed files. Files that already uploaded are rejected, not duplicated. After expiry it prints `manifest unavailable` and uploads nothing, so sign again.
- Treat the manifest URL like a credential: anyone who has it can upload the signed files until it expires. Do not paste it anywhere other than the command.

## `create_upload_signature`

For when the user runs the upload themselves (their own script or another machine). The result contains the signed tokens.

- One call can sign several files: send one entry per file with `fileName`, plus optional `folder`, `tags`, `customMetadata`, and other upload fields. `expire` applies to all of them.
- The result has `uploadUrl` and, per file, `formFields`: the exact fields its signature is bound to, including `token`.
- Each file is POSTed to `uploadUrl` with `file=@<LOCAL_FILE_PATH>`, or `file=<PUBLIC_URL>` to have ImageKit fetch it, plus that file's `formFields` exactly as returned. Adding, removing, or re-serializing fields fails the signature check.
- Tokens are short-lived and single-use. Sign shortly before uploading.

## Procedure

1. Confirm folder, filename, tags, and custom metadata. Fields must already exist (`list_custom_metadata_fields`).
2. Call the tool from the table above.
3. Confirm the files landed with `search_media_library`, the upload responses, or the bulk command's status lines.

## Notes

- Folder is a media-library path starting with `/`, not a local path. Nested folders are created as needed.
- Free plan limits: 25MB images, 100MB videos. Max 100 versions per file.
- To preserve a migrated asset's original creation date, set the reserved `_internal_original_created_datetime` custom metadata key to an ISO 8601 string. It exists only on accounts that enabled the original creation date setting; check `list_custom_metadata_fields` for it (`reserved: true`).
