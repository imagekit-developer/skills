---
name: upload-files
description: "Upload files to the ImageKit media library via DAM MCP: an interactive file picker, signed uploads, or a bulk upload command for many local files or URLs. Never inline file bytes into the conversation."
---

# Upload files

Uploads go through DAM (`https://imagekit.io/mcp/dam`). Tool names can change between server versions, so choose tools by what their descriptions say they do, using the capabilities below.

**Never put file bytes in the conversation or a tool argument.** No base64, data URIs, Buffers, or streams. That burns tokens and fails for large files.

## How an upload works

An upload is a multipart/form-data POST to ImageKit's upload endpoint, authorized by a short-lived, single-use signature. The DAM server only signs. The file goes straight from where it lives to ImageKit: from the user's machine for a local file, or fetched by ImageKit for a public URL. Your job is to get a signature for each file and make sure the POST runs where the file is.

## Pick the path

| Situation | Use |
|-----------|-----|
| User wants to choose a file on their computer, and the client can show MCP Apps | The **interactive upload tool**. It takes no parameters and opens a picker (file name, folder, tags, custom metadata). |
| One or a few files (local paths or public URLs), and you or the user can make the POST | The **signing tool that returns form fields**. |
| Many files (a local folder, or a list of URLs), and the environment can run shell commands | The **bulk signing tool that returns an upload command** instead of tokens. |

If they asked you to write upload code for their app, search the docs instead. Do not upload to their library unless they asked for that.

## Signed upload (form fields returned)

- One call can sign several files: send one entry per file with `fileName`, plus optional `folder`, `tags`, `customMetadata`, and other upload fields. `expire` applies to all of them.
- The result has the upload URL and, per file, `formFields`: the exact fields its signature is bound to, including `token`.
- POST each file to the upload URL from the user's environment with `file=@<LOCAL_FILE_PATH>`, or `file=<PUBLIC_URL>` to have ImageKit fetch it, plus that file's `formFields` exactly as returned. Adding, removing, or re-serializing fields fails the signature check.
- Tokens are short-lived and single-use. Sign shortly before uploading.

## Bulk upload (command returned)

- Signs up to 1,000 entries in one call. Each entry is either a file directly inside one local directory or a public URL, with its own `fileName`, `folder`, and upload fields.
- The tokens are not returned. They stay on the server behind a manifest URL until `expire` (60 to 3,600 seconds, default 600).
- The result includes a bash upload command. Run it in the user's shell. It changes into the local directory, fetches the manifest, and uploads up to 16 files at a time.
- It prints one line per file: `<status> <name>`. `200` means uploaded. `SKIP <name>` means the name was refused locally (empty, contains `/` or `"`, or starts with `.`).
- Before expiry, re-running the same command retries failed files. Files that already uploaded are rejected, not duplicated. After expiry it prints `manifest unavailable` and uploads nothing, so sign again.
- Treat the manifest URL like a credential: anyone who has it can upload the signed files until it expires. Do not paste it anywhere other than the command.

## Procedure

1. Confirm the destination folder, file names, tags, and custom metadata. Custom metadata fields must already exist, so list the account's custom metadata fields first.
2. Pick the path above, sign, and upload.
3. Confirm the files landed: the per-file status lines or upload responses, or a media library search.

## Notes

- Folder is a media-library path starting with `/`, not a local path. Nested folders are created as needed.
- Free plan limits: 25MB images, 100MB videos. Max 100 versions per file.
- To preserve a migrated asset's original creation date, set the reserved `_internal_original_created_datetime` custom metadata key to an ISO 8601 string. It exists only on accounts that enabled the original creation date setting; check the account's custom metadata fields for it (`reserved: true`).
