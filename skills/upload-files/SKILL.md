---
name: upload-files
description: 'Upload files to ImageKit using the upload CLI script. Use when: uploading images, videos, or files to ImageKit media library; specifying folder paths; setting file names, tags, or metadata during upload.'
---

# Upload Files to ImageKit

## CRITICAL: Do NOT use `mcp_imagekit_api_upload_files`

The MCP upload tool cannot handle local files — it uploads the path string as content, not actual file bytes. Always use the CLI script instead.

## Usage

Requires `IMAGEKIT_PRIVATE_KEY` in `.env` or environment, and `requests` package.

```bash
source .env && python3 skills/upload-files/resources/upload.py <file_path> [options]
```

### CLI Arguments

| Argument | Description |
|----------|-------------|
| `file` (positional) | Path to the local file to upload |
| `--file-name` | Name for the uploaded file (default: original filename) |
| `--folder` | Destination folder in ImageKit (default: `/`) |
| `--tags` | Comma-separated tags (e.g. `product,featured`) |
| `--private` | Mark file as private |
| `--no-unique-name` | Don't add unique suffix to filename |
| `--overwrite` | Overwrite existing file with same name |
| `--description` | Description for the file |
| `--custom-coordinates` | Important area: `x,y,width,height` |
| `--json` | Output full JSON response |

### Examples

```bash
python3 skills/upload-files/resources/upload.py images/photo.jpg --folder /products --tags product,featured
python3 skills/upload-files/resources/upload.py images/photo.jpg --file-name banner.jpg --overwrite --json
```

## Notes

- `--folder` is the ImageKit media library path (not local). Starts with `/`, auto-creates nested folders. Don't include filename in folder path.
- `--file-name` allows: `a-z`, `A-Z`, `0-9`, `.`, `-`. Other chars become `_`.
- If `useUniqueFileName: true` (default), ImageKit appends a unique suffix

## Procedure

1. **Load `.env`**: ALWAYS load the `.env` file before running the script. If `.env` does not exist or `IMAGEKIT_PRIVATE_KEY` is not set in it, **stop and ask the user** to provide the key.
2. **Determine the file path**: Resolve the local file path.
3. **Decide folder and tags**: Where in ImageKit media library the file should live.
4. **Run the upload script** in a terminal with the correct arguments.
5. **Verify the response**: Check that `fileType` is `image` (not `non-image`) and size matches.

## Example Invocation from Agent

**Always source `.env` first:**

```bash
source .env && python3 skills/upload-files/resources/upload.py images/photo.jpg --folder /products --tags product,featured
```

If `source .env` doesn't export the variable (some `.env` formats), use:

```bash
export $(grep -v '^#' .env | xargs) && python3 skills/upload-files/resources/upload.py images/photo.jpg --folder /products --tags product,featured
```

**If `.env` is missing or key is not set, tell the user:**
> "I need your ImageKit private key to upload files. Please create a `.env` file in the project root with: `IMAGEKIT_PRIVATE_KEY=your_key_here`"
  "useUniqueFileName": false
}
```

### Upload from URL
```json
{
  "file": "https://example.com/photos/sunset.jpg",
  "fileName": "sunset.jpg",
  "folder": "/stock-photos"
}
```

### Upload with pre-transformation (resize before storing)
```json
{
  "file": "https://example.com/large-photo.jpg",
  "fileName": "optimized-photo.jpg",
  "folder": "/optimized",
  "transformation": {
    "pre": "w-1200,h-800,q-80"
  }
}
```

## Optional Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `folder` | string | `/` | Destination folder in ImageKit |
| `useUniqueFileName` | boolean | `true` | Append unique suffix to avoid conflicts |
| `tags` | string[] | — | Array of tags (max 500 chars total) |
| `isPrivateFile` | boolean | `false` | Restrict access to signed URLs only |
| `customMetadata` | object | — | Key-value metadata (fields must exist first) |
| `overwriteFile` | boolean | `true` | Replace existing file at same path |
| `transformation` | object | — | Pre/post upload transformations |
| `extensions` | array | — | Extensions like `remove-bg`, `google-auto-tagging` |
| `webhookUrl` | string | — | URL to receive extension completion status |
| `description` | string | — | Text describing the file contents |

## Error Prevention

- **Auth errors**: Ensure `IMAGEKIT_PRIVATE_KEY` is set before calling.
- **URL timeout**: Remote URLs must respond within 8 seconds.
- **File size limits**: Free plan: 25MB images, 100MB videos. Paid plans: higher.
- **Version limit**: Max 100 versions per file.
