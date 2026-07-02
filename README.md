# ImageKit Skills

[![skills.sh](https://skills.sh/b/imagekit-developer/skills)](https://skills.sh/imagekit-developer/skills)

Reusable AI agent skills for [ImageKit.io](https://imagekit.io) — install them with the `skills` CLI to enhance your coding agent's capabilities.

## Skills

| Skill | Description |
|-------|-------------|
| **mcp-preflight** | Mandatory routing guide — tells the agent which MCP server to call for what, before every ImageKit tool invocation |
| **imagekit-sdk-reference** | TypeScript SDK reference — method signatures, types (File, Folder), error handling, and examples for `@imagekit/nodejs` |
| **imagekit-integrations** | Index of ImageKit SDKs, plugins, and integrations across front-end, back-end, mobile, CMS, storage, video, upload widgets, and URL generation |
| **search-assets** | Filter and search ImageKit files and folders using the Lucene-like `searchQuery` syntax, operators, and field reference |
| **search-docs** | Search ImageKit documentation with optimized queries and source selection |
| **transformation-builder** | Build ImageKit image/video transformations — AI editing, background removal, resize, crop, overlays, and more |
| **upload-files** | Upload files to the ImageKit media library from a public URL (local files not supported) with folder paths, tags, and metadata |
| **ai-tasks** | Apply AI-powered analysis to images for business-specific tagging, metadata extraction, and quality checks using controlled vocabularies |

## Installation

There are two pieces to install: the **skills** (this repo) and two **MCP servers**:

| MCP server | URL |
|------------|-----|
| `imagekit_devtools` | `https://devtools-mcp.imagekit.io/mcp` |
| `imagekit_api` | `https://api-mcp.imagekit.io/mcp` |

Pick one of the two methods below. Restart your editor after installing so the MCP servers take effect.

### Plugin method (recommended)

On **Claude Desktop** and **VS Code**, the ImageKit plugin installs the skills **and** both MCP servers in a single step.

**Claude Desktop**

1. Open **Customize** in the left sidebar, then click **+** → **Create Plugin** → **Add Marketplace**.
2. Enter `imagekit-developer/skills` as the marketplace, then find and install the **ImageKit Skills** plugin.
3. Open **Connectors** in the installed plugin, enable `imagekit_devtools` and `imagekit_api`, and complete authentication for `imagekit_api` when prompted.

**VS Code**

1. Open the Command Palette (`⇧⌘P`) and run **Install Plugin from Source**.
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
claude mcp add --transport http imagekit_api https://api-mcp.imagekit.io/mcp
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
    "imagekit_api": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://api-mcp.imagekit.io/mcp"]
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
codex mcp add imagekit_api --url https://api-mcp.imagekit.io/mcp
```

Or edit `~/.codex/config.toml`:

```toml
[mcp_servers.imagekit_devtools]
url = "https://devtools-mcp.imagekit.io/mcp"

[mcp_servers.imagekit_api]
url = "https://api-mcp.imagekit.io/mcp"
```
</details>

<details>
<summary><b>VS Code Copilot</b></summary>

```bash
code --add-mcp "{\"name\":\"imagekit_devtools\",\"type\":\"http\",\"url\":\"https://devtools-mcp.imagekit.io/mcp\"}"
code --add-mcp "{\"name\":\"imagekit_api\",\"type\":\"http\",\"url\":\"https://api-mcp.imagekit.io/mcp\"}"
```
</details>

<details>
<summary><b>Cursor</b></summary>

Install with these buttons:

- [![Install DevTools MCP Server](https://cursor.com/deeplink/mcp-install-light.svg)](https://cursor.com/en-US/install-mcp?name=imagekit_devtools&config=eyJ1cmwiOiJodHRwczovL2RldnRvb2xzLW1jcC5pbWFnZWtpdC5pby9tY3AifQ%3D%3D)
- [![Install API MCP Server](https://cursor.com/deeplink/mcp-install-light.svg)](https://cursor.com/en-US/install-mcp?name=imagekit_api&config=eyJ1cmwiOiJodHRwczovL2FwaS1tY3AuaW1hZ2VraXQuaW8vbWNwIn0%3D)

Or edit `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "imagekit_devtools": { "url": "https://devtools-mcp.imagekit.io/mcp" },
    "imagekit_api": { "url": "https://api-mcp.imagekit.io/mcp" }
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
    "imagekit_api": { "serverUrl": "https://api-mcp.imagekit.io/mcp" }
  }
}
```
</details>

## Usage

Once installed, these skills are automatically available to your AI agent. The agent will consult the relevant skill before performing ImageKit operations, ensuring correct tool usage and better results.

## License

MIT
