"""Reflect API client with OAuth2 support."""

import httpx
from typing import Optional, Dict, Any, List
from authlib.integrations.httpx_client import AsyncOAuth2Client
from .config import config
from .models import (
    Graph, Book, Link, CreateNoteResponse, AppendDailyNoteResponse, User,
    CreateLinkRequest, CreateNoteRequest, AppendDailyNoteRequest
)


class ReflectClient:
    """Async client for Reflect API with OAuth2 authentication."""
    
    def __init__(self):
        self.base_url = config.api_base_url
        self.client_id = config.client_id
        self.client_secret = config.client_secret
        self.redirect_uri = config.redirect_uri
        self.access_token = config.access_token
        self.refresh_token = config.refresh_token
        self._client: Optional[AsyncOAuth2Client] = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.setup()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()
    
    async def setup(self):
        """Initialize the OAuth2 client."""
        self._client = AsyncOAuth2Client(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            token_endpoint="https://reflect.app/api/oauth/token",
            grant_type="authorization_code",
        )
        
        if self.access_token:
            self._client.token = {"access_token": self.access_token, "token_type": "Bearer"}
            if self.refresh_token:
                self._client.token["refresh_token"] = self.refresh_token
    
    def get_authorization_url(self) -> str:
        """Get the OAuth2 authorization URL."""
        client = AsyncOAuth2Client(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
        )
        auth_url = "https://reflect.app/oauth"
        url, _ = client.create_authorization_url(
            auth_url,
            scope="read:graph write:graph"
        )
        return url
    
    async def fetch_token(self, code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token."""
        if not self._client:
            await self.setup()
        
        token = await self._client.fetch_token(
            "https://reflect.app/api/oauth/token",
            authorization_response=f"{self.redirect_uri}?code={code}",
            grant_type="authorization_code"
        )
        
        self.access_token = token["access_token"]
        if "refresh_token" in token:
            self.refresh_token = token["refresh_token"]
        
        # Update config
        config.access_token = self.access_token
        config.refresh_token = self.refresh_token
        
        return token
    
    async def _request(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        """Make authenticated request to Reflect API."""
        if not self._client:
            raise RuntimeError("Client not initialized. Use 'async with ReflectClient() as client:'")
        
        url = f"{self.base_url}{endpoint}"
        response = await self._client.request(method, url, **kwargs)
        response.raise_for_status()
        return response
    
    # Graph operations
    async def list_graphs(self) -> List[Graph]:
        """Get all graphs."""
        response = await self._request("GET", "/graphs")
        data = response.json()
        # API returns array directly
        return [Graph(**graph) for graph in data]
    
    # Book operations
    async def list_books(self, graph_id: str) -> List[Book]:
        """Get all books for a graph."""
        response = await self._request("GET", f"/graphs/{graph_id}/books")
        data = response.json()
        # API returns array directly
        return [Book(**book) for book in data]
    
    # Link operations
    async def list_links(self, graph_id: str) -> List[Link]:
        """Get all links for a graph."""
        response = await self._request("GET", f"/graphs/{graph_id}/links")
        data = response.json()
        # API returns array directly
        return [Link(**link) for link in data]
    
    async def create_link(self, graph_id: str, link_data: CreateLinkRequest) -> Link:
        """Create a new link."""
        response = await self._request(
            "POST",
            f"/graphs/{graph_id}/links",
            json=link_data.model_dump(exclude_none=True)
        )
        return Link(**response.json())
    
    # Note operations
    async def create_note(self, graph_id: str, note_data: CreateNoteRequest) -> CreateNoteResponse:
        """Create a new note."""
        response = await self._request(
            "POST",
            f"/graphs/{graph_id}/notes",
            json=note_data.model_dump(exclude_none=True)
        )
        return CreateNoteResponse(**response.json())
    
    async def append_daily_note(self, graph_id: str, append_data: AppendDailyNoteRequest) -> AppendDailyNoteResponse:
        """Append to daily note."""
        response = await self._request(
            "PUT",
            f"/graphs/{graph_id}/daily-notes",
            json=append_data.model_dump(exclude_none=True)
        )
        return AppendDailyNoteResponse(**response.json())
    
    # User operations
    async def get_current_user(self) -> User:
        """Get current user information."""
        response = await self._request("GET", "/users/me")
        return User(**response.json())