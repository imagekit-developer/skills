---
name: asset-access-control
description: "Share or revoke access on ImageKit files, folders, and media collections via DAM MCP. Use when the user asks who can see an asset, to grant READ/CONTRIBUTE/MANAGE, or to add/remove a user or group from an ACL."
---

# Asset access control

Use the **DAM MCP** tools. Tool names can change between server versions, so choose tools by what their descriptions say they do.

Files and folders, and media collections, are two separate access surfaces. Do not mix their tools.

| Target | Read access | Change access |
|--------|-------------|---------------|
| File or folder | The read-only tool that returns a file or folder's access list | The tool that updates a file or folder's access control list |
| Media collection | The tool that returns a media collection's access list | The media collection update tool, through its `acl` field |

A separate lookup only answers "which collections contain this file or folder?". It does not change membership; adding or removing an asset from a collection uses the add/remove collection-assets tools.

## Permission levels

Each level includes the ones before it:

- `READ`: view and download the asset.
- `CONTRIBUTE`: READ, plus add and edit (upload into a folder, change tags and custom metadata, apply extensions).
- `MANAGE`: full control, including delete, public links, and changing the access list.

Restricted users can only change access on assets they can manage.

## Workflow

1. If you only have a name or path, resolve the asset with a media library search.
2. Read the current access list. Use `userId` / `groupId` from that response; never invent ids.
3. Write the change. Then re-read if you need to confirm.

The file/folder access-list read also returns the account's `users` and `userGroups`. Match the person the user named against `userName` / `userEmail` / `label`.

## Changing a file or folder's access

- Always send **both** `acl.addOrModify` and `acl.remove`. Use `[]` on the unused side.
- `entity.type` is only `USER` or `USER_GROUP`. `MEDIA_COLLECTION` may appear on read (access inherited through a collection); do not send it on write.
- Do not change the asset owner's entry.
- Do not grant less than a parent folder already grants that same entity.

```json
{
  "assetId": "<file-or-folder-id>",
  "acl": {
    "addOrModify": [{ "entity": { "id": "<userId>", "type": "USER" }, "permission": "READ" }],
    "remove": []
  }
}
```

## Listing collections that contain an asset

Its `permission` filter is a **string**, not an array. Send `'["MANAGE"]'` or `'["READ","CONTRIBUTE"]'`. Omit it unless you are filtering for a restricted user.
