---
name: imagekit-sdk-reference
description: "TypeScript SDK reference for @imagekit/nodejs — method signatures, parameter and return types (File, Folder, CustomMetadataField), error handling, and examples. Use when writing ImageKit SDK code or calling the imagekit_api execute tool."
---

# ImageKit TypeScript SDK Reference

Read this skill before calling any `mcp_imagekit_api_*` tool or writing TypeScript code against the ImageKit SDK. It contains exact method signatures, parameter types, return shapes, and error handling patterns for `@imagekit/nodejs`.

**Rules:**
1. Use exact parameter names — the SDK is strict about camelCase
2. `assets.list()` returns `(File | Folder)[]`. Narrow with `for...of` + `if (item.type === 'file')`, never `.filter((i): i is File => ...)`. See the `search-assets` skill for the full rules on `searchQuery` vs a typed `File[]` and why the predicate fails.
3. In `execute`/MCP code, do NOT try/catch single API calls — the tool reports errors for you. Only catch when you branch on a specific failure, and **duck-type** the error (`'status' in err`) rather than `instanceof ImageKit.APIError`, since a value import of the SDK is not available in the sandbox.
4. Use `skip`/`limit` for pagination (max 1000 per request)
5. **Uploads are URL-only** — the `file` param must be a **URL string**; local file paths, Buffers, and streams cannot be passed. Read the `upload-files` skill first.
6. Nullable properties (`tags`, `AITags`, `customCoordinates`) require optional chaining (`?.`) or null checks
7. `.find()` returns `T | undefined` — always check for `undefined` before accessing properties

---

## TypeScript Gotchas

Union narrowing for `assets.list()` results — `for...of` + `if`, why the `.filter((i): i is File => ...)` predicate collides with Deno's global `File`, and `searchQuery` vs a typed `File[]` — is covered in full by the **`search-assets` skill**; follow it when handling list results. The gotchas below are the SDK-specific ones not covered there.

| Pattern | Problem | Fix |
|---------|---------|-----|
| `.find(i => ...)` | Returns `T \| undefined` | Check for `undefined` + narrow type |
| `file.tags` | `string[] \| null` | Use `?.` or null check |
| `file.AITags` | `Array \| null` | Use `?.` or null check |
| Any member-specific prop on a `File \| Folder` from `assets.list()` | Only shared fields (`name`, `type`, `createdAt`, `updatedAt`, `customMetadata`) exist on the union; the rest need narrowing | Narrow once with `if`, then access freely. Branch on `type === 'folder'` (→ `Folder`; else → `File`, since `File.type` is `'file' \| 'file-version'`) |

### `.find()` returns `T | undefined`

```typescript
const item = assets.find((i) => i.name === 'hero.jpg');
// Type: (File | Folder) | undefined

item.fileId; // ❌ Two errors: possibly undefined AND possibly Folder

// ✅ Fix:
if (item && item.type === 'file') {
  item.fileId; // works
}
```

### Nullable properties on File

```typescript
const file = await client.files.get(fileId);

file.tags.length;     // ❌ tags is string[] | null
file.tags?.length;    // ✅ optional chaining

file.AITags.map(...); // ❌ AITags is Array | null
file.AITags?.map(...); // ✅
```

---

## Types

### File
```typescript
{
  fileId: string; name: string; filePath: string; type: 'file' | 'file-version';
  url: string; thumbnail: string; isPrivateFile: boolean; isPublished: boolean;
  // Media
  fileType: string; // 'image' | 'non-image'
  mime: string; size: number; width: number; height: number; hasAlpha: boolean;
  // Video-only
  duration: number; videoCodec: string; audioCodec: string; bitRate: number;
  // Tags & metadata
  tags: string[] | null;
  AITags: Array<{ name: string; confidence: number; source: string }> | null;
  customMetadata: Record<string, unknown>; description: string;
  customCoordinates: string | null;
  embeddedMetadata: Record<string, unknown>;
  // Versioning
  versionInfo: { id: string; name: string };
  createdAt: string; updatedAt: string;
}
```

### Folder
```typescript
{
  folderId: string; folderPath: string; name: string; type: 'folder';
  customMetadata: Record<string, unknown>;
  createdAt: string; updatedAt: string;
}
```

### CustomMetadataField
```typescript
{
  id: string; name: string; label: string;
  schema: { type: 'Text' | 'Number' | 'Date' | 'Boolean' | 'SingleSelect' | 'MultiSelect'; /* ... */ };
}
```

---

## File Operations

### Upload a file (URL only)
```typescript
// ⚠️ ONLY URL-based uploads work. Local files cannot be uploaded.
const file = await client.files.upload({
  file: 'https://example.com/img.jpg', // URL string ONLY in MCP context
  fileName: 'img.jpg',
  folder: '/uploads',
  tags: ['tag1'],
  customMetadata: { key: 'value' },
  // Key optional params:
  // useUniqueFileName: true,      // default true — appends random suffix
  // isPrivateFile: false,
  // overwriteFile: false,         // replace existing file at same path
  // overwriteTags: false,
  // overwriteCustomMetadata: false,
  // extensions: [{ name: 'google-auto-tagging', maxTags: 5 }],
  // transformation: { pre: 'w-200' },
  // webhookUrl: 'https://...',
});
// Returns: File object
```

### Get file details
```typescript
const file = await client.files.get(fileId); // Returns: File
```

### List / search assets
```typescript
const result = await client.assets.list({
  searchQuery: 'name = "img.jpg"', // Lucene-like syntax
  path: '/uploads',
  fileType: 'image',           // 'image' | 'non-image' | 'all'
  type: 'file',                // 'file' | 'folder' | 'file-version' | 'all'
  sort: 'ASC_NAME',
  skip: 0,
  limit: 100,
});
// Returns: (File | Folder)[] — a flat array, NOT { files, folders }
```

**Type narrowing depends on whether you use `searchQuery`** — see the `search-assets` skill for the full rules (a top-level `type` gives a typed `File[]`; a `searchQuery` returns the `(File | Folder)[]` union, which you narrow with `for...of` + `if`).

**Shared properties** (safe on both File and Folder): `name`, `type`, `customMetadata`, `createdAt`, `updatedAt`

**File-only properties** (require narrowing): `fileId`, `filePath`, `fileType`, `mime`, `size`, `width`, `height`, `url`, `thumbnail`, `tags`, `AITags`, `description`, `isPrivateFile`, `isPublished`, `customCoordinates`, `embeddedMetadata`, `versionInfo`, `duration`, `videoCodec`, `audioCodec`, `bitRate`, `hasAlpha`

**Folder-only properties**: `folderId`, `folderPath`

### Update / delete file
```typescript
await client.files.update(fileId, { tags: ['newTag'], customMetadata: { key: 'value' } }); // Returns: File
await client.files.delete(fileId); // Returns: void
```

### Copy / move / rename file
```typescript
await client.files.copy({ sourceFilePath: '/a/img.jpg', destinationPath: '/b/', includeFileVersions: false });
await client.files.move({ sourceFilePath: '/a/img.jpg', destinationPath: '/b/' });
await client.files.rename({ filePath: '/a/img.jpg', newFileName: 'new.jpg', purgeCache: false });
```

---

## Bulk Operations

```typescript
await client.files.bulk.delete({ fileIds: ['id1', 'id2'] }); // { successfullyDeletedFileIds }
await client.files.bulk.addTags({ fileIds: ['id1'], tags: ['promo'] });    // max 50 files
await client.files.bulk.removeTags({ fileIds: ['id1'], tags: ['old'] });
await client.files.bulk.removeAITags({ fileIds: ['id1'], AITags: ['cat'] });
```

---

## Folder Operations

```typescript
await client.folders.create({ folderName: 'myfolder', parentFolderPath: '/' });
await client.folders.delete({ folderPath: '/myfolder' });

// Copy / move / rename — async operations, return { jobId }
const { jobId } = await client.folders.copy({ sourceFolderPath: '/a', destinationPath: '/b/' });
const { jobId } = await client.folders.move({ sourceFolderPath: '/a', destinationPath: '/b/' });
const { jobId } = await client.folders.rename({ folderPath: '/a', newFolderName: 'renamed' });

// Check job status
const job = await client.folders.job.get(jobId);
// job.status: 'Pending' | 'Completed'
```

---

## File Versions

```typescript
const versions = await client.files.versions.list(fileId);      // Returns: File[]
const version = await client.files.versions.get(versionId, { fileId }); // Returns: File
await client.files.versions.restore(versionId, { fileId });     // Returns: File
await client.files.versions.delete(versionId, { fileId });      // Returns: void
```

---

## File Metadata

```typescript
const metadata = await client.files.metadata.getFromURL({ url: 'https://ik.imagekit.io/x/img.jpg' });
// Returns EXIF/IPTC metadata: { height, width, exif, iptc, xmp, ... }
```

---

## Cache Invalidation

```typescript
const purge = await client.cache.invalidation.create({ url: 'https://ik.imagekit.io/x/img.jpg' });
const status = await client.cache.invalidation.get(purge.requestId);
// status.status: 'Pending' | 'Completed'
```

---

## URL Building

```typescript
const url = client.helper.buildSrc({
  urlEndpoint: 'https://ik.imagekit.io/your_id',
  src: '/path/img.jpg',
  transformation: [{ width: 400, height: 300, format: 'webp', quality: 80 }],
  signed: true,
  expiresIn: 3600,
});
// Returns: string
```

---

## Custom Metadata Fields

```typescript
// Define schema fields for your media library
const field = await client.customMetadataFields.create({
  name: 'brand', label: 'Brand Name',
  schema: { type: 'Text', defaultValue: '', isValueRequired: false },
});
const fields = await client.customMetadataFields.list(); // Returns: CustomMetadataField[]
await client.customMetadataFields.update(field.id, { label: 'Updated Label' });
await client.customMetadataFields.delete(field.id);
```

---

## Account Usage

```typescript
const usage = await client.accounts.usage.get({ startDate: '2025-01-01', endDate: '2025-01-31' });
// { bandwidthBytes, mediaLibraryStorageBytes, extensionUnitsCount, videoProcessingUnitsCount }
```

---

## Pagination & Error Handling

```typescript
// Offset-based pagination — skip / limit (max 1000). No cursor support.
for (let skip = 0; ; skip += 100) {
  const page = await client.assets.list({ skip, limit: 100 });
  if (!page.length) break;
  for (const item of page) {
    if (item.type === 'file') {
      // item is narrowed to File here
    }
  }
}

// Error handling — in execute/MCP code you normally DON'T need try/catch: let the
// error propagate and the tool reports it for you. The ONLY reason to catch is to
// branch on a specific failure (e.g. treat 404 as "not found") — and then you must
// re-throw everything you don't handle. Duck-type the error: a value import of the
// SDK (import ImageKit from '@imagekit/nodejs') is NOT available in the Deno sandbox
// and throws at runtime, so don't rely on `instanceof ImageKit.APIError`.
try {
  return await client.files.get(fileId);
} catch (err) {
  if (err && typeof err === 'object' && 'status' in err) {
    const e = err as { status?: number; message?: string };
    if (e.status === 404) return null;  // the one case we handle
  }
  throw err;  // re-throw anything else — don't swallow it
}
// Auto-retries: connection errors, 408/409/429/5xx — up to 2× with exponential backoff
```

## Parallel Execution for Bulk File Operations

When you have a list of files to operate on, never await in a loop. Chunk into batches of 100 and run each batch concurrently with Promise.allSettled().

```typescript
// ✅ files is any array of { fileId, name } — from assets.list(), a prior search, etc.
const CHUNK = 100;
const chunks = [];
for (let i = 0; i < files.length; i += CHUNK) chunks.push(files.slice(i, i + CHUNK));

for (const chunk of chunks) {
  await Promise.allSettled(
    chunk.map(({ fileId, name }) =>
      client.files.update(fileId, { tags: ['promo'] })
        .then(() => ({ fileId, name, status: 'ok' }))
        .catch((err: unknown) => ({ fileId, name, status: 'error', error: String(err) }))
    )
  );
}
```

Same pattern applies for files.delete(fileId), files.copy({...}), and files.move({...}).

For delete / addTags / removeTags, prefer the bulk endpoints (max 50 IDs each) — chunk IDs and run chunks in parallel:

```typescript
const CHUNK = 50;
const chunks = [];
for (let i = 0; i < allFileIds.length; i += CHUNK) chunks.push(allFileIds.slice(i, i + CHUNK));
await Promise.allSettled(chunks.map(ids => client.files.bulk.delete({ fileIds: ids })));
```