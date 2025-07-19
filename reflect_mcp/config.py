"""Configuration management for Reflect MCP server."""

import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ReflectConfig(BaseModel):
    """Configuration for Reflect API access."""
    
    client_id: str = Field(
        default_factory=lambda: os.getenv("REFLECT_CLIENT_ID", ""),
        description="OAuth2 client ID for Reflect API"
    )
    client_secret: str = Field(
        default_factory=lambda: os.getenv("REFLECT_CLIENT_SECRET", ""),
        description="OAuth2 client secret for Reflect API"
    )
    redirect_uri: str = Field(
        default_factory=lambda: os.getenv("REFLECT_REDIRECT_URI", "http://localhost:8080/callback"),
        description="OAuth2 redirect URI"
    )
    access_token: Optional[str] = Field(
        default_factory=lambda: os.getenv("REFLECT_ACCESS_TOKEN"),
        description="OAuth2 access token (can be set manually or via environment)"
    )
    refresh_token: Optional[str] = Field(
        default=None,
        description="OAuth2 refresh token"
    )
    api_base_url: str = Field(
        default="https://reflect.app/api",
        description="Base URL for Reflect API"
    )
    default_graph_id: Optional[str] = Field(
        default_factory=lambda: os.getenv("REFLECT_DEFAULT_GRAPH_ID"),
        description="Default graph ID to use for operations"
    )

    class Config:
        env_prefix = "REFLECT_"
        case_sensitive = False


# Global config instance
config = ReflectConfig()