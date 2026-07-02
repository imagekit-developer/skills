---
name: upload-files
description: 'Upload files to ImageKit from a publicly accessible URL. Use when: uploading images, videos, or files to ImageKit media library; specifying folder paths; setting file names, tags, or metadata during upload. NOTE: only URL-based uploads are supported — local file paths cannot be passed.'
---

# Upload Files to ImageKit

## CRITICAL: Only URL-based uploads are supported

The `file` parameter must be a **publicly accessible URL string**. **Local files cannot be uploaded** — local paths, Buffers, and streams are not supported and will fail. If the user has a local file, they must first host it at a public URL and pass that URL.

Both `file` and `fileName` are **required**.

**NEVER convert a local file to a base64 (data URI) string and try to upload it.** Reading a file into the model context to base64-encode it burns a huge number of LLM tokens and still won't work for large files. Always pass a URL — never inline file bytes.

Uploads are performed with the SDK's `client.files.upload()` method via `mcp_imagekit_api_execute`.

## Usage

```typescript
async function run(client) {
  const file = await client.files.upload({
    file: 'https://example.com/photo.jpg', // URL string ONLY — no local paths
    fileName: 'photo.jpg',
    folder: '/products',
    tags: ['product', 'featured'],
  });
  return { fileId: file.fileId, url: file.url, size: file.size, fileType: file.fileType };
}
```

## Parameters

Parameter names mirror the Upload API (`FileUploadV1`) field names in camelCase. When a field is omitted, ImageKit applies its own default.

| Parameter | Description |
|-----------|-------------|
| `file` (required) | **Publicly accessible URL** of the file to upload. Local paths are NOT allowed. |
| `fileName` (required) | Name for the uploaded file, e.g. `'photo.jpg'`. |
| `folder` | Destination folder in ImageKit (default: `/`) |
| `tags` | Array of tags (e.g. `['product', 'featured']`) |
| `isPrivateFile` | Mark file as private |
| `isPublished` | Publish the file; `false` uploads as draft (enterprise plans) |
| `useUniqueFileName` | Add a unique suffix to the filename (default `true`) |
| `overwriteFile` | Overwrite an existing file at the same path |
| `overwriteAITags` | Overwrite existing AITags when replacing |
| `overwriteTags` | Overwrite existing tags when replacing |
| `overwriteCustomMetadata` | Overwrite existing customMetadata when replacing |
| `description` | Description for the file |
| `customCoordinates` | Important area: `"x,y,width,height"` |
| `customMetadata` | Object of custom metadata, e.g. `{ brand: 'Nike' }` (fields must exist in DAM first) |
| `extensions` | Array of extensions, e.g. `[{ name: 'google-auto-tagging', maxTags: 5 }]` |
| `transformation` | Object of pre/post transformations, e.g. `{ pre: 'w-1200,q-80' }` |
| `webhookUrl` | URL to receive extension completion status |
| `responseFields` | Fields to include in the response (e.g. `['tags', 'customMetadata', 'metadata']`) |
| `checks` | Server-side upload check expression |

## Examples

```typescript
// Basic upload to a folder with tags
await client.files.upload({
  file: 'https://example.com/photo.jpg',
  fileName: 'photo.jpg',
  folder: '/products',
  tags: ['product', 'featured'],
});

// Overwrite an exact-named file
await client.files.upload({
  file: 'https://example.com/banner.jpg',
  fileName: 'banner.jpg',
  useUniqueFileName: false,
  overwriteFile: true,
});

// Upload with auto-tagging extension
await client.files.upload({
  file: 'https://example.com/photo.jpg',
  fileName: 'photo.jpg',
  extensions: [{ name: 'google-auto-tagging', maxTags: 5 }],
});

// Upload with custom metadata and a pre-transformation
await client.files.upload({
  file: 'https://example.com/photo.jpg',
  fileName: 'photo.jpg',
  customMetadata: { brand: 'Nike' },
  transformation: { pre: 'w-1200,q-80' },
});
```

## Notes

- **Local files cannot be uploaded.** Only a publicly accessible URL works. If the user provides a local path, tell them to host it publicly first and share the URL.
- `folder` is the ImageKit media library path (not local). Starts with `/`, auto-creates nested folders. Don't include the filename in the folder path.
- `fileName` allows: `a-z`, `A-Z`, `0-9`, `.`, `-`. Other characters become `_`.
- `useUniqueFileName` defaults to `true` (a unique suffix is appended). To overwrite an exact-named file, set `useUniqueFileName: false` and `overwriteFile: true`.
- `customMetadata` fields must be created in the DAM first.

## Procedure

1. **Get a public URL**: Confirm the file is available at a publicly accessible URL. If the user has only a local file, stop and ask them to host it and provide the URL.
2. **Decide folder and tags**: Where in the ImageKit media library the file should live.
3. **Run the upload** via `mcp_imagekit_api_execute` using `client.files.upload()`.
4. **Verify the response**: Confirm a `fileId` and `url` are returned and the reported `size`/`fileType` match (`fileType` is `image` for images, `non-image` for video and other files).

## Error Prevention

- **Local paths fail**: Passing a local file path, Buffer, or stream is not supported — always pass a URL string.
- **Never base64-encode a file to upload it**: Converting a local file to a base64/data-URI string wastes LLM tokens and fails for large files. Host the file and pass its URL instead.
- **File size limits**: Free plan: 25MB images, 100MB videos. Paid plans: higher.
- **Version limit**: Max 100 versions per file.
