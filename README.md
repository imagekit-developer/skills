# ImageKit Skills

[![skills.sh](https://skills.sh/b/imagekit-developer/skills)](https://skills.sh/imagekit-developer/skills)

Reusable AI agent skills for [ImageKit.io](https://imagekit.io) — install them with the `skills` CLI to enhance your coding agent's capabilities.

## Skills

| Skill | Description |
|-------|-------------|
| **mcp-preflight** | Mandatory routing guide — tells the agent which MCP server (DAM, Admin, or DevTools) to call for what, before every ImageKit tool invocation |
| **imagekit-sdk-reference** | TypeScript SDK reference — method signatures, types (File, Folder), error handling, and examples for `@imagekit/nodejs` |
| **imagekit-integrations** | Index of ImageKit SDKs, plugins, and integrations across front-end, back-end, mobile, CMS, storage, video, upload widgets, and URL generation |
| **search-assets** | Filter and search ImageKit files and folders using the Lucene-like `searchQuery` syntax, operators, and field reference |
| **asset-access-control** | Share or revoke access on files, folders, and media collections via DAM MCP |
| **search-docs** | Search ImageKit documentation with optimized queries and source selection |
| **transformation-builder** | Build ImageKit image/video transformations — AI editing, background removal, resize, crop, overlays, and more |
| **upload-files** | Upload files to the ImageKit media library via DAM MCP (`upload_file` picker or `create_upload_signature`) |
| **ai-tasks** | Apply AI-powered analysis to images for business-specific tagging, metadata extraction, and quality checks using controlled vocabularies |

## Installation

There are two pieces to install: the **skills** (this repo) and the **MCP servers**:

| MCP server | URL | Auth |
|------------|-----|------|
| `imagekit_devtools` | `https://devtools-mcp.imagekit.io/mcp` | None |
| `imagekit_dam` | `https://imagekit.io/mcp/dam` | Sign in with your ImageKit account |
| `imagekit_admin` | `https://imagekit.io/mcp/admin` | Sign in with your ImageKit account |

If you previously connected `https://api-mcp.imagekit.io/mcp`, remove it and add DAM and Admin instead.

Pick one of the two methods below. Restart your editor after installing so the MCP servers take effect. Authenticate DAM and Admin when prompted.

### Plugin method (recommended)

On Claude Desktop, Claude.ai (web), and VS Code, the ImageKit plugin installs the skills and MCP servers in a single step.

**Claude Desktop & Claude.ai (web)**

1. Open Customize in the left sidebar and go to the Plugins tab.
2. Under Personal plugins, click **+** → Add marketplace → Add from a repository, and enter `imagekit-developer/skills`.
3. Install the ImageKit plugin from that marketplace.
4. Enable the bundled `imagekit_devtools`, `imagekit_dam`, and `imagekit_admin` connectors, and authenticate DAM and Admin when prompted.

**VS Code**

1. Open the Command Palette (`⇧⌘P`) and run Install Plugin from Source.
2. Enter `imagekit-developer/skills` as the plugin source.
3. Restart VS Code.

### Manual method

**1. Install the skills** (same command on every platform):

```bash
npx skills add imagekit-developer/skills --all
```

**2. Add the MCP servers** for your tool:

<details>
<summary><b>Claude Code</b></summary>

```bash
claude mcp add --transport http imagekit_devtools https://devtools-mcp.imagekit.io/mcp
claude mcp add --transport http imagekit_dam https://imagekit.io/mcp/dam
claude mcp add --transport http imagekit_admin https://imagekit.io/mcp/admin
```
</details>

<details>
<summary><b>Claude Desktop</b></summary>

Edit your config file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "imagekit_devtools": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://devtools-mcp.imagekit.io/mcp"]
    },
    "imagekit_dam": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://imagekit.io/mcp/dam"]
    },
    "imagekit_admin": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://imagekit.io/mcp/admin"]
    }
  }
}
```
</details>

<details>
<summary><b>Codex</b></summary>

Via CLI:

```bash
codex mcp add imagekit_devtools --url https://devtools-mcp.imagekit.io/mcp
codex mcp add imagekit_dam --url https://imagekit.io/mcp/dam
codex mcp add imagekit_admin --url https://imagekit.io/mcp/admin
```

Or edit `~/.codex/config.toml`:

```toml
[mcp_servers.imagekit_devtools]
url = "https://devtools-mcp.imagekit.io/mcp"

[mcp_servers.imagekit_dam]
url = "https://imagekit.io/mcp/dam"

[mcp_servers.imagekit_admin]
url = "https://imagekit.io/mcp/admin"
```
</details>

<details>
<summary><b>VS Code Copilot</b></summary>

```bash
code --add-mcp "{\"name\":\"imagekit_devtools\",\"type\":\"http\",\"url\":\"https://devtools-mcp.imagekit.io/mcp\"}"
code --add-mcp "{\"name\":\"imagekit_dam\",\"type\":\"http\",\"url\":\"https://imagekit.io/mcp/dam\"}"
code --add-mcp "{\"name\":\"imagekit_admin\",\"type\":\"http\",\"url\":\"https://imagekit.io/mcp/admin\"}"
```
</details>

<details>
<summary><b>Cursor</b></summary>

Install with these buttons:

- [![Install DevTools MCP Server](https://cursor.com/deeplink/mcp-install-light.svg)](https://cursor.com/en-US/install-mcp?name=imagekit_devtools&config=eyJ1cmwiOiJodHRwczovL2RldnRvb2xzLW1jcC5pbWFnZWtpdC5pby9tY3AifQ%3D%3D)
- [![Install DAM MCP Server](https://cursor.com/deeplink/mcp-install-light.svg)](https://cursor.com/en-US/install-mcp?name=imagekit_dam&config=eyJ1cmwiOiJodHRwczovL2ltYWdla2l0LmlvL21jcC9kYW0ifQ%3D%3D)
- [![Install Admin MCP Server](https://cursor.com/deeplink/mcp-install-light.svg)](https://cursor.com/en-US/install-mcp?name=imagekit_admin&config=eyJ1cmwiOiJodHRwczovL2ltYWdla2l0LmlvL21jcC9hZG1pbiJ9)

Or edit `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "imagekit_devtools": { "url": "https://devtools-mcp.imagekit.io/mcp" },
    "imagekit_dam": { "url": "https://imagekit.io/mcp/dam" },
    "imagekit_admin": { "url": "https://imagekit.io/mcp/admin" }
  }
}
```
</details>

<details>
<summary><b>Windsurf</b></summary>

Edit `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "imagekit_devtools": { "serverUrl": "https://devtools-mcp.imagekit.io/mcp" },
    "imagekit_dam": { "serverUrl": "https://imagekit.io/mcp/dam" },
    "imagekit_admin": { "serverUrl": "https://imagekit.io/mcp/admin" }
  }
}
```
</details>

## Usage

Once installed, these skills are automatically available to your AI agent. The agent will consult the relevant skill before performing ImageKit operations, ensuring correct tool usage and better results.

## License

MIT
