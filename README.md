# Reflect MCP Server

A Python MCP (Model Context Protocol) server that provides seamless integration with the [Reflect Notes API](https://reflect.app). This server enables AI assistants to interact with your Reflect notes, allowing you to create notes, save links, append to daily notes, and manage your knowledge graph programmatically.

## Features

- **OAuth2 Authentication**: Secure authentication flow with automatic token management
- **Note Management**: Create new notes with Markdown content
- **Daily Notes**: Append text to daily notes with optional list targeting
- **Link Saving**: Save web links with titles, descriptions, and highlights
- **Graph Operations**: List and manage multiple knowledge graphs
- **User Management**: Get current user information and default graph settings

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
        "REFLECT_ACCESS_TOKEN": "your_access_token_here"
      }
    }
  }
}
```

To get your access token:
1. Go to [Reflect Developer OAuth](https://reflect.app/developer/oauth)
2. Create credentials if you haven't already
3. Generate an access token
4. Copy the token and add it to the configuration above

### Manual Installation

```bash
pip install reflect-mcp
```

Or with uv:

```bash
uv pip install reflect-mcp
```

## Configuration

### Using an Access Token (Recommended)

The simplest way to use the server is with a direct access token:

```bash
REFLECT_ACCESS_TOKEN=your_access_token_here
REFLECT_DEFAULT_GRAPH_ID=your_default_graph_id  # Optional
```

To get your access token:
1. Go to [Reflect Developer OAuth](https://reflect.app/developer/oauth)
2. Create credentials if you haven't already
3. Generate an access token
4. Copy the token and add it to your configuration

### Using OAuth2 (Alternative)

If you prefer OAuth2 authentication:

```bash
REFLECT_CLIENT_ID=your_oauth_client_id
REFLECT_CLIENT_SECRET=your_oauth_client_secret
REFLECT_REDIRECT_URI=http://localhost:8080/callback  # Optional
REFLECT_DEFAULT_GRAPH_ID=your_default_graph_id  # Optional
```

### Claude Desktop Configuration

Add the server to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Using the published package with access token:

```json
{
  "mcpServers": {
    "reflect": {
      "command": "uvx",
      "args": ["reflect-mcp"],
      "env": {
        "REFLECT_ACCESS_TOKEN": "your_access_token_here"
      }
    }
  }
}
```

If running from source:

```json
{
  "mcpServers": {
    "reflect": {
      "command": "/path/to/uv",
      "args": [
        "--directory",
        "/path/to/reflect-mcp",
        "run",
        "reflect_server.py"
      ],
      "env": {
        "REFLECT_ACCESS_TOKEN": "your_access_token_here"
      }
    }
  }
}
```

Alternative OAuth2 configuration (if not using access token):

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

## Available Tools

### Authentication
- `authenticate` - Start OAuth2 authentication flow (opens browser)
- `set_access_token` - Complete OAuth2 flow with authorization code
- `set_token_directly` - Set access token manually (useful if you already have one)

### Graphs
- `list_graphs` - Get all accessible graphs with IDs, names, and timestamps
- `get_default_graph` - Get the default graph ID from configuration or user profile

### Notes & Content
- `create_note` - Create a new note with title and Markdown content
- `append_daily_note` - Append text to daily note (today or specific date)
- `list_books` - Get all books in a graph
- `list_links` - Get all links in a graph
- `create_link` - Save a web link with optional metadata

### User
- `get_current_user` - Get information about the authenticated user

## Authentication

### Using Access Token (Recommended)

If you've configured the server with `REFLECT_ACCESS_TOKEN`, you're already authenticated and can start using all tools immediately.

### Using OAuth2 Flow

If you're using OAuth2 credentials instead of a direct access token:

1. Start the authentication process:
   ```
   authenticate
   ```
   This opens your browser to the Reflect OAuth page.

2. After authorizing, you'll be redirected to a URL containing an authorization code.

3. Complete authentication by providing the code:
   ```
   set_access_token code="your_authorization_code"
   ```

4. The server will handle token exchange and refresh automatically.

## Usage Examples

### Create a Note

```python
create_note(
    subject="Meeting Notes",
    content="## Project Review\n\n- Discussed timeline\n- Set Q2 goals",
    pinned=false
)
```

### Append to Daily Note

```python
# Append to today's daily note
append_daily_note(
    text="Remember to review the project proposal"
)

# Append to a specific list in yesterday's note
append_daily_note(
    text="Completed user authentication feature",
    date="2024-01-18",
    list_name="Done"
)
```

### Save a Link

```python
create_link(
    url="https://example.com/article",
    title="Interesting Article",
    description="Key insights about productivity",
    highlights=["Important quote from the article", "Another highlight"]
)
```

### List and Manage Graphs

```python
# Get all accessible graphs
list_graphs()

# Get the default graph ID
get_default_graph()

# List all links in a specific graph
list_links(graph_id="your_graph_id")
```

## Resources

The server provides these MCP resources for checking status:

- **get_auth_status** (`reflect://auth/status`): Check current authentication status
- **get_config** (`reflect://config`): View current configuration (excluding secrets)

## Prompts

Built-in workflow prompts for common tasks:

- **create_reading_list**: Template for creating organized reading lists in Reflect
- **daily_journal_workflow**: Structured template for daily journaling

## Development

### Running from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/reflect-mcp
cd reflect-mcp

# Install dependencies
uv sync

# Run in development mode
uv run mcp dev reflect_mcp/server.py
```

### Testing

```bash
# Run with MCP inspector for testing
uv run mcp inspector reflect_mcp/server.py
```

### Building and Publishing

```bash
# Build the package
uv build

# Publish to PyPI (requires credentials)
uv publish
```

## API Reference

The server implements the [Reflect API](https://reflect.app/api) v0.1.0 with the following endpoints:

- `GET /graphs` - List all graphs
- `GET /graphs/{id}/books` - List books in a graph
- `GET /graphs/{id}/links` - List links in a graph
- `POST /graphs/{id}/links` - Create a new link
- `POST /graphs/{id}/notes` - Create a new note
- `PUT /graphs/{id}/daily-notes` - Append to daily note
- `GET /users/me` - Get current user info

### Authentication

The Reflect API uses OAuth2 with the following flows:

- **Authorization URL**: `https://reflect.app/oauth`
- **Token URL**: `https://reflect.app/api/oauth/token`
- **Scopes**: 
  - `read:graph` - Read access to protected resources
  - `write:graph` - Write access to protected resources

## Troubleshooting

### Authentication Issues

- **Missing credentials**: Ensure `REFLECT_CLIENT_ID` and `REFLECT_CLIENT_SECRET` are set
- **Invalid redirect**: Check that your OAuth app's redirect URI matches the server's expected callback
- **Token refresh**: The server automatically handles token refresh using the `authlib` library

### Connection Errors

- Verify your internet connection
- Check if the Reflect API is accessible at `https://api.reflect.app`
- Review server logs for detailed error messages
- Ensure your OAuth app has the necessary scopes enabled

### Common Issues

1. **"Server disconnected" error in Claude**: Usually means the server couldn't start. Check:
   - OAuth credentials are correctly set
   - No syntax errors in configuration
   - The `reflect_server.py` file exists (if running from source)

2. **"Not authenticated" errors**: Run the `authenticate` tool first to set up OAuth

3. **Graph ID errors**: Use `list_graphs` to find valid graph IDs, or set `REFLECT_DEFAULT_GRAPH_ID`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Support

For issues and feature requests, please use the [GitHub issue tracker](https://github.com/yourusername/reflect-mcp/issues).