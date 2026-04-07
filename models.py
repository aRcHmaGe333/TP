from __future__ import annotations

import datetime as dt
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    display_name: str = Field(index=True)
    legal_name: Optional[str] = Field(default=None, index=True)
    email: Optional[str] = Field(default=None, index=True)
    password_hash: str
    password_salt: str
    signing_key: str
    fingerprint: str = Field(index=True)
    is_admin: bool = Field(default=False, index=True)
    identity_provider: Optional[str] = Field(default=None, index=True)
    identity_subject_key: Optional[str] = Field(default=None, index=True)
    identity_country_code: Optional[str] = Field(default=None, index=True)
    identity_verified_at: Optional[dt.datetime] = Field(default=None, index=True)
    created_at: dt.datetime = Field(default_factory=lambda: dt.datetime.utcnow())


class Idea(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    body: str
    tags: str = Field(default="")
    author_id: int = Field(foreign_key="user.id")
    merged_into_id: Optional[int] = Field(default=None, foreign_key="idea.id")
    status: str = Field(default="submitted", index=True)
    status_updated_at: Optional[dt.datetime] = Field(default=None)
    status_updated_by: Optional[int] = Field(default=None, foreign_key="user.id")
    signature: str
    created_at: dt.datetime = Field(default_factory=lambda: dt.datetime.utcnow())
    updated_at: dt.datetime = Field(default_factory=lambda: dt.datetime.utcnow())


class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    idea_id: int = Field(foreign_key="idea.id")
    author_id: int = Field(foreign_key="user.id")
    body: str
    signature: str
    created_at: dt.datetime = Field(default_factory=lambda: dt.datetime.utcnow())


class Vote(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    idea_id: int = Field(foreign_key="idea.id")
    user_id: int = Field(foreign_key="user.id")
    value: int
    created_at: dt.datetime = Field(default_factory=lambda: dt.datetime.utcnow())


class MergeRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    source_id: int = Field(foreign_key="idea.id")
    target_id: int = Field(foreign_key="idea.id")
    author_id: int = Field(foreign_key="user.id")
    created_at: dt.datetime = Field(default_factory=lambda: dt.datetime.utcnow())


class AuditEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_type: str = Field(index=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    target_type: Optional[str] = Field(default=None, index=True)
    target_id: Optional[int] = Field(default=None, index=True)
    ip_address: Optional[str] = Field(default=None)
    details_json: str = Field(default="{}")
    created_at: dt.datetime = Field(default_factory=lambda: dt.datetime.utcnow(), index=True)
