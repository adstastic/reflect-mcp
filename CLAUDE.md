# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python MCP (Model Context Protocol) server that provides integration with the Reflect Notes API. The server is designed to be installed and run via `uvx` without cloning the repository, making it easy for users to add Reflect capabilities to their AI assistants.

## Architecture

### Package Structure
- `reflect_mcp/` - Main Python package
  - `__main__.py` - Entry point for CLI execution
  - `server.py` - FastMCP server implementation with all tools
  - `client.py` - Async HTTP client for Reflect API with OAuth2
  - `models.py` - Pydantic models for API requests/responses
  - `config.py` - Configuration management with environment variables

### Key Components

1. **OAuth2 Authentication Flow**
   - Browser-based authorization at `https://reflect.app/oauth`
   - Token exchange using authorization code
   - Automatic token refresh via authlib
   - Tokens stored in memory (consider persistence for production)

2. **API Client Design**
   - Async/await throughout using httpx
   - Context manager pattern for proper cleanup
   - Type-safe with Pydantic models
   - Centralized error handling

3. **MCP Tool Organization**
   - Authentication tools: `authenticate`, `set_access_token`, `set_token_directly`
   - Graph operations: `list_graphs`, `get_default_graph`
   - Content tools: `create_note`, `append_daily_note`, `list_links`, `create_link`
   - User tools: `get_current_user`

## Development Commands

```bash
# Install dependencies
uv sync

# Run in development mode
uv run mcp dev reflect_mcp/server.py

# Test the server
uv run mcp inspector reflect_mcp/server.py

# Build for distribution
uv build

# Run tests (when implemented)
uv run pytest
```

## Common Tasks

### Adding New API Endpoints

1. Add model to `models.py` if needed
2. Implement method in `client.py` following existing patterns
3. Create MCP tool in `server.py` with proper error handling
4. Update documentation

### Testing OAuth2 Flow

1. Set environment variables for client ID/secret
2. Use `authenticate` tool to get auth URL
3. Complete browser flow
4. Use `set_access_token` with the code from redirect

### Debugging API Issues

- Check `httpx` response in client methods
- Use `response.raise_for_status()` for automatic error handling
- Log full request/response when debugging
- Verify OAuth2 scopes match API requirements

## API Endpoint Mappings

| MCP Tool | Reflect API Endpoint | Method |
|----------|---------------------|---------|
| list_graphs | /graphs | GET |
| list_books | /graphs/{id}/books | GET |
| list_links | /graphs/{id}/links | GET |
| create_link | /graphs/{id}/links | POST |
| create_note | /graphs/{id}/notes | POST |
| append_daily_note | /graphs/{id}/daily-notes | PUT |
| get_current_user | /users/me | GET |

## Publishing to PyPI

The package is configured for PyPI distribution:

```bash
# Ensure version is updated in pyproject.toml
# Build the distribution
uv build

# Upload to PyPI (requires credentials)
uv publish
```

Users can then install with:
```bash
uvx reflect-mcp
```

## Error Handling Strategy

1. **Authentication Errors**: Clear messages about missing credentials or expired tokens
2. **API Errors**: Pass through Reflect API error messages with context
3. **Network Errors**: Handled by httpx with appropriate retries
4. **Validation Errors**: Caught by Pydantic before API calls

## Future Enhancements

Consider implementing:
- Token persistence between sessions
- Batch operations for better performance
- Search functionality within notes/links
- WebSocket support for real-time updates
- Local caching of frequently accessed data