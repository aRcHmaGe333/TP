import datetime as dt
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, validator
class IdeaStatus(str, Enum):
    submitted = "submitted"
    acknowledged = "acknowledged"
    in_progress = "in_progress"
    resolved = "resolved"
class RegisterRequest(BaseModel):
    display_name: str
    password: str
    email: Optional[str] = None
class LoginRequest(BaseModel):
    display_name: str
    password: str
class UserResponse(BaseModel):
    id: int
    display_name: str
    email: Optional[str]
    fingerprint: str
    is_admin: bool
    created_at: dt.datetime
class TokenResponse(UserResponse):
    token: str
class IdeaCreate(BaseModel):
    title: str
    body: str
    tags: List[str] = Field(default_factory=list)
    merged_into_id: Optional[int] = None
class IdeaUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    tags: Optional[List[str]] = None
    merged_into_id: Optional[int] = None
class IdeaResponse(BaseModel):
    id: int
    title: str
    body: str
    tags: List[str]
    author: UserResponse
    merged_into_id: Optional[int]
    status: IdeaStatus
    status_updated_at: Optional[dt.datetime]
    status_updated_by: Optional[int]
    signature: str
    score: int
    created_at: dt.datetime
    updated_at: dt.datetime
    comment_count: int
class CommentCreate(BaseModel):
    body: str
class CommentResponse(BaseModel):
    id: int
    body: str
    author: UserResponse
    signature: str
    created_at: dt.datetime
class VoteRequest(BaseModel):
    value: int
    @validator("value")
    def validate_value(cls, value: int) -> int:
        if value not in (-1, 1):
            raise ValueError("Vote must be -1 or 1")
        return value
class MergeRequest(BaseModel):
    target_id: int
class IdeaStatusUpdate(BaseModel):
    status: IdeaStatus
class TopIdeaSummary(BaseModel):
    id: int
    title: str
    status: IdeaStatus
    score: int
class ReportSummaryResponse(BaseModel):
    generated_at: dt.datetime
    total_ideas: int
    counts_by_status: Dict[str, int]
    top_ideas: List[TopIdeaSummary]
    median_response_hours: Optional[float]
class AuditEventResponse(BaseModel):
    id: int
    event_type: str
    user_id: Optional[int]
    target_type: Optional[str]
    target_id: Optional[int]
    ip_address: Optional[str]
    details: Dict[str, Any]
