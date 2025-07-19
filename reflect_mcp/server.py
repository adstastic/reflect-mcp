"""Reflect MCP Server implementation."""

import os
import webbrowser
from typing import Optional, List, Dict, Any
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
from .client import ReflectClient
from .config import config
from .models import CreateLinkRequest, CreateNoteRequest, AppendDailyNoteRequest

# Initialize FastMCP server
mcp = FastMCP("Reflect Notes MCP Server")

# Store client instance
_client: Optional[ReflectClient] = None


@mcp.tool()
async def authenticate() -> str:
    """
    Start OAuth2 authentication flow for Reflect API.
    Opens browser for authorization and returns instructions.
    """
    if not config.client_id or not config.client_secret:
        return "Error: REFLECT_CLIENT_ID and REFLECT_CLIENT_SECRET environment variables must be set"
    
    async with ReflectClient() as client:
        auth_url = client.get_authorization_url()
        
    # Try to open browser
    try:
        webbrowser.open(auth_url)
        return f"Authentication URL opened in browser. After authorizing, use 'set_access_token' with the authorization code from the redirect URL."
    except:
        return f"Please open this URL in your browser to authenticate:\n{auth_url}\n\nAfter authorizing, use 'set_access_token' with the authorization code from the redirect URL."


@mcp.tool()
async def set_access_token(code: str) -> str:
    """
    Exchange authorization code for access token.
    Use this after completing the OAuth2 flow.
    
    Args:
        code: Authorization code from redirect URL
    """
    try:
        async with ReflectClient() as client:
            token = await client.fetch_token(code)
            return f"Authentication successful! Access token saved. Token type: {token.get('token_type', 'Bearer')}"
    except Exception as e:
        return f"Error exchanging code for token: {str(e)}"


@mcp.tool()
async def set_token_directly(access_token: str, refresh_token: Optional[str] = None) -> str:
    """
    Directly set access token (and optionally refresh token).
    Useful if you already have valid tokens.
    
    Args:
        access_token: OAuth2 access token
        refresh_token: Optional OAuth2 refresh token
    """
    config.access_token = access_token
    if refresh_token:
        config.refresh_token = refresh_token
    return "Access token set successfully"


@mcp.tool()
async def list_graphs() -> List[Dict[str, Any]]:
    """
    Get all graphs accessible to the authenticated user.
    Returns list of graphs with id, name, and timestamps.
    """
    if not config.access_token:
        raise ValueError("Not authenticated. Use 'authenticate' tool first.")
    
    async with ReflectClient() as client:
        graphs = await client.list_graphs()
        return [graph.model_dump() for graph in graphs]


@mcp.tool()
async def get_default_graph() -> Optional[str]:
    """
    Get the default graph ID from configuration or user profile.
    Returns the graph ID that will be used if not specified in operations.
    """
    if config.default_graph_id:
        return config.default_graph_id
    
    if not config.access_token:
        raise ValueError("Not authenticated. Use 'authenticate' tool first.")
    
    async with ReflectClient() as client:
        user = await client.get_current_user()
        # Return first graph_id if available
        return user.graph_ids[0] if user.graph_ids else None


@mcp.tool()
async def list_books(graph_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get all books for a specific graph.
    
    Args:
        graph_id: Graph ID (uses default if not provided)
    """
    if not config.access_token:
        raise ValueError("Not authenticated. Use 'authenticate' tool first.")
    
    if not graph_id:
        graph_id = await get_default_graph()
        if not graph_id:
            raise ValueError("No graph_id provided and no default graph configured")
    
    async with ReflectClient() as client:
        books = await client.list_books(graph_id)
        return [book.model_dump() for book in books]


@mcp.tool()
async def list_links(graph_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get all links for a specific graph.
    
    Args:
        graph_id: Graph ID (uses default if not provided)
    """
    if not config.access_token:
        raise ValueError("Not authenticated. Use 'authenticate' tool first.")
    
    if not graph_id:
        graph_id = await get_default_graph()
        if not graph_id:
            raise ValueError("No graph_id provided and no default graph configured")
    
    async with ReflectClient() as client:
        links = await client.list_links(graph_id)
        return [link.model_dump() for link in links]


@mcp.tool()
async def create_link(
    url: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    highlights: Optional[List[str]] = None,
    graph_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new link in Reflect.
    
    Args:
        url: URL to save
        title: Optional title for the link
        description: Optional description
        highlights: Optional list of text highlights
        graph_id: Graph ID (uses default if not provided)
    """
    if not config.access_token:
        raise ValueError("Not authenticated. Use 'authenticate' tool first.")
    
    if not graph_id:
        graph_id = await get_default_graph()
        if not graph_id:
            raise ValueError("No graph_id provided and no default graph configured")
    
    link_data = CreateLinkRequest(
        url=url,
        title=title,
        description=description,
        highlights=highlights or []
    )
    
    async with ReflectClient() as client:
        link = await client.create_link(graph_id, link_data)
        return link.model_dump()


@mcp.tool()
async def create_note(
    subject: str,
    content: str,
    pinned: bool = False,
    graph_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new note in Reflect.
    
    Args:
        subject: Note title/subject
        content: Note content in Markdown format
        pinned: Whether to pin the note
        graph_id: Graph ID (uses default if not provided)
    """
    if not config.access_token:
        raise ValueError("Not authenticated. Use 'authenticate' tool first.")
    
    if not graph_id:
        graph_id = await get_default_graph()
        if not graph_id:
            raise ValueError("No graph_id provided and no default graph configured")
    
    note_data = CreateNoteRequest(
        subject=subject,
        content_markdown=content,
        pinned=pinned
    )
    
    async with ReflectClient() as client:
        note = await client.create_note(graph_id, note_data)
        return note.model_dump()


@mcp.tool()
async def append_daily_note(
    text: str,
    date: Optional[str] = None,
    list_name: Optional[str] = None,
    graph_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Append text to a daily note in Reflect.
    
    Args:
        text: Text to append
        date: Optional date (YYYY-MM-DD format, defaults to today)
        list_name: Optional list name to append to
        graph_id: Graph ID (uses default if not provided)
    """
    if not config.access_token:
        raise ValueError("Not authenticated. Use 'authenticate' tool first.")
    
    if not graph_id:
        graph_id = await get_default_graph()
        if not graph_id:
            raise ValueError("No graph_id provided and no default graph configured")
    
    append_data = AppendDailyNoteRequest(
        text=text,
        date=date,
        list_name=list_name
    )
    
    async with ReflectClient() as client:
        result = await client.append_daily_note(graph_id, append_data)
        return result


@mcp.tool()
async def get_current_user() -> Dict[str, Any]:
    """
    Get information about the currently authenticated user.
    Returns user details including default graph ID.
    """
    if not config.access_token:
        raise ValueError("Not authenticated. Use 'authenticate' tool first.")
    
    async with ReflectClient() as client:
        user = await client.get_current_user()
        return user.model_dump()


# Resources for displaying current state
@mcp.resource("reflect://auth/status")
async def get_auth_status() -> str:
    """Get current authentication status."""
    if config.access_token:
        try:
            async with ReflectClient() as client:
                user = await client.get_current_user()
                return f"Authenticated as: {user.email}"
        except:
            return "Authentication token present but may be invalid"
    return "Not authenticated"


@mcp.resource("reflect://config")
async def get_config() -> str:
    """Get current configuration (excluding secrets)."""
    return f"""Reflect MCP Configuration:
- API Base URL: {config.api_base_url}
- Client ID Set: {'Yes' if config.client_id else 'No'}
- Client Secret Set: {'Yes' if config.client_secret else 'No'}
- Access Token Set: {'Yes' if config.access_token else 'No'}
- Default Graph ID: {config.default_graph_id or 'Not set'}
- Redirect URI: {config.redirect_uri}"""


# Prompts for common workflows
@mcp.prompt()
async def create_reading_list() -> List[TextContent]:
    """Template for creating a reading list in Reflect."""
    return [
        TextContent(
            type="text",
            text="""To create a reading list in Reflect:

1. First authenticate if needed:
   - Use 'authenticate' tool
   - Follow the browser flow
   - Use 'set_access_token' with the code

2. Create a new note for your reading list:
   - Use 'create_note' with subject "Reading List"
   - Include your books/articles in markdown format

3. Add links to articles:
   - Use 'create_link' for each article
   - Include title and highlights

Example:
```
create_note(
    subject="2024 Reading List",
    content="## Books to Read\\n- Book 1\\n- Book 2\\n\\n## Articles\\n"
)
```"""
        )
    ]


@mcp.prompt()
async def daily_journal_workflow() -> List[TextContent]:
    """Template for daily journaling workflow."""
    return [
        TextContent(
            type="text",
            text="""Daily journaling workflow in Reflect:

1. Append to today's daily note:
   ```
   append_daily_note(
       text="- Completed project X\\n- Meeting with team\\n- Ideas for tomorrow",
       list_name="Journal"
   )
   ```

2. Create a reflection note:
   ```
   create_note(
       subject="Weekly Reflection - Week 1",
       content="## Accomplishments\\n\\n## Challenges\\n\\n## Next Week"
   )
   ```

3. Save interesting links:
   ```
   create_link(
       url="https://example.com/article",
       title="Interesting Article",
       highlights=["Key insight 1", "Important quote"]
   )
   ```"""
        )
    ]


def main():
    """Run the MCP server."""
    # FastMCP handles stdio transport internally
    mcp.run("stdio")