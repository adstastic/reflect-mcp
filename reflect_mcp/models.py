"""Pydantic models for Reflect API responses."""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class Graph(BaseModel):
    """Reflect graph model."""
    id: str
    name: str
    acl: Optional[List[str]] = Field(default_factory=list)


class Book(BaseModel):
    """Reflect book model."""
    id: str
    asin: str
    title: str
    authors: List[str] = Field(default_factory=list)
    cover_src: Optional[str] = None
    notes: List[Dict[str, Any]] = Field(default_factory=list)
    updated_at: Optional[str] = None
    created_at: Optional[str] = None


class Highlight(BaseModel):
    """Highlight within a link."""
    text: str
    offset: Optional[int] = None


class Link(BaseModel):
    """Reflect link model."""
    id: str
    url: str
    title: Optional[str] = None
    description: Optional[str] = None
    updated_at: str
    highlights: List[Highlight] = Field(default_factory=list)


class CreateNoteResponse(BaseModel):
    """Response from creating a note."""
    id: str
    created_at: str
    updated_at: str


class AppendDailyNoteResponse(BaseModel):
    """Response from appending to daily note."""
    success: bool


class User(BaseModel):
    """Reflect user model."""
    id: str
    email: str
    name: Optional[str] = None
    graph_ids: List[str] = Field(default_factory=list)
    preferences: Optional[Dict[str, Any]] = None


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