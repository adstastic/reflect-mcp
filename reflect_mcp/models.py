"""Pydantic models for Reflect API responses."""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class Graph(BaseModel):
    """Reflect graph model."""
    id: str
    name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Book(BaseModel):
    """Reflect book model."""
    id: str
    title: str
    author: Optional[str] = None
    graph_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Link(BaseModel):
    """Reflect link model."""
    id: str
    url: str
    title: Optional[str] = None
    description: Optional[str] = None
    graph_id: str
    highlights: List[str] = Field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Note(BaseModel):
    """Reflect note model."""
    id: str
    subject: str
    content_markdown: str
    graph_id: str
    pinned: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class User(BaseModel):
    """Reflect user model."""
    id: str
    email: str
    name: Optional[str] = None
    default_graph_id: Optional[str] = None


class CreateLinkRequest(BaseModel):
    """Request model for creating a link."""
    url: str
    id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    highlights: List[str] = Field(default_factory=list)
    updated_at: Optional[str] = None


class CreateNoteRequest(BaseModel):
    """Request model for creating a note."""
    subject: str
    content_markdown: str
    pinned: bool = False


class AppendDailyNoteRequest(BaseModel):
    """Request model for appending to daily note."""
    text: str
    transform_type: str = "list-append"
    date: Optional[str] = None
    list_name: Optional[str] = None