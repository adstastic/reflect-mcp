# Reflect MCP Server

An MCP (Model Context Protocol) server for interacting with the Reflect Notes API. This server allows AI assistants to create notes, manage links, and interact with your Reflect knowledge graph.

## Installation

### Quick Start with uvx (Recommended)

No need to clone the repository! Simply configure and run:

```json
{
  "mcpServers": {
    "reflect": {
      "command": "uvx",
      "args": ["reflect-mcp"],
      "env": {
        "REFLECT_CLIENT_ID": "your_client_id",
        "REFLECT_CLIENT_SECRET": "your_client_secret"
      }
    }
  }
}
```

### Manual Installation

```bash
pip install reflect-mcp
```

Or with uv:

```bash
uv pip install reflect-mcp
```

## Configuration

### Environment Variables

Create a `.env` file or set these environment variables:

```bash
REFLECT_CLIENT_ID=your_oauth_client_id
REFLECT_CLIENT_SECRET=your_oauth_client_secret
REFLECT_REDIRECT_URI=http://localhost:8080/callback  # Optional
REFLECT_DEFAULT_GRAPH_ID=your_default_graph_id  # Optional
```

### OAuth2 Setup

1. Register your application at [Reflect OAuth Settings](https://reflect.app/oauth)
2. Set your redirect URI (default: `http://localhost:8080/callback`)
3. Copy your Client ID and Client Secret

## Available Tools

### Authentication
- `authenticate` - Start OAuth2 flow
- `set_access_token` - Complete OAuth2 flow with authorization code
- `set_token_directly` - Set access token manually

### Graphs
- `list_graphs` - Get all accessible graphs
- `get_default_graph` - Get default graph ID

### Notes & Content
- `create_note` - Create a new note
- `append_daily_note` - Add to daily note
- `list_books` - Get books in a graph
- `list_links` - Get links in a graph
- `create_link` - Save a new link

### User
- `get_current_user` - Get authenticated user info

## Usage Examples

### First-Time Setup

1. Start authentication:
```
Use the 'authenticate' tool
```

2. Complete authentication:
```
Use 'set_access_token' with code: "AUTH_CODE_FROM_REDIRECT"
```

### Create a Note
```
Use 'create_note' with:
- subject: "Meeting Notes"
- content: "## Action Items\n- Follow up with team\n- Review proposal"
```

### Save a Link
```
Use 'create_link' with:
- url: "https://example.com/article"
- title: "Interesting Article"
- highlights: ["Key insight", "Important quote"]
```

### Daily Journaling
```
Use 'append_daily_note' with:
- text: "- Completed project review\n- Started new feature"
- list_name: "Work Log"
```

## Development

### Building from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/reflect-mcp
cd reflect-mcp

# Install with uv
uv sync

# Run in development mode
uv run mcp dev src/reflect_mcp/server.py
```

### Publishing to PyPI

```bash
# Build the package
uv build

# Upload to PyPI (requires PyPI account)
uv publish
```

## Resources

The server provides these MCP resources:
- `reflect://auth/status` - Current authentication status
- `reflect://config` - Current configuration (sanitized)

## Prompts

Built-in workflow prompts:
- `create_reading_list` - Template for creating reading lists
- `daily_journal_workflow` - Daily journaling workflow guide

## License

MIT License - see LICENSE file for details.