# free-for-dev MCP Server

This folder turns the repository README into a local read-only MCP server.

The server exposes the free-for.dev list as tools that AI clients such as Claude Desktop, Cursor, Windsurf, or other MCP-compatible clients can call.

## What this MCP server does

It reads the root `README.md` and provides these tools:

- `list_categories` — shows all main categories in the free-for.dev list.
- `get_category` — returns the full Markdown section for one category.
- `search_services` — searches services by keyword.
- `recommend_free_services` — recommends services based on a use case.

## Local setup

Clone the repository:

```bash
git clone https://github.com/christophernemala/free-for-dev.git
cd free-for-dev/mcp-server
```

Create and activate a Python virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the MCP server locally:

```bash
python server.py
```

The server uses stdio transport, which means it is normally launched by your MCP client rather than kept open manually.

## Claude Desktop configuration

Open your Claude Desktop config file.

Windows path:

```text
%APPDATA%\Claude\claude_desktop_config.json
```

macOS path:

```text
~/Library/Application Support/Claude/claude_desktop_config.json
```

Add this entry. Update the path to match your local repo path:

```json
{
  "mcpServers": {
    "free-for-dev": {
      "command": "python",
      "args": [
        "C:/Users/YOUR_NAME/path/to/free-for-dev/mcp-server/server.py"
      ]
    }
  }
}
```

Restart Claude Desktop after saving the file.

## Example prompts after connection

Use prompts like:

```text
Use free-for-dev MCP and find free hosting options for a Python API.
```

```text
Use free-for-dev MCP and list all CI/CD free-tier services.
```

```text
Use free-for-dev MCP and recommend free services for hosting a finance dashboard with database and cron jobs.
```

```text
Use free-for-dev MCP and search for Postgres, Redis, and email services.
```

## Notes

This is a read-only MCP server. It does not scrape websites, create accounts, or deploy applications. It only exposes this repository's README knowledge base to MCP-compatible AI clients.
